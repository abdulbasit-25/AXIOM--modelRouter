"""Page and section headings."""

from html import escape

import streamlit as st


def page_header(eyebrow: str, title: str, description: str) -> None:
    """Render the eyebrow, page title, and introduction."""
    st.markdown(f'<div class="eyebrow">{escape(eyebrow)}</div>', unsafe_allow_html=True)
    st.title(title)
    st.markdown(f'<p class="page-intro">{escape(description)}</p>', unsafe_allow_html=True)


def section_heading(title: str, description: str | None = None) -> None:
    """Render a section title with optional supporting text."""
    st.markdown(f'<h3 class="section-heading">{escape(title)}</h3>', unsafe_allow_html=True)
    if description:
        st.caption(description)
