<!-- TokenCap v1.6 Savings: baseline 41,498 tok → actual 33,663 tok (18.9% saved) -->
# AI ENTRY POINT

This repository has been indexed by TokenCap.

Before analyzing files, read:

.tokencap/agent/START_HERE.md

Use:

- .tokencap/agent/agent-pack.md
- .tokencap/agent/allowed-context.json
- .tokencap/agent/context-manifest.json

Do not rediscover the repository from scratch.

---

# TokenCap Snapshot

| Field | Value |
| --- | --- |
| Generated | 2026-11-08T02:13:02.858Z |
| Workspace | a:\Bambinos |
| Profile | balanced |
| Selected files | 22 |
| Source bytes | 124127 |
| Estimated source tokens | 41498 |

## Read First

This file is a compressed coding-session handoff. Read it before editing, then inspect the referenced files directly. Prefer the live repository over this snapshot when there is a conflict.

## TokenCap Intelligence Files

- TOKENCAP_GRAPH.md — Project dependency and architecture graph *(JS/TS projects only)*
- TOKENCAP_MEMORY.md — Developer notes, current task, constraints, and context memory

## Handoff Summary

| Field | Value |
| --- | --- |
| Read order | README.md > requirements.txt > src/messages.py > src/pipeline.py > src/rules.py |
| Primary anchors | README.md, requirements.txt, src/messages.py |
| Changed files | 0 |
| TODO notes | 0 |
| File budget used | 24% |
| Source budget used | 56% |
| Token estimate | 41498 |
| Contents mode | enabled |

## Handoff Guidelines

- Preserve user changes; avoid reverting unrelated work.
- Start with changed files and files marked `high-signal` in the manifest.
- Treat the Git diff as intent and verify changes in source files.
- Update this snapshot after meaningful edits or before handing off.

## Git Snapshot

| Field | Value |
| --- | --- |
| Branch | main |
| Git root | A:/Bambinos |

Recent commits:
```text
16caab6 Remove embedded assets clone from index
60020ec Renewal reconciliation agent: rules engine, LangGraph pipeline, dashboard, report
e12d5c4 INAM KING
2b79734 first commit
```

Status:
```text
clean or unavailable
```

## Project Map

```text
dashboard/
data/
outputs/
prompts/
report/
src/
README.md
dashboard/app.py
data/1_invoices.csv
data/2_faculty_form_unapproved.csv
data/3_booking_requests.csv
data/4_class_schedule_bookings.csv
data/reference_active_batches_and_students.csv
outputs/0_reconciliation_ledger.csv
outputs/1_auto_approved_ready_for_scheduling.csv
outputs/1b_class_schedule_bookings_to_insert.csv
outputs/2_flagged_exceptions.csv
outputs/3_followup_messages.csv
outputs/3_followup_messages.md
outputs/metrics.json
prompts/exception_triage_rules.md
prompts/message_drafter.md
report/report.html
requirements.txt
src/messages.py
src/pipeline.py
src/reconcile.py
src/rules.py
```

## File Manifest

| File | Bytes | Score | Why |
| --- | ---: | ---: | --- |
| README.md | 4793 | 105 | project-metadata, high-signal-doc |
| requirements.txt | 43 | 70 | project-metadata |
| src/messages.py | 11377 | 30 | source |
| src/pipeline.py | 6482 | 30 | source |
| src/rules.py | 6982 | 30 | source |
| src/reconcile.py | 14545 | 29 | source |
| dashboard/app.py | 2421 | 0 | context |
| data/1_invoices.csv | 4193 | 0 | context |
| data/2_faculty_form_unapproved.csv | 3488 | 0 | context |
| data/3_booking_requests.csv | 882 | 0 | context |
| data/4_class_schedule_bookings.csv | 514 | 0 | context |
| data/reference_active_batches_and_students.csv | 2829 | 0 | context |
| outputs/0_reconciliation_ledger.csv | 3582 | 0 | context |
| outputs/1_auto_approved_ready_for_scheduling.csv | 1199 | 0 | context |
| outputs/2_flagged_exceptions.csv | 3519 | 0 | context |
| outputs/3_followup_messages.csv | 5681 | 0 | context |
| outputs/3_followup_messages.md | 5997 | 0 | context |
| outputs/metrics.json | 1158 | 0 | context |
| prompts/exception_triage_rules.md | 2590 | 0 | context |
| prompts/message_drafter.md | 1108 | 0 | context |
| outputs/1b_class_schedule_bookings_to_insert.csv | 18883 | -1 | context |
| report/report.html | 21861 | -1 | context |

## Changed Files

No Git changes found, or this is not a Git repository.

## Git Diff Snippets

No diff available, or Git is unavailable.

## TODO / FIXME / HACK Notes

No TODO/FIXME/HACK notes found in selected files.

## Selected File Context

### README.md

| Field | Value |
| --- | --- |
| Bytes | 4793 |
| Score | 105 |
| Why | project-metadata, high-signal-doc |
| Status | Full content |


```markdown
# Bambinos.live: Renewal → Scheduling Reconciliation Agent

AI Program Manager (Operations) take-home. This repo is **Deliverable C**, the working prototype. The PDF report covers A, B and D: [`report/Bambinos_Renewal_Case_Report.pdf`](report/Bambinos_Renewal_Case_Report.pdf).

**The main idea:** the payment gateway is the source of truth. For a same-batch renewal, the teacher form (Step 2) and the manual Ops approval (Step 3) add no new information. The engine approves those clean cases automatically and sends only real exceptions to a person: the one who can fix it, with a reason code and an SLA.

## What it does

The engine reads the 5 provided CSVs (`data/`) and runs them through a LangGraph pipeline:

```
load → reconcile (rules) → draft_messages (templates, optional Gemini) → metrics → write
```

| Output | File |
|---|---|
| (1) Auto-approved renewals ready for scheduling | `outputs/1_auto_approved_ready_for_scheduling.csv` |
| (1b) `class_schedule_bookings` rows to insert, 24 sessions each | `outputs/1b_class_schedule_bookings_to_insert.csv` |
| (2) Flagged exceptions with reason code, severity, owner, SLA and action | `outputs/2_flagged_exceptions.csv` |
| (3) Drafted WhatsApp/Slack follow-ups | `outputs/3_followup_messages.csv`, `.md` |
| Full ledger: every invoice, its current stage and its ages | `outputs/0_reconciliation_ledger.csv` |
| SLA metrics | `outputs/metrics.json` |

## Result on the provided dataset (as of 2026-11-04 09:00)

| Invoice | Decision | Reason codes |
|---|---|---|
| 84901 | Already scheduled | none |
| 84902 | ✅ Auto-approve | STUCK_AT_ALLOCATION (same batch, waiting 66.7h) |
| 84903 | ✅ Auto-approve | CLEAN (was sitting 47.9h in the Ops queue) |
| 84904 | ✅ Auto-approve | PAYER_CONTACT_MISMATCH (mother paid from her own number, IDs match) |
| 84905 | ✅ Auto-approve | FALSE_BATCH_FULL (the child already holds 1 of the 6 seats) |
| 84906 | ✅ Auto-approve | ORPHANED_INVOICE (no teacher form, fast-tracked) |
| 84907 | ⛔ Exception | DISCOUNT_NEEDS_APPROVAL (20% > 10% limit) → Ops Lead |
| 84908 | ✅ Auto-approve | DUPLICATE_FORM (3309 closed) |
| 84909 | ⛔ Exception | PARTIAL_PAYMENT + TEACHER_AMOUNT_MISMATCH → Ops Finance |
| 84910 | ✅ Auto-approve | ORPHANED_INVOICE |
| 84911 | ⛔ Exception | PAYMENT_FAILED (screenshot ≠ payment) → Parent retry link |
| 84912 | ⛔ Exception | BATCH_CHANGE_NO_MATCH (no Sat-Sun 11:00 batch for class 301) → Scheduler |
| 84913 | ✅ Auto-approve | INVOICE_REF_AUTOCORRECTED (84931→84913) + NAME_ENCODING_ANOMALY (Cyrillic "Ме") |

Result: **8 auto-approved, 4 exceptions, 192 sessions ready to book, 22 messages drafted.**

## Run it

```bash
pip install -r requirements.txt
cd src && python pipeline.py --data ../data --out ../outputs --as-of "2026-11-04 09:00:00"
cd .. && streamlit run dashboard/app.py          # Ops Head morning board
```

Optional: copy `.env.example` to `.env` and add `GROQ_API_KEY` (or `GEMINI_API_KEY`). The LLM then polishes the message tone. Groq is tried first. Without a key, the deterministic templates are used and everything still works.
If `langgraph` is not installed, the same nodes run one after another as plain Python.

## Design decisions

- **Rules decide, the LLM only writes.** All approve/reject logic lives in `src/rules.py` and `src/reconcile.py`, so it can be tested and audited. Gemini only rewrites wording, and code checks that every number in the template is still in its output. If any number is missing, the template is sent instead.
- **Match on system IDs, not contact details.** `student_id`, `user_id`, `class_id` and `educator_id` are compared first. Phone and email differences become advisory notes, not blockers.
- **Fuzzy fallback for typos.** If a form's invoice ID is wrong, the engine looks for a unique match on student + user + class + amount and corrects it.
- **Unicode look-alikes are normalised** before any text comparison. Invoice 84913 contains Cyrillic letters that look like Latin ones.
- **Renewing students already hold their seat**, so the capacity check excludes them.
- **No class gap.** A student is never removed from their current batch until the new bookings exist.
- **Assumptions:** sessions start from the next batch day after `as_of`. In production they would start after the current term's last session. The discount auto-limit is 10%. Each renewal takes about 20 minutes of manual work today.

## Repo map

```
data/        the 5 provided CSVs (unchanged)
src/         rules.py · reconcile.py · messages.py · pipeline.py (LangGraph)
prompts/     message_drafter.md (LLM prompt) · exception_triage_rules.md (rule spec)
dashboard/   app.py (Streamlit Ops morning board)
outputs/     generated results
report/      case report (HTML source + PDF)
```
```

### requirements.txt

| Field | Value |
| --- | --- |
| Bytes | 43 |
| Score | 70 |
| Why | project-metadata |
| Status | Full content |


```txt
pandas>=2.0
langgraph>=0.2
streamlit>=1.30
```

### src/messages.py

| Field | Value |
| --- | --- |
| Bytes | 11377 |
| Score | 30 |
| Why | source |
| Status | Full content |


```py
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
```

### src/pipeline.py

| Field | Value |
| --- | --- |
| Bytes | 6482 |
| Score | 30 |
| Why | source |
| Status | Full content |


