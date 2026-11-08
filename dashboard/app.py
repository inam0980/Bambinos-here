"""Ops Head morning board.  Run:  python -m streamlit run streamlit_app.py"""
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

# ---------------------------------------------------------------- palette
VIOLET, INDIGO, PINK, ORANGE, AMBER, GREEN, CYAN, RED, BLUE = (
    "#7C3AED", "#4F46E5", "#EC4899", "#F97316", "#F59E0B", "#10B981", "#06B6D4", "#EF4444", "#3B82F6")


def grad(a: str, b: str, horizontal: bool = True) -> dict:
    """ECharts linear gradient fill."""
    return {"type": "linear", "x": 0, "y": 0, "x2": 1 if horizontal else 0, "y2": 0 if horizontal else 1,
            "colorStops": [{"offset": 0, "color": a}, {"offset": 1, "color": b}]}


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
STEP_GRAD = {"Step 2 · no form": (RED, PINK), "Step 3 · Ops queue": (ORANGE, AMBER),
             "Step 4 · allocation": (INDIGO, VIOLET), "Needs a human": (PINK, VIOLET), "Scheduled": (GREEN, CYAN)}
CHANNEL_STYLE = {"WhatsApp": (":material/chat:", "green", "wa"), "Slack": (":material/tag:", "violet", "sl")}


def md(text) -> str:
    """Escape masked names like Ka***k so Markdown does not turn *** into bold/italic."""
    return str(text).replace("*", r"\*")


# ---------------------------------------------------------------- styling (user asked for a colourful UI)
st.html("""
<style>
.bmb-hero{background:linear-gradient(120deg,#4F46E5 0%,#7C3AED 38%,#EC4899 72%,#F97316 100%);
  border-radius:20px;padding:26px 30px 22px;color:#fff;position:relative;overflow:hidden;
  box-shadow:0 14px 40px -12px rgba(124,58,237,.55);margin-bottom:6px}
.bmb-hero:before{content:"";position:absolute;right:-60px;top:-80px;width:280px;height:280px;border-radius:50%;
  background:rgba(255,255,255,.12)}
.bmb-hero:after{content:"";position:absolute;right:120px;bottom:-110px;width:220px;height:220px;border-radius:50%;
  background:rgba(255,255,255,.08)}
.bmb-hero .eyebrow{font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;opacity:.9}
.bmb-hero h1{color:#fff!important;font-size:34px!important;font-weight:800!important;margin:6px 0 4px!important;
  padding:0!important;line-height:1.15!important}
.bmb-hero p{margin:0;opacity:.92;font-size:14.5px}
.bmb-pills{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px;position:relative;z-index:1}
.bmb-pill{background:rgba(255,255,255,.18);border:1px solid rgba(255,255,255,.35);backdrop-filter:blur(4px);
  border-radius:999px;padding:5px 12px;font-size:12.5px;font-weight:600;color:#fff}
.bmb-kpis{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:12px;margin:10px 0 4px}
@media (max-width:1100px){.bmb-kpis{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media (max-width:640px){.bmb-kpis{grid-template-columns:repeat(2,minmax(0,1fr))}}
.bmb-kpi{border-radius:16px;padding:14px 16px 13px;color:#fff;position:relative;overflow:hidden;
  box-shadow:0 10px 24px -12px rgba(15,23,42,.45);transition:transform .15s}
.bmb-kpi:hover{transform:translateY(-3px)}
.bmb-kpi:after{content:"";position:absolute;right:-24px;top:-24px;width:90px;height:90px;border-radius:50%;
  background:rgba(255,255,255,.16)}
.bmb-kpi .ic{font-size:20px;line-height:1}
.bmb-kpi .l{font-size:12px;font-weight:600;opacity:.92;margin-top:6px}
.bmb-kpi .v{font-size:30px;font-weight:800;line-height:1.1;margin-top:2px}
.bmb-kpi .s{display:inline-block;margin-top:6px;font-size:11.5px;font-weight:600;background:rgba(255,255,255,.22);
  border-radius:999px;padding:2px 9px}
.k1{background:linear-gradient(135deg,#EF4444,#F97316)} .k2{background:linear-gradient(135deg,#F97316,#F59E0B)}
.k3{background:linear-gradient(135deg,#10B981,#06B6D4)} .k4{background:linear-gradient(135deg,#EC4899,#8B5CF6)}
.k5{background:linear-gradient(135deg,#8B5CF6,#4F46E5)} .k6{background:linear-gradient(135deg,#3B82F6,#06B6D4)}
/* tabs */
button[role="tab"]{border-radius:999px!important;padding:6px 14px!important;margin-right:4px!important}
button[role="tab"][aria-selected="true"]{background:linear-gradient(120deg,#4F46E5,#EC4899)!important;color:#fff!important}
button[role="tab"][aria-selected="true"] *{color:#fff!important}
/* chart cards: coloured top stripe */
[class*="st-key-card_"]{border-radius:16px!important;background:#fff;box-shadow:0 8px 24px -14px rgba(79,70,229,.35)}
.st-key-card_wait{box-shadow:inset 0 5px 0 #F97316,0 8px 24px -14px rgba(249,115,22,.4)!important}
.st-key-card_before{box-shadow:inset 0 5px 0 #10B981,0 8px 24px -14px rgba(16,185,129,.4)!important}
.st-key-card_owner{box-shadow:inset 0 5px 0 #EC4899,0 8px 24px -14px rgba(236,72,153,.4)!important}
.st-key-card_codes{box-shadow:inset 0 5px 0 #7C3AED,0 8px 24px -14px rgba(124,58,237,.4)!important}
/* exception cards */
[class*="st-key-exc_"]{border-radius:16px!important;border-left:6px solid #EF4444!important;
  background:linear-gradient(90deg,#FFF1F2 0%,#FFFFFF 45%)!important}
/* message cards */
[class*="st-key-msg_wa_"]{border-radius:16px!important;border-left:6px solid #10B981!important;
  background:linear-gradient(135deg,#ECFDF5 0%,#FFFFFF 70%)!important}
[class*="st-key-msg_sl_"]{border-radius:16px!important;border-left:6px solid #8B5CF6!important;
  background:linear-gradient(135deg,#F5F3FF 0%,#FFFFFF 70%)!important}
.st-key-impact{border-radius:16px!important;background:linear-gradient(120deg,#EEF2FF,#FDF2F8,#FFF7ED)!important}
</style>
""")

