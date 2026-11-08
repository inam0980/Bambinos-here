"""Ops Head morning board.  Run:  python -m streamlit run dashboard/app.py"""
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from pipeline import run  # noqa: E402
from rules import REASON_CODES  # noqa: E402

LOGO_FULL = "https://www.bambinos.live/assets/bambinos-logo-full.svg"
LOGO_MARK = "https://www.bambinos.live/assets/bambinos-logo-mark.svg"

st.set_page_config(page_title="Renewal ops board", page_icon=LOGO_MARK, layout="wide")
st.logo(LOGO_FULL, icon_image=LOGO_MARK, link="https://www.bambinos.live", size="large")

STAGE_LABELS = {
    "1_PAID_NO_FORM": "Paid, no teacher form",
    "2_FORM_PENDING": "Form waiting in Ops queue",
    "3_BOOKING_PENDING_BATCH_ALLOCATION": "Booking: waiting for allocation",
    "3_BOOKING_FAILED_BATCH_FULL": "Booking: failed 'batch full'",
    "3_BOOKING_AWAITING_PARENT_BATCH_SELECTION": "Booking: waiting for parent slot",
    "4_SCHEDULED": "Scheduled",
    "2_FORM_UNMATCHED": "Form with no matching invoice",
}
STAGE_STEP = {"1": "Step 2 · no form", "2": "Step 3 · Ops queue", "3": "Step 4 · allocation", "4": "Scheduled"}
STEP_COLORS = {"Step 2 · no form": "#C0392B", "Step 3 · Ops queue": "#B7791F",
               "Step 4 · allocation": "#13233A", "Scheduled": "#0E7C6B"}
def md(text) -> str:
    """Escape masked names like Ka***k so Markdown does not turn *** into bold/italic."""
    return str(text).replace("*", r"\*")


CHANNEL_STYLE = {"WhatsApp": (":material/chat:", "green"), "Slack": (":material/tag:", "violet")}

# ---------------------------------------------------------------- sidebar
with st.sidebar:
    st.subheader(":material/tune: Controls")
    as_of = st.text_input("Snapshot as of", "2026-11-04 09:00:00", help="Format YYYY-MM-DD HH:MM:SS")
    use_llm = st.toggle("Polish messages with LLM", value=False,
                        help="Off: instant deterministic templates. On: Groq → Gemini → template, ~20–40 s, "
                             "needs GROQ_API_KEY / GEMINI_API_KEY in .env or Streamlit secrets.")
    if st.button("Re-run reconciliation", icon=":material/refresh:", width="stretch"):
        st.cache_data.clear()
    st.divider()
    st.caption("**How decisions are made**")
    st.caption("Approve / reject is deterministic Python rules (`src/rules.py`). "
               "The LLM only rewrites message tone, and every number is verified in code.")
    st.link_button("GitHub repo", "https://github.com/inam0980/Bambinos-here",
                   icon=":material/code:", width="stretch")


@st.cache_data(show_spinner="Reconciling 4 tables and drafting messages…")
def load(as_of: str, use_llm: bool):
    # Writes to outputs_dashboard/ so the committed outputs/ stay untouched.
    s = run(str(ROOT / "data"), str(ROOT / "outputs_dashboard"), as_of, use_llm=use_llm)
    r = s["result"]
    return (s["metrics"], r["cases"], r["exceptions"], r["approved"], r["schedule_rows"],
            pd.DataFrame(s["messages"]))


try:
    m, cases, ex, approved, sched, msgs = load(as_of, use_llm)
except ValueError:
    st.error("Use the format YYYY-MM-DD HH:MM:SS for the snapshot time.", icon=":material/error:")
    st.stop()

blocking = ex[ex["severity"] == "BLOCKING"]
advisory = ex[ex["severity"] == "ADVISORY"]
open_cases = cases[(cases["decision"] != "ALREADY_SCHEDULED") & cases["invoice_id"].notna()].copy()

# ---------------------------------------------------------------- header
head_l, head_r = st.columns([3, 2], vertical_alignment="bottom")
with head_l:
    st.title("Renewal → scheduling: morning board")
    st.caption(f"Snapshot **{m['as_of']}** · {m['renewal_invoices']} renewal invoices across 4 tables · "
               "Bambinos.live Operations")
with head_r:
    with st.container(horizontal=True, horizontal_alignment="right"):
        st.badge(f"{m['straight_through_rate_pct']:.0f}% straight-through", icon=":material/bolt:", color="green")
        st.badge(f"{m['exceptions_open']} need a human", icon=":material/person:", color="orange")
        st.badge("LLM on" if use_llm else "Templates", icon=":material/smart_toy:",
                 color="violet" if use_llm else "gray")