```py
"""
Renewal Reconciliation Agent - orchestrated as a LangGraph StateGraph.

  load -> reconcile -> draft_messages -> metrics -> write
(falls back to plain sequential execution if langgraph is not installed)

Usage:
  python src/pipeline.py                       # uses ./data, as-of 2026-11-04 09:00
  python src/pipeline.py --as-of "2026-11-04 09:00:00" --data data --out outputs
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any, TypedDict

import pandas as pd

from messages import draft_messages
from reconcile import reconcile
from rules import REASON_CODES, load_tables

MANUAL_MIN_PER_CASE = {           # current-state manual effort estimate (minutes)
    "teacher_form": 6,            # teacher finds invoice, fills 15-field form
    "ops_verify": 8,              # ops opens invoice, cross-checks amount/phone/batch
    "ops_allocate": 6,            # ops picks batch, creates bookings
    "chasing": 10,                # avg follow-up chasing per exception
}


class State(TypedDict, total=False):
    data_dir: str
    out_dir: str
    as_of: datetime
    tables: dict
    result: dict
    messages: list
    metrics: dict


def node_load(s: State) -> State:
    return {"tables": load_tables(s["data_dir"])}


def node_reconcile(s: State) -> State:
    return {"result": reconcile(s["tables"], s["as_of"])}


def node_messages(s: State) -> State:
    r = s["result"]
    return {"messages": draft_messages(r["raw_cases"], r["exceptions"], r["approved"], r["schedule_rows"])}


def node_metrics(s: State) -> State:
    r, t = s["result"], s["tables"]
    cases, ex = r["cases"], r["exceptions"]
    inv = cases[cases["invoice_id"].notna()]
    paid = inv[inv["payment_status"].isin(["Paid", "Partially_Paid"])]
    unscheduled = paid[paid["current_stage"] != "4_SCHEDULED"]
    p2s = inv["payment_to_schedule_hours"].dropna()
    n_auto = int((cases["decision"] == "AUTO_APPROVE").sum())
    n_exc = int((cases["decision"] == "EXCEPTION").sum())
    blocking = ex[ex["severity"] == "BLOCKING"] if len(ex) else ex
    m = {
        "as_of": s["as_of"].strftime("%Y-%m-%d %H:%M"),
        "renewal_invoices": int(len(inv)),
        "paid_or_partial": int(len(paid)),
        "already_scheduled": int((cases["decision"] == "ALREADY_SCHEDULED").sum()),
        "auto_approved_now": n_auto,
        "exceptions_open": n_exc,
        "paid_not_scheduled": int(len(unscheduled)),
        "paid_not_scheduled_gt_12h": int((unscheduled["hours_since_payment"] > 12).sum()),
        "revenue_paid_not_scheduled_inr": float(unscheduled["net_amount"].sum()),
        "orphaned_invoice_rate_pct": round(100 * (paid["current_stage"] == "1_PAID_NO_FORM").sum() / max(len(paid), 1), 1),
        "teacher_forms_pending_ops": int((t["forms"]["approval_status"] == "Pending").sum()),
        "duplicate_form_rate_pct": round(100 * (ex["reason_code"] == "DUPLICATE_FORM").sum() / max(len(t["forms"]), 1), 1) if len(ex) else 0,
        "form_data_error_rate_pct": round(100 * ex[ex["reason_code"].isin(
            ["INVOICE_REF_AUTOCORRECTED", "TEACHER_AMOUNT_MISMATCH", "DUPLICATE_FORM"])]["form_id"].nunique()
            / max(len(t["forms"]), 1), 1) if len(ex) else 0,
        "median_payment_to_schedule_hours": float(p2s.median()) if len(p2s) else None,
        "oldest_unscheduled_paid_hours": float(unscheduled["hours_since_payment"].max()) if len(unscheduled) else 0,
        "straight_through_rate_pct": round(100 * n_auto / max(n_auto + n_exc, 1), 1),
        "exceptions_by_owner": blocking.groupby("owner").size().to_dict() if len(blocking) else {},
        "reason_code_counts": ex["reason_code"].value_counts().to_dict() if len(ex) else {},
    }
    manual = sum(MANUAL_MIN_PER_CASE[k] for k in ("teacher_form", "ops_verify", "ops_allocate"))
    m["manual_minutes_saved_this_run"] = n_auto * manual
    m["manual_minutes_per_renewal_today"] = manual
    return {"metrics": m}


def node_write(s: State) -> State:
    out = Path(s["out_dir"])
    out.mkdir(parents=True, exist_ok=True)
    r = s["result"]
    r["approved"].to_csv(out / "1_auto_approved_ready_for_scheduling.csv", index=False)
    r["schedule_rows"].to_csv(out / "1b_class_schedule_bookings_to_insert.csv", index=False)
    r["exceptions"].to_csv(out / "2_flagged_exceptions.csv", index=False)
    pd.DataFrame(s["messages"]).to_csv(out / "3_followup_messages.csv", index=False)
    r["cases"].to_csv(out / "0_reconciliation_ledger.csv", index=False)
    (out / "metrics.json").write_text(json.dumps(s["metrics"], indent=2, default=str), encoding="utf-8")

    md = ["# Follow-up messages (auto-drafted)\n"]
    for cid, grp in pd.DataFrame(s["messages"]).groupby("case_id", sort=False):
        md.append(f"\n## {cid}\n")
        for _, m in grp.iterrows():
            md.append(f"- **{m['channel']} -> {m['recipient']}** (`{m['reason_code']}`)\n  > {m['message']}\n")
    (out / "3_followup_messages.md").write_text("".join(md), encoding="utf-8")
    return {}


NODES = [("load", node_load), ("reconcile", node_reconcile), ("draft_messages", node_messages),
         ("metrics", node_metrics), ("write", node_write)]


def build_graph():
    from langgraph.graph import END, START, StateGraph
    g = StateGraph(State)
    for name, fn in NODES:
        g.add_node(name, fn)
    g.add_edge(START, NODES[0][0])
    for (a, _), (b, _) in zip(NODES, NODES[1:]):
        g.add_edge(a, b)
    g.add_edge(NODES[-1][0], END)
    return g.compile()


def run(data_dir="data", out_dir="outputs", as_of="2026-11-04 09:00:00") -> State:
    state: State = {"data_dir": data_dir, "out_dir": out_dir,
                    "as_of": datetime.strptime(as_of, "%Y-%m-%d %H:%M:%S")}
    try:
        return build_graph().invoke(state)
    except ImportError:
        for _, fn in NODES:
            state.update(fn(state))
        return state


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data")
    ap.add_argument("--out", default="outputs")
    ap.add_argument("--as-of", default="2026-11-04 09:00:00")
    a = ap.parse_args()
    s = run(a.data, a.out, a.as_of)
    m = s["metrics"]
    print(f"As of {m['as_of']}: {m['renewal_invoices']} renewal invoices | "
          f"auto-approved {m['auto_approved_now']} | exceptions {m['exceptions_open']} | "
          f"already scheduled {m['already_scheduled']}")
    print(json.dumps(m["reason_code_counts"], indent=1))
```

### src/rules.py

| Field | Value |
| --- | --- |
| Bytes | 6982 |
| Score | 30 |
| Why | source |
| Status | Full content |


```py
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
```

### src/reconcile.py

| Field | Value |
| --- | --- |
| Bytes | 14545 |
| Score | 29 |
| Why | source |
| Status | Truncated (budget limit) |

**Structural Outline:**
  - `def dedupe_forms` (line 15)
  - `def resolve_form_invoice` (line 25)
  - `def reconcile` (line 41)
  - `def add_reason` (line 57)


```py
// … lines 1–19
"""
Reconciliation engine: one 'case' per renewal invoice (+ any teacher form that
cannot be tied to an invoice). Produces a decision, reason codes and stage ages.
"""
from __future__ import annotations

from datetime import datetime

import pandas as pd

from rules import (REASON_CODES, DISCOUNT_AUTO_LIMIT_PCT, batch_catalog, clean, has_homoglyph,
                   hours_between, money, norm_phone, norm_text, next_sessions, ts)


def dedupe_forms(forms: pd.DataFrame):
    """Keep the earliest form per (student, invoice, amount); flag the rest."""
    forms = forms.sort_values("created_at")
    key = forms["student_id"] + "|" + forms["invoice_id"].fillna("") + "|" + forms["amount_paid"].fillna("")
    dup_mask = key.duplicated(keep="first")
// … lines 24–29

def resolve_form_invoice(form, invoices):
    """Return (invoice_row | None, autocorrected: bool)."""
    exact = invoices[(invoices["id"] == form["invoice_id"]) & (invoices["student_id"] == form["student_id"])]
    if len(exact) == 1:
        return exact.iloc[0], False
// … lines 40–45

def reconcile(t: dict, as_of: datetime) -> dict:
    inv, roster, bookings, sched = t["invoices"], t["roster"], t["bookings"], t["schedule"]
    inv = inv[inv["is_renewal"] == "Yes"]
    catalog = batch_catalog(roster)
    forms, dup_forms = dedupe_forms(t["forms"])
// … lines 56–61

    def add_reason(case, code, detail):
        sev, owner, sla, action = REASON_CODES[code]
        case["reasons"].append(code)
        exceptions.append({
            "case_id": case["case_id"], "invoice_id": case["invoice_id"], "form_id": case["form_id"],
```

### dashboard/app.py

| Field | Value |
| --- | --- |
| Bytes | 2421 |
| Score | 0 |
| Why | context |
| Status | Full content |


```py
"""Ops Head morning dashboard.  Run:  streamlit run dashboard/app.py"""
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from pipeline import run  # noqa: E402

st.set_page_config(page_title="Renewal Ops - Morning Board", layout="wide")
st.title("Renewal -> Scheduling: Ops Morning Board")

as_of = st.sidebar.text_input("As of", "2026-11-04 09:00:00")
s = run(str(ROOT / "data"), str(ROOT / "outputs"), as_of)
m, r = s["metrics"], s["result"]
cases, ex, msgs = r["cases"], r["exceptions"], pd.DataFrame(s["messages"])

k = st.columns(6)
k[0].metric("Paid, not scheduled", m["paid_not_scheduled"], f"INR {m['revenue_paid_not_scheduled_inr']:,.0f}", delta_color="off")
k[1].metric("Stuck > 12h", m["paid_not_scheduled_gt_12h"], f"oldest {m['oldest_unscheduled_paid_hours']:.0f}h", delta_color="inverse")
k[2].metric("Auto-approved now", m["auto_approved_now"])
k[3].metric("Open exceptions", m["exceptions_open"])
k[4].metric("Orphaned invoice rate", f"{m['orphaned_invoice_rate_pct']}%")
k[5].metric("Ops hours saved (run)", f"{m['manual_minutes_saved_this_run']/60:.1f}h")

st.subheader("Pipeline: where every paid renewal is sitting right now")
st.bar_chart(cases["current_stage"].value_counts())

c1, c2 = st.columns(2)
with c1:
    st.subheader("Blocking exceptions (needs a human)")
    b = ex[ex["severity"] == "BLOCKING"]
    st.dataframe(b[["case_id", "reason_code", "owner", "sla_hours", "detail"]], hide_index=True, use_container_width=True)
with c2:
    st.subheader("Exceptions by owner")
    st.bar_chart(b.groupby("owner").size())

st.subheader("Auto-approved -> ready for class_schedule_bookings")
st.dataframe(r["approved"], hide_index=True, use_container_width=True)

st.subheader("Advisory notes (auto-handled, FYI)")
st.dataframe(ex[ex["severity"] == "ADVISORY"][["case_id", "reason_code", "owner", "detail"]], hide_index=True, use_container_width=True)

st.subheader("Drafted follow-ups")
who = st.selectbox("Recipient", ["All"] + sorted(msgs["recipient"].unique()))
view = msgs if who == "All" else msgs[msgs["recipient"] == who]
for _, x in view.iterrows():
    st.markdown(f"**{x['case_id']} · {x['channel']} -> {x['recipient']}** `{x['reason_code']}`\n\n> {x['message']}")

st.subheader("Full reconciliation ledger")
st.dataframe(cases, hide_index=True, use_container_width=True)
```

### data/1_invoices.csv

| Field | Value |
| --- | --- |
| Bytes | 4193 |
| Score | 0 |
| Why | context |
| Status | Full content |


