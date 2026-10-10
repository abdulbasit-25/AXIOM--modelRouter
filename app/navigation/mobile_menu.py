"""Responsive mobile navigation preserving the existing menu/dialog behavior."""

import streamlit as st

from app.config import NAVIGATION, NAV_ICONS
from app.components.branding import mobile_brand
from app.navigation.router import set_destination


def _nav_label(name: str) -> str:
    return f"{NAV_ICONS[name]}  {name}"


@st.dialog("Menu")
def _render_menu() -> None:
    current = st.session_state.get("active_destination", NAVIGATION[0])
    for name in NAVIGATION:
        if st.button(
            _nav_label(name),
            key=f"mobile_nav_{name}",
            type="primary" if name == current else "secondary",
            width="stretch",
        ):
            set_destination(name)
    st.caption("The tutor is connected to the routing engine.")


def render_mobile_bar() -> None:
    """Render the sticky mobile brand and hamburger menu."""
    with st.container(key="mobile_nav"):
        mobile_brand()
        if st.button("Menu", key="open_menu", icon=":material/menu:"):
            _render_menu()