# ---------------------------------------------------------------- KPI wall
with st.grid(6, min_column_width=150, gap="small"):
    st.metric("Not scheduled", m["paid_not_scheduled"], f"₹{m['revenue_paid_not_scheduled_inr']:,.0f} paid",
              delta_color="off", delta_arrow="off", border=True, height="stretch",
              icon=":material/hourglass_top:")
    st.metric("Stuck > 12 h", m["paid_not_scheduled_gt_12h"], f"oldest {m['oldest_unscheduled_paid_hours']:.0f} h",
              delta_color="inverse", border=True, height="stretch", icon=":material/warning:")
    st.metric("Auto-approved", m["auto_approved_now"], f"{len(sched)} sessions",
              delta_color="normal", border=True, height="stretch", icon=":material/task_alt:")
    st.metric("Exceptions", m["exceptions_open"], f"{len(blocking)} blocking",
              delta_color="off", delta_arrow="off", border=True, height="stretch", icon=":material/rule:")
    st.metric("Orphan invoices", f"{m['orphaned_invoice_rate_pct']}%", "no teacher form",
              delta_color="off", delta_arrow="off", border=True, height="stretch", icon=":material/link_off:")
    st.metric("Ops time saved", f"{m['manual_minutes_saved_this_run'] / 60:.1f} h",
              f"{m['auto_approved_now']} × {m['manual_minutes_per_renewal_today']} min",
              delta_color="off", delta_arrow="off", border=True, height="stretch", icon=":material/schedule:")

tab_overview, tab_exc, tab_appr, tab_msg, tab_ledger = st.tabs([
    ":material/dashboard: Overview",
    f":material/report: Exceptions ({m['exceptions_open']})",
    f":material/check_circle: Auto-approved ({m['auto_approved_now']})",
    f":material/forum: Messages ({len(msgs)})",
    ":material/table: Ledger",
])

# ---------------------------------------------------------------- overview
with tab_overview:
    c1, c2 = st.columns([1.15, 1], gap="medium")
    with c1:
        with st.container(border=True, height="stretch"):
            st.markdown("**How long each paid renewal has waited** · hours since payment, dashed line = 12 h SLA")
            w = open_cases[open_cases["hours_since_payment"].notna()].sort_values("hours_since_payment")
            w = w.assign(step=w["current_stage"].str[0].map(STAGE_STEP))
            series = [{
                "type": "bar", "name": step, "stack": "h", "barWidth": 14,
                "itemStyle": {"color": STEP_COLORS[step], "borderRadius": [0, 4, 4, 0]},
                "data": [round(h, 1) if s == step else None for h, s in zip(w["hours_since_payment"], w["step"])],
                **({"markLine": {"symbol": "none", "silent": True, "label": {"formatter": "12h SLA"},
                                 "lineStyle": {"type": "dashed", "color": "#C0392B"},
                                 "data": [{"xAxis": 12}]}} if i == 0 else {}),
            } for i, step in enumerate(["Step 2 · no form", "Step 3 · Ops queue", "Step 4 · allocation"])]
            st.echarts_chart({
                "animationDuration": 500,
                "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}, "valueFormatter": "%.1f h"},
                "legend": {"bottom": 0},
                "grid": {"left": 8, "right": 30, "top": 10, "bottom": 34, "containLabel": True},
                "xAxis": {"type": "value", "name": "hours", "nameLocation": "end"},
                "yAxis": {"type": "category", "data": [f"RNW-{i}" for i in w["invoice_id"]]},
                "series": series,
            }, height=360, alt="Hours each paid renewal has waited since payment, colored by the stuck step")
    with c2:
        with st.container(border=True, height="stretch"):
            st.markdown("**Before vs after one engine run** · renewals per stage")
            before = cases["current_stage"].str[0].map(STAGE_STEP).value_counts()
            after = pd.Series({"Scheduled": int((cases["decision"] != "EXCEPTION").sum()),
                               "Needs a human": int((cases["decision"] == "EXCEPTION").sum())})
            cats = ["Step 2 · no form", "Step 3 · Ops queue", "Step 4 · allocation", "Needs a human", "Scheduled"]
            st.echarts_chart({
                "animationDuration": 500,
                "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
                "legend": {"bottom": 0},
                "grid": {"left": 8, "right": 24, "top": 10, "bottom": 34, "containLabel": True},
                "xAxis": {"type": "value", "minInterval": 1},
                "yAxis": {"type": "category", "data": cats, "inverse": True},
                "series": [
                    {"type": "bar", "name": "Today (manual)", "barWidth": 12, "label": {"show": True, "position": "right"},
                     "itemStyle": {"color": "#B7791F", "borderRadius": [0, 4, 4, 0]},
                     "data": [int(before.get(c, 0)) or None for c in cats]},
                    {"type": "bar", "name": "After engine", "barWidth": 12, "label": {"show": True, "position": "right"},
                     "itemStyle": {"color": "#0E7C6B", "borderRadius": [0, 4, 4, 0]},
                     "data": [int(after.get(c, 0)) or None for c in cats]},
                ],
            }, height=360, alt="Renewals per stage today versus after one engine run")

    c3, c4 = st.columns(2, gap="medium")
    with c3:
        with st.container(border=True, height="stretch"):
            st.markdown("**Blocking exceptions by owner** · each has one owner and one SLA")
            by_owner = blocking.groupby("owner").agg(n=("case_id", "count"), sla=("sla_hours", "min")).reset_index()
            st.echarts_chart({
                "tooltip": {"trigger": "axis"},
                "grid": {"left": 8, "right": 20, "top": 10, "bottom": 10, "containLabel": True},
                "xAxis": {"type": "value", "minInterval": 1},
                "yAxis": {"type": "category", "data": [f"{o} · {s}h SLA" for o, s in zip(by_owner["owner"], by_owner["sla"])]},
                "animationDuration": 500,
                "series": [{"type": "bar", "data": by_owner["n"].tolist(), "barWidth": 16,
                            "itemStyle": {"color": "#B7791F", "borderRadius": [0, 4, 4, 0]},
                            "label": {"show": True, "position": "right"}}],
            }, height=230, alt="Blocking exceptions per owner")
    with c4:
        with st.container(border=True, height="stretch"):
            st.markdown("**Every reason code the engine raised**")
            rc = ex["reason_code"].value_counts().sort_values()
            sev = {k: v[0] for k, v in REASON_CODES.items()}
            st.echarts_chart({
                "tooltip": {"trigger": "axis"},
                "grid": {"left": 8, "right": 20, "top": 10, "bottom": 10, "containLabel": True},
                "xAxis": {"type": "value", "minInterval": 1},
                "yAxis": {"type": "category", "data": rc.index.tolist(), "axisLabel": {"fontSize": 10}},
                "series": [{"type": "bar", "barWidth": 10, "label": {"show": True, "position": "right"},
                            "data": [{"value": int(v), "itemStyle": {
                                "color": "#C0392B" if sev[k] == "BLOCKING" else "#0E7C6B",
                                "borderRadius": [0, 4, 4, 0]}} for k, v in rc.items()]}],
            }, height=230, alt="Count of each reason code, red for blocking and teal for advisory")

    st.info("Before the engine: **1 of 12** paid renewals scheduled. After one run: **9 scheduled** "
            f"({m['auto_approved_now']} auto-approved) and **{m['exceptions_open']}** routed to the right owner.",
            title="What the engine changed", icon=":material/insights:")