# ---------------------------------------------------------------- sidebar
with st.sidebar:
    st.subheader(":material/tune: Controls")
    as_of = st.text_input("Snapshot as of", "2026-11-04 09:00:00", help="Format YYYY-MM-DD HH:MM:SS")
    use_llm = st.toggle("Polish messages with LLM", value=False,
                        help="Off: instant deterministic templates. On: Groq → Gemini → template, ~20–40 s, "
                             "needs GROQ_API_KEY / GEMINI_API_KEY in .env or Streamlit secrets.")
    if st.button("Re-run reconciliation", icon=":material/refresh:", width="stretch", type="primary"):
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

# ---------------------------------------------------------------- hero + KPI wall
st.html(f"""
<div class="bmb-hero">
  <div class="eyebrow">Bambinos.live · Operations</div>
  <h1>Renewal → scheduling morning board</h1>
  <p>Snapshot {m['as_of']} · {m['renewal_invoices']} renewal invoices reconciled across 4 tables.
     Every paid child should be in class, with no one waiting on a form.</p>
  <div class="bmb-pills">
    <span class="bmb-pill">⚡ {m['straight_through_rate_pct']:.0f}% straight-through</span>
    <span class="bmb-pill">🙋 {m['exceptions_open']} need a human</span>
    <span class="bmb-pill">📅 {len(sched)} sessions ready to book</span>
    <span class="bmb-pill">{'🤖 LLM polishing on' if use_llm else '📝 Template messages'}</span>
  </div>
</div>
<div class="bmb-kpis">
  <div class="bmb-kpi k1"><div class="ic">⏳</div><div class="l">Paid, not scheduled</div>
    <div class="v">{m['paid_not_scheduled']}</div><span class="s">₹{m['revenue_paid_not_scheduled_inr']:,.0f} waiting</span></div>
  <div class="bmb-kpi k2"><div class="ic">🚨</div><div class="l">Stuck &gt; 12 h</div>
    <div class="v">{m['paid_not_scheduled_gt_12h']}</div><span class="s">oldest {m['oldest_unscheduled_paid_hours']:.0f} h</span></div>
  <div class="bmb-kpi k3"><div class="ic">✅</div><div class="l">Auto-approved</div>
    <div class="v">{m['auto_approved_now']}</div><span class="s">{len(sched)} sessions</span></div>
  <div class="bmb-kpi k4"><div class="ic">🧩</div><div class="l">Exceptions</div>
    <div class="v">{m['exceptions_open']}</div><span class="s">{len(blocking)} blocking</span></div>
  <div class="bmb-kpi k5"><div class="ic">🔗</div><div class="l">Orphan invoices</div>
    <div class="v">{m['orphaned_invoice_rate_pct']}%</div><span class="s">no teacher form</span></div>
  <div class="bmb-kpi k6"><div class="ic">⏱️</div><div class="l">Ops time saved</div>
    <div class="v">{m['manual_minutes_saved_this_run'] / 60:.1f} h</div>
    <span class="s">{m['auto_approved_now']} × {m['manual_minutes_per_renewal_today']} min</span></div>
</div>
""")

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
        with st.container(border=True, height="stretch", key="card_wait"):
            st.markdown("**⏳ How long each paid renewal has waited** · dashed line = 12 h SLA")
            w = open_cases[open_cases["hours_since_payment"].notna()].sort_values("hours_since_payment")
            w = w.assign(step=w["current_stage"].str[0].map(STAGE_STEP))
            series = [{
                "type": "bar", "name": step, "stack": "h", "barWidth": 16,
                "itemStyle": {"color": grad(*STEP_GRAD[step]), "borderRadius": [0, 8, 8, 0]},
                "data": [round(h, 1) if s == step else None for h, s in zip(w["hours_since_payment"], w["step"])],
                **({"markLine": {"symbol": "none", "silent": True,
                                 "label": {"formatter": "12h SLA", "position": "end", "color": RED, "fontWeight": "bold"},
                                 "lineStyle": {"type": "dashed", "color": RED, "width": 2},
                                 "data": [{"xAxis": 12}]}} if i == 0 else {}),
            } for i, step in enumerate(["Step 2 · no form", "Step 3 · Ops queue", "Step 4 · allocation"])]
            st.echarts_chart({
                "animationDuration": 600,
                "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}, "valueFormatter": "%.1f h"},
                "legend": {"bottom": 0},
                "grid": {"left": 8, "right": 30, "top": 14, "bottom": 34, "containLabel": True},
                "xAxis": {"type": "value", "axisLabel": {"formatter": "{value} h"}},
                "yAxis": {"type": "category", "data": [f"RNW-{i}" for i in w["invoice_id"]]},
                "series": series,
            }, height=370, alt="Hours each paid renewal has waited since payment, colored by the stuck step")
    with c2:
        with st.container(border=True, height="stretch", key="card_before"):
            st.markdown("**🚀 Before vs after one engine run** · renewals per stage")
            before = cases["current_stage"].str[0].map(STAGE_STEP).value_counts()
            after = pd.Series({"Scheduled": int((cases["decision"] != "EXCEPTION").sum()),
                               "Needs a human": int((cases["decision"] == "EXCEPTION").sum())})
            cats = ["Step 2 · no form", "Step 3 · Ops queue", "Step 4 · allocation", "Needs a human", "Scheduled"]
            st.echarts_chart({
                "animationDuration": 600,
                "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
                "legend": {"bottom": 0},
                "grid": {"left": 8, "right": 24, "top": 14, "bottom": 34, "containLabel": True},
                "xAxis": {"type": "value", "minInterval": 1},
                "yAxis": {"type": "category", "data": cats, "inverse": True},
                "series": [
                    {"type": "bar", "name": "Today (manual)", "barWidth": 14, "label": {"show": True, "position": "right"},
                     "itemStyle": {"color": grad(ORANGE, AMBER), "borderRadius": [0, 8, 8, 0]},
                     "data": [int(before.get(c, 0)) or None for c in cats]},
                    {"type": "bar", "name": "After engine", "barWidth": 14, "label": {"show": True, "position": "right"},
                     "itemStyle": {"color": grad(VIOLET, PINK), "borderRadius": [0, 8, 8, 0]},
                     "data": [int(after.get(c, 0)) or None for c in cats]},
                ],
            }, height=370, alt="Renewals per stage today versus after one engine run")

    c3, c4 = st.columns(2, gap="medium")
    with c3:
        with st.container(border=True, height="stretch", key="card_owner"):
            st.markdown("**🎯 Who owns each blocking exception** · one owner, one SLA")
            by_owner = blocking.groupby("owner").agg(n=("case_id", "count"), sla=("sla_hours", "min")).reset_index()
            palette = [PINK, VIOLET, ORANGE, CYAN, GREEN, BLUE]
            st.echarts_chart({
                "animationDuration": 600,
                "tooltip": {"trigger": "item", "formatter": "{b}: {c}"},
                "legend": {"bottom": 0, "type": "scroll"},
                "series": [{"type": "pie", "radius": ["45%", "72%"], "center": ["50%", "45%"],
                            "itemStyle": {"borderRadius": 10, "borderColor": "#fff", "borderWidth": 3},
                            "label": {"formatter": "{c}", "fontWeight": "bold"},
                            "data": [{"name": f"{o} · {s}h", "value": int(n),
                                      "itemStyle": {"color": palette[i % len(palette)]}}
                                     for i, (o, s, n) in enumerate(zip(by_owner["owner"], by_owner["sla"], by_owner["n"]))]}],
            }, height=260, alt="Blocking exceptions per owner with SLA")
    with c4:
        with st.container(border=True, height="stretch", key="card_codes"):
            st.markdown("**🧠 Every reason code the engine raised** · red blocks, green auto-fixed")
            rc = ex["reason_code"].value_counts().sort_values()
            sev = {k: v[0] for k, v in REASON_CODES.items()}
            st.echarts_chart({
                "animationDuration": 600,
                "tooltip": {"trigger": "axis"},
                "grid": {"left": 8, "right": 24, "top": 10, "bottom": 10, "containLabel": True},
                "xAxis": {"type": "value", "minInterval": 1},
                "yAxis": {"type": "category", "data": rc.index.tolist(), "axisLabel": {"fontSize": 10}},
                "series": [{"type": "bar", "barWidth": 11, "label": {"show": True, "position": "right"},
                            "data": [{"value": int(v), "itemStyle": {
                                "color": grad(RED, PINK) if sev[k] == "BLOCKING" else grad(GREEN, CYAN),
                                "borderRadius": [0, 8, 8, 0]}} for k, v in rc.items()]}],
            }, height=260, alt="Count of each reason code, red for blocking and green for advisory")

    with st.container(border=True, key="impact"):
        st.markdown(f"#### 🌈 What one engine run changed")
        a, b, c = st.columns(3)
        a.metric("Scheduled before", "1 of 12", border=False)
        b.metric("Scheduled after", f"{1 + m['auto_approved_now']} of 12", f"+{m['auto_approved_now']}", border=False)
        c.metric("Routed to the right owner", m["exceptions_open"], "0 sent to 'just Ops'",
                 delta_color="off", delta_arrow="off", border=False)

