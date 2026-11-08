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
    from messages import LLM_STATS
    print(f"Messages written by: {LLM_STATS}")
