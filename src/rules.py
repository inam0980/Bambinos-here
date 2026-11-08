"""
Deterministic reconciliation rules for the Bambinos renewal pipeline.

invoices -> faculty_form_unapproved -> booking_requests -> class_schedule_bookings

Design principle: the PAYMENT GATEWAY LEDGER (invoices) is the source of truth.
The teacher form is treated as optional metadata, never as the trigger.
No LLM is involved in any approve / reject decision.
"""
from __future__ import annotations

import unicodedata
from datetime import datetime, timedelta

import pandas as pd

# ---------------------------------------------------------------------------
# Reason-code catalogue  (code -> severity, owner, SLA hours, action)
#   BLOCKING  = case cannot be auto-approved until a human resolves it
#   ADVISORY  = auto-approved; humans are informed / data gets corrected
# ---------------------------------------------------------------------------
REASON_CODES = {
    # --- blocking --------------------------------------------------------
    "PAYMENT_FAILED": ("BLOCKING", "Parent", 24,
        "Gateway shows payment failed. Do NOT approve. Resend payment link to parent; ignore screenshots."),
    "PARTIAL_PAYMENT": ("BLOCKING", "Ops (Finance)", 12,
        "Only an installment is captured. Approve under installment policy (schedule paid sessions) or collect balance."),
    "DISCOUNT_NEEDS_APPROVAL": ("BLOCKING", "Ops Lead", 4,
        "Discount above the 10% teacher limit. Ops Lead approves/rejects in one click."),
    "FEE_MISMATCH": ("BLOCKING", "Ops (Finance)", 12,
        "Net amount differs from the standard fee with no discount recorded."),
    "IDENTITY_MISMATCH": ("BLOCKING", "Ops Agent", 4,
        "Invoice user_id / class / educator does not match the student's active record."),
    "INVOICE_NOT_FOUND": ("BLOCKING", "Teacher", 12,
        "Teacher form references an invoice that cannot be matched to any payment."),
    "BATCH_CHANGE_NO_MATCH": ("BLOCKING", "Ops Scheduler", 24,
        "Parent wants a different slot and no existing batch of this class matches. Student stays in current batch until moved."),
    "BATCH_CHANGE_TARGET_FULL": ("BLOCKING", "Ops Scheduler", 24,
        "Requested batch exists but is at capacity."),
    "BATCH_ID_MISMATCH": ("BLOCKING", "Teacher", 12,
        "Teacher form batch differs from the student's active batch without a batch-change request."),
    "STUDENT_NOT_ACTIVE": ("BLOCKING", "Ops Agent", 12,
        "Student not found in the active batch roster."),
    # --- advisory --------------------------------------------------------
    "ORPHANED_INVOICE": ("ADVISORY", "Teacher", 12,
        "Paid renewal with no teacher form. Fast-tracked into the same batch; teacher only informed."),
    "PAYER_CONTACT_MISMATCH": ("ADVISORY", "Ops Agent", 24,
        "Payer phone/email differs from the registered contact but system IDs match. Approved; parent asked to confirm the secondary contact."),
    "INVOICE_REF_AUTOCORRECTED": ("ADVISORY", "Teacher", 24,
        "Teacher typed the wrong invoice ID; matched uniquely on student_id + user_id + class + amount and corrected."),
    "TEACHER_AMOUNT_MISMATCH": ("ADVISORY", "Teacher", 24,
        "Amount typed in the form differs from the gateway amount; gateway amount used."),
    "DUPLICATE_FORM": ("ADVISORY", "Teacher", 24,
        "Same renewal submitted more than once; duplicate auto-closed."),
    "FALSE_BATCH_FULL": ("ADVISORY", "Ops Scheduler", 4,
        "Booking failed as 'batch full' but the renewing student already occupies a seat in that batch. Re-allocated."),
    "STUCK_AT_ALLOCATION": ("ADVISORY", "Ops Scheduler", 4,
        "Approved same-batch renewal waiting for manual batch allocation. Auto-allocated."),
    "NAME_ENCODING_ANOMALY": ("ADVISORY", "Ops Agent", 48,
        "Name contains look-alike (non-Latin) characters; exact-name matching would silently fail."),
}

DISCOUNT_AUTO_LIMIT_PCT = 10.0
SESSION_MINUTES = 50
DAY_IDX = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6}

# Cyrillic / Greek glyphs that render identically to Latin letters
HOMOGLYPHS = str.maketrans({
    "А": "A", "В": "B", "Е": "E", "К": "K", "М": "M", "Н": "H", "О": "O", "Р": "P",
    "С": "C", "Т": "T", "Х": "X", "а": "a", "е": "e", "о": "o", "р": "p", "с": "c",
    "у": "y", "х": "x", "і": "i", "Ι": "I", "Ο": "O", "ο": "o",
})


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def clean(v):
    if v is None:
        return None
    s = str(v).strip()
    return None if s in ("", "NULL", "nan", "None") else s


def ts(v):
    v = clean(v)
    return datetime.strptime(v, "%Y-%m-%d %H:%M:%S") if v else None


def money(v):
    v = clean(v)
    return round(float(v), 2) if v else 0.0


def norm_text(v):
    v = clean(v) or ""
    return unicodedata.normalize("NFKC", v).translate(HOMOGLYPHS).lower().strip()


def has_homoglyph(v):
    v = clean(v) or ""
    return v.translate(HOMOGLYPHS) != v


def norm_phone(v):
    return "".join(ch for ch in (clean(v) or "") if ch.isalnum()).upper()


def load_tables(data_dir: str) -> dict:
    files = {
        "invoices": "1_invoices.csv",
        "forms": "2_faculty_form_unapproved.csv",
        "bookings": "3_booking_requests.csv",
        "schedule": "4_class_schedule_bookings.csv",
        "roster": "reference_active_batches_and_students.csv",
    }
    out = {}
    for k, f in files.items():
        df = pd.read_csv(f"{data_dir}/{f}", dtype=str, keep_default_na=False)
        df = df.map(clean)
        if "deleted_at" in df.columns:          # respect soft deletes
            df = df[df["deleted_at"].isna()]
        out[k] = df.reset_index(drop=True)
    return out


def batch_catalog(roster: pd.DataFrame) -> pd.DataFrame:
    cols = ["current_classbatch_id", "classbatch_name", "class_id", "educator_id",
            "batch_days", "batch_start_time", "active_students_count", "max_batch_size"]
    cat = roster[cols].drop_duplicates("current_classbatch_id").copy()
    cat["active_students_count"] = cat["active_students_count"].astype(int)
    cat["max_batch_size"] = cat["max_batch_size"].astype(int)
    return cat.rename(columns={"current_classbatch_id": "classbatch_id"})


def next_sessions(start_after: datetime, days_csv: str, start_time: str, n: int):
    days = [DAY_IDX[d.strip()] for d in days_csv.split(",")]
    hh, mm, ss = (int(x) for x in start_time.split(":"))
    d = start_after.date() + timedelta(days=1)
    out = []
    while len(out) < n:
        if d.weekday() in days:
            st = datetime(d.year, d.month, d.day, hh, mm, ss)
            out.append((d.isoformat(), st.strftime("%H:%M:%S"),
                        (st + timedelta(minutes=SESSION_MINUTES)).strftime("%H:%M:%S")))
        d += timedelta(days=1)
    return out


def hours_between(a: datetime | None, b: datetime | None):
    if not a or not b:
        return None
    return round((b - a).total_seconds() / 3600, 1)
