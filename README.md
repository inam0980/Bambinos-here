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

Optional: copy `.env.example` to `.env` and add `GROQ_API_KEY` (or `GEMINI_API_KEY`). The LLM then polishes the message tone. Fallback chain: Groq → Gemini → template. If a provider errors (bad key, quota, model removed), it is skipped for the rest of the run and the next one is used. Without a key, the deterministic templates are used and everything still works.
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
