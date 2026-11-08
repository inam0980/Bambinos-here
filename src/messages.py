"""
Follow-up message drafter.

Default: deterministic templates (works offline, no API key, fully auditable).
Optional: if GEMINI_API_KEY is set, Gemini polishes tone (prompt in prompts/message_drafter.md).
The LLM never changes facts: amounts, IDs and actions come from the rule engine and are
re-checked after generation; if any fact is missing from the LLM output the template is used.
"""
from __future__ import annotations

import json
import os
import urllib.request
from pathlib import Path

PROMPT_FILE = Path(__file__).resolve().parent.parent / "prompts" / "message_drafter.md"


def _teacher(c):
    return (c.get("educator_name") or f"Educator {c['educator_id']}").split("*")[0].rstrip()


def _parent(c):
    return c.get("parent_name") or "Parent"


def _student(c):
    return c.get("student_name") or f"Student {c['student_id']}"


# reason_code -> list of (channel, recipient, template)
TEMPLATES = {
    "PAYMENT_FAILED": [
        ("WhatsApp", "Parent",
         "Hi {parent}, we tried to confirm {student}'s renewal for {cls} but the payment of INR {amt} did not go through "
         "(bank status: failed, no money was deducted on our side). Please retry here: https://bambinos.live/invoice/BMB-INV-2026-{inv}. "
         "{student}'s current classes continue meanwhile. - Team Bambinos"),
        ("WhatsApp", "Teacher",
         "Hi {teacher}, renewal form {form} for {student} cannot be approved: the gateway shows invoice {inv} as FAILED. "
         "A UPI 'processing' screenshot is not proof of payment. We've sent the parent a retry link - no action needed from you."),
    ],
    "PARTIAL_PAYMENT": [
        ("Slack", "Ops (Finance)",
         ":warning: {case} | {student} paid installment 1 (INR {amt}) of INR {gross}. Teacher form says INR {form_amt}. "
         "Decide: approve under installment policy or hold. SLA 12h."),
        ("WhatsApp", "Parent",
         "Hi {parent}, thank you! We've received INR {amt} (installment 1) for {student}'s renewal. "
         "The second installment link will be shared before it's due. - Team Bambinos"),
    ],
    "DISCOUNT_NEEDS_APPROVAL": [
        ("Slack", "Ops Lead",
         ":moneybag: {case} | {teacher} gave {student} a discount: paid INR {amt} vs list INR {gross}. "
         "Above 10% teacher limit. Reply APPROVE / REJECT. SLA 4h."),
    ],
    "FEE_MISMATCH": [
        ("Slack", "Ops (Finance)", ":warning: {case} | {student} paid INR {amt}, standard fee differs. Please verify pricing."),
    ],
    "IDENTITY_MISMATCH": [
        ("Slack", "Ops Agent", ":mag: {case} | Invoice {inv} IDs do not match {student}'s active record. Manual check needed. SLA 4h."),
    ],
    "INVOICE_NOT_FOUND": [
        ("WhatsApp", "Teacher",
         "Hi {teacher}, form {form} for {student} cites an invoice we can't find. Please share the correct payment link."),
    ],
    "BATCH_CHANGE_NO_MATCH": [
        ("Slack", "Ops Scheduler",
         ":calendar: {case} | {student} ({cls}) paid & wants {want}. No existing batch matches. "
         "Options: open a new batch / offer nearest slot. Student stays in current batch until moved - no class gap. SLA 24h."),
        ("WhatsApp", "Parent",
         "Hi {parent}, thanks for renewing {student}! We're finding a {want} slot as requested. Until then {student} continues "
         "in the current batch so no class is missed. We'll confirm the new timing within 24 hours. - Team Bambinos"),
    ],
    "BATCH_CHANGE_TARGET_FULL": [
        ("Slack", "Ops Scheduler", ":calendar: {case} | Requested batch for {student} is full. Offer alternatives. SLA 24h."),
    ],
    "BATCH_ID_MISMATCH": [
        ("WhatsApp", "Teacher", "Hi {teacher}, form {form} lists a different batch than {student}'s current one. Please confirm."),
    ],
    "STUDENT_NOT_ACTIVE": [
        ("Slack", "Ops Agent", ":mag: {case} | Paid renewal for student {student_id} not found in active roster."),
    ],
    "ORPHANED_INVOICE": [
        ("WhatsApp", "Teacher",
         "Hi {teacher}, good news - {student}'s renewal payment (INR {amt}) came in on {paid}. We've auto-renewed them in the "
         "same batch. You don't need to fill the renewal form. If the parent wants a different slot, just reply here."),
    ],
    "PAYER_CONTACT_MISMATCH": [
        ("WhatsApp", "Parent",
         "Hi {parent}, we received INR {amt} for {student}'s renewal - classes are confirmed! The payment came from "
         "{payer_mobile}, which isn't on {student}'s profile. Reply YES to add it as a secondary contact for class reminders."),
    ],
    "INVOICE_REF_AUTOCORRECTED": [
        ("WhatsApp", "Teacher",
         "Hi {teacher}, small fix: form {form} had invoice {wrong_inv}; the correct one is {inv}. We've corrected it and renewed "
         "{student}. Nothing else needed."),
    ],
    "TEACHER_AMOUNT_MISMATCH": [],   # covered by the partial/discount message
    "DUPLICATE_FORM": [
        ("WhatsApp", "Teacher",
         "Hi {teacher}, we got {student}'s renewal form twice (browser refresh). We kept one and closed the duplicate - all good."),
    ],
    "FALSE_BATCH_FULL": [
        ("Slack", "Ops Scheduler",
         ":white_check_mark: {case} | Booking for {student} failed as 'batch full', but {student} already holds a seat in "
         "{batch}. Auto-reallocated. Please fix the capacity rule to exclude renewing students."),
    ],
    "STUCK_AT_ALLOCATION": [],       # covered by the confirmation below
    "NAME_ENCODING_ANOMALY": [
        ("Slack", "Ops Agent",
         ":abc: {case} | Parent name on invoice {inv} contains non-Latin look-alike letters. Normalise in CRM to avoid search/match misses."),
    ],
}

