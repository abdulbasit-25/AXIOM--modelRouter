"""About page."""

import streamlit as st

from app.components import info_section, page_header, team_member_card
from app.config import BRAND_DESCRIPTION, BRAND_EXPANSION, BRAND_NAME, BRAND_TAGLINE


def render() -> None:
    page_header(
        "About",
        BRAND_NAME,
        BRAND_DESCRIPTION,
    )

    info_section(
        BRAND_EXPANSION,
        f"{BRAND_TAGLINE} Axiom classifies educational questions using deterministic keyword and prompt-length rules, routes them to a tiered model, verifies candidate responses with lightweight heuristics, escalates when checks fail, and records session-scoped token and estimated cost telemetry.",
    )
    info_section(
        "Meet the team",
        "The people building Axiom across its application, routing, and quality workflows.",
    )
    with st.container(key="team_grid"):
        columns = st.columns(3, gap="medium")
        team = (
            ("Muhammad Arslan Jaffer", "Backend", "MJ"),
            ("Abdul Basit", "Frontend", "AB"),
            ("Fatima Asim", "Classifier · Testing", "FA"),
        )
        for column, (name, role, initials) in zip(columns, team):
            with column:
                team_member_card(name, role, initials)

    info_section(
        "How to use Axiom",
        steps=(
            ("Classify the question.", "A deterministic rule-based classifier assigns a complexity tier."),
            ("Select a model.", "The router maps the tier to a configured Groq model."),
            ("Generate a response.", "A live Groq response is used when available; otherwise a labeled local mock response is returned."),
            ("Verify and escalate.", "Lightweight heuristic checks may trigger a second model call when the initial candidate fails."),
            ("Review session telemetry.", "The app records request and token data and calculates estimates against a configured baseline proxy."),
        ),
    )
