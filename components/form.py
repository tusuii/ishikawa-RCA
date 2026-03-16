import streamlit as st
from utils.state import CATEGORIES, CATEGORY_COLORS, add_cause, remove_cause, get_all_causes

CATEGORY_ICONS = {
    "People":               "👤",
    "Process":              "⚙️",
    "Tools / Technology":   "🔧",
    "Environment":          "🌐",
    "Measurement":          "📏",
    "Materials / Data":     "💾",
}


def render_cause_form():
    st.markdown("### 📋 Incident Details")

    inc = st.session_state.incident

    inc["title"] = st.text_input(
        "Incident Title",
        value=inc["title"],
        placeholder="e.g. K8s Pod CrashLoopBackOff — prod",
    )
    inc["effect"] = st.text_input(
        "Problem Statement (Fish Head)",
        value=inc["effect"],
        placeholder="e.g. Production Incident",
    )

    col1, col2 = st.columns(2)
    with col1:
        inc["severity"] = st.selectbox(
            "Severity",
            ["P1 - Critical", "P2 - High", "P3 - Medium", "P4 - Low"],
            index=["P1 - Critical", "P2 - High", "P3 - Medium", "P4 - Low"].index(
                inc.get("severity", "P2 - High")
            ),
        )
        inc["service"] = st.text_input(
            "Affected Service",
            value=inc["service"],
            placeholder="api-gateway / ArgoCD / Jenkins",
        )
    with col2:
        inc["date"] = st.text_input(
            "Incident Date",
            value=inc["date"],
            placeholder="2026-03-16",
        )
        inc["owner"] = st.text_input(
            "RCA Owner",
            value=inc["owner"],
            placeholder="@you / SRE Team",
        )

    st.markdown("---")
    st.markdown("### 🦴 Root Causes by Category")
    st.caption("Add causes under each category. Diagram updates live.")

    causes = get_all_causes()

    for cat in CATEGORIES:
        color = CATEGORY_COLORS[cat]
        icon  = CATEGORY_ICONS.get(cat, "•")
        count = len(causes[cat])
        label = f"{icon} **{cat}**" + (f" `{count}`" if count else "")

        with st.expander(label, expanded=(count > 0)):
            for i, cause in enumerate(causes[cat]):
                c1, c2 = st.columns([10, 1])
                with c1:
                    st.markdown(
                        f'<div class="cause-tag" style="border-left:3px solid {color}">'
                        f'{cause}</div>',
                        unsafe_allow_html=True,
                    )
                with c2:
                    if st.button("✕", key=f"del_{cat}_{i}", help="Remove"):
                        remove_cause(cat, i)
                        st.rerun()

            new_val = st.text_input(
                label=f"New {cat} cause",
                key=f"new_{cat}",
                placeholder=f"Add {cat} cause...",
                label_visibility="collapsed",
            )
            if st.button(f"＋ Add", key=f"add_{cat}", use_container_width=True):
                add_cause(cat, new_val)
                st.rerun()

    st.markdown("---")
    if st.button("🗑️ Clear All", use_container_width=True):
        from utils.state import clear_all
        clear_all()
        st.rerun()
