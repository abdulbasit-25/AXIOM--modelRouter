"""Shared Axiom brand components."""

import streamlit as st

from app.config import (
    BRAND_LOGO_PATH,
    BRAND_MARK_PATH,
    BRAND_TAGLINE,
    BRAND_WORDMARK,
)


def brand_lockup() -> None:
    """Render the sidebar brand block."""
    st.image(
        BRAND_LOGO_PATH,
        width=128,
        alt=f"{BRAND_WORDMARK} — {BRAND_TAGLINE}",
    )


def mobile_brand() -> None:
    """Render the compact mobile brand."""
    st.image(BRAND_MARK_PATH, width=30, alt="")
    st.markdown(
        f'<span class="mobile-brand-name">{BRAND_WORDMARK}</span>',
        unsafe_allow_html=True,
    )