```csv
id,invoice_number,user_id,student_id,class_id,educator_id,parent_name,mobile,email,currency,amount,discount_amount,net_amount,payment_type,payment_mode,payment_gateway,gateway_order_id,gateway_payment_id,invoice_link,payment_status,is_renewal,paid_at,created_at,updated_at,deleted_at
84901,BMB-INV-2026-84901,41021,68101,104,1102,Pr***a Sh***a,+91-9811XXXX01,pr***a.sh***@gmail.com,INR,12000.00,0.00,12000.00,Full,UPI,Razorpay,order_P8x91****01,pay_P8x99****01,https://bambinos.live/invoice/BMB-INV-2026-84901,Paid,Yes,2026-11-01 10:15:22,2026-11-01 10:12:00,2026-11-01 10:15:22,NULL
84902,BMB-INV-2026-84902,41022,68102,205,1108,Ka***k Na***r,+91-9822XXXX02,ka***k.n***@yahoo.com,INR,10500.00,0.00,10500.00,Full,Card,Razorpay,order_P8x91****02,pay_P8x99****02,https://bambinos.live/invoice/BMB-INV-2026-84902,Paid,Yes,2026-11-01 14:20:10,2026-11-01 14:15:00,2026-11-01 14:20:10,NULL
84903,BMB-INV-2026-84903,41023,68103,301,1115,Ne***a Ve***a,+91-9833XXXX03,ne***a.v***@gmail.com,INR,9000.00,0.00,9000.00,Full,UPI,Razorpay,order_P8x91****03,pay_P8x99****03,https://bambinos.live/invoice/BMB-INV-2026-84903,Paid,Yes,2026-11-02 09:05:44,2026-11-02 09:00:12,2026-11-02 09:05:44,NULL
84904,BMB-INV-2026-84904,41024,68104,104,1102,Ri***u Iy***r,+91-9844XXXX77,ri***u.iy***@gmail.com,INR,12000.00,0.00,12000.00,Full,Netbanking,Razorpay,order_P8x91****04,pay_P8x99****04,https://bambinos.live/invoice/BMB-INV-2026-84904,Paid,Yes,2026-11-02 11:30:05,2026-11-02 11:25:00,2026-11-02 11:30:05,NULL
84905,BMB-INV-2026-84905,41025,68105,402,1122,Me***a Pa***l,+91-9855XXXX05,me***a.p***@gmail.com,INR,11000.00,0.00,11000.00,Full,UPI,Razorpay,order_P8x91****05,pay_P8x99****05,https://bambinos.live/invoice/BMB-INV-2026-84905,Paid,Yes,2026-11-02 13:10:19,2026-11-02 13:05:00,2026-11-02 13:10:19,NULL
84906,BMB-INV-2026-84906,41026,68106,108,1102,Fa***n Kh***n,+971-5012XXX06,fa***n.k***@dubai.ae,INR,18000.00,0.00,18000.00,Full,Card,Stripe,order_S9m21****06,pay_S9m99****06,https://bambinos.live/invoice/BMB-INV-2026-84906,Paid,Yes,2026-11-02 16:00:00,2026-11-02 15:55:00,2026-11-02 16:00:00,NULL
84907,BMB-INV-2026-84907,41027,68107,101,1125,Po***a Jo***i,+91-9877XXXX07,po***a.j***@gmail.com,INR,9500.00,1900.00,7600.00,Full,UPI,Razorpay,order_P8x91****07,pay_P8x99****07,https://bambinos.live/invoice/BMB-INV-2026-84907,Paid,Yes,2026-11-02 18:45:30,2026-11-02 18:40:00,2026-11-02 18:45:30,NULL
84908,BMB-INV-2026-84908,41028,68108,302,1115,Ro***n Ma***a,+1-40855XXX08,ro***n.m***@techcorp.com,INR,22000.00,0.00,22000.00,Full,Card,Stripe,order_S9m21****08,pay_S9m99****08,https://bambinos.live/invoice/BMB-INV-2026-84908,Paid,Yes,2026-11-03 08:15:11,2026-11-03 08:10:00,2026-11-03 08:15:11,NULL
84909,BMB-INV-2026-84909,41029,68109,204,1108,Sn***a Ku***i,+91-9899XXXX09,sn***a.k***@gmail.com,INR,10500.00,0.00,5250.00,Installment_1_of_2,UPI,Razorpay,order_P8x91****09,pay_P8x99****09,https://bambinos.live/invoice/BMB-INV-2026-84909,Partially_Paid,Yes,2026-11-03 10:00:00,2026-11-03 09:55:00,2026-11-03 10:00:00,NULL
84910,BMB-INV-2026-84910,41030,68110,401,1122,Vi***m Re***y,+91-9800XXXX10,vi***m.r***@gmail.com,INR,11000.00,0.00,11000.00,Full,UPI,Razorpay,order_P8x91****10,pay_P8x99****10,https://bambinos.live/invoice/BMB-INV-2026-84910,Paid,Yes,2026-11-03 11:20:45,2026-11-03 11:15:00,2026-11-03 11:20:45,NULL
84911,BMB-INV-2026-84911,41031,68111,102,1125,An***i Gu***a,+91-9811XXXX11,an***i.g***@gmail.com,INR,12000.00,0.00,12000.00,Full,UPI,Razorpay,order_P8x91****11,NULL,https://bambinos.live/invoice/BMB-INV-2026-84911,Failed,Yes,NULL,2026-11-03 12:30:00,2026-11-03 12:35:00,NULL
84912,BMB-INV-2026-84912,41032,68112,301,1115,De***k Me***n,+91-9822XXXX12,de***k.m***@gmail.com,INR,9000.00,0.00,9000.00,Full,Card,Razorpay,order_P8x91****12,pay_P8x99****12,https://bambinos.live/invoice/BMB-INV-2026-84912,Paid,Yes,2026-11-03 15:40:12,2026-11-03 15:35:00,2026-11-03 15:40:12,NULL
84913,BMB-INV-2026-84913,41033,68113,501,1130,Ar***n Ме***a,+91-9833XXXX13,ar***n.m***@gmail.com,INR,11500.00,0.00,11500.00,Full,UPI,Razorpay,order_P8x91****13,pay_P8x99****13,https://bambinos.live/invoice/BMB-INV-2026-84913,Paid,Yes,2026-11-03 16:50:00,2026-11-03 16:45:00,2026-11-03 16:50:00,NULL
```

### data/2_faculty_form_unapproved.csv

| Field | Value |
| --- | --- |
| Bytes | 3488 |
| Score | 0 |
| Why | context |
| Status | Full content |


```csv
id,educator_id,educator_name,user_id,student_id,student_name,parent_mobile,class_id,current_classbatch_id,invoice_id,invoice_link,amount_paid,sessions_purchased,continue_same_batch,preferred_days,preferred_time_slot,remarks,approval_status,approved_by,approved_at,created_at,updated_at,deleted_at
3301,1102,Ms. Rhea B***,41021,68101,Aa***v Sh***a,+91-9811XXXX01,104,9201,84901,https://bambinos.live/invoice/BMB-INV-2026-84901,12000.00,24,Yes,"Tue,Thu",17:00:00,Continue in same batch 9201,Approved,ops_exec_02,2026-11-01 11:30:00,2026-11-01 10:45:00,2026-11-01 11:30:00,NULL
3302,1108,Mr. Vikram S***,41022,68102,Di***a Na***r,+91-9822XXXX02,205,9202,84902,https://bambinos.live/invoice/BMB-INV-2026-84902,10500.00,24,Yes,"Mon,Wed",18:00:00,Same batch 9202,Approved,ops_exec_01,2026-11-01 17:00:00,2026-11-01 15:10:00,2026-11-01 17:00:00,NULL
3303,1115,Acharya Nancy S***,41023,68103,Ka***r Ve***a,+91-9833XXXX03,301,9203,84903,https://bambinos.live/invoice/BMB-INV-2026-84903,9000.00,24,Yes,"Wed,Fri",16:30:00,Continue same batch 9203,Pending,NULL,NULL,2026-11-02 09:30:00,2026-11-02 09:30:00,NULL
3304,1102,Ms. Rhea B***,41024,68104,An***a Iy***r,+91-9844XXXX04,104,9201,84904,https://bambinos.live/invoice/BMB-INV-2026-84904,12000.00,24,Yes,"Tue,Thu",17:00:00,Mother paid from her number,Pending,NULL,NULL,2026-11-02 12:00:00,2026-11-02 12:00:00,NULL
3305,1122,Coach Arvind K***,41025,68105,Re***h Pa***l,+91-9855XXXX05,402,9205,84905,https://bambinos.live/invoice/BMB-INV-2026-84905,11000.00,24,Yes,"Sat,Sun",11:00:00,Continue batch 9205,Approved,ops_exec_03,2026-11-02 16:30:00,2026-11-02 14:00:00,2026-11-02 16:30:00,NULL
3307,1125,Ms. Simran D***,41027,68107,Vi***n Jo***i,+91-9877XXXX07,101,9207,84907,https://bambinos.live/invoice/BMB-INV-2026-84907,7600.00,24,Yes,"Mon,Thu",15:30:00,Offered 20% retention scholarship discount,Pending,NULL,NULL,2026-11-02 19:10:00,2026-11-02 19:10:00,NULL
3308,1115,Acharya Nancy S***,41028,68108,Si***a Ma***a,+1-40855XXX08,302,9208,84908,https://bambinos.live/invoice/BMB-INV-2026-84908,22000.00,24,Yes,"Sat,Sun",09:30:00,Continue US batch 9208,Pending,NULL,NULL,2026-11-03 08:30:00,2026-11-03 08:30:00,NULL
3309,1115,Acharya Nancy S***,41028,68108,Si***a Ma***a,+1-40855XXX08,302,9208,84908,https://bambinos.live/invoice/BMB-INV-2026-84908,22000.00,24,Yes,"Sat,Sun",09:30:00,Resubmitted as browser froze,Pending,NULL,NULL,2026-11-03 08:35:12,2026-11-03 08:35:12,NULL
3310,1108,Mr. Vikram S***,41029,68109,Ad***t Ku***i,+91-9899XXXX09,204,9209,84909,https://bambinos.live/invoice/BMB-INV-2026-84909,10500.00,24,Yes,"Tue,Fri",17:30:00,Same batch 9209,Pending,NULL,NULL,2026-11-03 10:30:00,2026-11-03 10:30:00,NULL
3311,1125,Ms. Simran D***,41031,68111,Is***n Gu***a,+91-9811XXXX11,102,9211,84911,https://bambinos.live/invoice/BMB-INV-2026-84911,12000.00,24,Yes,"Mon,Wed",16:00:00,Parent shared UPI processing screenshot,Pending,NULL,NULL,2026-11-03 12:45:00,2026-11-03 12:45:00,NULL
3312,1115,Acharya Nancy S***,41032,68112,Ta***a Me***n,+91-9822XXXX12,301,9203,84912,https://bambinos.live/invoice/BMB-INV-2026-84912,9000.00,24,No,"Sat,Sun",11:00:00,Parent wants weekend 11 AM batch instead of Wed-Fri,Approved,ops_exec_02,2026-11-03 17:15:00,2026-11-03 16:00:00,2026-11-03 17:15:00,NULL
3313,1130,Ms. Mary M***,41033,68113,De***a Me***a,+91-9833XXXX13,501,9213,84931,https://bambinos.live/invoice/BMB-INV-2026-84931,11500.00,24,Yes,"Tue,Thu",18:00:00,Same batch 9213,Pending,NULL,NULL,2026-11-03 17:10:00,2026-11-03 17:10:00,NULL
```

### data/3_booking_requests.csv

| Field | Value |
| --- | --- |
| Bytes | 882 |
| Score | 0 |
| Why | context |
| Status | Full content |


```csv
id,faculty_form_id,invoice_id,user_id,student_id,class_id,educator_id,classbatch_id,sessions_count,is_renewal,continue_same_batch,preferred_days,preferred_time,request_status,batch_allocated,allocated_by,allocated_at,created_at,updated_at,deleted_at
5501,3301,84901,41021,68101,104,1102,9201,24,Yes,Yes,"Tue,Thu",17:00:00,Completed,Yes,ops_exec_02,2026-11-01 12:00:00,2026-11-01 11:30:00,2026-11-01 12:00:00,NULL
5502,3302,84902,41022,68102,205,1108,9202,24,Yes,Yes,"Mon,Wed",18:00:00,Pending_Batch_Allocation,No,NULL,NULL,2026-11-01 17:00:00,2026-11-01 17:00:00,NULL
5505,3305,84905,41025,68105,402,1122,9205,24,Yes,Yes,"Sat,Sun",11:00:00,Failed_Batch_Full,No,NULL,NULL,2026-11-02 16:30:00,2026-11-02 16:35:00,NULL
5512,3312,84912,41032,68112,301,1115,NULL,24,Yes,No,"Sat,Sun",11:00:00,Awaiting_Parent_Batch_Selection,No,NULL,NULL,2026-11-03 17:15:00,2026-11-03 17:15:00,NULL
```

### data/4_class_schedule_bookings.csv

| Field | Value |
| --- | --- |
| Bytes | 514 |
| Score | 0 |
| Why | context |
| Status | Full content |


```csv
id,bookingrequest_id,invoice_id,classschedule_id,classbatch_id,class_id,user_id,student_id,educator_id,class_date,start_time,end_time,booking_type,is_cancelled,attended_class,created_at,updated_at,deleted_at
990101,5501,84901,2126100101,9201,104,41021,68101,1102,2026-11-03,17:00:00,17:50:00,Regular_Renewal,No,Yes,2026-11-01 12:00:05,2026-11-03 18:00:00,NULL
990102,5501,84901,2126100102,9201,104,41021,68101,1102,2026-11-05,17:00:00,17:50:00,Regular_Renewal,No,No,2026-11-01 12:00:05,2026-11-01 12:00:05,NULL
```

### data/reference_active_batches_and_students.csv

| Field | Value |
| --- | --- |
| Bytes | 2829 |
| Score | 0 |
| Why | context |
| Status | Full content |


