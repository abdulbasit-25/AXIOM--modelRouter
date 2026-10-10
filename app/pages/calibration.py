"""Capability Calibration Studio - Dev Mode page."""

import csv
from datetime import datetime, timezone
from html import escape
from io import StringIO
import logging

import streamlit as st

from app.config import MAX_QUESTION_CHARS
from app.services.router_service import get_router
from app.pages import page_base as ui
from core import BenchmarkProfiler, CapabilityMatrix
from engine.model_client import SUPPORTED_MODELS
from engine.router import TIER_MODEL_MAP
from engine.telemetry import PRICING_PER_1M

logger = logging.getLogger(__name__)

_TIER_LABELS = {
    1: "Tier 1 · Vocab & Factual Recall",
    2: "Tier 2 · Conceptual Synthesis & Essay",
    3: "Tier 3 · STEM, Proofs & Code",
}

_DEFAULT_PROMPT = (
    "Explain the key differences between mitosis and meiosis for high school biology students, "
    "highlighting cellular purpose, division stages, and genetic variation."
)

_DEFAULT_RUBRIC = """### Ground-Truth Reference Rubric: Mitosis vs. Meiosis

1. Purpose: Mitosis produces 2 genetically identical diploid (2n) somatic cells for growth and tissue repair. Meiosis produces 4 genetically diverse haploid (n) gametes for sexual reproduction.
2. Divisions: Mitosis involves 1 nuclear division (PMAT). Meiosis involves 2 consecutive nuclear divisions (Meiosis I and Meiosis II).
3. Genetic Variation: Crossing over (prophase I) and independent assortment occur exclusively in meiosis, creating genetic diversity, whereas mitosis maintains clonal genetic consistency.
4. Formatting: Clear markdown headings, numbered or bulleted comparative lists, and concise pedagogical terminology."""

_CARD_CSS = """
<style>
.cal-winner {
    position: relative;
    overflow: hidden;
    margin: 1.5rem 0;
    padding: 1.8rem 2rem;
    border-radius: 24px;
    border: 1px solid #D4D7D3;
    background: linear-gradient(135deg, #2C423F, #1F302D);
    box-shadow: 0 16px 40px rgba(0,0,0,0.3);
}
.cal-winner small {
    display: block;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #A3ADA5;
}
.cal-winner h2 {
    margin: 0.4rem 0 0.8rem;
    font-size: clamp(1.4rem, 2.5vw, 2.1rem);
    font-weight: 300;
    letter-spacing: 0.05em;
    color: #D4D7D3 !important;
}
.cal-winner p {
    margin: 0;
    font-size: 0.95rem;
    color: #A3ADA5;
}
.cal-model-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.2rem;
    margin: 1.5rem 0;
}
.cal-card {
    position: relative;
    padding: 1.6rem;
    border-radius: 20px;
    border: 1px solid rgba(212,215,211,0.25);
    background: linear-gradient(160deg, #2b413d, #1f312e);
    box-shadow: 0 12px 28px rgba(0,0,0,0.25);
    transition: transform 0.4s ease, border-color 0.4s;
}
.cal-card:hover {
    transform: translateY(-5px);
    border-color: rgba(212,215,211,0.55);
}
.cal-card.winner-card {
    border: 1.5px solid #D4D7D3;
    background: linear-gradient(160deg, #344B45, #263A36);
    box-shadow: 0 16px 36px rgba(0,0,0,0.35);
}
.cal-card h3 {
    margin: 0.2rem 0 0.8rem;
    font-size: 1.2rem;
    font-weight: 400;
    color: #D4D7D3 !important;
}
.cal-score-big {
    font-size: 2.2rem;
    font-weight: 200;
    color: #D4D7D3;
    margin: 0.6rem 0;
}
.cal-stat-row {
    display: flex;
    justify-content: space-between;
    padding: 0.45rem 0;
    border-top: 1px solid rgba(212,215,211,0.12);
    font-size: 0.82rem;
    color: #A3ADA5;
}
.cal-stat-row b {
    color: #D4D7D3;
    font-weight: 500;
}

/* Form inputs & typed text styling for Calibration Studio */
[data-testid="stForm"] {
    background: #FFFFFF !important;
    border: 1px solid rgba(44,66,63,.25) !important;
    border-radius: 20px !important;
    padding: 1.8rem !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08) !important;
}

[data-testid="stForm"] [data-baseweb="textarea"],
[data-testid="stForm"] [data-baseweb="base-input"] {
    background: #FFFFFF !important;
    border: 1px solid #899B9A !important;
    border-radius: 12px !important;
}

[data-testid="stForm"] [data-testid="stTextArea"] textarea {
    background: #FFFFFF !important;
    color: #263A36 !important;
    -webkit-text-fill-color: #263A36 !important;
    caret-color: #263A36 !important;
    font-size: 0.98rem !important;
    line-height: 1.6 !important;
}

[data-testid="stForm"] [data-testid="stTextArea"] textarea::placeholder {
    color: #566970 !important;
    -webkit-text-fill-color: #566970 !important;
    opacity: 1 !important;
}

[data-testid="stForm"] [data-testid="stWidgetLabel"] p,
[data-testid="stForm"] [data-testid="stWidgetLabel"] label {
    color: #263A36 !important;
    font-weight: 500 !important;
}

[data-testid="stForm"] [data-baseweb="select"] > div {
    background: #FFFFFF !important;
    color: #263A36 !important;
    border: 1px solid #899B9A !important;
    border-radius: 10px !important;
}

[data-testid="stForm"] [data-baseweb="select"] span,
[data-testid="stForm"] [data-baseweb="select"] div {
    color: #263A36 !important;
}

[data-testid="stForm"] .stButton > button[kind="primary"] {
    background: #263A36 !important;
    border-color: #263A36 !important;
    color: #FFFFFF !important;
}

[data-testid="stForm"] .stButton > button[kind="primary"] p,
[data-testid="stForm"] .stButton > button[kind="primary"] span {
    color: #FFFFFF !important;
}

[data-testid="stForm"] .stButton > button[kind="primary"]:hover {
    background: #405653 !important;
    border-color: #405653 !important;
}
</style>
"""


