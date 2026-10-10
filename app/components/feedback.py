"""Small labels and empty-state feedback components."""

from html import escape

import streamlit as st


def chip(label: str) -> str:
    """Return markup for a small pill label (caller renders it)."""
    return f'<span class="chip">{escape(label)}</span>'


def empty_state(title: str, message: str, icon: str = "◌") -> None:
    """Render a calm placeholder for panels that have no data yet."""
    st.markdown(
        (
            '<div class="empty-state">'
            f'<div class="empty-icon" aria-hidden="true">{escape(icon)}</div>'
            f'<div class="empty-title">{escape(title)}</div>'
            f'<div class="result-placeholder">{escape(message)}</div>'
            "</div>"
        ),
        unsafe_allow_html=True,
    )
