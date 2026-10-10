"""Production AI Tutor page."""

import logging

import streamlit as st

from app.components import (
    chip,
    empty_state,
    metric_card,
    page_header,
    routing_path_display,
    section_heading,
)
from app.config import MAX_QUESTION_CHARS, SCENARIOS, SCENARIO_DESCRIPTIONS
from app.services.router_service import get_router

logger = logging.getLogger(__name__)


def _render_scenario_picker() -> None:
    with st.container(key="scenario_grid"):
        columns = st.columns(2, gap="medium")
        for index, (scenario_name, prompt) in enumerate(SCENARIOS.items()):
            with columns[index % 2]:
                selected = st.session_state["scenario"] == scenario_name
                title = f"✓ {scenario_name}" if selected else scenario_name
                if st.button(
                    f"**{title}**  \n{SCENARIO_DESCRIPTIONS[scenario_name]}",
                    key=f"scenario_{index}",
                    type="primary" if selected else "secondary",
                    width="stretch",
                ):
                    st.session_state["scenario"] = scenario_name
                    st.session_state["question_input"] = prompt
                    st.rerun()


def render() -> None:
    page_header(
        "Production AI Tutor",
        "A clearer route to learning.",
        "Choose a scenario, refine the prompt, and send it through the connected classification, model, verification, and telemetry workflow.",
    )

    intro_left, intro_right = st.columns([1.9, 1.1], gap="medium")
    with intro_left:
        st.markdown(
            """
            <div class="insight-card">
                <div class="insight-label">Tutor workflow</div>
                <p>Questions are classified, routed to a model, checked for basic quality, and escalated when verification fails.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with intro_right:
        st.markdown(
            """
            <div class="status-card">
                <div class="insight-label">Model provider</div>
                <p>Live Groq responses are used when configured; otherwise the app clearly labels simulated responses.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    section_heading("1 · Choose a scenario", "Select the teaching pattern that best matches the learning goal.")
    _render_scenario_picker()

    section_heading("2 · Shape the question", "Adapt the sample prompt before sending it through the tutor.")
    with st.container(border=True):
        question = st.text_area(
            "Educational question",
            key="question_input",
            height=140,
            max_chars=MAX_QUESTION_CHARS,
            placeholder="Enter a question you would like help understanding.",
            label_visibility="collapsed",
        )
        with st.container(key="composer_actions"):
            action_col, meta_col = st.columns([1, 2], vertical_alignment="center")
            with action_col:
                run_clicked = st.button("Run tutor", type="primary", key="run_tutor")
            with meta_col:
                st.markdown(
                    f'<div class="composer-meta">{chip(st.session_state.get("scenario", ""))}</div>',
                    unsafe_allow_html=True,
                )

    if run_clicked:
        if question.strip():
            try:
                with st.spinner("Routing your question and checking the response..."):
                    result = get_router().route_and_execute(
                        question.strip(),
                        force_fallback_demo=(
                            st.session_state.get("scenario") == "Fallback Demonstration"
                        ),
                    )
                st.session_state["tutor_result"] = result
                st.session_state.pop("tutor_error", None)
            except Exception:
                logger.exception("Tutor request failed")
                st.session_state["tutor_error"] = (
                    "The tutor could not complete this request. Check the application logs."
                )
        else:
            st.warning("Add a question first, or pick a scenario to start from a sample prompt.")

    section_heading("3 · Tutor results", "Review the answer, selected route, fallback decision, and estimated request cost.")
    if error_message := st.session_state.get("tutor_error"):
        st.error(error_message)

    result = st.session_state.get("tutor_result")
    answer_column, route_column = st.columns([1.5, 1], gap="medium")
    with answer_column:
        with st.container(border=True):
            st.markdown('<div class="panel-heading">Answer</div>', unsafe_allow_html=True)
            if result:
                st.markdown(result["response_text"])
                if result["mock_fallback"]:
                    st.info(
                        "Simulated response: configure GROQ_API_KEY to use the live Groq model service."
                    )
                elif result["fallback_triggered"]:
                    st.caption("The live model response was escalated after verification.")
            else:
                empty_state("No answer yet", "Run a tutor question to see its response.", "✎")
    with route_column:
        with st.container(border=True):
            st.markdown('<div class="panel-heading">Routing path</div>', unsafe_allow_html=True)
            if result:
                route_stages = [
                    "Question received",
                    f"Tier {result['tier']} · {result['initial_model']}",
                    "Response verification",
                ]
                if result["fallback_triggered"]:
                    route_stages.append(f"Escalated · {result['final_model']}")
                route_stages.append("Answer returned")
                routing_path_display(route_stages)
                if result["fallback_triggered"]:
                    st.caption(
                        f"Escalation reason: {result['impact_metrics'].get('fallback_reason', 'verification failed')}"
                    )
            else:
                routing_path_display(())

    st.write("")
    if result:
        impact = result["impact_metrics"]
        metrics = (
            ("Latency", f"{result['latency_ms']:.0f} ms", "End-to-end model latency"),
            ("Estimated cost", f"${impact['actual_cost']:.6f}", f"{impact['savings_pct']:.1f}% below baseline"),
            (
                "Fallback status",
                "Escalated" if result["fallback_triggered"] else "Direct",
                result["final_model"],
            ),
        )
    else:
        metrics = (
            ("Latency", "—", "Run a tutor question"),
            ("Estimated cost", "—", "Run a tutor question"),
            ("Fallback status", "—", "Not evaluated"),
        )
    for column, (label, value, note) in zip(st.columns(3, gap="medium"), metrics):
        with column:
            metric_card(label, value, note)