def _get_benchmark_profiler() -> BenchmarkProfiler:
    profiler = st.session_state.get("benchmark_profiler")
    if not isinstance(profiler, BenchmarkProfiler):
        profiler = BenchmarkProfiler(
            capability_matrix=CapabilityMatrix(initial_matrix=TIER_MODEL_MAP)
        )
        st.session_state["benchmark_profiler"] = profiler
    return profiler


def render() -> None:
    ui.inject()
    st.markdown(_CARD_CSS, unsafe_allow_html=True)

    ui.hero(
        "Dev Calibration Studio",
        "Capability Calibration Studio",
        "Benchmarking candidate model architectures against ground-truth rubrics.",
        note=(
            "Developer ground-truth calibration mode: evaluates candidate LLMs on semantic alignment, "
            "formatting conformity, latency, and token efficiency to recommend winning model profiles."
        ),
    )

    ui.label(
        "Calibration Inputs",
        "Input a test prompt and reference rubric to profile candidate model architectures.",
        index="01",
    )

    with st.form("calibration_studio_form"):
        prompt = st.text_area(
            "Evaluation Prompt / Student Query",
            value="",
            height=100,
            max_chars=MAX_QUESTION_CHARS,
            key="cal_prompt_input",
            placeholder="Enter the standardized evaluation prompt or query to benchmark across models...",
            help="The standardized prompt sent to all candidate models.",
        )
        ground_truth = st.text_area(
            "Ground-Truth Answer / Scoring Rubric",
            value="",
            height=140,
            max_chars=3000,
            key="cal_rubric_input",
            placeholder="Enter the ground-truth reference answer or scoring criteria rubric...",
            help="Reference answer or scoring rubric used to evaluate candidate outputs.",
        )
        col1, col2 = st.columns([1, 2])
        with col1:
            tier_to_calibrate = st.selectbox(
                "Target Complexity Tier",
                options=(1, 2, 3),
                format_func=lambda t: _TIER_LABELS[t],
                index=1,
                key="cal_target_tier",
            )
        with col2:
            models_to_benchmark = st.multiselect(
                "Candidate Models to Compare",
                options=SUPPORTED_MODELS,
                default=SUPPORTED_MODELS,
                key="cal_models_select",
            )

        submit_btn = st.form_submit_button(
            "Run Multi-Model Calibration",
            type="primary",
            width="stretch",
            key="run_calibration",
        )

    if submit_btn:
        if not prompt.strip():
            st.warning("Enter an evaluation prompt before running calibration.")
        elif not ground_truth.strip():
            st.warning("Enter a ground-truth rubric before evaluating model candidates.")
        elif not models_to_benchmark:
            st.warning("Select at least one candidate model to evaluate.")
        else:
            profiler = _get_benchmark_profiler()
            router = get_router()
            candidate_records = []
            all_live = True

            try:
                with st.spinner("Executing candidate model inference and calculating evaluation rubrics..."):
                    for model_name in models_to_benchmark:
                        generated = router.model_client.generate(
                            model_name=model_name,
                            prompt=prompt.strip(),
                            system_prompt=(
                                "You are an expert educational AI tutor. Provide a comprehensive, accurate, "
                                "and well-structured response meeting the highest pedagogical standards."
                            ),
                        )
                        pricing = PRICING_PER_1M.get(
                            model_name, {"input": 0.10, "output": 0.30}
                        )
                        cost = (
                            generated["input_tokens"] * pricing["input"]
                            + generated["output_tokens"] * pricing["output"]
                        ) / 1_000_000.0
                        is_mock = bool(generated.get("mock_fallback", False))
                        all_live = all_live and not is_mock

                        candidate_records.append(
                            {
                                "model": model_name,
                                "output": generated["text"],
                                "latency_ms": generated["latency_ms"],
                                "cost": cost,
                                "input_tokens": generated["input_tokens"],
                                "output_tokens": generated["output_tokens"],
                                "mock_fallback": is_mock,
                            }
                        )

                    # Benchmark using BenchmarkProfiler
                    evaluated = profiler.benchmark_models(
                        candidate_records=candidate_records,
                        ground_truth=ground_truth.strip(),
                        auto_update_tier=int(tier_to_calibrate),
                    )

                best_model = evaluated[0]["model"]
                best_score = evaluated[0]["composite_score"]
                calibration_record = {
                    "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "tier": int(tier_to_calibrate),
                    "tier_name": _TIER_LABELS[tier_to_calibrate],
                    "best_model": best_model,
                    "best_score": best_score,
                    "results": evaluated,
                    "all_live": all_live,
                }
                st.session_state["active_calibration"] = calibration_record
                st.session_state.setdefault("calibration_history", []).append(
                    {
                        "Timestamp (UTC)": calibration_record["timestamp"],
                        "Tier": calibration_record["tier_name"],
                        "Winning Model": best_model,
                        "Composite Score": f"{best_score:.2%}",
                        "Live Provider": all_live,
                    }
                )
                st.session_state.pop("calibration_error", None)

            except Exception:
                logger.exception("Calibration benchmark execution failed")
                st.session_state["calibration_error"] = (
                    "Calibration could not be completed. Check application logs."
                )

    if error_msg := st.session_state.get("calibration_error"):
        st.error(error_msg)

    # Render Calibration Results
    active = st.session_state.get("active_calibration")
    if active:
        ui.label(
            "Winning Architecture & Comparative Profiling",
            "Scored on Semantic Match (60%), Format Adherence (20%), and Speed (20%).",
            index="02",
        )

        best_m = active["best_model"]
        best_s = active["best_score"]
        tier_str = active["tier_name"]

        # Winning Architecture Badge Card
        st.markdown(
            f"""
            <div class="cal-winner">
                <small>🏆 Winning Architecture Recommendation</small>
                <h2>{escape(best_m)}</h2>
                <p>
                    Ranked <b>#1 for {escape(tier_str)}</b> with a composite score of 
                    <b>{best_s:.1%}</b>. CapabilityMatrix has been calibrated for this session.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Side-by-Side Model Comparison Cards
        card_html_list = []
        for index, res in enumerate(active["results"], start=1):
            is_winner = res["model"] == best_m
            winner_cls = "winner-card" if is_winner else ""
            status_text = "Live Groq" if not res.get("mock_fallback") else "Mock Fallback"
            card_html_list.append(
                f"""
                <div class="cal-card {winner_cls}">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="font-size:0.7rem;letter-spacing:0.18em;text-transform:uppercase;color:#899B9A;">
                            {'🥇 Winner' if is_winner else f'Rank #{index}'}
                        </span>
                        <span style="font-size:0.7rem;color:#A3ADA5;">{status_text}</span>
                    </div>
                    <h3>{escape(res["model"])}</h3>
                    <div class="cal-score-big">{res["composite_score"]:.1%}</div>
                    <div style="font-size:0.75rem;color:#899B9A;margin-bottom:0.8rem;">Composite Calibration Score</div>
                    <div class="cal-stat-row"><span>Semantic Match</span><b>{res["semantic_score"]:.1%}</b></div>
                    <div class="cal-stat-row"><span>Token Overlap</span><b>{res["token_overlap_score"]:.1%}</b></div>
                    <div class="cal-stat-row"><span>Format Adherence</span><b>{res["format_score"]:.1%}</b></div>
                    <div class="cal-stat-row"><span>Latency</span><b>{res["latency_ms"]:.0f} ms</b></div>
                    <div class="cal-stat-row"><span>Token Cost</span><b>${res["cost"]:.6f}</b></div>
                </div>
                """
            )

        st.markdown(
            f'<div class="cal-model-grid">{"".join(card_html_list)}</div>',
            unsafe_allow_html=True,
        )

        # Detailed Outputs Expanders
        st.write("")
        ui.label("Candidate Model Outputs", "Inspect generated candidate responses against the ground truth rubric.", index="03")
        for res in active["results"]:
            with st.expander(f"Candidate: {res['model']} (Score: {res['composite_score']:.1%})"):
                st.markdown(res["output"])

        # CSV Download
        table_rows = [
            {
                "Rank": i,
                "Model": r["model"],
                "Composite Score": r["composite_score"],
                "Semantic Score": r["semantic_score"],
                "Token Overlap": r["token_overlap_score"],
                "Format Score": r["format_score"],
                "Speed Score": r["speed_score"],
                "Latency (ms)": r["latency_ms"],
                "Cost ($)": r["cost"],
                "Simulated": r.get("mock_fallback", False),
            }
            for i, r in enumerate(active["results"], start=1)
        ]
        report_buf = StringIO()
        writer = csv.DictWriter(report_buf, fieldnames=list(table_rows[0].keys()))
        writer.writeheader()
        writer.writerows(table_rows)

        st.download_button(
            "Download Calibration Results (CSV)",
            data=report_buf.getvalue(),
            file_name="axiom-calibration-benchmark.csv",
            mime="text/csv",
            key="download_cal_csv",
        )

    # Session Calibration History
    history = st.session_state.get("calibration_history", [])
    if history:
        with st.expander("Session Calibration History"):
            st.dataframe(history, width="stretch", hide_index=True)