```csv
student_id,user_id,student_name_masked,parent_name_masked,registered_mobile_masked,registered_email_masked,current_classbatch_id,classbatch_name,class_id,class_name,category_id,category_name,educator_id,educator_name,standard_fee_24_sessions_inr,batch_days,batch_start_time,active_students_count,max_batch_size,deleted_at
68101,41021,Aa***v Sh***a,Pr***a Sh***a,+91-9811XXXX01,pr***a.sh***@gmail.com,9201,YC-G4-Batch-A,104,Young Communicators Level 2,1,English,1102,Ms. Rhea B***,12000.00,"Tue,Thu",17:00:00,4,6,NULL
68102,41022,Di***a Na***r,Ka***k Na***r,+91-9822XXXX02,ka***k.n***@yahoo.com,9202,BM-G5-Batch-C,205,Unbox Maths Level 3,2,Maths,1108,Mr. Vikram S***,10500.00,"Mon,Wed",18:00:00,5,6,NULL
68103,41023,Ka***r Ve***a,Ne***a Ve***a,+91-9833XXXX03,ne***a.v***@gmail.com,9203,LY-G3-Batch-B,301,Little Yogi Gita Level 1,3,Gita,1115,Acharya Nancy S***,9000.00,"Wed,Fri",16:30:00,3,6,NULL
68104,41024,An***a Iy***r,Su***h Iy***r,+91-9844XXXX04,su***h.iy***@outlook.com,9201,YC-G4-Batch-A,104,Young Communicators Level 2,1,English,1102,Ms. Rhea B***,12000.00,"Tue,Thu",17:00:00,4,6,NULL
68105,41025,Re***h Pa***l,Me***a Pa***l,+91-9855XXXX05,me***a.p***@gmail.com,9205,CM-G4-Batch-D,402,Unbox Chess Level 2,4,Chess,1122,Coach Arvind K***,11000.00,"Sat,Sun",11:00:00,6,6,NULL
68106,41026,Zo***a Kh***n,Fa***n Kh***n,+971-5012XXX06,fa***n.k***@dubai.ae,9206,YC-GCC-Batch-E,108,Young Communicators GCC Track,1,English,1102,Ms. Rhea B***,18000.00,"Sun,Tue",19:00:00,5,6,NULL
68107,41027,Vi***n Jo***i,Po***a Jo***i,+91-9877XXXX07,po***a.j***@gmail.com,9207,PH-G1-Batch-F,101,Phonics Champions Level 1,1,English,1125,Ms. Simran D***,9500.00,"Mon,Thu",15:30:00,4,6,NULL
68108,41028,Si***a Ma***a,Ro***n Ma***a,+1-40855XXX08,ro***n.m***@techcorp.com,9208,LY-US-Batch-G,302,Little Yogi Gita US Track,3,Gita,1115,Acharya Nancy S***,22000.00,"Sat,Sun",09:30:00,5,6,NULL
68109,41029,Ad***t Ku***i,Sn***a Ku***i,+91-9899XXXX09,sn***a.k***@gmail.com,9209,BM-G3-Batch-H,204,Unbox Maths Level 2,2,Maths,1108,Mr. Vikram S***,10500.00,"Tue,Fri",17:30:00,4,6,NULL
68110,41030,My***a Re***y,Vi***m Re***y,+91-9800XXXX10,vi***m.r***@gmail.com,9210,CM-G2-Batch-I,401,Unbox Chess Level 1,4,Chess,1122,Coach Arvind K***,11000.00,"Wed,Fri",17:00:00,5,6,NULL
68111,41031,Is***n Gu***a,An***i Gu***a,+91-9811XXXX11,an***i.g***@gmail.com,9211,YC-G2-Batch-J,102,Young Communicators Level 1,1,English,1125,Ms. Simran D***,12000.00,"Mon,Wed",16:00:00,5,6,NULL
68112,41032,Ta***a Me***n,De***k Me***n,+91-9822XXXX12,de***k.m***@gmail.com,9203,LY-G3-Batch-B,301,Little Yogi Gita Level 1,3,Gita,1115,Acharya Nancy S***,9000.00,"Wed,Fri",16:30:00,3,6,NULL
68113,41033,De***a Me***a,Ar***n Me***a,+91-9833XXXX13,ar***n.m***@gmail.com,9213,SC-G4-Batch-K,501,Unbox Science Level 1,5,Science,1130,Ms. Mary M***,11500.00,"Tue,Thu",18:00:00,4,6,NULL
```

### outputs/0_reconciliation_ledger.csv

| Field | Value |
| --- | --- |
| Bytes | 3582 |
| Score | 0 |
| Why | context |
| Status | Full content |


```csv
case_id,invoice_id,form_id,student_id,user_id,class_id,educator_id,student_name,parent_name,parent_mobile,registered_mobile,educator_name,class_name,payment_status,net_amount,paid_at,paid_on_weekend,target_classbatch_id,current_stage,hours_since_payment,form_lag_hours,ops_approval_lag_hours,payment_to_schedule_hours,decision,blocking_reasons,advisory_reasons
RNW-84901,84901,3301,68101,41021,104,1102,Aa***v Sh***a,Pr***a Sh***a,+91-9811XXXX01,+91-9811XXXX01,Ms. Rhea B***,Young Communicators Level 2,Paid,12000.0,2026-11-01 10:15:22,True,,4_SCHEDULED,70.7,0.5,0.8,1.7,ALREADY_SCHEDULED,,
RNW-84902,84902,3302,68102,41022,205,1108,Di***a Na***r,Ka***k Na***r,+91-9822XXXX02,+91-9822XXXX02,Mr. Vikram S***,Unbox Maths Level 3,Paid,10500.0,2026-11-01 14:20:10,True,9202,3_BOOKING_PENDING_BATCH_ALLOCATION,66.7,0.8,1.8,,AUTO_APPROVE,,STUCK_AT_ALLOCATION
RNW-84903,84903,3303,68103,41023,301,1115,Ka***r Ve***a,Ne***a Ve***a,+91-9833XXXX03,+91-9833XXXX03,Acharya Nancy S***,Little Yogi Gita Level 1,Paid,9000.0,2026-11-02 09:05:44,False,9203,2_FORM_PENDING,47.9,0.4,,,AUTO_APPROVE,,
RNW-84904,84904,3304,68104,41024,104,1102,An***a Iy***r,Ri***u Iy***r,+91-9844XXXX77,+91-9844XXXX04,Ms. Rhea B***,Young Communicators Level 2,Paid,12000.0,2026-11-02 11:30:05,False,9201,2_FORM_PENDING,45.5,0.5,,,AUTO_APPROVE,,PAYER_CONTACT_MISMATCH
RNW-84905,84905,3305,68105,41025,402,1122,Re***h Pa***l,Me***a Pa***l,+91-9855XXXX05,+91-9855XXXX05,Coach Arvind K***,Unbox Chess Level 2,Paid,11000.0,2026-11-02 13:10:19,False,9205,3_BOOKING_FAILED_BATCH_FULL,43.8,0.8,2.5,,AUTO_APPROVE,,FALSE_BATCH_FULL
RNW-84906,84906,,68106,41026,108,1102,Zo***a Kh***n,Fa***n Kh***n,+971-5012XXX06,+971-5012XXX06,Ms. Rhea B***,Young Communicators GCC Track,Paid,18000.0,2026-11-02 16:00:00,False,9206,1_PAID_NO_FORM,41.0,,,,AUTO_APPROVE,,ORPHANED_INVOICE
RNW-84907,84907,3307,68107,41027,101,1125,Vi***n Jo***i,Po***a Jo***i,+91-9877XXXX07,+91-9877XXXX07,Ms. Simran D***,Phonics Champions Level 1,Paid,7600.0,2026-11-02 18:45:30,False,9207,2_FORM_PENDING,38.2,0.4,,,EXCEPTION,DISCOUNT_NEEDS_APPROVAL,
RNW-84908,84908,3308,68108,41028,302,1115,Si***a Ma***a,Ro***n Ma***a,+1-40855XXX08,+1-40855XXX08,Acharya Nancy S***,Little Yogi Gita US Track,Paid,22000.0,2026-11-03 08:15:11,False,9208,2_FORM_PENDING,24.7,0.2,,,AUTO_APPROVE,,DUPLICATE_FORM
RNW-84909,84909,3310,68109,41029,204,1108,Ad***t Ku***i,Sn***a Ku***i,+91-9899XXXX09,+91-9899XXXX09,Mr. Vikram S***,Unbox Maths Level 2,Partially_Paid,5250.0,2026-11-03 10:00:00,False,9209,2_FORM_PENDING,23.0,0.5,,,EXCEPTION,PARTIAL_PAYMENT,TEACHER_AMOUNT_MISMATCH
RNW-84910,84910,,68110,41030,401,1122,My***a Re***y,Vi***m Re***y,+91-9800XXXX10,+91-9800XXXX10,Coach Arvind K***,Unbox Chess Level 1,Paid,11000.0,2026-11-03 11:20:45,False,9210,1_PAID_NO_FORM,21.7,,,,AUTO_APPROVE,,ORPHANED_INVOICE
RNW-84911,84911,3311,68111,41031,102,1125,Is***n Gu***a,An***i Gu***a,+91-9811XXXX11,+91-9811XXXX11,Ms. Simran D***,Young Communicators Level 1,Failed,12000.0,,False,9211,2_FORM_PENDING,,,,,EXCEPTION,PAYMENT_FAILED,
RNW-84912,84912,3312,68112,41032,301,1115,Ta***a Me***n,De***k Me***n,+91-9822XXXX12,+91-9822XXXX12,Acharya Nancy S***,Little Yogi Gita Level 1,Paid,9000.0,2026-11-03 15:40:12,False,,3_BOOKING_AWAITING_PARENT_BATCH_SELECTION,17.3,0.3,1.2,,EXCEPTION,BATCH_CHANGE_NO_MATCH,
RNW-84913,84913,3313,68113,41033,501,1130,De***a Me***a,Ar***n Ме***a,+91-9833XXXX13,+91-9833XXXX13,Ms. Mary M***,Unbox Science Level 1,Paid,11500.0,2026-11-03 16:50:00,False,9213,2_FORM_PENDING,16.2,0.3,,,AUTO_APPROVE,,"NAME_ENCODING_ANOMALY,INVOICE_REF_AUTOCORRECTED"
```

### outputs/1_auto_approved_ready_for_scheduling.csv

| Field | Value |
| --- | --- |
| Bytes | 1199 |
| Score | 0 |
| Why | context |
| Status | Full content |


```csv
case_id,bookingrequest_id,invoice_id,faculty_form_id,student_id,user_id,class_id,educator_id,classbatch_id,classbatch_name,batch_days,start_time,sessions_count,fast_track,advisory_notes
RNW-84902,5502,84902,3302,68102,41022,205,1108,9202,BM-G5-Batch-C,"Mon,Wed",18:00:00,24,SAME_BATCH,STUCK_AT_ALLOCATION
RNW-84903,NEW-84903,84903,3303,68103,41023,301,1115,9203,LY-G3-Batch-B,"Wed,Fri",16:30:00,24,SAME_BATCH,CLEAN
RNW-84904,NEW-84904,84904,3304,68104,41024,104,1102,9201,YC-G4-Batch-A,"Tue,Thu",17:00:00,24,SAME_BATCH,PAYER_CONTACT_MISMATCH
RNW-84905,5505,84905,3305,68105,41025,402,1122,9205,CM-G4-Batch-D,"Sat,Sun",11:00:00,24,SAME_BATCH,FALSE_BATCH_FULL
RNW-84906,NEW-84906,84906,NOT_REQUIRED,68106,41026,108,1102,9206,YC-GCC-Batch-E,"Sun,Tue",19:00:00,24,SAME_BATCH,ORPHANED_INVOICE
RNW-84908,NEW-84908,84908,3308,68108,41028,302,1115,9208,LY-US-Batch-G,"Sat,Sun",09:30:00,24,SAME_BATCH,DUPLICATE_FORM
RNW-84910,NEW-84910,84910,NOT_REQUIRED,68110,41030,401,1122,9210,CM-G2-Batch-I,"Wed,Fri",17:00:00,24,SAME_BATCH,ORPHANED_INVOICE
RNW-84913,NEW-84913,84913,3313,68113,41033,501,1130,9213,SC-G4-Batch-K,"Tue,Thu",18:00:00,24,SAME_BATCH,"NAME_ENCODING_ANOMALY,INVOICE_REF_AUTOCORRECTED"
```

### outputs/2_flagged_exceptions.csv

| Field | Value |
| --- | --- |
| Bytes | 3519 |
| Score | 0 |
| Why | context |
| Status | Full content |


