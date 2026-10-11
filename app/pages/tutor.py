"""Production AI Tutor page."""

import logging

import streamlit as st

from app.config import MAX_QUESTION_CHARS, SCENARIOS, SCENARIO_DESCRIPTIONS
from app.services.router_service import get_router
from app.pages import page_base as ui

logger = logging.getLogger(__name__)

_TUTOR_CSS = """
<style>
.st-key-scenario_grid button { height: auto; min-height: 96px; padding: 1.1rem 1.3rem; border-radius: 18px; justify-content: flex-start; text-align: left; }
.st-key-scenario_grid button > div { justify-content: flex-start; text-align: left; width: 100%; }
.st-key-scenario_grid button p { text-align: left; line-height: 1.6; font-size: .86rem; letter-spacing: .02em; color: var(--sage); }
.st-key-scenario_grid button p strong { display: block; margin-bottom: .2rem; font-size: 1.05rem; font-weight: 400; letter-spacing: .06em; color: var(--mist); }
.st-key-scenario_grid button[kind="secondary"] { background: rgba(70,86,93,.28); border-color: rgba(212,215,211,.22); }
.st-key-scenario_grid button[kind="secondary"]:hover { background: var(--forest-hover); border-color: rgba(212,215,211,.6); }
.st-key-scenario_grid button[kind="secondary"]:hover p, .st-key-scenario_grid button[kind="secondary"]:hover p strong { color: var(--mist); }
.st-key-scenario_grid button[kind="primary"] { background: linear-gradient(135deg, #405653, #344B45); border: 1px solid var(--mist); box-shadow: 0 0 0 1px rgba(212,215,211,.25), 0 14px 34px rgba(0,0,0,.28); color: var(--mist); }
.st-key-scenario_grid button[kind="primary"] p { color: var(--mist); }
.st-key-scenario_grid button[kind="primary"] p strong { color: var(--mist-hover); }
.st-key-scenario_grid button[kind="primary"]:hover { background: linear-gradient(135deg, #4a625f, #3b544e); color: var(--mist); }
.st-key-scenario_grid button[kind="primary"]:active { background: var(--slate-hover); color: var(--mist); }
.st-key-composer_actions { margin-top: .4rem; }
.st-key-question_section .px-label { color: #344B45 !important; }
.st-key-question_section .px-label em { color: #263A36 !important; }
.st-key-question_section .px-sub { color: #4C5B61 !important; }
.st-key-question_composer [data-testid="stVerticalBlockBorderWrapper"] {
    border-color: rgba(44,66,63,.35) !important;
    background: #FFFFFF !important;
}
.st-key-question_composer [data-baseweb="textarea"] {
    background: #FFFFFF !important;
    border: 1px solid #899B9A !important;
}
.st-key-question_composer [data-testid="stTextArea"] textarea {
    background: #FFFFFF !important;
    color: #263A36 !important;
    -webkit-text-fill-color: #263A36 !important;
    caret-color: #263A36 !important;
}
.st-key-question_composer [data-testid="stTextArea"] textarea::placeholder {
    color: #566970 !important;
    -webkit-text-fill-color: #566970 !important;
    opacity: 1 !important;
}
.st-key-question_composer [data-testid="stTextArea"] [data-testid="stWidgetLabel"] p {
    color: #344B45 !important;
}
.st-key-question_composer .stButton > button[kind="primary"] {
    background: #263A36 !important;
    border-color: #263A36 !important;
    color: #FFFFFF !important;
}
.st-key-question_composer .stButton > button[kind="primary"] p,
.st-key-question_composer .stButton > button[kind="primary"] span {
    color: #FFFFFF !important;
}
.st-key-question_composer .stButton > button[kind="primary"]:hover {
    background: #405653 !important;
    border-color: #405653 !important;
}
.st-key-question_composer .stButton > button[kind="primary"]:active {
    background: #4C5B61 !important;
    border-color: #4C5B61 !important;
}
.st-key-question_composer .stButton > button[kind="primary"]:disabled {
    background: #D4D7D3 !important;
    border-color: #899B9A !important;
    color: #263A36 !important;
    opacity: 1 !important;
}
.composer-meta { text-align: right; }
.px-answer-empty { opacity: .9; }
[data-testid="stVerticalBlockBorderWrapper"] .stMarkdown p, [data-testid="stVerticalBlockBorderWrapper"] .stMarkdown li { color: var(--mist); line-height: 1.8; }
</style>
"""


def _render_scenario_picker() -> None:
    with st.container(key="scenario_grid"):
        columns = st.columns(2, gap="medium")
        for index, (scenario_name, prompt) in enumerate(SCENARIOS.items()):
            with columns[index % 2]:
                selected = st.session_state["scenario"] == scenario_name
                if st.button(
                    f"**{scenario_name}**  \n{SCENARIO_DESCRIPTIONS[scenario_name]}",
                    key=f"scenario_{index}",
                    type="primary" if selected else "secondary",
                    width="stretch",
                ):
                    st.session_state["scenario"] = scenario_name
                    st.session_state["question_input"] = prompt
                    st.rerun()


