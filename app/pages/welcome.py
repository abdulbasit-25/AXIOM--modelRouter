"""Welcome page."""

import streamlit as st

from app.components import feature_card, page_footer, page_header, section_heading, steps_markup
from app.config import GETTING_STARTED
from app.navigation.router import set_destination


def render() -> None:
    page_header(
        "Welcome",
        "A more thoughtful way to learn.",
        "EduRoute routes learning questions through a structured tutoring workflow, with transparent model selection and response checks.",
    )

    hero_left, hero_right = st.columns([1.45, 1.05], gap="medium")
    with hero_left:
        st.markdown(
            """
            <div class="hero-copy">
                <div class="mini-brand">
                    <div class="mini-brand-mark">E</div>
                    <div class="mini-brand-text">EduRoute</div>
                </div>
                <div class="hero-text">A calm, structured way to get educational AI assistance.</div>
                <p>Ask a learning question and see it classified, routed to an appropriate model, checked, and returned with transparent session metrics.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        cta_left, cta_right = st.columns(2, gap="small")
        with cta_left:
            if st.button(
                "Open Production AI Tutor",
                type="primary",
                width="stretch",
                key="cta_tutor",
            ):
                set_destination("Production AI Tutor")
        with cta_right:
            if st.button("About EduRoute", width="stretch", key="cta_about"):
                set_destination("About")

    with hero_right:
        st.markdown(
            """
            <div class="welcome-visual" aria-hidden="true">
                <div class="visual-window">
                    <div class="visual-badge">EduRoute</div>
                    <div class="visual-grid">
                        <div class="visual-card primary">Vocabulary</div>
                        <div class="visual-card">Curriculum</div>
                        <div class="visual-card">STEM</div>
                        <div class="visual-card muted">Feedback</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    section_heading(
        "Project overview",
        "EduRoute connects an educational tutoring interface to the model-routing engine, response verifier, and cost telemetry.",
    )
    st.markdown(
        """
        <div class="overview-panel">
            <p>The tutor uses the integrated routing engine to classify questions, select a model, verify the response, and escalate when needed. If Groq is not configured or available, the app clearly labels its local mock response.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    section_heading("Feature overview", "Explore the tutor, evaluate routing behavior, and review live session telemetry.")
    features = (
        ("Production AI Tutor", "Route educational questions, review model responses, and inspect fallback and cost metrics."),
        ("Calibration Studio", "Run editable examples through the router and compare its selected tier with your expected tier."),
        ("SDG Analytics", "Review session-level education-support activity and cost-efficiency proxies from routed questions."),
    )
    with st.container(key="features"):
        for column, (heading, body) in zip(st.columns(3, gap="medium"), features):
            with column:
                feature_card(heading, body)
                if st.button(f"Open {heading}", key=f"feature_{heading}", width="stretch"):
                    set_destination(heading)

    section_heading("Getting started", "These steps help a first-time user understand the current prototype flow.")
    st.markdown(f'<div class="overview-panel">{steps_markup(GETTING_STARTED)}</div>', unsafe_allow_html=True)
    page_footer()
