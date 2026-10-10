"""Streamlit entry point for the integrated EduRoute tutoring app."""

from collections.abc import Callable
from datetime import datetime, timezone
import csv
from io import StringIO
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
            width="stretch",
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
            if st.button("Open Production AI Tutor", type="primary", width="stretch", key="cta_tutor"):
                _set_destination("Production AI Tutor")
        with cta_right:
            if st.button("About EduRoute", width="stretch", key="cta_about"):
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
                    width="stretch",
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


def _render_calibration_studio() -> None:
    page_header(
        "Calibration Studio",
        "Check whether questions take the expected route.",
        "Submit an evaluation prompt to the live router, compare its selected complexity tier with your expected tier, and inspect the resulting route and cost.",
    )
    st.info(
        "Each evaluation makes a real router request and is included in session analytics. "
        "Without GROQ_API_KEY, the router uses its clearly labeled local mock response."
    )

    with st.form("calibration_form"):
        prompt = st.text_area(
            "Evaluation question",
            value="Explain the difference between mitosis and meiosis, including their outcomes.",
            max_chars=MAX_QUESTION_CHARS,
            key="calibration_prompt",
        )
        expected_tier = st.selectbox(
            "Expected complexity tier",
            options=(1, 2, 3),
            format_func=lambda tier: {
                1: "Tier 1 · Factual recall",
                2: "Tier 2 · Conceptual explanation",
                3: "Tier 3 · Multi-step reasoning",
            }[tier],
            key="calibration_expected_tier",
        )
        submitted = st.form_submit_button(
            "Evaluate route",
            type="primary",
            key="run_calibration",
        )

    if submitted:
        if not prompt.strip():
            st.warning("Enter an evaluation question before running calibration.")
        else:
            try:
                with st.spinner("Running the evaluation through the router..."):
                    result = _get_router().route_and_execute(prompt.strip())
                record = {
                    "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "expected_tier": expected_tier,
                    "actual_tier": result["tier"],
                    "tier_match": expected_tier == result["tier"],
                    "initial_model": result["initial_model"],
                    "final_model": result["final_model"],
                    "fallback_triggered": result["fallback_triggered"],
                    "mock_fallback": result["mock_fallback"],
                    "latency_ms": result["latency_ms"],
                    "actual_cost": result["impact_metrics"]["actual_cost"],
                }
                st.session_state.setdefault("calibration_results", []).append(record)
                st.session_state["latest_calibration"] = record
                st.session_state.pop("calibration_error", None)
            except Exception:
                logger.exception("Calibration evaluation failed")
                st.session_state["calibration_error"] = (
                    "The evaluation could not be completed. Check the application logs."
                )

    if error_message := st.session_state.get("calibration_error"):
        st.error(error_message)

    latest = st.session_state.get("latest_calibration")
    if latest:
        if latest["tier_match"]:
            st.success(f"Tier agreement: expected and selected Tier {latest['actual_tier']}.")
        else:
            st.warning(
                f"Tier mismatch: expected Tier {latest['expected_tier']}, "
                f"router selected Tier {latest['actual_tier']}."
            )
        st.write(
            f"Route: {latest['initial_model']} → {latest['final_model']} · "
            f"{'escalated' if latest['fallback_triggered'] else 'no escalation'} · "
            f"{'simulated' if latest['mock_fallback'] else 'live'}"
        )

    calibration_results = st.session_state.get("calibration_results", [])
    if calibration_results:
        section_heading("Evaluation history", "Tier agreement reflects the expected tier you supplied; it is not a response-quality score.")
        st.dataframe(calibration_results, width="stretch", hide_index=True)
        matches = sum(item["tier_match"] for item in calibration_results)
        st.caption(f"{matches} of {len(calibration_results)} evaluations matched the expected tier.")
    else:
        empty_state(
            "No evaluations yet",
            "Run an evaluation above to see the router's selected tier and route details.",
            "◎",
        )


