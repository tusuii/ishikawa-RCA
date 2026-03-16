import streamlit as st
from utils.presets import DEVOPS_PRESETS
from utils.state import CATEGORIES, CATEGORY_COLORS


def render_sidebar():
    with st.sidebar:
        st.markdown("## ⚡ Quick Presets")
        st.caption("Load a pre-built DevOps incident template")

        preset_name = st.selectbox(
            "Choose Preset",
            options=["— Select —"] + list(DEVOPS_PRESETS.keys()),
            key="preset_selector",
        )

        if st.button("Load Preset", use_container_width=True):
            if preset_name != "— Select —":
                preset = DEVOPS_PRESETS[preset_name]
                st.session_state.incident["effect"]   = preset["effect"]
                st.session_state.incident["severity"] = preset["severity"]
                st.session_state.incident["service"]  = preset["service"]
                st.session_state.incident["title"]    = preset_name
                st.session_state.causes = {
                    cat: list(preset["causes"].get(cat, []))
                    for cat in CATEGORIES
                }
                st.rerun()

        st.divider()

        st.markdown("## 📊 Summary")
        causes = st.session_state.get("causes", {})
        total  = sum(len(v) for v in causes.values())
        st.metric("Total Causes", total)

        populated = {cat: v for cat, v in causes.items() if v}
        if populated:
            for cat, cat_causes in populated.items():
                color = CATEGORY_COLORS.get(cat, "#8b949e")
                st.markdown(
                    f'<div style="display:flex; justify-content:space-between; '
                    f'align-items:center; padding:3px 0;">'
                    f'<span style="color:{color}; font-size:0.78rem; font-weight:600;">'
                    f'{cat}</span>'
                    f'<span style="background:#21262d; color:#8b949e; padding:1px 8px; '
                    f'border-radius:10px; font-size:0.72rem;">{len(cat_causes)}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.caption("No causes added yet.")

        st.divider()

        st.markdown("## 🛠️ About")
        st.caption(
            "Fishbone RCA Analyzer · Streamlit  \n"
            "For DevOps/SRE post-mortem analysis  \n"
            "Ishikawa Method · 6M Framework"
        )
