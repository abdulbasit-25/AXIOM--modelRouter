"""Streamlit entry point for the integrated EduRoute tutoring app."""

from collections.abc import Callable
import logging
from pathlib import Path
import sys

import streamlit as st

if __package__ in (None, ""):
    project_root = Path(__file__).resolve().parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    from app.components import (
        brand_lockup,
        chip,
        empty_state,
        feature_card,
        info_section,
        metric_card,
        mobile_brand,
        page_footer,
        page_header,
        plan_card,
        routing_path_display,
        section_heading,
        status_indicator,
        steps_markup,
    )
    from app.styles import APP_CSS
else:
    from app.components import (
        brand_lockup,
        chip,
        empty_state,
        feature_card,
        info_section,
        metric_card,
        mobile_brand,
        page_footer,
        page_header,
        plan_card,
        routing_path_display,
        section_heading,
        status_indicator,
        steps_markup,
    )
    from app.styles import APP_CSS

from engine import ProductionRouter

SCENARIOS = {
    "Vocabulary Flashcard": "Explain the meaning of a vocabulary word and give one example sentence.",
    "Curriculum Synthesis": "Summarize the key ideas in a topic for a secondary-school student.",
    "STEM Reasoning": "Explain how to approach a multi-step science or mathematics problem.",
    "Fallback Demonstration": "Show how a learning assistant could respond when its preferred route is unavailable.",
}

SCENARIO_DESCRIPTIONS = {
    "Vocabulary Flashcard": "Build quick, memorable language understanding.",
    "Curriculum Synthesis": "Turn broad topics into student-friendly summaries.",
    "STEM Reasoning": "Work through analytical problem solving step by step.",
    "Fallback Demonstration": "Show a graceful response when the main route is unavailable.",
}

NAVIGATION = (
    "Welcome",
    "Production AI Tutor",
    "Calibration Studio",
    "SDG Analytics",
    "About",
)

NAV_ICONS = {
    "Welcome": "⌂",
    "Production AI Tutor": "✎",
    "Calibration Studio": "◎",
    "SDG Analytics": "◔",
    "About": "ⓘ",
}

GETTING_STARTED = (
    ("Open Production AI Tutor.", "This is the primary workspace for the integrated tutoring workflow."),
    ("Select an educational scenario.", "Choose from Vocabulary Flashcard, Curriculum Synthesis, STEM Reasoning, or Fallback Demonstration."),
    ("Review or edit the suggested question.", "The prompt reflects a sample learning task that can be refined before running the demonstration."),
    ("Run the question.", "The routing engine selects a model, checks the response, and reports the route and estimated cost."),
)

MAX_QUESTION_CHARS = 600
logger = logging.getLogger(__name__)


def _get_router() -> ProductionRouter:
    """Keep router and telemetry state for the lifetime of the Streamlit session."""
    router = st.session_state.get("production_router")
    if router is None:
        router = ProductionRouter()
        st.session_state["production_router"] = router
    return router


def _nav_label(name: str) -> str:
    return f"{NAV_ICONS[name]}  {name}"


def _set_destination(destination: str) -> None:
    """Queue a page change and rerun the whole app (also closes the mobile menu)."""
    st.session_state["pending_destination"] = destination
    st.rerun()


@st.dialog("Menu")
def _mobile_menu() -> None:
    current = st.session_state.get("active_destination", NAVIGATION[0])
    for name in NAVIGATION:
        if st.button(
            _nav_label(name),
            key=f"mobile_nav_{name}",
            type="primary" if name == current else "secondary",
            use_container_width=True,
        ):
            _set_destination(name)
    st.caption("The tutor is connected to the routing engine.")


def _render_mobile_bar() -> None:
    """Sticky top bar with a hamburger; CSS shows it only on small screens."""
    with st.container(key="mobile_nav"):
        mobile_brand()
        if st.button("Menu", key="open_menu", icon=":material/menu:"):
            _mobile_menu()


def _render_sidebar() -> str:
    if "pending_destination" in st.session_state:
        st.session_state["active_destination"] = st.session_state.pop("pending_destination")

    if "active_destination" not in st.session_state:
        st.session_state["active_destination"] = NAVIGATION[0]

    with st.sidebar:
        brand_lockup()
        st.markdown('<div class="sidebar-section-label">Workspace</div>', unsafe_allow_html=True)
        destination = st.radio(
            "Workspace",
            NAVIGATION,
            format_func=_nav_label,
            label_visibility="collapsed",
            key="active_destination",
        )
        st.divider()
        st.markdown('<div class="sidebar-meta">Application status</div>', unsafe_allow_html=True)
        status_indicator("Tutor and router ready")
        st.caption("Tutor questions are routed by the integrated model engine.")
    return destination