```csv
case_id,invoice_id,form_id,student_id,educator_id,reason_code,severity,owner,sla_hours,detail,recommended_action
RNW-84902,84902,3302,68102,1108,STUCK_AT_ALLOCATION,ADVISORY,Ops Scheduler,4,Booking 5502 pending allocation since 2026-11-01 17:00:00 (64.0h).,Approved same-batch renewal waiting for manual batch allocation. Auto-allocated.
RNW-84904,84904,3304,68104,1102,PAYER_CONTACT_MISMATCH,ADVISORY,Ops Agent,24,Payer Ri***u Iy***r / +91-9844XXXX77 / ri***u.iy***@gmail.com vs registered Su***h Iy***r / +91-9844XXXX04 / su***h.iy***@outlook.com. student_id + user_id match.,Payer phone/email differs from the registered contact but system IDs match. Approved; parent asked to confirm the secondary contact.
RNW-84905,84905,3305,68105,1122,FALSE_BATCH_FULL,ADVISORY,Ops Scheduler,4,"Booking 5505 failed: batch 9205 at 6/6, but this student is one of those 6.",Booking failed as 'batch full' but the renewing student already occupies a seat in that batch. Re-allocated.
RNW-84906,84906,,68106,1102,ORPHANED_INVOICE,ADVISORY,Teacher,12,Paid 2026-11-02 16:00:00 (41.0h ago); teacher 1102 has not submitted a form.,Paid renewal with no teacher form. Fast-tracked into the same batch; teacher only informed.
RNW-84907,84907,3307,68107,1125,DISCOUNT_NEEDS_APPROVAL,BLOCKING,Ops Lead,4,"20% discount (INR 1,900) on INR 9,500; net INR 7,600. Teacher note: 'Offered 20% retention scholarship discount'.",Discount above the 10% teacher limit. Ops Lead approves/rejects in one click.
RNW-84908,84908,3308,68108,1115,DUPLICATE_FORM,ADVISORY,Teacher,24,Form 3309 duplicates 3308 ('Resubmitted as browser froze'); auto-closed.,Same renewal submitted more than once; duplicate auto-closed.
RNW-84909,84909,3310,68109,1108,PARTIAL_PAYMENT,BLOCKING,Ops (Finance),12,"Installment_1_of_2: captured INR 5,250 of INR 10,500.",Only an installment is captured. Approve under installment policy (schedule paid sessions) or collect balance.
RNW-84909,84909,3310,68109,1108,TEACHER_AMOUNT_MISMATCH,ADVISORY,Teacher,24,"Form says INR 10,500; gateway captured INR 5,250.",Amount typed in the form differs from the gateway amount; gateway amount used.
RNW-84910,84910,,68110,1122,ORPHANED_INVOICE,ADVISORY,Teacher,12,Paid 2026-11-03 11:20:45 (21.7h ago); teacher 1122 has not submitted a form.,Paid renewal with no teacher form. Fast-tracked into the same batch; teacher only informed.
RNW-84911,84911,3311,68111,1125,PAYMENT_FAILED,BLOCKING,Parent,24,"Gateway status=Failed, no payment_id. Teacher form 3311 submitted anyway: 'Parent shared UPI processing screenshot'.",Gateway shows payment failed. Do NOT approve. Resend payment link to parent; ignore screenshots.
RNW-84912,84912,3312,68112,1115,BATCH_CHANGE_NO_MATCH,BLOCKING,Ops Scheduler,24,"Wants Sat,Sun 11:00:00 for class 301; no such batch. Currently in 9203 (Wed,Fri 16:30:00); booking 5512 = Awaiting_Parent_Batch_Selection.",Parent wants a different slot and no existing batch of this class matches. Student stays in current batch until moved.
RNW-84913,84913,3313,68113,1130,NAME_ENCODING_ANOMALY,ADVISORY,Ops Agent,48,'Ar***n Ме***a' contains non-Latin look-alike characters (vs roster 'Ar***n Me***a').,Name contains look-alike (non-Latin) characters; exact-name matching would silently fail.
RNW-84913,84913,3313,68113,1130,INVOICE_REF_AUTOCORRECTED,ADVISORY,Teacher,24,Form 3313 cites invoice 84931 (does not exist / wrong student); matched to 84913.,Teacher typed the wrong invoice ID; matched uniquely on student_id + user_id + class + amount and corrected.
```

### outputs/3_followup_messages.csv

| Field | Value |
| --- | --- |
| Bytes | 5681 |
| Score | 0 |
| Why | context |
| Status | Full content |


```csv
case_id,reason_code,channel,recipient,message
RNW-84902,AUTO_APPROVED,WhatsApp,Parent,"Hi Ka***k Na***r, Di***a Na***r's renewal for Unbox Maths Level 3 is confirmed! Classes continue in BM-G5-Batch-C on Mon,Wed at 18:00. First class of the new term: 2026-11-09. See you there! - Team Bambinos"
RNW-84903,AUTO_APPROVED,WhatsApp,Parent,"Hi Ne***a Ve***a, Ka***r Ve***a's renewal for Little Yogi Gita Level 1 is confirmed! Classes continue in LY-G3-Batch-B on Wed,Fri at 16:30. First class of the new term: 2026-11-06. See you there! - Team Bambinos"
RNW-84904,PAYER_CONTACT_MISMATCH,WhatsApp,Parent,"Hi Ri***u Iy***r, we received INR 12,000 for An***a Iy***r's renewal - classes are confirmed! The payment came from +91-9844XXXX77, which isn't on An***a Iy***r's profile. Reply YES to add it as a secondary contact for class reminders."
RNW-84904,AUTO_APPROVED,WhatsApp,Parent,"Hi Ri***u Iy***r, An***a Iy***r's renewal for Young Communicators Level 2 is confirmed! Classes continue in YC-G4-Batch-A on Tue,Thu at 17:00. First class of the new term: 2026-11-05. See you there! - Team Bambinos"
RNW-84905,FALSE_BATCH_FULL,Slack,Ops Scheduler,":white_check_mark: RNW-84905 | Booking for Re***h Pa***l failed as 'batch full', but Re***h Pa***l already holds a seat in CM-G4-Batch-D. Auto-reallocated. Please fix the capacity rule to exclude renewing students."
RNW-84905,AUTO_APPROVED,WhatsApp,Parent,"Hi Me***a Pa***l, Re***h Pa***l's renewal for Unbox Chess Level 2 is confirmed! Classes continue in CM-G4-Batch-D on Sat,Sun at 11:00. First class of the new term: 2026-11-07. See you there! - Team Bambinos"
RNW-84906,ORPHANED_INVOICE,WhatsApp,Teacher,"Hi Ms. Rhea B, good news - Zo***a Kh***n's renewal payment (INR 18,000) came in on 2026-11-02 16:00:00. We've auto-renewed them in the same batch. You don't need to fill the renewal form. If the parent wants a different slot, just reply here."
RNW-84906,AUTO_APPROVED,WhatsApp,Parent,"Hi Fa***n Kh***n, Zo***a Kh***n's renewal for Young Communicators GCC Track is confirmed! Classes continue in YC-GCC-Batch-E on Sun,Tue at 19:00. First class of the new term: 2026-11-08. See you there! - Team Bambinos"
RNW-84907,DISCOUNT_NEEDS_APPROVAL,Slack,Ops Lead,":moneybag: RNW-84907 | Ms. Simran D gave Vi***n Jo***i a discount: paid INR 7,600 vs list INR 9,500. Above 10% teacher limit. Reply APPROVE / REJECT. SLA 4h."
RNW-84908,DUPLICATE_FORM,WhatsApp,Teacher,"Hi Acharya Nancy S, we got Si***a Ma***a's renewal form twice (browser refresh). We kept one and closed the duplicate - all good."
RNW-84908,AUTO_APPROVED,WhatsApp,Parent,"Hi Ro***n Ma***a, Si***a Ma***a's renewal for Little Yogi Gita US Track is confirmed! Classes continue in LY-US-Batch-G on Sat,Sun at 09:30. First class of the new term: 2026-11-07. See you there! - Team Bambinos"
RNW-84909,PARTIAL_PAYMENT,Slack,Ops (Finance),":warning: RNW-84909 | Ad***t Ku***i paid installment 1 (INR 5,250) of INR 10,500. Teacher form says INR 10,500. Decide: approve under installment policy or hold. SLA 12h."
RNW-84909,PARTIAL_PAYMENT,WhatsApp,Parent,"Hi Sn***a Ku***i, thank you! We've received INR 5,250 (installment 1) for Ad***t Ku***i's renewal. The second installment link will be shared before it's due. - Team Bambinos"
RNW-84910,ORPHANED_INVOICE,WhatsApp,Teacher,"Hi Coach Arvind K, good news - My***a Re***y's renewal payment (INR 11,000) came in on 2026-11-03 11:20:45. We've auto-renewed them in the same batch. You don't need to fill the renewal form. If the parent wants a different slot, just reply here."
RNW-84910,AUTO_APPROVED,WhatsApp,Parent,"Hi Vi***m Re***y, My***a Re***y's renewal for Unbox Chess Level 1 is confirmed! Classes continue in CM-G2-Batch-I on Wed,Fri at 17:00. First class of the new term: 2026-11-06. See you there! - Team Bambinos"
RNW-84911,PAYMENT_FAILED,WhatsApp,Parent,"Hi An***i Gu***a, we tried to confirm Is***n Gu***a's renewal for Young Communicators Level 1 but the payment of INR 12,000 did not go through (bank status: failed, no money was deducted on our side). Please retry here: https://bambinos.live/invoice/BMB-INV-2026-84911. Is***n Gu***a's current classes continue meanwhile. - Team Bambinos"
RNW-84911,PAYMENT_FAILED,WhatsApp,Teacher,"Hi Ms. Simran D, renewal form 3311 for Is***n Gu***a cannot be approved: the gateway shows invoice 84911 as FAILED. A UPI 'processing' screenshot is not proof of payment. We've sent the parent a retry link - no action needed from you."
RNW-84912,BATCH_CHANGE_NO_MATCH,Slack,Ops Scheduler,":calendar: RNW-84912 | Ta***a Me***n (Little Yogi Gita Level 1) paid & wants Sat,Sun 11:00:00. No existing batch matches. Options: open a new batch / offer nearest slot. Student stays in current batch until moved - no class gap. SLA 24h."
RNW-84912,BATCH_CHANGE_NO_MATCH,WhatsApp,Parent,"Hi De***k Me***n, thanks for renewing Ta***a Me***n! We're finding a Sat,Sun 11:00:00 slot as requested. Until then Ta***a Me***n continues in the current batch so no class is missed. We'll confirm the new timing within 24 hours. - Team Bambinos"
RNW-84913,NAME_ENCODING_ANOMALY,Slack,Ops Agent,:abc: RNW-84913 | Parent name on invoice 84913 contains non-Latin look-alike letters. Normalise in CRM to avoid search/match misses.
RNW-84913,INVOICE_REF_AUTOCORRECTED,WhatsApp,Teacher,"Hi Ms. Mary M, small fix: form 3313 had invoice 84931; the correct one is 84913. We've corrected it and renewed De***a Me***a. Nothing else needed."
RNW-84913,AUTO_APPROVED,WhatsApp,Parent,"Hi Ar***n Ме***a, De***a Me***a's renewal for Unbox Science Level 1 is confirmed! Classes continue in SC-G4-Batch-K on Tue,Thu at 18:00. First class of the new term: 2026-11-05. See you there! - Team Bambinos"
```

### outputs/3_followup_messages.md

| Field | Value |
| --- | --- |
| Bytes | 5997 |
| Score | 0 |
| Why | context |
| Status | Full content |


