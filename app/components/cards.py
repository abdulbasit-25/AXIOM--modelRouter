"""Feature and information cards."""

from collections.abc import Sequence
from html import escape

import streamlit as st


def feature_card(title: str, body: str) -> None:
    """Render a feature card; the icon is the title's first letter."""
    st.markdown(
        (
            '<div class="feature-card">'
            f'<div class="feature-icon" aria-hidden="true">{escape(title[0])}</div>'
            f'<div class="feature-title">{escape(title)}</div>'
            f"<p>{escape(body)}</p>"
            "</div>"
        ),
        unsafe_allow_html=True,
    )


def steps_markup(steps: Sequence[tuple[str, str]]) -> str:
    items = "".join(
        f"<li><strong>{escape(title)}</strong> {escape(text)}</li>" for title, text in steps
    )
    return f'<ol class="step-list">{items}</ol>'


def info_section(
    kicker: str,
    body: str = "",
    steps: Sequence[tuple[str, str]] = (),
    placeholder: str | None = None,
) -> None:
    """Render a titled information section."""
    parts = [f'<div class="about-kicker">{escape(kicker)}</div>']
    if body:
        parts.append(f"<p>{escape(body)}</p>")
    if steps:
        parts.append(steps_markup(steps))
    if placeholder:
        parts.append(
            '<div class="team-placeholder"><div class="team-mark" aria-hidden="true">T</div>'
            f'<div class="team-copy">{escape(placeholder)}</div></div>'
        )
    st.markdown(f'<div class="about-section">{"".join(parts)}</div>', unsafe_allow_html=True)
