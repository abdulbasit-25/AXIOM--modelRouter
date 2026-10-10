"""Shared page footer."""

import streamlit as st

from app.components.feedback import chip


def page_footer() -> None:
    st.markdown(
        '<div class="page-footer"><div class="footer-brand"><div class="mini-brand-mark">E</div>'
        '<div><div class="mini-brand-text">EduRoute</div>'
        '<div class="footer-tagline">Learning, thoughtfully routed.</div></div></div>'
        f'<div class="footer-links">{chip("Integrated routing")}{chip("Transparent telemetry")}</div></div>',
        unsafe_allow_html=True,
    )
