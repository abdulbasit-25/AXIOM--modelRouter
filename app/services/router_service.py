"""Session-scoped access to the production routing engine."""

import streamlit as st

from engine import ProductionRouter


def get_router() -> ProductionRouter:
    """Return the existing session router or create it once for this session."""
    router = st.session_state.get("production_router")
    if router is None:
        router = ProductionRouter()
        st.session_state["production_router"] = router
    return router
