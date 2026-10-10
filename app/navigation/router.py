"""Coordinate custom page transitions and page dispatch."""

import logging
from collections.abc import Callable

import streamlit as st

from app.config import NAVIGATION

logger = logging.getLogger(__name__)


def set_destination(destination: str) -> bool:
    """Queue a valid destination and rerun the app; reject unknown destinations."""
    if destination not in NAVIGATION:
        logger.warning("Ignoring unknown navigation destination: %r", destination)
        return False
    st.session_state["pending_destination"] = destination
    st.rerun()
    return True


def get_page_renderers() -> dict[str, Callable[[], None]]:
    """Load page renderers lazily to keep navigation independent of page imports."""
    from app.pages.about import render as render_about
    from app.pages.analytics import render as render_analytics
    from app.pages.calibration import render as render_calibration
    from app.pages.tutor import render as render_tutor
    from app.pages.welcome import render as render_welcome

    return {
        "Welcome": render_welcome,
        "Production AI Tutor": render_tutor,
        "🚀 Production AI Tutor": render_tutor,
        "Calibration Studio": render_calibration,
        "🔬 Capability Calibration Studio - Dev Mode": render_calibration,
        "SDG Analytics": render_analytics,
        "📊 SDG 4/8 Institutional Impact Analytics": render_analytics,
        "About": render_about,
    }


def render_destination(destination: str) -> str:
    """Render a known destination, falling back safely to Welcome otherwise."""
    renderers = get_page_renderers()
    if destination not in renderers:
        logger.warning("Unknown active destination %r; rendering Welcome.", destination)
        destination = "Welcome"
    renderers[destination]()
    return destination
