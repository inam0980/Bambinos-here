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
