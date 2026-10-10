"""Route visualization."""

from collections.abc import Sequence
from html import escape

import streamlit as st

PLACEHOLDER_STAGES: tuple[tuple[str, str], ...] = (
    ("Question", "Your prompt enters the workflow"),
    ("Router", "Matches the task to a capable model"),
    ("Model", "Generates the response"),
    ("Answer", "Returned to the learner"),
)


def routing_path_display(stages: Sequence[str]) -> None:
    """Render route stages as a vertical timeline."""
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
