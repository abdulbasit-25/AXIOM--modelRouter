"""Calibration Studio page."""

from datetime import datetime, timezone
from html import escape
import logging

import streamlit as st

from app.config import MAX_QUESTION_CHARS
from app.services.router_service import get_router
from app.pages import page_base as ui

logger = logging.getLogger(__name__)

_VERDICT_CSS = """
<style>
[data-testid="stForm"] [data-testid="stWidgetLabel"] p {
    color: #E5E7E3 !important;
}
[data-testid="stForm"] [data-testid="stTextArea"] textarea {
    background: #FFFFFF !important;
    color: #263A36 !important;
    -webkit-text-fill-color: #263A36 !important;
    caret-color: #263A36 !important;
}
[data-testid="stForm"] [data-testid="stTextArea"] textarea::placeholder {
    color: #566970 !important;
    -webkit-text-fill-color: #566970 !important;
    opacity: 1 !important;
}
[data-testid="stForm"] [data-baseweb="textarea"] {
    background: #FFFFFF !important;
    border-color: #899B9A !important;
}
[data-testid="stForm"] [data-testid="stSelectbox"] [data-baseweb="select"] > div {
    background: #FFFFFF !important;
    border-color: #899B9A !important;
}
[data-testid="stForm"] [data-testid="stSelectbox"] [data-baseweb="select"] span,
[data-testid="stForm"] [data-testid="stSelectbox"] [data-baseweb="select"] div {
    color: #263A36 !important;
}
[data-testid="stForm"] [data-testid="stSelectbox"] [data-baseweb="select"] svg {
    color: #263A36 !important;
    fill: #263A36 !important;
}
[data-testid="stForm"] [data-testid="stSelectbox"] [data-baseweb="select"] > div:hover {
    border-color: #263A36 !important;
}
[data-testid="stForm"] [data-baseweb="textarea"]:focus-within,
[data-testid="stForm"] [data-testid="stSelectbox"] [data-baseweb="select"] > div:focus-within {
    border-color: #263A36 !important;
    box-shadow: 0 0 0 2px rgba(38,58,54,.24) !important;
}
[data-testid="stForm"] .stFormSubmitButton > button[kind="primaryFormSubmit"] {
    background: #263A36 !important;
    border-color: #263A36 !important;
    color: #FFFFFF !important;
}
[data-testid="stForm"] .stFormSubmitButton > button[kind="primaryFormSubmit"] p,
[data-testid="stForm"] .stFormSubmitButton > button[kind="primaryFormSubmit"] span {
    color: #FFFFFF !important;
}
[data-testid="stForm"] .stFormSubmitButton > button[kind="primaryFormSubmit"]:hover {
    background: #405653 !important;
    border-color: #405653 !important;
}
[data-testid="stForm"] .stFormSubmitButton > button[kind="primaryFormSubmit"]:active {
    background: #4C5B61 !important;
    border-color: #4C5B61 !important;
}
[data-testid="stForm"] .stFormSubmitButton > button[kind="primaryFormSubmit"]:focus-visible {
    outline: 3px solid #A3ADA5 !important;
    outline-offset: 3px;
}
.px-verdict { position: relative; overflow: hidden; margin-top: 1.4rem; padding: 1.8rem; border-radius: 24px; border: 1px solid rgba(212,215,211,.3); background: linear-gradient(160deg, #405653, #2C423F); box-shadow: 0 18px 44px rgba(0,0,0,.25); animation: px-rise .9s both; }
.px-verdict.match { border-color: rgba(212,215,211,.55); }
.px-verdict.miss { border-style: dashed; }
.px-verdict::before { content:""; position:absolute; right:-80px; top:-80px; width:240px; height:240px; border-radius:50%; background: radial-gradient(circle, rgba(212,215,211,.3), transparent 70%); }
.px-verdict small { position: relative; display: block; font-size: .7rem; font-weight: 600; letter-spacing: .26em; text-transform: uppercase; color: var(--steel); }
.stMarkdown .px-verdict h3 { position: relative; margin: .6rem 0 1.4rem; padding: 0; font-size: clamp(1.15rem, 2.2vw, 1.5rem); font-weight: 300; line-height: 1.5; color: var(--mist) !important; }
.px-tiers { position: relative; display: flex; align-items: center; gap: 1.4rem; margin-bottom: 1.4rem; }
.px-tiers div small { margin-bottom: .3rem; }
.px-tiers b { font-size: 2.6rem; font-weight: 200; line-height: 1; color: var(--mist); }
.px-arrow { flex: 0 0 72px; height: 1px; background: linear-gradient(90deg, var(--mist), rgba(212,215,211,.2)); transform-origin: left; animation: px-line 1.2s .3s both; }
.px-verdict.miss .px-arrow { background: repeating-linear-gradient(90deg, var(--sage) 0 6px, transparent 6px 12px); }
</style>
"""