# ---------------------------------------------------------------- exceptions
with tab_exc:
    view = st.segmented_control("Show", ["Blocking", "Advisory", "All"], default="Blocking",
                                required=True, label_visibility="collapsed")
    data = {"Blocking": blocking, "Advisory": advisory, "All": ex}[view]
    if view == "Blocking":
        for cid, grp in data.groupby("case_id", sort=False):
            c = cases[cases["case_id"] == cid].iloc[0]
            with st.container(border=True):
                top = st.container(horizontal=True, vertical_alignment="center")
                top.markdown(f"#### {cid}")
                for _, e in grp.iterrows():
                    top.badge(e["reason_code"], color="red", icon=":material/block:")
                    top.badge(f"{e['owner']} · {e['sla_hours']}h SLA", color="orange", icon=":material/timer:")
                left, right = st.columns([3, 2])
                with left:
                    for _, e in grp.iterrows():
                        st.markdown(md(e["detail"]))
                        st.caption(f":material/arrow_forward: {e['recommended_action']}")
                with right:
                    waited = c.get("hours_since_payment")
                    st.caption(f"Student **{md(c.get('student_name'))}** · {c.get('class_name')}  \n"
                               f"Paid ₹{c.get('net_amount', 0):,.0f} · status {c.get('payment_status')}  \n"
                               f"Waiting {waited if pd.notna(waited) else '—'} h · "
                               f"{STAGE_LABELS.get(c['current_stage'], c['current_stage'])}")
                drafts = msgs[(msgs["case_id"] == cid) & (msgs["reason_code"] != "AUTO_APPROVED")]
                if len(drafts):
                    with st.expander(f"Drafted follow-ups ({len(drafts)})", icon=":material/forum:"):
                        for _, d in drafts.iterrows():
                            st.markdown(f"**{d['channel']} → {d['recipient']}**")
                            st.code(d["message"], language=None, wrap_lines=True)
    else:
        st.dataframe(
            data[["case_id", "reason_code", "severity", "owner", "sla_hours", "detail", "recommended_action"]],
            hide_index=True,
            column_config={
                "case_id": st.column_config.TextColumn("Case", width="small"),
                "reason_code": st.column_config.TextColumn("Reason code"),
                "severity": st.column_config.TextColumn("Severity", width="small"),
                "owner": st.column_config.TextColumn("Owner", width="small"),
                "sla_hours": st.column_config.NumberColumn("SLA", format="%d h", width="small"),
                "detail": st.column_config.TextColumn("Evidence", width="large"),
                "recommended_action": st.column_config.TextColumn("Action", width="large"),
            },
        )
    st.download_button("Download exceptions CSV", ex.to_csv(index=False), "2_flagged_exceptions.csv",
                       "text/csv", icon=":material/download:", on_click="ignore")

