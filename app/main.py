"""Minimal Streamlit entry point for Axiom's custom page navigation."""

import streamlit as st

from app.config import BRAND_DESCRIPTION, BRAND_NAME, BRAND_TAGLINE, PAGE_ICON, PAGE_TITLE
from app.navigation.mobile_menu import render_mobile_bar
from app.navigation.router import render_destination
from app.navigation.sidebar import render_sidebar
from app.state.session import initialize_session_state
from app.styles import apply_theme


def main() -> None:
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "About": f"**{BRAND_NAME} — {BRAND_TAGLINE}**\n\n{BRAND_DESCRIPTION}"
        },
    )
    apply_theme()
    active_destination = initialize_session_state()
    destination = render_sidebar()
    render_mobile_bar()
    render_destination(destination or active_destination)

    st.divider()
    st.caption(f"{BRAND_NAME} · SDG 4 Quality Education · SDG 8 Decent Work and Economic Growth")


if __name__ == "__main__":
    main()