```markdown
# Follow-up messages (auto-drafted)

## RNW-84902
- **WhatsApp -> Parent** (`AUTO_APPROVED`)
  > Hi Ka***k Na***r, Di***a Na***r's renewal for Unbox Maths Level 3 is confirmed! Classes continue in BM-G5-Batch-C on Mon,Wed at 18:00. First class of the new term: 2026-11-09. See you there! - Team Bambinos

## RNW-84903
- **WhatsApp -> Parent** (`AUTO_APPROVED`)
  > Hi Ne***a Ve***a, Ka***r Ve***a's renewal for Little Yogi Gita Level 1 is confirmed! Classes continue in LY-G3-Batch-B on Wed,Fri at 16:30. First class of the new term: 2026-11-06. See you there! - Team Bambinos

## RNW-84904
- **WhatsApp -> Parent** (`PAYER_CONTACT_MISMATCH`)
  > Hi Ri***u Iy***r, we received INR 12,000 for An***a Iy***r's renewal - classes are confirmed! The payment came from +91-9844XXXX77, which isn't on An***a Iy***r's profile. Reply YES to add it as a secondary contact for class reminders.
- **WhatsApp -> Parent** (`AUTO_APPROVED`)
  > Hi Ri***u Iy***r, An***a Iy***r's renewal for Young Communicators Level 2 is confirmed! Classes continue in YC-G4-Batch-A on Tue,Thu at 17:00. First class of the new term: 2026-11-05. See you there! - Team Bambinos

## RNW-84905
- **Slack -> Ops Scheduler** (`FALSE_BATCH_FULL`)
  > :white_check_mark: RNW-84905 | Booking for Re***h Pa***l failed as 'batch full', but Re***h Pa***l already holds a seat in CM-G4-Batch-D. Auto-reallocated. Please fix the capacity rule to exclude renewing students.
- **WhatsApp -> Parent** (`AUTO_APPROVED`)
  > Hi Me***a Pa***l, Re***h Pa***l's renewal for Unbox Chess Level 2 is confirmed! Classes continue in CM-G4-Batch-D on Sat,Sun at 11:00. First class of the new term: 2026-11-07. See you there! - Team Bambinos

## RNW-84906
- **WhatsApp -> Teacher** (`ORPHANED_INVOICE`)
  > Hi Ms. Rhea B, good news - Zo***a Kh***n's renewal payment (INR 18,000) came in on 2026-11-02 16:00:00. We've auto-renewed them in the same batch. You don't need to fill the renewal form. If the parent wants a different slot, just reply here.
- **WhatsApp -> Parent** (`AUTO_APPROVED`)
  > Hi Fa***n Kh***n, Zo***a Kh***n's renewal for Young Communicators GCC Track is confirmed! Classes continue in YC-GCC-Batch-E on Sun,Tue at 19:00. First class of the new term: 2026-11-08. See you there! - Team Bambinos

## RNW-84907
- **Slack -> Ops Lead** (`DISCOUNT_NEEDS_APPROVAL`)
  > :moneybag: RNW-84907 | Ms. Simran D gave Vi***n Jo***i a discount: paid INR 7,600 vs list INR 9,500. Above 10% teacher limit. Reply APPROVE / REJECT. SLA 4h.

## RNW-84908
- **WhatsApp -> Teacher** (`DUPLICATE_FORM`)
  > Hi Acharya Nancy S, we got Si***a Ma***a's renewal form twice (browser refresh). We kept one and closed the duplicate - all good.
- **WhatsApp -> Parent** (`AUTO_APPROVED`)
  > Hi Ro***n Ma***a, Si***a Ma***a's renewal for Little Yogi Gita US Track is confirmed! Classes continue in LY-US-Batch-G on Sat,Sun at 09:30. First class of the new term: 2026-11-07. See you there! - Team Bambinos

## RNW-84909
- **Slack -> Ops (Finance)** (`PARTIAL_PAYMENT`)
  > :warning: RNW-84909 | Ad***t Ku***i paid installment 1 (INR 5,250) of INR 10,500. Teacher form says INR 10,500. Decide: approve under installment policy or hold. SLA 12h.
- **WhatsApp -> Parent** (`PARTIAL_PAYMENT`)
  > Hi Sn***a Ku***i, thank you! We've received INR 5,250 (installment 1) for Ad***t Ku***i's renewal. The second installment link will be shared before it's due. - Team Bambinos

## RNW-84910
- **WhatsApp -> Teacher** (`ORPHANED_INVOICE`)
  > Hi Coach Arvind K, good news - My***a Re***y's renewal payment (INR 11,000) came in on 2026-11-03 11:20:45. We've auto-renewed them in the same batch. You don't need to fill the renewal form. If the parent wants a different slot, just reply here.
- **WhatsApp -> Parent** (`AUTO_APPROVED`)
  > Hi Vi***m Re***y, My***a Re***y's renewal for Unbox Chess Level 1 is confirmed! Classes continue in CM-G2-Batch-I on Wed,Fri at 17:00. First class of the new term: 2026-11-06. See you there! - Team Bambinos

## RNW-84911
- **WhatsApp -> Parent** (`PAYMENT_FAILED`)
  > Hi An***i Gu***a, we tried to confirm Is***n Gu***a's renewal for Young Communicators Level 1 but the payment of INR 12,000 did not go through (bank status: failed, no money was deducted on our side). Please retry here: https://bambinos.live/invoice/BMB-INV-2026-84911. Is***n Gu***a's current classes continue meanwhile. - Team Bambinos
- **WhatsApp -> Teacher** (`PAYMENT_FAILED`)
  > Hi Ms. Simran D, renewal form 3311 for Is***n Gu***a cannot be approved: the gateway shows invoice 84911 as FAILED. A UPI 'processing' screenshot is not proof of payment. We've sent the parent a retry link - no action needed from you.

## RNW-84912
- **Slack -> Ops Scheduler** (`BATCH_CHANGE_NO_MATCH`)
  > :calendar: RNW-84912 | Ta***a Me***n (Little Yogi Gita Level 1) paid & wants Sat,Sun 11:00:00. No existing batch matches. Options: open a new batch / offer nearest slot. Student stays in current batch until moved - no class gap. SLA 24h.
- **WhatsApp -> Parent** (`BATCH_CHANGE_NO_MATCH`)
  > Hi De***k Me***n, thanks for renewing Ta***a Me***n! We're finding a Sat,Sun 11:00:00 slot as requested. Until then Ta***a Me***n continues in the current batch so no class is missed. We'll confirm the new timing within 24 hours. - Team Bambinos

## RNW-84913
- **Slack -> Ops Agent** (`NAME_ENCODING_ANOMALY`)
  > :abc: RNW-84913 | Parent name on invoice 84913 contains non-Latin look-alike letters. Normalise in CRM to avoid search/match misses.
- **WhatsApp -> Teacher** (`INVOICE_REF_AUTOCORRECTED`)
  > Hi Ms. Mary M, small fix: form 3313 had invoice 84931; the correct one is 84913. We've corrected it and renewed De***a Me***a. Nothing else needed.
- **WhatsApp -> Parent** (`AUTO_APPROVED`)
  > Hi Ar***n Ме***a, De***a Me***a's renewal for Unbox Science Level 1 is confirmed! Classes continue in SC-G4-Batch-K on Tue,Thu at 18:00. First class of the new term: 2026-11-05. See you there! - Team Bambinos
```

### outputs/metrics.json

| Field | Value |
| --- | --- |
| Bytes | 1158 |
| Score | 0 |
| Why | context |
| Status | Full content |


```json
{
  "as_of": "2026-11-04 09:00",
  "renewal_invoices": 13,
  "paid_or_partial": 12,
  "already_scheduled": 1,
  "auto_approved_now": 8,
  "exceptions_open": 4,
  "paid_not_scheduled": 11,
  "paid_not_scheduled_gt_12h": 11,
  "revenue_paid_not_scheduled_inr": 126850.0,
  "orphaned_invoice_rate_pct": 16.7,
  "teacher_forms_pending_ops": 8,
  "duplicate_form_rate_pct": 8.3,
  "form_data_error_rate_pct": 25.0,
  "median_payment_to_schedule_hours": 1.7,
  "oldest_unscheduled_paid_hours": 66.7,
  "straight_through_rate_pct": 66.7,
  "exceptions_by_owner": {
    "Ops (Finance)": 1,
    "Ops Lead": 1,
    "Ops Scheduler": 1,
    "Parent": 1
  },
  "reason_code_counts": {
    "ORPHANED_INVOICE": 2,
    "STUCK_AT_ALLOCATION": 1,
    "PAYER_CONTACT_MISMATCH": 1,
    "FALSE_BATCH_FULL": 1,
    "DISCOUNT_NEEDS_APPROVAL": 1,
    "DUPLICATE_FORM": 1,
    "PARTIAL_PAYMENT": 1,
    "TEACHER_AMOUNT_MISMATCH": 1,
    "PAYMENT_FAILED": 1,
    "BATCH_CHANGE_NO_MATCH": 1,
    "NAME_ENCODING_ANOMALY": 1,
    "INVOICE_REF_AUTOCORRECTED": 1
  },
  "manual_minutes_saved_this_run": 160,
  "manual_minutes_per_renewal_today": 20
}
```

### prompts/exception_triage_rules.md

| Field | Value |
| --- | --- |
| Bytes | 2590 |
| Score | 0 |
| Why | context |
| Status | Full content |


```markdown
# Exception Triage Rules (human-readable spec of `src/rules.py`)

Source of truth = payment gateway (`invoices`). Teacher form = optional metadata.
LLM never decides; it only words messages.

| Reason code | Severity | Owner | SLA | Trigger | Auto action |
|---|---|---|---|---|---|
| PAYMENT_FAILED | Blocking | Parent | 24h | `payment_status = Failed` (even if teacher attached a screenshot) | Resend pay link; teacher told no action |
| PARTIAL_PAYMENT | Blocking | Ops Finance | 12h | `Partially_Paid` / installment | Finance decides installment policy |
| DISCOUNT_NEEDS_APPROVAL | Blocking | Ops Lead | 4h | discount > 10% of list price | 1-click approve on Slack |
| FEE_MISMATCH | Blocking | Ops Finance | 12h | net != standard fee and no discount | Verify pricing |
| IDENTITY_MISMATCH | Blocking | Ops Agent | 4h | invoice user/class/educator != roster | Manual check |
| INVOICE_NOT_FOUND | Blocking | Teacher | 12h | form invoice can't be resolved even by fuzzy match | Ask teacher for link |
| BATCH_CHANGE_NO_MATCH | Blocking | Ops Scheduler | 24h | parent wants new slot, no batch of that class matches | Keep in old batch (no gap), offer options |
| BATCH_CHANGE_TARGET_FULL | Blocking | Ops Scheduler | 24h | target batch at capacity | Offer alternatives |
| BATCH_ID_MISMATCH | Blocking | Teacher | 12h | form batch != roster batch, no change requested | Confirm with teacher |
| STUDENT_NOT_ACTIVE | Blocking | Ops Agent | 12h | student not in active roster | Manual check |
| ORPHANED_INVOICE | Advisory | Teacher | — | paid, no teacher form | **Fast-track same batch**; teacher informed |
| PAYER_CONTACT_MISMATCH | Advisory | Ops Agent | 24h | payer phone/email != registered, IDs match | Approve; parent asked to confirm 2nd number |
| INVOICE_REF_AUTOCORRECTED | Advisory | Teacher | — | form invoice wrong, unique match on student+user+class+amount | Correct & approve |
| TEACHER_AMOUNT_MISMATCH | Advisory | Teacher | — | form amount != gateway amount | Gateway amount wins |
| DUPLICATE_FORM | Advisory | Teacher | — | same student+invoice+amount submitted twice | Keep earliest, close rest |
| FALSE_BATCH_FULL | Advisory | Ops Scheduler | 4h | booking failed "batch full" but student already holds a seat | Re-allocate; fix capacity rule |
| STUCK_AT_ALLOCATION | Advisory | Ops Scheduler | 4h | same-batch booking waiting for manual allocation | Auto-allocate |
| NAME_ENCODING_ANOMALY | Advisory | Ops Agent | 48h | Cyrillic/Greek look-alike letters in names | Normalise CRM record |

Decision = `AUTO_APPROVE` if no blocking code, else `EXCEPTION`.
```

### prompts/message_drafter.md

| Field | Value |
| --- | --- |
| Bytes | 1108 |
| Score | 0 |
| Why | context |
| Status | Full content |


```markdown
# Prompt: Follow-up Message Drafter (Gemini, optional layer)

You are the communications assistant for Bambinos.live Operations.
You receive a DRAFT message produced by a deterministic rule engine and a RECIPIENT
(Parent, Teacher, Ops Agent, Ops Lead, Ops Scheduler, Ops (Finance)).

Rewrite the draft so it reads naturally for that recipient:
- Parent (WhatsApp): warm, reassuring, max 60 words, no internal jargon (no "reason code", "batch_id", "form").
  Always say what happens to the child's classes next. Never blame the teacher.
- Teacher (WhatsApp): respectful, short, say clearly whether any action is needed. Max 50 words.
- Ops roles (Slack): one line, starts with the case ID, states the decision needed and the SLA.

HARD RULES (outputs violating these are discarded by code and the template is sent instead):
1. Keep every number exactly as written (amounts, IDs, dates, times, invoice numbers, links).
2. Do not add facts, promises, discounts or dates that are not in the draft.
3. Do not approve, reject or change any decision. You only change wording.
4. Output only the final message text.
```

### outputs/1b_class_schedule_bookings_to_insert.csv

| Field | Value |
| --- | --- |
| Bytes | 18883 |
| Score | -1 |
| Why | context |
| Status | Truncated (budget limit) |


