"""EduRoute branding components."""

import streamlit as st


def brand_lockup() -> None:
    """Render the sidebar brand block."""
    st.markdown(
        '<div class="brand-shell"><div class="brand-mark">E</div><div>'
        '<div class="brand-name">EduRoute</div>'
        '<div class="brand-tagline">Learning, thoughtfully routed.</div>'
        "</div></div>",
        unsafe_allow_html=True,
    )


def mobile_brand() -> None:
    """Render the compact mobile brand."""
    st.markdown(
        '<div class="mobile-brand"><div class="mini-brand-mark">E</div>EduRoute</div>',
        unsafe_allow_html=True,
    )