def _render_welcome_page() -> None:
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
            if st.button("Open Production AI Tutor", type="primary", use_container_width=True, key="cta_tutor"):
                _set_destination("Production AI Tutor")
        with cta_right:
            if st.button("About EduRoute", use_container_width=True, key="cta_about"):
                _set_destination("About")

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

    section_heading("Feature overview", "The tutor workflow is connected; calibration and impact reporting remain planned.")
    features = (
        ("Production AI Tutor", "Route educational questions, review model responses, and inspect fallback and cost metrics."),
        ("Calibration Studio", "A planned workspace for calibration and evaluation workflows that will guide routing decisions in future iterations."),
        ("SDG Analytics", "A planned reporting workspace focused on SDG 4 and SDG 8, designed to surface impact insights when data becomes available."),
    )
    with st.container(key="features"):
        for column, (heading, body) in zip(st.columns(3, gap="medium"), features):
            with column:
                feature_card(heading, body)
                if st.button(f"Open {heading}", key=f"feature_{heading}", use_container_width=True):
                    _set_destination(heading)

    section_heading("Getting started", "These steps help a first-time user understand the current prototype flow.")
    st.markdown(f'<div class="overview-panel">{steps_markup(GETTING_STARTED)}</div>', unsafe_allow_html=True)

    page_footer()


def _render_scenario_picker() -> None:
    scenario_names = tuple(SCENARIOS)
    if "scenario" not in st.session_state:
        st.session_state["scenario"] = scenario_names[0]
    if "question_input" not in st.session_state:
        st.session_state["question_input"] = SCENARIOS[st.session_state["scenario"]]

    with st.container(key="scenario_grid"):
        columns = st.columns(2, gap="medium")
        for index, scenario_name in enumerate(scenario_names):
            with columns[index % 2]:
                selected = st.session_state["scenario"] == scenario_name
                title = f"✓ {scenario_name}" if selected else scenario_name
                if st.button(
                    f"**{title}**  \n{SCENARIO_DESCRIPTIONS[scenario_name]}",
                    key=f"scenario_{index}",
                    type="primary" if selected else "secondary",
                    use_container_width=True,
                ):
                    st.session_state["scenario"] = scenario_name
                    st.session_state["question_input"] = SCENARIOS[scenario_name]
                    st.rerun()


def _render_tutor() -> None:
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
                    result = _get_router().route_and_execute(
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


def _render_pending_destination(
    eyebrow: str,
    title: str,
    description: str,
    planned_sections: tuple[tuple[str, str], ...],
) -> None:
    page_header(eyebrow, title, description)
    st.markdown(
        """
        <div class="planning-banner">
            <div class="planning-pill">Planned</div>
            <span>Backend integration is pending. This workspace is intentionally designed for future live reporting.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cards = st.columns(2, gap="medium")
    for index, (heading, explanation) in enumerate(planned_sections):
        with cards[index % 2]:
            plan_card(heading, explanation)


def _render_calibration_studio() -> None:
    _render_pending_destination(
        "Calibration Studio",
        "Prepare routing calibration.",
        "Review how educational tasks should be matched to model capability and response quality before any deployment decisions are made.",
        (
            (
                "Calibration workflow",
                "Future tools will support comparing task difficulty, response quality, and routing decisions with transparent controls and review states.",
            ),
            (
                "Evaluation data",
                "Dataset connections, calibration notes, and benchmark snapshots will appear here when available, without implying measured outcomes.",
            ),
        ),
    )


def _render_sdg_analytics() -> None:
    _render_pending_destination(
        "SDG Analytics",
        "Measure impact when data is ready.",
        "A planned reporting workspace for SDG 4 and SDG 8 indicators, explaining how impact insights will be surfaced when the data pipeline exists.",
        (
            (
                "Quality education · SDG 4",
                "Future reporting may summarize access, learning-quality, and educational-support indicators in a transparent, explainable way.",
            ),
            (
                "Decent work · SDG 8",
                "Future dashboards may compare efficiency and affordability signals once live operational data is connected.",
            ),
        ),
    )


def _render_about_page() -> None:
    page_header(
        "About",
        "About EduRoute",
        "EduRoute is an educational tutoring app integrated with a model-classification, routing, verification, and telemetry backend.",
    )

    info_section(
        "About the Project",
        "EduRoute helps students ask learning questions and routes them through a structured workflow. The Production AI Tutor integrates classification, model selection, response verification, fallback escalation, and per-request telemetry. Calibration Studio and SDG Analytics remain planned workspaces.",
    )
    info_section("About the Team", placeholder="Team information will be added here.")
    info_section(
        "How to Use EduRoute",
        steps=(
            ("Open Production AI Tutor.", "This is the primary educational question workspace."),
            ("Choose a scenario.", "Use Vocabulary Flashcard, Curriculum Synthesis, STEM Reasoning, or Fallback Demonstration. Selecting a scenario loads the matching sample prompt."),
            ("Review and edit the question.", "Users can adapt the suggested prompt before running the demonstration."),
            ("Run the tutor.", "The router returns a live Groq answer when configured, or a clearly labelled local mock response otherwise."),
        ),
    )


def main() -> None:
    st.set_page_config(
        page_title="EduRoute | Learning, thoughtfully routed",
        page_icon="E",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(APP_CSS, unsafe_allow_html=True)
    destination = _render_sidebar()
    _render_mobile_bar()

    renderers: dict[str, Callable[[], None]] = {
        "Welcome": _render_welcome_page,
        "Production AI Tutor": _render_tutor,
        "Calibration Studio": _render_calibration_studio,
        "SDG Analytics": _render_sdg_analytics,
        "About": _render_about_page,
    }
    renderers[destination]()

    st.divider()
    st.caption("EduRoute · SDG 4 Quality Education · SDG 8 Decent Work and Economic Growth")


if __name__ == "__main__":
    main()