```csv
// … lines 1–29
id,bookingrequest_id,invoice_id,classschedule_id,classbatch_id,class_id,user_id,student_id,educator_id,session_no,class_date,start_time,end_time,booking_type,is_cancelled,attended_class
,5502,84902,,9202,205,41022,68102,1108,1,2026-11-09,18:00:00,18:50:00,Regular_Renewal,No,No
,5502,84902,,9202,205,41022,68102,1108,2,2026-11-11,18:00:00,18:50:00,Regular_Renewal,No,No
,5502,84902,,9202,205,41022,68102,1108,3,2026-11-16,18:00:00,18:50:00,Regular_Renewal,No,No
,5502,84902,,9202,205,41022,68102,1108,4,2026-11-18,18:00:00,18:50:00,Regular_Renewal,No,No
,5502,84902,,9202,205,41022,68102,1108,5,2026-11-23,18:00:00,18:50:00,Regular_Renewal,No,No
,5502,84902,,9202,205,41022,68102,1108,6,2026-11-25,18:00:00,18:50:00,Regular_Renewal,No,No
,5502,84902,,9202,205,41022,68102,1108,7,2026-11-30,18:00:00,18:50:00,Regular_Renewal,No,No
,5502,84902,,9202,205,41022,68102,1108,8,2026-12-02,18:00:00,18:50:00,Regular_Renewal,No,No
,5502,84902,,9202,205,41022,68102,1108,9,2026-12-07,18:00:00,18:50:00,Regular_Renewal,No,No
,5502,84902,,9202,205,41022,68102,1108,10,2026-12-09,18:00:00,18:50:00,Regular_Renewal,No,No
,5502,84902,,9202,205,41022,68102,1108,11,2026-12-14,18:00:00,18:50:00,Regular_Renewal,No,No
,5502,84902,,9202,205,41022,68102,1108,12,2026-12-16,18:00:00,18:50:00,Regular_Renewal,No,No
,5502,84902,,9202,205,41022,68102,1108,13,2026-12-21,18:00:00,18:50:00,Regular_Renewal,No,No
,5502,84902,,9202,205,41022,68102,1108,14,2026-12-23,18:00:00,18:50:00,Regular_Renewal,No,No
,5502,84902,,9202,205,41022,68102,1108,15,2026-12-28,18:00:00,18:50:00,Regular_Renewal,No,No
,5502,84902,,9202,205,41022,68102,1108,16,2026-12-30,18:00:00,18:50:00,Regular_Renewal,No,No
,5502,84902,,9202,205,41022,68102,1108,17,2027-01-04,18:00:00,18:50:00,Regular_Renewal,No,No
,5502,84902,,9202,205,41022,68102,1108,18,2027-01-06,18:00:00,18:50:00,Regular_Renewal,No,No
,5502,84902,,9202,205,41022,68102,1108,19,2027-01-11,18:00:00,18:50:00,Regular_Renewal,No,No
,5502,84902,,9202,205,41022,68102,1108,20,2027-01-13,18:00:00,18:50:00,Regular_Renewal,No,No
,5502,84902,,9202,205,41022,68102,1108,21,2027-01-18,18:00:00,18:50:00,Regular_Renewal,No,No
,5502,84902,,9202,205,41022,68102,1108,22,2027-01-20,18:00:00,18:50:00,Regular_Renewal,No,No
,5502,84902,,9202,205,41022,68102,1108,23,2027-01-25,18:00:00,18:50:00,Regular_Renewal,No,No
,5502,84902,,9202,205,41022,68102,1108,24,2027-01-27,18:00:00,18:50:00,Regular_Renewal,No,No
,NEW-84903,84903,,9203,301,41023,68103,1115,1,2026-11-06,16:30:00,17:20:00,Regular_Renewal,No,No
,NEW-84903,84903,,9203,301,41023,68103,1115,2,2026-11-11,16:30:00,17:20:00,Regular_Renewal,No,No
,NEW-84903,84903,,9203,301,41023,68103,1115,3,2026-11-13,16:30:00,17:20:00,Regular_Renewal,No,No
,NEW-84903,84903,,9203,301,41023,68103,1115,4,2026-11-18,16:30:00,17:20:00,Regular_Renewal,No,No
// … lines 33–61
,NEW-84903,84903,,9203,301,41023,68103,1115,8,2026-12-02,16:30:00,17:20:00,Regular_Renewal,No,No
,NEW-84903,84903,,9203,301,41023,68103,1115,9,2026-12-04,16:30:00,17:20:00,Regular_Renewal,No,No
,NEW-84903,84903,,9203,301,41023,68103,1115,10,2026-12-09,16:30:00,17:20:00,Regular_Renewal,No,No
,NEW-84903,84903,,9203,301,41023,68103,1115,11,2026-12-11,16:30:00,17:20:00,Regular_Renewal,No,No
,NEW-84903,84903,,9203,301,41023,68103,1115,12,2026-12-16,16:30:00,17:20:00,Regular_Renewal,No,No
,NEW-84903,84903,,9203,301,41023,68103,1115,13,2026-12-18,16:30:00,17:20:00,Regular_Renewal,No,No
,NEW-84903,84903,,9203,301,41023,68103,1115,14,2026-12-23,16:30:00,17:20:00,Regular_Renewal,No,No
,NEW-84903,84903,,9203,301,41023,68103,1115,15,2026-12-25,16:30:00,17:20:00,Regular_Renewal,No,No
,NEW-84903,84903,,9203,301,41023,68103,1115,16,2026-12-30,16:30:00,17:20:00,Regular_Renewal,No,No
,NEW-84903,84903,,9203,301,41023,68103,1115,17,2027-01-01,16:30:00,17:20:00,Regular_Renewal,No,No
,NEW-84903,84903,,9203,301,41023,68103,1115,18,2027-01-06,16:30:00,17:20:00,Regular_Renewal,No,No
,NEW-84903,84903,,9203,301,41023,68103,1115,19,2027-01-08,16:30:00,17:20:00,Regular_Renewal,No,No
,NEW-84903,84903,,9203,301,41023,68103,1115,20,2027-01-13,16:30:00,17:20:00,Regular_Renewal,No,No
,NEW-84903,84903,,9203,301,41023,68103,1115,21,2027-01-15,16:30:00,17:20:00,Regular_Renewal,No,No
,NEW-84903,84903,,9203,301,41023,68103,1115,22,2027-01-20,16:30:00,17:20:00,Regular_Renewal,No,No
,NEW-84903,84903,,9203,301,41023,68103,1115,23,2027-01-22,16:30:00,17:20:00,Regular_Renewal,No,No
,NEW-84903,84903,,9203,301,41023,68103,1115,24,2027-01-27,16:30:00,17:20:00,Regular_Renewal,No,No
,NEW-84904,84904,,9201,104,41024,68104,1102,1,2026-11-05,17:00:00,17:50:00,Regular_Renewal,No,No
,NEW-84904,84904,,9201,104,41024,68104,1102,2,2026-11-10,17:00:00,17:50:00,Regular_Renewal,No,No
,NEW-84904,84904,,9201,104,41024,68104,1102,3,2026-11-12,17:00:00,17:50:00,Regular_Renewal,No,No
,NEW-84904,84904,,9201,104,41024,68104,1102,4,2026-11-17,17:00:00,17:50:00,Regular_Renewal,No,No
,NEW-84904,84904,,9201,104,41024,68104,1102,5,2026-11-19,17:00:00,17:50:00,Regular_Renewal,No,No
,NEW-84904,84904,,9201,104,41024,68104,1102,6,2026-11-24,17:00:00,17:50:00,Regular_Renewal,No,No
,NEW-84904,84904,,9201,104,41024,68104,1102,7,2026-11-26,17:00:00,17:50:00,Regular_Renewal,No,No
,NEW-84904,84904,,9201,104,41024,68104,1102,8,2026-12-01,17:00:00,17:50:00,Regular_Renewal,No,No
,NEW-84904,84904,,9201,104,41024,68104,1102,9,2026-12-03,17:00:00,17:50:00,Regular_Renewal,No,No
,NEW-84904,84904,,9201,104,41024,68104,1102,10,2026-12-08,17:00:00,17:50:00,Regular_Renewal,No,No
,NEW-84904,84904,,9201,104,41024,68104,1102,11,2026-12-10,17:00:00,17:50:00,Regular_Renewal,No,No
,NEW-84904,84904,,9201,104,41024,68104,1102,12,2026-12-15,17:00:00,17:50:00,Regular_Renewal,No,No
// … lines 65–93
,NEW-84904,84904,,9201,104,41024,68104,1102,16,2026-12-29,17:00:00,17:50:00,Regular_Renewal,No,No
,NEW-84904,84904,,9201,104,41024,68104,1102,17,2026-12-31,17:00:00,17:50:00,Regular_Renewal,No,No
,NEW-84904,84904,,9201,104,41024,68104,1102,18,2027-01-05,17:00:00,17:50:00,Regular_Renewal,No,No
,NEW-84904,84904,,9201,104,41024,68104,1102,19,2027-01-07,17:00:00,17:50:00,Regular_Renewal,No,No
,NEW-84904,84904,,9201,104,41024,68104,1102,20,2027-01-12,17:00:00,17:50:00,Regular_Renewal,No,No
,NEW-84904,84904,,9201,104,41024,68104,1102,21,2027-01-14,17:00:00,17:50:00,Regular_Renewal,No,No
,NEW-84904,84904,,9201,104,41024,68104,1102,22,2027-01-19,17:00:00,17:50:00,Regular_Renewal,No,No
,NEW-84904,84904,,9201,104,41024,68104,1102,23,2027-01-21,17:00:00,17:50:00,Regular_Renewal,No,No
,NEW-84904,84904,,9201,104,41024,68104,1102,24,2027-01-26,17:00:00,17:50:00,Regular_Renewal,No,No
,5505,84905,,9205,402,41025,68105,1122,1,2026-11-07,11:00:00,11:50:00,Regular_Renewal,No,No
,5505,84905,,9205,402,41025,68105,1122,2,2026-11-08,11:00:00,11:50:00,Regular_Renewal,No,No
,5505,84905,,9205,402,41025,68105,1122,3,2026-11-14,11:00:00,11:50:00,Regular_Renewal,No,No
,5505,84905,,9205,402,41025,68105,1122,4,2026-11-15,11:00:00,11:50:00,Regular_Renewal,No,No
,5505,84905,,9205,402,41025,68105,1122,5,2026-11-21,11:00:00,11:50:00,Regular_Renewal,No,No
,5505,84905,,9205,402,41025,68105,1122,6,2026-11-22,11:00:00,11:50:00,Regular_Renewal,No,No
,5505,84905,,9205,402,41025,68105,1122,7,2026-11-28,11:00:00,11:50:00,Regular_Renewal,No,No
,5505,84905,,9205,402,41025,68105,1122,8,2026-11-29,11:00:00,11:50:00,Regular_Renewal,No,No
,5505,84905,,9205,402,41025,68105,1122,9,2026-12-05,11:00:00,11:50:00,Regular_Renewal,No,No
,5505,84905,,9205,402,41025,68105,1122,10,2026-12-06,11:00:00,11:50:00,Regular_Renewal,No,No
,5505,84905,,9205,402,41025,68105,1122,11,2026-12-12,11:00:00,11:50:00,Regular_Renewal,No,No
,5505,84905,,9205,402,41025,68105,1122,12,2026-12-13,11:00:00,11:50:00,Regular_Renewal,No,No
,5505,84905,,9205,402,41025,68105,1122,13,2026-12-19,11:00:00,11:50:00,Regular_Renewal,No,No
,5505,84905,,9205,402,41025,68105,1122,14,2026-12-20,11:00:00,11:50:00,Regular_Renewal,No,No
,5505,84905,,9205,402,41025,68105,1122,15,2026-12-26,11:00:00,11:50:00,Regular_Renewal,No,No
,5505,84905,,9205,402,41025,68105,1122,16,2026-12-27,11:00:00,11:50:00,Regular_Renewal,No,No
,5505,84905,,9205,402,41025,68105,1122,17,2027-01-02,11:00:00,11:50:00,Regular_Renewal,No,No
,5505,84905,,9205,402,41025,68105,1122,18,2027-01-03,11:00:00,11:50:00,Regular_Renewal,No,No
,5505,84905,,9205,402,41025,68105,1122,19,2027-01-09,11:00:00,11:50:00,Regular_Renewal,No,No
,5505,84905,,9205,402,41025,68105,1122,20,2027-01-10,11:00:00,11:50:00,Regular_Renewal,No,No
// … lines 97–125
,5505,84905,,9205,402,41025,68105,1122,24,2027-01-24,11:00:00,11:50:00,Regular_Renewal,No,No
,NEW-84906,84906,,9206,108,41026,68106,1102,1,2026-11-08,19:00:00,19:50:00,Regular_Renewal,No,No
,NEW-84906,84906,,9206,108,41026,68106,1102,2,2026-11-10,19:00:00,19:50:00,Regular_Renewal,No,No
,NEW-84906,84906,,9206,108,41026,68106,1102,3,2026-11-15,19:00:00,19:50:00,Regular_Renewal,No,No
,NEW-84906,84906,,9206,108,41026,68106,1102,4,2026-11-17,19:00:00,19:50:00,Regular_Renewal,No,No
,NEW-84906,84906,,9206,108,41026,68106,1102,5,2026-11-22,19:00:00,19:50:00,Regular_Renewal,No,No
,NEW-84906,84906,,9206,108,41026,68106,1102,6,2026-11-24,19:00:00,19:50:00,Regular_Renewal,No,No
,NEW-84906,84906,,9206,108,41026,68106,1102,7,2026-11-29,19:00:00,19:50:00,Regular_Renewal,No,No
,NEW-84906,84906,,9206,108,41026,68106,1102,8,2026-12-01,19:00:00,19:50:00,Regular_Renewal,No,No
,NEW-84906,84906,,9206,108,41026,68106,1102,9,2026-12-06,19:00:00,19:50:00,Regular_Renewal,No,No
,NEW-84906,84906,,9206,108,41026,68106,1102,10,2026-12-08,19:00:00,19:50:00,Regular_Renewal,No,No
,NEW-84906,84906,,9206,108,41026,68106,1102,11,2026-12-13,19:00:00,19:50:00,Regular_Renewal,No,No
,NEW-84906,84906,,9206,108,41026,68106,1102,12,2026-12-15,19:00:00,19:50:00,Regular_Renewal,No,No
,NEW-84906,84906,,9206,108,41026,68106,1102,13,2026-12-20,19:00:00,19:50:00,Regular_Renewal,No,No
,NEW-84906,84906,,9206,108,41026,68106,1102,14,2026-12-22,19:00:00,19:50:00,Regular_Renewal,No,No
,NEW-84906,84906,,9206,108,41026,68106,1102,15,2026-12-27,19:00:00,19:50:00,Regular_Renewal,No,No
,NEW-84906,84906,,9206,108,41026,68106,1102,16,2026-12-29,19:00:00,19:50:00,Regular_Renewal,No,No
,NEW-84906,84906,,9206,108,41026,68106,1102,17,2027-01-03,19:00:00,19:50:00,Regular_Renewal,No,No
,NEW-84906,84906,,9206,108,41026,68106,1102,18,2027-01-05,19:00:00,19:50:00,Regular_Renewal,No,No
,NEW-84906,84906,,9206,108,41026,68106,1102,19,2027-01-10,19:00:00,19:50:00,Regular_Renewal,No,No
,NEW-84906,84906,,9206,108,41026,68106,1102,20,2027-01-12,19:00:00,19:50:00,Regular_Renewal,No,No
,NEW-84906,84906,,9206,108,41026,68106,1102,21,2027-01-17,19:00:00,19:50:00,Regular_Renewal,No,No
,NEW-84906,84906,,9206,108,41026,68106,1102,22,2027-01-19,19:00:00,19:50:00,Regular_Renewal,No,No
,NEW-84906,84906,,9206,108,41026,68106,1102,23,2027-01-24,19:00:00,19:50:00,Regular_Renewal,No,No
,NEW-84906,84906,,9206,108,41026,68106,1102,24,2027-01-26,19:00:00,19:50:00,Regular_Renewal,No,No
,NEW-84908,84908,,9208,302,41028,68108,1115,1,2026-11-07,09:30:00,10:20:00,Regular_Renewal,No,No
,NEW-84908,84908,,9208,302,41028,68108,1115,2,2026-11-08,09:30:00,10:20:00,Regular_Renewal,No,No
,NEW-84908,84908,,9208,302,41028,68108,1115,3,2026-11-14,09:30:00,10:20:00,Regular_Renewal,No,No
,NEW-84908,84908,,9208,302,41028,68108,1115,4,2026-11-15,09:30:00,10:20:00,Regular_Renewal,No,No

/* …78 lines not shown — file has no detected definitions; ask for full content if needed. */
```