def render() -> None:
    ui.inject()
    st.markdown(ui.html(_VERDICT_CSS), unsafe_allow_html=True)

    ui.hero(
        "Calibration",
        "Calibration Studio",
        "Check whether questions take the expected route.",
        note=(
            "Each evaluation makes a real router request and is included in session analytics. "
            "Without GROQ_API_KEY, the router uses its clearly labeled local mock response."
        ),
    )

    ui.label(
        "Evaluate",
        "Evaluate routing decisions with controlled examples, compare expected and selected "
        "complexity tiers, and inspect the resulting route and cost estimates.",
        index="01",
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
                    result = get_router().route_and_execute(prompt.strip())
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
        ui.label("Result", index="02")
        if latest["tier_match"]:
            state, kicker = "match", "Tier agreement"
            message = f"Tier agreement: expected and selected Tier {latest['actual_tier']}."
        else:
            state, kicker = "miss", "Tier mismatch"
            message = (
                f"Tier mismatch: expected Tier {latest['expected_tier']}, "
                f"router selected Tier {latest['actual_tier']}."
            )
        route = f"{latest['initial_model']} → {latest['final_model']}"
        pills = "".join(
            (
                ui.pill(route),
                ui.pill("escalated" if latest["fallback_triggered"] else "no escalation"),
                ui.pill("simulated" if latest["mock_fallback"] else "live"),
            )
        )
        st.markdown(
            ui.html(
                f"""
                <div class="px-verdict {state}">
                    <small>{escape(kicker)}</small>
                    <h3>{escape(message)}</h3>
                    <div class="px-tiers">
                        <div><small>Expected</small><b>{escape(str(latest["expected_tier"]))}</b></div>
                        <span class="px-arrow"></span>
                        <div><small>Selected</small><b>{escape(str(latest["actual_tier"]))}</b></div>
                    </div>
                    <div class="px-pills">{pills}</div>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )

    calibration_results = st.session_state.get("calibration_results", [])
    if calibration_results:
        matches = sum(item["tier_match"] for item in calibration_results)
        total = len(calibration_results)
        ui.label(
            "Evaluation history",
            "Tier agreement reflects the expected tier you supplied; it is not a response-quality score.",
            index="03",
        )
        st.markdown(
            ui.tiles(
                (
                    ("Evaluations", str(total), "This session"),
                    ("Matched", str(matches), "Expected tier equals selected tier"),
                    ("Agreement", f"{matches / total * 100:.0f}%", "Of evaluations so far"),
                )
            ),
            unsafe_allow_html=True,
        )
        st.write("")
        st.dataframe(calibration_results, width="stretch", hide_index=True)
        st.caption(f"{matches} of {total} evaluations matched the expected tier.")
    else:
        ui.label("Evaluation history", index="03")
        st.markdown(
            ui.empty(
                "No evaluations yet",
                "Run an evaluation above to see the router's selected tier and route details.",
            ),
            unsafe_allow_html=True,
        )