"""Shared page footer."""

import streamlit as st

from app.config import BRAND_TAGLINE, BRAND_WORDMARK
from app.components.feedback import chip


def page_footer() -> None:
    st.markdown(
        f'<div class="page-footer"><div class="footer-brand"><div class="mini-brand-mark" aria-hidden="true">A</div>'
        f'<div><div class="mini-brand-text">{BRAND_WORDMARK}</div>'
        f'<div class="footer-tagline">{BRAND_TAGLINE}</div></div></div>'
        f'<div class="footer-links">{chip("Integrated routing")}{chip("Transparent telemetry")}</div></div>',
        unsafe_allow_html=True,
    )