### report/report.html

| Field | Value |
| --- | --- |
| Bytes | 21861 |
| Score | -1 |
| Why | context |
| Status | Truncated (budget limit) |

**Structural Outline:**
  - `class and` (line 28)
  - `class 301` (line 53)
  - `class because` (line 80)
  - `class gap` (line 110)
  - `class 301` (line 125)
  - `class gaps` (line 167)


```html
// … lines 1–57
<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>Bambinos Renewal Pipeline — Case Report</title>
<style>
  @page { size: A4; margin: 14mm 13mm; }
  :root { --ink:#1b2430; --mute:#5b6675; --line:#d9dee5; --acc:#0f7a6c; --bad:#b4362f; --warn:#a86b00; --bg2:#f4f7f8; }
  body { font: 10.2pt/1.45 "Segoe UI", Arial, sans-serif; color: var(--ink); background:#fff; margin:0; }
  h1 { font-size: 21pt; margin: 0 0 2px; } h2 { font-size: 14pt; color: var(--acc); border-bottom: 2px solid var(--acc); padding-bottom: 3px; margin: 20px 0 8px; page-break-after: avoid; }
  h3 { font-size: 11pt; margin: 14px 0 5px; page-break-after: avoid; }
  .sub { color: var(--mute); margin-bottom: 10px; } p { margin: 5px 0; } ul { margin: 4px 0 4px 18px; padding: 0; } li { margin: 2px 0; }
  table { border-collapse: collapse; width: 100%; margin: 6px 0 10px; font-size: 8.8pt; page-break-inside: auto; }
  tr { page-break-inside: avoid; } th { background: #1f2a37; color: #fff; text-align: left; padding: 4px 6px; font-weight: 600; }
  td { border-bottom: 1px solid var(--line); padding: 4px 6px; vertical-align: top; }
  .box { background: var(--bg2); border-left: 4px solid var(--acc); padding: 8px 12px; margin: 8px 0; }
  .kpis { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin: 8px 0; }
  .kpi { border: 1px solid var(--line); border-radius: 6px; padding: 7px 9px; } .kpi b { display: block; font-size: 15pt; } .kpi span { color: var(--mute); font-size: 8.5pt; }
  .b { color: var(--bad); font-weight: 600; } .w { color: var(--warn); font-weight: 600; } .g { color: var(--acc); font-weight: 600; }
  code { font: 8.6pt Consolas, monospace; background: #eef1f4; padding: 0 3px; border-radius: 3px; }
  pre { font: 8.4pt/1.35 Consolas, monospace; background: var(--bg2); padding: 8px 10px; border-radius: 6px; white-space: pre; margin: 6px 0; }
  .pb { page-break-before: always; } .two { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
  .small { font-size: 8.6pt; color: var(--mute); }
</style></head><body>

<h1>Paid Is Not Scheduled</h1>
<div class="sub">Re-engineering the Bambinos.live Student Renewal → Class Scheduling pipeline · AI Program Manager (Operations) take-home · Nov 2026<br>
Prototype + data + outputs: see GitHub repo (README). Analysis run on the provided 5-table dataset, snapshot <b>as of 2026-11-04 09:00</b>.</div>

<div class="box"><b>One-line thesis.</b> The pipeline treats the <i>teacher's form</i> as the trigger and the <i>payment</i> as something to verify. It should be the other way round. The gateway already knows who paid, how much, for which student, class and teacher. For a same-batch renewal (the majority) Steps 2 and 3 add no information, only delay and typos. Remove them, let the ledger drive scheduling, and send humans only the cases that genuinely need judgement.</div>

<div class="kpis">
  <div class="kpi"><b class="b">11 / 12</b><span>paid renewals NOT scheduled (all &gt;12h)</span></div>
  <div class="kpi"><b class="b">₹1.27 L</b><span>collected revenue with no classes booked</span></div>
  <div class="kpi"><b class="b">66.7 h</b><span>oldest paid-but-unscheduled (a clean same-batch case)</span></div>
  <div class="kpi"><b class="g">8 of 12</b><span>clear automatically with the new rules (67% straight-through)</span></div>
</div>

<h2>A. Root-Cause Problem Definition &amp; Leakage Audit</h2>

<h3>A1. What the data actually shows (every invoice traced through all 4 tables)</h3>
<table>
<tr><th>Invoice</th><th>Where it is stuck</th><th>Hidden failure mode</th><th>Root cause</th></tr>
<tr><td>84901</td><td class="g">Scheduled in 1.7h</td><td>The only one that worked: Sunday payment, teacher fast, Ops fast.</td><td>Depends on 3 people being online at the same time.</td></tr>
<tr><td>84902</td><td>booking = Pending_Batch_Allocation, <b>66.7h</b></td><td>Approved same-batch renewal still waiting for someone to "choose" the batch the child is already in.</td><td>Step 4 is manual even when there is nothing to choose.</td></tr>
<tr><td>84903</td><td>form Pending, <b>47.9h</b></td><td>Perfectly clean case: amount, IDs, batch all match. Sitting in the Ops queue for 2 days.</td><td>Ops verifies 100% of rows by hand, so clean ones queue behind messy ones.</td></tr>
<tr><td>84904</td><td>form Pending</td><td>Mother paid from her own phone/email (<code>…XXXX77</code>, outlook vs gmail). A phone-based match fails.</td><td>Matching on contact details, not system IDs (the invoice carries student_id/user_id).</td></tr>
<tr><td>84905</td><td>booking = <b>Failed_Batch_Full</b></td><td>Batch 9205 is 6/6, but one of those 6 <i>is this child</i>. A renewing student is refused their own seat.</td><td>Capacity check doesn't exclude the renewing student.</td></tr>
<tr><td>84906</td><td>No form, 41h</td><td><b>Orphaned invoice</b> (GCC parent, ₹18,000). Nobody knows this child paid.</td><td>Pipeline only starts when the teacher remembers to fill a form.</td></tr>
<tr><td>84907</td><td>form Pending</td><td>Teacher gave a 20% "retention scholarship" (₹1,900). No approval trail.</td><td>No discount policy enforced at the payment-link stage.</td></tr>
<tr><td>84908</td><td>2 forms Pending</td><td>Same renewal submitted twice ("browser froze"). Risk of double booking.</td><td>No idempotency key on the form.</td></tr>
<tr><td>84909</td><td>form Pending</td><td>Installment 1 of 2: ₹5,250 captured, but the teacher typed ₹10,500.</td><td>Teacher re-types financial data the gateway already has.</td></tr>
<tr><td>84910</td><td>No form, 21.7h</td><td>Second orphaned invoice (Coach Arvind).</td><td>Same as 84906.</td></tr>
<tr><td>84911</td><td>form Pending</td><td>Payment <b>Failed</b>, but the teacher submitted a form with a "UPI processing" screenshot. A tired Ops agent could approve it.</td><td>The form allows a screenshot to stand in for gateway proof.</td></tr>
<tr><td>84912</td><td>Awaiting_Parent_Batch_Selection</td><td>Ops <i>approved</i> a batch change to Sat-Sun 11:00, but class 301 has no weekend batch. The parent is asked to pick from options that don't exist.</td><td>Approval happens before a feasibility check.</td></tr>
<tr><td>84913</td><td>form Pending</td><td>Teacher typed invoice <b>84931</b> (digits swapped, real one is 84913). Parent name also contains a <b>Cyrillic "Ме"</b> that looks like Latin "Me". Exact-text matching fails silently.</td><td>Free-text keys and no input validation.</td></tr>
</table>

<h3>A2. Failure-mode taxonomy (beyond this sample)</h3>
// … lines 79–84
<tr><td><b>Exception Ageing by Owner</b></td><td>Open blocking exceptions × hours × owner</td><td>Invisible</td><td>Owner-specific SLA (4h / 12h / 24h)</td></tr>
<tr><td><b>Class-Gap Incidents</b></td><td>Paid students who missed a class because the new term wasn't booked</td><td>Invisible</td><td>0</td></tr>
<tr><td><b>False Rejection Rate</b></td><td>Bookings failed for a reason that wasn't true (e.g. false "batch full")</td><td>1 of 4 booking requests</td><td>0</td></tr>
</table>

<h2 class="pb">B. Re-Engineered Workflow — "Zero-Touch" for the Happy Path</h2>
// … lines 109–114
  → WhatsApp confirmation to parent               │       → WhatsApp to parent / teacher when they must act
  → FYI to teacher (no form needed)               │       → student KEPT in current batch, so no class gap
                                                  ▼
                              Ops Morning Board (Streamlit / Metabase)
</pre>
<p><b>Guardrail:</b> every approve/reject decision is a deterministic rule (<code>src/rules.py</code>), so it is auditable and testable. The LLM (Gemini) only rewrites message tone. Code checks that every number survives the rewrite, otherwise the template is sent.</p>
// … lines 124–129
<tr><td>Discount &gt;10% (84907)</td><td>Policy limit</td><td>Ops Lead (Slack APPROVE/REJECT, 4h)</td><td class="w">Exception</td></tr>
<tr><td>Batch change to a slot that doesn't exist (84912)</td><td>No batch of class 301 on Sat-Sun 11:00</td><td>Ops Scheduler (24h) + parent reassurance</td><td class="w">Exception, child stays in current batch</td></tr>
<tr><td>False "batch full" (84905)</td><td>Renewing student already holds a seat</td><td>Ops Scheduler FYI + bug ticket</td><td class="g">Auto-approved</td></tr>
<tr><td>Duplicate form (84908)</td><td>Same student+invoice+amount</td><td>Teacher FYI</td><td class="g">Earliest kept, duplicate closed</td></tr>
<tr><td>No teacher form (84906, 84910)</td><td>Paid + IDs match roster</td><td>Teacher FYI</td><td class="g">Fast-tracked into the same batch</td></tr>
</table>
// … lines 166–171
<li><b>Shadow mode first.</b> The engine runs alongside the manual process and writes to a <i>shadow</i> table. Ops keeps working as today. Every day we compare engine decisions with human decisions and target ≥98% agreement before switching on.</li>
<li><b>Never delete a seat.</b> In every mode, an existing student is never removed from the current batch until the new bookings are written. That rules out class gaps by design.</li>
<li><b>Kill switch and rollback.</b> A single config flag sends everything back to the manual queue. Auto-approvals are reversible for 24h.</li>
<li><b>Teachers:</b> the message is "you no longer need to fill a form", which removes work, so adoption is easy. Pilot with 20 high-renewal teachers, then onboard in waves through 10-minute WhatsApp voice notes and a pinned FAQ. The Teacher League rewards teachers, it doesn't name and shame them.</li>
<li><b>Ops team:</b> roles move from "verifier" to "exception specialist". Two Ops champions co-own the rule book, and nobody is made redundant in the first 90 days.</li>
</ul>
```