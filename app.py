import streamlit as st
from components.sidebar import render_sidebar
from components.form import render_cause_form
from components.diagram import render_fishbone_svg
from components.report import render_report_panel
from utils.state import init_session_state

st.set_page_config(
    page_title="Fishbone RCA Analyzer",
    page_icon="🦴",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inject dark CSS ────────────────────────────────────────────────────────────
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

init_session_state()

# ── Header ─────────────────────────────────────────────────────────────────────
severity = st.session_state.incident.get("severity", "")
sev_color = {
    "P1 - Critical": "#ef4444",
    "P2 - High":     "#f97316",
    "P3 - Medium":   "#eab308",
    "P4 - Low":      "#22c55e",
}.get(severity, "transparent")

sev_badge = (
    f'<span style="background:{sev_color};color:#0d1117;padding:2px 10px;'
    f'border-radius:20px;font-size:0.65rem;font-weight:700;'
    f'letter-spacing:1px;margin-left:8px;vertical-align:middle;">'
    f'{severity}</span>'
    if severity else ""
)

st.markdown(f"""
<div class="rca-header">
  <div>
    <span class="rca-badge">SRE</span>
    <span class="rca-badge" style="background:#21262d;color:#58a6ff;margin-left:4px;">
      ISHIKAWA
    </span>
    {sev_badge}
  </div>
  <h1>Fishbone RCA Analyzer</h1>
  <p class="subtitle">Root Cause Analysis · Ishikawa Diagram · Incident Post-Mortem</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
render_sidebar()

# ── Main layout ────────────────────────────────────────────────────────────────
left_col, right_col = st.columns([1, 1.65], gap="large")

with left_col:
    render_cause_form()

with right_col:
    render_fishbone_svg()
    render_report_panel()