def _render_sdg_analytics() -> None:
    page_header(
        "SDG Analytics",
        "See what the router is doing in this session.",
        "Live operational metrics from completed tutor and calibration requests, including query volume, latency, model usage, and estimated cost.",
    )
    telemetry = _get_router().telemetry
    rows = telemetry.query_history
    summary = telemetry.get_session_summary()
    latencies = [row["latency_ms"] for row in rows if "latency_ms" in row]
    average_latency = sum(latencies) / len(latencies) if latencies else 0.0
    fallback_count = sum(bool(row.get("fallback_triggered")) for row in rows)

    st.caption(
        "Session-scoped operational proxies only. Query counts do not measure learning outcomes "
        "or access; savings compare estimated token cost with the configured frontier-model proxy."
    )
    metrics = (
        ("Routed questions", str(summary["total_queries"]), "Current Streamlit session"),
        ("Average latency", f"{average_latency:.0f} ms" if latencies else "—", "Recorded model-call latency"),
        ("Estimated spend", f"${summary['cumulative_spend']:.6f}", "Based on configured token pricing"),
        ("Estimated savings", f"${summary['cumulative_dollars_saved']:.6f}", "Versus configured baseline proxy"),
    )
    for column, (label, value, note) in zip(st.columns(4, gap="medium"), metrics):
        with column:
            metric_card(label, value, note)

    if not rows:
        empty_state(
            "No session data yet",
            "Run a tutor question or calibration evaluation to populate live analytics.",
            "◔",
        )
        return

    chart_column, breakdown_column = st.columns(2, gap="medium")
    with chart_column:
        section_heading("Model usage", "Counts include each model call; escalated requests count both models.")
        model_counts: dict[str, int] = {}
        for row in rows:
            for model in row.get("models", []):
                model_counts[model] = model_counts.get(model, 0) + 1
        st.bar_chart(model_counts)
    with breakdown_column:
        section_heading("Routing and efficiency")
        st.metric("Fallback rate", f"{fallback_count / len(rows) * 100:.1f}%")
        st.metric("Estimated savings vs baseline", f"{summary['overall_savings_pct']:.1f}%")
        st.metric("Input / output tokens", f"{summary['total_input_tokens']:,} / {summary['total_output_tokens']:,}")

    section_heading("Request history", "Detailed estimates are local to this active Streamlit session.")
    display_rows = [
        {
            "Timestamp (UTC)": row.get("timestamp", ""),
            "Tier": row.get("tier", ""),
            "Route": " -> ".join(row.get("models", [])),
            "Latency (ms)": row.get("latency_ms", ""),
            "Escalated": row.get("fallback_triggered", False),
            "Simulated": row.get("mock_fallback", False),
            "Input tokens": row["in_tokens"],
            "Output tokens": row["out_tokens"],
            "Estimated cost (USD)": row["actual_cost"],
            "Baseline proxy (USD)": row["baseline_cost"],
            "Estimated savings (USD)": row["dollars_saved"],
        }
        for row in reversed(rows)
    ]
    st.dataframe(display_rows, width="stretch", hide_index=True)

    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=list(display_rows[0]))
    writer.writeheader()
    writer.writerows(display_rows)
    st.download_button(
        "Download session report (CSV)",
        data=output.getvalue(),
        file_name="eduroute-session-report.csv",
        mime="text/csv",
    )


def _render_about_page() -> None:
    page_header(
        "About",
        "About EduRoute",
        "EduRoute is an educational tutoring app integrated with a model-classification, routing, verification, and telemetry backend.",
    )

    info_section(
        "About the Project",
        "EduRoute helps students ask learning questions and routes them through a structured workflow. The Production AI Tutor integrates classification, model selection, response verification, fallback escalation, and per-request telemetry. Calibration Studio compares router tiers with user-provided expectations, and SDG Analytics summarizes session-level operational proxies.",
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