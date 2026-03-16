import streamlit as st

CATEGORIES = [
    "People",
    "Process",
    "Tools / Technology",
    "Environment",
    "Measurement",
    "Materials / Data",
]

CATEGORY_COLORS = {
    "People":               "#ef4444",
    "Process":              "#f97316",
    "Tools / Technology":   "#3b82f6",
    "Environment":          "#22c55e",
    "Measurement":          "#a855f7",
    "Materials / Data":     "#eab308",
}

INCIDENT_DEFAULTS = {
    "title":    "",
    "date":     "",
    "severity": "P2 - High",
    "service":  "",
    "owner":    "",
    "effect":   "Production Incident",
}


def init_session_state():
    if "incident" not in st.session_state:
        st.session_state.incident = INCIDENT_DEFAULTS.copy()

    if "causes" not in st.session_state:
        st.session_state.causes = {cat: [] for cat in CATEGORIES}

    if "selected_preset" not in st.session_state:
        st.session_state.selected_preset = None

    if "show_report" not in st.session_state:
        st.session_state.show_report = False


def get_all_causes() -> dict:
    return st.session_state.causes


def add_cause(category: str, cause: str):
    if cause.strip():
        st.session_state.causes[category].append(cause.strip())


def remove_cause(category: str, index: int):
    st.session_state.causes[category].pop(index)


def clear_all():
    st.session_state.causes = {cat: [] for cat in CATEGORIES}
    st.session_state.incident = INCIDENT_DEFAULTS.copy()
