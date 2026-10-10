"""Metric cards and status indicators."""

from html import escape

import streamlit as st


def metric_card(label: str, value: str, note: str = "") -> None:
    """Render a compact dashboard metric card."""
    note_markup = f'<div class="metric-note">{escape(note)}</div>' if note else ""
    st.markdown(
        (
            '<div class="metric-card">'
            f'<div class="metric-label">{escape(label)}</div>'
            f'<div class="metric-value">{escape(value)}</div>'
            f"{note_markup}"
            "</div>"
        ),
        unsafe_allow_html=True,
    )


def status_indicator(label: str) -> None:
    """Render a restrained status badge."""
    st.markdown(
        (
            '<span class="status-pill"><span class="status-dot"></span>'
            f"{escape(label)}</span>"
        ),
        unsafe_allow_html=True,
    )