# ---------------------------------------------------------------- auto-approved
with tab_appr:
    st.success(f"{m['auto_approved_now']} renewals pass all five gates (paid · identity · fee · batch · unique) "
               f"and are ready for `class_schedule_bookings`: {len(sched)} sessions generated.",
               icon=":material/verified:")
    st.dataframe(
        approved[["case_id", "invoice_id", "student_id", "classbatch_name", "batch_days", "start_time",
                  "sessions_count", "fast_track", "faculty_form_id", "advisory_notes"]],
        hide_index=True,
        column_config={
            "case_id": "Case", "invoice_id": "Invoice", "student_id": "Student",
            "classbatch_name": "Batch", "batch_days": "Days",
            "start_time": st.column_config.TextColumn("Time", width="small"),
            "sessions_count": st.column_config.NumberColumn("Sessions", width="small"),
            "fast_track": "Track",
            "faculty_form_id": st.column_config.TextColumn("Teacher form", help="NOT_REQUIRED = fast-tracked with no form"),
            "advisory_notes": st.column_config.TextColumn("Auto-fixed notes", width="large"),
        },
    )
    with st.container(horizontal=True):
        st.download_button("Approved renewals CSV", approved.to_csv(index=False),
                           "1_auto_approved_ready_for_scheduling.csv", "text/csv",
                           icon=":material/download:", on_click="ignore")
        st.download_button("Sessions to insert CSV", sched.to_csv(index=False),
                           "1b_class_schedule_bookings_to_insert.csv", "text/csv",
                           icon=":material/download:", on_click="ignore")
    st.markdown("**First sessions of the new term**")
    first = sched[sched["session_no"] <= 2][["invoice_id", "student_id", "classbatch_id", "session_no",
                                              "class_date", "start_time", "end_time", "booking_type"]]
    st.dataframe(first, hide_index=True)

# ---------------------------------------------------------------- messages
with tab_msg:
    who = st.pills("Recipient", sorted(msgs["recipient"].unique()), selection_mode="multi",
                   default=None, help="Leave empty to show everyone")
    view_msgs = msgs if not who else msgs[msgs["recipient"].isin(who)]
    with st.grid(2, min_column_width=320, gap="small"):
        for _, x in view_msgs.iterrows():
            icon, color = CHANNEL_STYLE.get(x["channel"], (":material/send:", "gray"))
            with st.container(border=True, height="stretch"):
                row = st.container(horizontal=True, vertical_alignment="center")
                row.badge(f"{x['channel']} → {x['recipient']}", icon=icon, color=color)
                row.badge(x["case_id"], color="gray")
                st.caption(f"`{x['reason_code']}`")
                st.markdown(md(x["message"]))

# ---------------------------------------------------------------- ledger
with tab_ledger:
    st.caption("One row per invoice: where it sits, how long it has waited, and what the engine decided.")
    led = cases.copy()
    led["current_stage"] = led["current_stage"].map(STAGE_LABELS).fillna(led["current_stage"])
    st.dataframe(
        led[["case_id", "student_name", "class_name", "payment_status", "net_amount", "current_stage",
             "hours_since_payment", "decision", "blocking_reasons", "advisory_reasons"]],
        hide_index=True,
        column_config={
            "case_id": "Case", "student_name": "Student", "class_name": "Class", "payment_status": "Payment",
            "net_amount": st.column_config.NumberColumn("Paid", format="₹%d"),
            "current_stage": "Stage today",
            "hours_since_payment": st.column_config.ProgressColumn("Waiting", min_value=0, max_value=72,
                                                                   format="%.1f h"),
            "decision": "Engine decision", "blocking_reasons": "Blocking", "advisory_reasons": "Auto-fixed",
        },
    )
    st.download_button("Download ledger CSV", cases.to_csv(index=False), "0_reconciliation_ledger.csv",
                       "text/csv", icon=":material/download:", on_click="ignore")