def render() -> None:
    ui.inject()
    st.markdown(ui.html(_TUTOR_CSS), unsafe_allow_html=True)

    ui.hero(
        "Production tutor",
        "Production AI Tutor",
        "A clearer route to learning.",
        note=(
            "Choose a scenario, refine the prompt, and send it through the connected "
            "classification, model, verification, and telemetry workflow."
        ),
    )

    st.write("")
    intro_left, intro_right = st.columns([1.9, 1.1], gap="medium")
    with intro_left:
        st.markdown(
            ui.info_card(
                "Tutor workflow",
                "Questions are classified, routed to a model, checked for basic quality, "
                "and escalated when verification fails.",
            ),
            unsafe_allow_html=True,
        )
    with intro_right:
        st.markdown(
            ui.info_card(
                "Model provider",
                "Live Groq responses are used when configured; otherwise the app clearly "
                "labels simulated responses.",
            ),
            unsafe_allow_html=True,
        )

    ui.label("Choose a scenario", "Select the teaching pattern that best matches the learning goal.", index="01")
    _render_scenario_picker()

    with st.container(key="question_section"):
        ui.label("Shape the question", "Adapt the sample prompt before sending it through the tutor.", index="02")
        with st.container(border=True, key="question_composer"):
            question = st.text_area(
                "Educational question",
                key="question_input",
                height=140,
                max_chars=MAX_QUESTION_CHARS,
                placeholder="Enter an educational question to route (e.g., Define photosynthesis, Explain mitosis vs meiosis, Prove by induction...)",
                label_visibility="collapsed",
            )
            with st.container(key="composer_actions"):
                action_col, meta_col = st.columns([1, 2], vertical_alignment="center")
                with action_col:
                    run_clicked = st.button("Run tutor", type="primary", key="run_tutor")
                with meta_col:
                    st.markdown(
                        f'<div class="composer-meta"><div class="px-pills" style="justify-content:flex-end">'
                        f'{ui.pill(st.session_state.get("scenario", ""))}</div></div>',
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

    ui.label(
        "Tutor results",
        "Review the answer, selected route, fallback decision, and estimated request cost.",
        index="03",
    )
    if error_message := st.session_state.get("tutor_error"):
        st.error(error_message)

    result = st.session_state.get("tutor_result")
    
    # Prominent Amber Fallback Warning Banner
    if result and result.get("fallback_triggered"):
        reason = result["impact_metrics"].get("fallback_reason", "Heuristic verification criteria failed")
        st.warning(
            f"⚠️ **Automated Fallback Triggered**: Speculative output from `{result['initial_model']}` "
            f"failed verification criteria ({reason}). Immediately escalated to Frontier Reasoning Model `{result['final_model']}`."
        )

    answer_column, route_column = st.columns([1.5, 1], gap="medium")
    with answer_column:
        with st.container(border=True):
            st.markdown('<div class="px-panel-head">Answer</div>', unsafe_allow_html=True)
            if result:
                # Routing Badge
                tier_badge_color = {1: "#899B9A", 2: "#A3ADA5", 3: "#D4D7D3"}.get(result["tier"], "#D4D7D3")
                escalated_badge = (
                    '<span style="margin-left: 0.5rem; background: rgba(220,130,20,0.25); '
                    'border: 1px solid #E08820; color: #F5A540; padding: 0.35rem 0.85rem; '
                    'border-radius: 999px; font-size: 0.74rem; font-weight: 600; '
                    'letter-spacing: 0.12em;">⚠️ Escalated</span>'
                    if result["fallback_triggered"]
                    else ""
                )
                badge_html = (
                    f'<div style="margin-bottom: 1rem;">'
                    f'<span style="background: rgba(38,58,54,0.9); border: 1px solid {tier_badge_color}; '
                    f'color: {tier_badge_color}; padding: 0.35rem 0.85rem; border-radius: 999px; '
                    f'font-size: 0.76rem; font-weight: 600; letter-spacing: 0.15em; text-transform: uppercase;">'
                    f'Tier {result["tier"]} Route · {result["final_model"]}</span>'
                    f'{escalated_badge}'
                    f'</div>'
                )
                st.markdown(badge_html, unsafe_allow_html=True)
                st.markdown(result["response_text"])
                if result["mock_fallback"]:
                    st.info(
                        "Simulated response: configure GROQ_API_KEY in .env to enable live Groq model execution."
                    )
            else:
                st.markdown(
                    ui.empty("No answer yet", "Run a tutor question above to see its response and routing telemetry."),
                    unsafe_allow_html=True,
                )
    with route_column:
        with st.container(border=True):
            st.markdown('<div class="px-panel-head">Routing path & Escalation</div>', unsafe_allow_html=True)
            if result:
                route_stages = [
                    "Question received",
                    f"Tier {result['tier']} Selection · {result['initial_model']}",
                    "Response heuristic verification",
                ]
                if result["fallback_triggered"]:
                    route_stages.append(f"Escalation · {result['final_model']}")
                route_stages.append("Verified answer returned")
                st.markdown(ui.path(route_stages), unsafe_allow_html=True)
                if result["fallback_triggered"]:
                    st.caption(
                        f"Escalation trigger: {result['impact_metrics'].get('fallback_reason', 'Verification heuristic failed')}"
                    )
            else:
                st.markdown(
                    ui.path(("Question received", "Complexity classification", "Target model inference", "Verification & Telemetry"), idle=True),
                    unsafe_allow_html=True,
                )

    if result:
        impact = result["impact_metrics"]
        multiplier_str = f"{impact.get('edtech_multiplier', 1.0):.1f}x students"
        metrics = (
            ("Model Latency", f"{result['latency_ms']:.0f} ms", "Wall-clock inference time"),
            ("Axiom Cost", f"${impact['actual_cost']:.6f}", f"{impact['savings_pct']:.1f}% below baseline"),
            ("Frontier Cost", f"${impact['baseline_cost']:.6f}", "GPT-4o proxy reference"),
            ("EdTech Multiplier", multiplier_str, "SDG 4/8 Access Multiplier"),
        )
    else:
        metrics = (
            ("Model Latency", "—", "Run a tutor question"),
            ("Axiom Cost", "—", "Run a tutor question"),
            ("Frontier Cost", "—", "Run a tutor question"),
            ("EdTech Multiplier", "—", "Run a tutor question"),
        )
    st.markdown(ui.tiles(metrics), unsafe_allow_html=True)