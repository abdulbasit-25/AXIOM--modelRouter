"""Minimal Streamlit entry point for EduRoute's custom page navigation."""

import streamlit as st

from app.config import PAGE_ICON, PAGE_TITLE
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
    )
    apply_theme()
    active_destination = initialize_session_state()
    destination = render_sidebar()
    render_mobile_bar()
    render_destination(destination or active_destination)

    st.divider()
    st.caption("EduRoute · SDG 4 Quality Education · SDG 8 Decent Work and Economic Growth")


if __name__ == "__main__":
    main()
