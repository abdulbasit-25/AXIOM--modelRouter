"""Reusable, backend-independent UI components."""

from collections.abc import Sequence
from html import escape

import streamlit as st

PLACEHOLDER_STAGES: tuple[tuple[str, str], ...] = (
    ("Question", "Your prompt enters the workflow"),
    ("Router", "Matches the task to a capable model"),
    ("Model", "Generates the response"),
    ("Answer", "Returned to the learner"),
)


def page_header(eyebrow: str, title: str, description: str) -> None:
    """Render the eyebrow, page title and intro paragraph."""
    st.markdown(f'<div class="eyebrow">{escape(eyebrow)}</div>', unsafe_allow_html=True)
    st.title(title)
    st.markdown(f'<p class="page-intro">{escape(description)}</p>', unsafe_allow_html=True)


def section_heading(title: str, description: str | None = None) -> None:
    """Render a section title with an optional supporting sentence."""
    st.markdown(f'<h3 class="section-heading">{escape(title)}</h3>', unsafe_allow_html=True)
    if description:
        st.caption(description)


def brand_lockup() -> None:
    """Sidebar brand block."""
    st.markdown(
        '<div class="brand-shell"><div class="brand-mark">E</div><div>'
        '<div class="brand-name">EduRoute</div>'
        '<div class="brand-tagline">Learning, thoughtfully routed.</div>'
        "</div></div>",
        unsafe_allow_html=True,
    )


def mobile_brand() -> None:
    """Compact brand shown in the mobile top bar."""
    st.markdown(
        '<div class="mobile-brand"><div class="mini-brand-mark">E</div>EduRoute</div>',
        unsafe_allow_html=True,
    )


def chip(label: str) -> str:
    """Return markup for a small pill label (caller renders it)."""
    return f'<span class="chip">{escape(label)}</span>'


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
    """Render a titled content section with optional steps or a placeholder row."""
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


def page_footer() -> None:
    st.markdown(
        '<div class="page-footer"><div class="footer-brand"><div class="mini-brand-mark">E</div>'
        '<div><div class="mini-brand-text">EduRoute</div>'
        '<div class="footer-tagline">Learning, thoughtfully routed.</div></div></div>'
        f'<div class="footer-links">{chip("Integrated routing")}{chip("Transparent telemetry")}</div></div>',
        unsafe_allow_html=True,
    )


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


def status_indicator(label: str) -> None:
    """Render a restrained status badge."""
    st.markdown(
        (
            '<span class="status-pill"><span class="status-dot"></span>'
            f"{escape(label)}</span>"
        ),
        unsafe_allow_html=True,
    )


def routing_path_display(stages: Sequence[str]) -> None:
    """Render route stages as a vertical timeline.

    With no stages, a dimmed preview of the planned flow is shown so the
    panel explains itself without implying a live route.
    """
    live = bool(stages)
    items = [(stage, "") for stage in stages] if live else list(PLACEHOLDER_STAGES)

    markup = '<div class="route" role="list">'
    for index, (title, hint) in enumerate(items, start=1):
        hint_markup = f'<div class="route-hint">{escape(hint)}</div>' if hint else ""
        markup += (
            f'<div class="route-step{" is-live" if live else ""}" role="listitem">'
            f'<div class="route-node">{index}</div>'
            f'<div><div class="route-title">{escape(title)}</div>{hint_markup}</div>'
            "</div>"
        )
    markup += "</div>"
    if not live:
        markup += '<div class="route-note">Preview only. The real path appears once routing is connected.</div>'
    st.markdown(markup, unsafe_allow_html=True)