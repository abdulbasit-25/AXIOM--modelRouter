"""Calibration Studio page."""

from datetime import datetime, timezone
import logging

import streamlit as st

from app.components import empty_state, page_header, section_heading
from app.config import MAX_QUESTION_CHARS
from app.services.router_service import get_router

logger = logging.getLogger(__name__)


def render() -> None:
    page_header(
        "Calibration Studio",
        "Check whether questions take the expected route.",
        "Evaluate routing decisions with controlled examples, compare expected and selected complexity tiers, and inspect the resulting route and cost estimates.",
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
        section_heading(
            "Evaluation history",
            "Tier agreement reflects the expected tier you supplied; it is not a response-quality score.",
        )
        st.dataframe(calibration_results, width="stretch", hide_index=True)
        matches = sum(item["tier_match"] for item in calibration_results)
        st.caption(f"{matches} of {len(calibration_results)} evaluations matched the expected tier.")
    else:
        empty_state(
            "No evaluations yet",
            "Run an evaluation above to see the router's selected tier and route details.",
            "◎",
        )