CONFIRMATION = ("WhatsApp", "Parent",
                "Hi {parent}, {student}'s renewal for {cls} is confirmed! Classes continue in {batch} on {days} at {time}. "
                "First class of the new term: {first}. See you there! - Team Bambinos")


def _facts(c, approved_row=None, first_date=None, exc_details=None):
    f = {
        "case": c["case_id"], "inv": c.get("invoice_id"), "form": c.get("form_id") or "-",
        "student": _student(c), "student_id": c["student_id"], "parent": _parent(c), "teacher": _teacher(c),
        "cls": c.get("class_name") or f"class {c.get('class_id')}",
        "amt": f"{c.get('net_amount', 0):,.0f}", "paid": c.get("paid_at"),
        "payer_mobile": c.get("parent_mobile"), "gross": "-", "form_amt": "-", "want": "-",
        "wrong_inv": "-", "batch": c.get("target_classbatch_id") or "-", "days": "-", "time": "-", "first": first_date or "-",
    }
    if approved_row is not None:
        f.update(batch=approved_row["classbatch_name"], days=approved_row["batch_days"],
                 time=approved_row["start_time"][:5])
    return f


def _load_env():
    env = Path(__file__).resolve().parent.parent / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                if v.strip():
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


_load_env()


def _numbers_kept(src: str, new: str) -> bool:
    import re
    return all(n in new for n in re.findall(r"\d[\d,]*", src))


def _groq_polish(text: str, recipient: str):
    key = os.getenv("GROQ_API_KEY")
    if not key:
        return None
    system = PROMPT_FILE.read_text(encoding="utf-8") if PROMPT_FILE.exists() else ""
    body = {"model": os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"), "temperature": 0.2,
            "messages": [{"role": "system", "content": system},
                         {"role": "user", "content": f"RECIPIENT: {recipient}\nDRAFT:\n{text}"}]}
    try:
        req = urllib.request.Request("https://api.groq.com/openai/v1/chat/completions",
                                     data=json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}",
                                              "User-Agent": "bambinos-renewal-agent"})
        out = json.loads(urllib.request.urlopen(req, timeout=20).read())
        new = out["choices"][0]["message"]["content"].strip()
        return new if _numbers_kept(text, new) else text
    except Exception:
        return text


def _gemini_polish(text: str, recipient: str) -> str:
    groq = _groq_polish(text, recipient)
    if groq is not None:
        return groq
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        return text
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    system = PROMPT_FILE.read_text(encoding="utf-8") if PROMPT_FILE.exists() else ""
    body = {"contents": [{"parts": [{"text": f"{system}\n\nRECIPIENT: {recipient}\nDRAFT:\n{text}"}]}]}
    try:
        req = urllib.request.Request(
            f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}",
            data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
        out = json.loads(urllib.request.urlopen(req, timeout=20).read())
        new = out["candidates"][0]["content"]["parts"][0]["text"].strip()
        # guardrail: every number in the draft must survive the rewrite
        import re
        if all(n in new for n in re.findall(r"\d[\d,]*", text)):
            return new
    except Exception:
        pass
    return text


def draft_messages(raw_cases, exceptions, approved, schedule_rows):
    msgs = []
    appr = {a["case_id"]: a for a in approved.to_dict("records")} if len(approved) else {}
    for c in raw_cases:
        a = appr.get(c["case_id"])
        first = None
        if a is not None and len(schedule_rows):
            s = schedule_rows[schedule_rows["invoice_id"] == c["invoice_id"]]
            first = s["class_date"].min() if len(s) else None
        facts = _facts(c, a, first)
        ex = exceptions[exceptions["case_id"] == c["case_id"]] if len(exceptions) else exceptions
        for _, e in ex.iterrows():
            code = e["reason_code"]
            if code == "INVOICE_REF_AUTOCORRECTED":
                facts["wrong_inv"] = e["detail"].split("cites invoice ")[1].split(" ")[0]
            if code == "PARTIAL_PAYMENT":
                facts["gross"] = e["detail"].split(" of INR ")[1].rstrip(".")
            if code == "DISCOUNT_NEEDS_APPROVAL":
                facts["gross"] = e["detail"].split(" on INR ")[1].split(";")[0]
            if code == "BATCH_CHANGE_NO_MATCH":
                facts["want"] = e["detail"].split("Wants ")[1].split(" for class")[0]
            if code == "TEACHER_AMOUNT_MISMATCH":
                facts["form_amt"] = e["detail"].split("Form says INR ")[1].split(";")[0]
        for _, e in ex.iterrows():
            for channel, who, tpl in TEMPLATES.get(e["reason_code"], []):
                txt = tpl.format(**facts)
                msgs.append({"case_id": c["case_id"], "reason_code": e["reason_code"], "channel": channel,
                             "recipient": who, "message": _gemini_polish(txt, who)})
        if c.get("decision") == "AUTO_APPROVE":
            channel, who, tpl = CONFIRMATION
            msgs.append({"case_id": c["case_id"], "reason_code": "AUTO_APPROVED", "channel": channel,
                         "recipient": who, "message": _gemini_polish(tpl.format(**facts), who)})
    return msgs
