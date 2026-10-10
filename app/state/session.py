"""Initialize shared Streamlit session values without resetting user work."""

import streamlit as st

from app.config import NAVIGATION, SCENARIOS


def initialize_session_state() -> str:
    """Apply any queued destination and return a valid active page."""
    pending = st.session_state.pop("pending_destination", None)
    if pending in NAVIGATION:
        st.session_state["active_destination"] = pending

    active = st.session_state.get("active_destination")
    if active not in NAVIGATION:
        active = NAVIGATION[0]
        st.session_state["active_destination"] = active

    scenario = st.session_state.get("scenario")
    if scenario not in SCENARIOS:
        scenario = next(iter(SCENARIOS))
        st.session_state["scenario"] = scenario

    if "question_input" not in st.session_state:
        st.session_state["question_input"] = SCENARIOS[scenario]

    return active