# ---------------------------------------------------------------- exceptions
with tab_exc:
    view = st.segmented_control("Show", ["Blocking", "Advisory", "All"], default="Blocking",
                                required=True, label_visibility="collapsed")
    data = {"Blocking": blocking, "Advisory": advisory, "All": ex}[view]
    if view == "Blocking":
        for cid, grp in data.groupby("case_id", sort=False):
            c = cases[cases["case_id"] == cid].iloc[0]
            with st.container(border=True, key=f"exc_{cid}"):
                top = st.container(horizontal=True, vertical_alignment="center")
                top.markdown(f"#### 🚩 {cid}")
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
                       "text/csv", icon=":material/download:", on_click="ignore", type="primary")

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
                           icon=":material/download:", on_click="ignore", type="primary")
        st.download_button("Sessions to insert CSV", sched.to_csv(index=False),
                           "1b_class_schedule_bookings_to_insert.csv", "text/csv",
                           icon=":material/download:", on_click="ignore")
    st.markdown("**📅 First sessions of the new term**")
    first = sched[sched["session_no"] <= 2][["invoice_id", "student_id", "classbatch_id", "session_no",
                                              "class_date", "start_time", "end_time", "booking_type"]]
    st.dataframe(first, hide_index=True)

# ---------------------------------------------------------------- messages
with tab_msg:
    who = st.pills("Recipient", sorted(msgs["recipient"].unique()), selection_mode="multi",
                   default=None, help="Leave empty to show everyone")
    view_msgs = msgs if not who else msgs[msgs["recipient"].isin(who)]
    with st.grid(2, min_column_width=320, gap="small"):
        for i, x in view_msgs.reset_index(drop=True).iterrows():
            icon, color, k = CHANNEL_STYLE.get(x["channel"], (":material/send:", "gray", "wa"))
            with st.container(border=True, height="stretch", key=f"msg_{k}_{i}"):
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
                       "text/csv", icon=":material/download:", on_click="ignore", type="primary")
