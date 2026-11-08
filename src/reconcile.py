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
    dups = forms[dup_mask].copy()
    dups["duplicate_of"] = [forms[key == k].iloc[0]["id"] for k in key[dup_mask]]
    return forms[~dup_mask].reset_index(drop=True), dups.reset_index(drop=True)


def resolve_form_invoice(form, invoices):
    """Return (invoice_row | None, autocorrected: bool)."""
    exact = invoices[(invoices["id"] == form["invoice_id"]) & (invoices["student_id"] == form["student_id"])]
    if len(exact) == 1:
        return exact.iloc[0], False
    # Fallback: unique match on system IDs + amount (catches typos like 84931 vs 84913)
    cand = invoices[(invoices["student_id"] == form["student_id"]) &
                    (invoices["user_id"] == form["user_id"]) &
                    (invoices["class_id"] == form["class_id"])]
    if len(cand) > 1:
        cand = cand[cand["amount"].map(money) == money(form["amount_paid"])]
    if len(cand) == 1:
        return cand.iloc[0], True
    return None, False


def reconcile(t: dict, as_of: datetime) -> dict:
    inv, roster, bookings, sched = t["invoices"], t["roster"], t["bookings"], t["schedule"]
    inv = inv[inv["is_renewal"] == "Yes"]
    catalog = batch_catalog(roster)
    forms, dup_forms = dedupe_forms(t["forms"])

    form_by_invoice, unmatched_forms = {}, []
    for _, f in forms.iterrows():
        row, fixed = resolve_form_invoice(f, inv)
        if row is None:
            unmatched_forms.append(f)
        else:
            form_by_invoice[row["id"]] = (f, fixed)

    cases, exceptions, approved, schedule_rows = [], [], [], []

    def add_reason(case, code, detail):
        sev, owner, sla, action = REASON_CODES[code]
        case["reasons"].append(code)
        exceptions.append({
            "case_id": case["case_id"], "invoice_id": case["invoice_id"], "form_id": case["form_id"],
            "student_id": case["student_id"], "educator_id": case["educator_id"],
            "reason_code": code, "severity": sev, "owner": owner, "sla_hours": sla,
            "detail": detail, "recommended_action": action,
        })

    for _, i in inv.iterrows():
        f, fixed = form_by_invoice.get(i["id"], (None, False))
        r = roster[roster["student_id"] == i["student_id"]]
        r = r.iloc[0] if len(r) else None
        br = bookings[bookings["invoice_id"] == i["id"]]
        br = br.iloc[0] if len(br) else None
        sc = sched[sched["invoice_id"] == i["id"]]

        paid_at = ts(i["paid_at"])
        case = {
            "case_id": f"RNW-{i['id']}", "invoice_id": i["id"], "form_id": f["id"] if f is not None else None,
            "student_id": i["student_id"], "user_id": i["user_id"], "class_id": i["class_id"],
            "educator_id": i["educator_id"],
            "student_name": r["student_name_masked"] if r is not None else None,
            "parent_name": i["parent_name"], "parent_mobile": i["mobile"],
            "registered_mobile": r["registered_mobile_masked"] if r is not None else None,
            "educator_name": r["educator_name"] if r is not None else None,
            "class_name": r["class_name"] if r is not None else None,
            "payment_status": i["payment_status"], "net_amount": money(i["net_amount"]),
            "paid_at": i["paid_at"], "paid_on_weekend": bool(paid_at and paid_at.weekday() >= 5),
            "target_classbatch_id": None, "reasons": [],
        }

        # ---- current pipeline position ---------------------------------
        if len(sc):
            stage = "4_SCHEDULED"
        elif br is not None:
            stage = f"3_BOOKING_{br['request_status'].upper()}"
        elif f is not None:
            stage = f"2_FORM_{f['approval_status'].upper()}"
        elif i["payment_status"] == "Failed":
            stage = "0_PAYMENT_FAILED"
        else:
            stage = "1_PAID_NO_FORM"
        case["current_stage"] = stage
        case["hours_since_payment"] = hours_between(paid_at, as_of)
        case["form_lag_hours"] = hours_between(paid_at, ts(f["created_at"])) if f is not None else None
        case["ops_approval_lag_hours"] = (hours_between(ts(f["created_at"]), ts(f["approved_at"]))
                                          if f is not None and f["approved_at"] else None)
        first_sched = min(sc["created_at"]) if len(sc) else None
        case["payment_to_schedule_hours"] = hours_between(paid_at, ts(first_sched)) if first_sched else None

        if stage == "4_SCHEDULED":
            case["decision"] = "ALREADY_SCHEDULED"
            cases.append(case)
            continue

        # ---- 1. payment truth (gateway wins over screenshots) -----------
        if i["payment_status"] == "Failed":
            add_reason(case, "PAYMENT_FAILED",
                       f"Gateway status=Failed, no payment_id. "
                       + (f"Teacher form {f['id']} submitted anyway: '{f['remarks']}'." if f is not None else "No form."))
        elif i["payment_status"] == "Partially_Paid":
            add_reason(case, "PARTIAL_PAYMENT",
                       f"{i['payment_type']}: captured INR {money(i['net_amount']):,.0f} of INR {money(i['amount']):,.0f}.")

        # ---- 2. identity -------------------------------------------------
        if r is None:
            add_reason(case, "STUDENT_NOT_ACTIVE", f"student_id {i['student_id']} not in active roster.")
        else:
            mism = [c for c in ("user_id", "class_id", "educator_id") if i[c] != r[c]]
            if mism:
                add_reason(case, "IDENTITY_MISMATCH", f"Invoice vs roster differ on: {', '.join(mism)}.")
            phone_ok = norm_phone(i["mobile"]) == norm_phone(r["registered_mobile_masked"])
            email_ok = norm_text(i["email"]) == norm_text(r["registered_email_masked"])
            if not (phone_ok and email_ok) and not mism:
                add_reason(case, "PAYER_CONTACT_MISMATCH",
                           f"Payer {i['parent_name']} / {i['mobile']} / {i['email']} vs registered "
                           f"{r['parent_name_masked']} / {r['registered_mobile_masked']} / {r['registered_email_masked']}. "
                           "student_id + user_id match.")
            if has_homoglyph(i["parent_name"]) or has_homoglyph(r["parent_name_masked"]):
                add_reason(case, "NAME_ENCODING_ANOMALY",
                           f"'{i['parent_name']}' contains non-Latin look-alike characters (vs roster '{r['parent_name_masked']}').")

            # ---- 3. fee ----------------------------------------------------
            std = money(r["standard_fee_24_sessions_inr"])
            disc = money(i["discount_amount"])
            if i["payment_status"] == "Paid":
                if disc > 0:
                    pct = 100 * disc / money(i["amount"])
                    if pct > DISCOUNT_AUTO_LIMIT_PCT:
                        add_reason(case, "DISCOUNT_NEEDS_APPROVAL",
                                   f"{pct:.0f}% discount (INR {disc:,.0f}) on INR {money(i['amount']):,.0f}; net INR {money(i['net_amount']):,.0f}."
                                   + (f" Teacher note: '{f['remarks']}'." if f is not None else ""))
                elif money(i["net_amount"]) != std:
                    add_reason(case, "FEE_MISMATCH", f"Paid INR {money(i['net_amount']):,.0f} vs standard INR {std:,.0f}.")

        # ---- 4. teacher form quality ---------------------------------------
        if f is None and i["payment_status"] != "Failed":
            add_reason(case, "ORPHANED_INVOICE",
                       f"Paid {i['paid_at']} ({case['hours_since_payment']}h ago); teacher {i['educator_id']} has not submitted a form.")
        if f is not None:
            if fixed:
                add_reason(case, "INVOICE_REF_AUTOCORRECTED",
                           f"Form {f['id']} cites invoice {f['invoice_id']} (does not exist / wrong student); matched to {i['id']}.")
            if money(f["amount_paid"]) != money(i["net_amount"]):
                add_reason(case, "TEACHER_AMOUNT_MISMATCH",
                           f"Form says INR {money(f['amount_paid']):,.0f}; gateway captured INR {money(i['net_amount']):,.0f}.")
            dups = dup_forms[dup_forms["duplicate_of"] == f["id"]]
            for _, d in dups.iterrows():
                add_reason(case, "DUPLICATE_FORM", f"Form {d['id']} duplicates {f['id']} ('{d['remarks']}'); auto-closed.")

        # ---- 5. batch decision ---------------------------------------------
        same_batch = (f is None) or (f["continue_same_batch"] == "Yes")
        if r is not None:
            if same_batch:
                if f is not None and f["current_classbatch_id"] != r["current_classbatch_id"]:
                    add_reason(case, "BATCH_ID_MISMATCH",
                               f"Form batch {f['current_classbatch_id']} vs roster batch {r['current_classbatch_id']}.")
                case["target_classbatch_id"] = r["current_classbatch_id"]
                # Renewing student already holds a seat -> capacity check is not needed.
                if br is not None and br["request_status"] == "Failed_Batch_Full":
                    add_reason(case, "FALSE_BATCH_FULL",
                               f"Booking {br['id']} failed: batch {r['current_classbatch_id']} at "
                               f"{r['active_students_count']}/{r['max_batch_size']}, but this student is one of those {r['active_students_count']}.")
                elif br is not None and br["request_status"] == "Pending_Batch_Allocation":
                    add_reason(case, "STUCK_AT_ALLOCATION",
                               f"Booking {br['id']} pending allocation since {br['created_at']} "
                               f"({hours_between(ts(br['created_at']), as_of)}h).")
            else:
                want_days = set(x.strip() for x in f["preferred_days"].split(","))
                options = catalog[(catalog["class_id"] == i["class_id"]) &
                                  (catalog["classbatch_id"] != r["current_classbatch_id"])]
                keep = [set(x.strip() for x in d.split(",")) == want_days and t_ == f["preferred_time_slot"]
                        for d, t_ in zip(options["batch_days"], options["batch_start_time"])]
                options = options[keep]
                if options.empty:
                    add_reason(case, "BATCH_CHANGE_NO_MATCH",
                               f"Wants {f['preferred_days']} {f['preferred_time_slot']} for class {i['class_id']}; "
                               f"no such batch. Currently in {r['current_classbatch_id']} ({r['batch_days']} {r['batch_start_time']})"
                               + (f"; booking {br['id']} = {br['request_status']}." if br is not None else "."))
                else:
                    o = options.iloc[0]
                    if o["active_students_count"] >= o["max_batch_size"]:
                        add_reason(case, "BATCH_CHANGE_TARGET_FULL", f"Batch {o['classbatch_id']} is full.")
                    else:
                        case["target_classbatch_id"] = o["classbatch_id"]

        blocking = [c for c in case["reasons"] if REASON_CODES[c][0] == "BLOCKING"]
        case["decision"] = "EXCEPTION" if blocking else "AUTO_APPROVE"
        case["blocking_reasons"] = ",".join(blocking)
        case["advisory_reasons"] = ",".join(c for c in case["reasons"] if c not in blocking)

        if case["decision"] == "AUTO_APPROVE":
            b = catalog[catalog["classbatch_id"] == case["target_classbatch_id"]].iloc[0]
            sessions = int(f["sessions_purchased"]) if f is not None else 24
            booking_id = br["id"] if br is not None else f"NEW-{i['id']}"
            approved.append({
                "case_id": case["case_id"], "bookingrequest_id": booking_id, "invoice_id": i["id"],
                "faculty_form_id": f["id"] if f is not None else "NOT_REQUIRED",
                "student_id": i["student_id"], "user_id": i["user_id"], "class_id": i["class_id"],
                "educator_id": i["educator_id"], "classbatch_id": b["classbatch_id"],
                "classbatch_name": b["classbatch_name"], "batch_days": b["batch_days"],
                "start_time": b["batch_start_time"], "sessions_count": sessions,
                "fast_track": "SAME_BATCH" if same_batch else "BATCH_CHANGE_MATCHED",
                "advisory_notes": case["advisory_reasons"] or "CLEAN",
            })
            for n, (d, st, en) in enumerate(next_sessions(as_of, b["batch_days"], b["batch_start_time"], sessions), 1):
                schedule_rows.append({
                    "id": None, "bookingrequest_id": booking_id, "invoice_id": i["id"], "classschedule_id": None,
                    "classbatch_id": b["classbatch_id"], "class_id": i["class_id"], "user_id": i["user_id"],
                    "student_id": i["student_id"], "educator_id": i["educator_id"], "session_no": n,
                    "class_date": d, "start_time": st, "end_time": en, "booking_type": "Regular_Renewal",
                    "is_cancelled": "No", "attended_class": "No",
                })
        cases.append(case)

    # teacher forms that point at nothing
    for f in unmatched_forms:
        case = {"case_id": f"FORM-{f['id']}", "invoice_id": None, "form_id": f["id"],
                "student_id": f["student_id"], "educator_id": f["educator_id"], "reasons": [],
                "decision": "EXCEPTION", "current_stage": "2_FORM_UNMATCHED"}
        add_reason(case, "INVOICE_NOT_FOUND", f"Form {f['id']} cites invoice {f['invoice_id']}; no matching payment.")
        case["blocking_reasons"] = "INVOICE_NOT_FOUND"
        cases.append(case)

    return {
        "cases": pd.DataFrame(cases).drop(columns=["reasons"]),
        "exceptions": pd.DataFrame(exceptions),
        "approved": pd.DataFrame(approved),
        "schedule_rows": pd.DataFrame(schedule_rows),
        "raw_cases": cases,
    }
