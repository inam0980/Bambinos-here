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
