"""Tests for reference-based model evaluation and capability recommendations."""

import math
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.profiler import BenchmarkProfiler, CapabilityMatrix


def test_evaluate_response_scores_reference_format_and_latency():
    profiler = BenchmarkProfiler(max_latency_ms=2000.0)
    result = profiler.evaluate_response(
        candidate_output="Water is H2O.",
        ground_truth="Water is H2O.",
        latency_ms=1000,
        cost=0.001,
    )

    assert result["semantic_score"] == 1.0
    assert result["token_overlap_score"] == 1.0
    assert result["content_score"] == 1.0
    assert result["format_score"] == 1.0
    assert result["speed_score"] == 0.5
    assert result["composite_score"] == 0.9
    assert result["cost"] == 0.001


def test_format_score_penalizes_missing_expected_structure():
    score = BenchmarkProfiler.calculate_format_score(
        "Mitosis creates two identical cells.",
        "1. Mitosis creates two cells.\n2. Meiosis creates four cells.",
    )
    assert score == 0.5


def test_benchmark_ranks_models_and_updates_only_selected_tier():
    matrix = CapabilityMatrix()
    profiler = BenchmarkProfiler(capability_matrix=matrix)
    results = profiler.benchmark_models(
        [
            {
                "model": "model-a",
                "output": "Water is H2O.",
                "latency_ms": 100,
                "cost": 0.001,
            },
            {
                "model": "model-b",
                "output": "The sky is blue.",
                "latency_ms": 100,
                "cost": 0.001,
            },
        ],
        ground_truth="Water is H2O.",
        auto_update_tier=2,
    )

    assert [result["model"] for result in results] == ["model-a", "model-b"]
    assert matrix.get_model(2) == "model-a"
    assert matrix.get_model(1) == "openai/gpt-oss-20b"
    assert math.isclose(results[0]["composite_score"], 0.99)


def test_absa_lda_benchmark_reports_each_rubric_dimension():
    profiler = BenchmarkProfiler()
    results = profiler.benchmark_absa_lda_models(
        [
            {
                "model": "model-a",
                "output": (
                    "# ABSA and LDA pipeline\n"
                    "1. ABSA assigns sentiment polarity to aspects or entities: positive, "
                    "negative, or neutral.\n"
                    "2. Preprocessing includes tokenization, stop-word removal, POS tagging "
                    "to find nouns and noun phrases, and lemmatization.\n"
                    "3. LDA (Latent Dirichlet Allocation) discovers topics and topic-word "
                    "distributions over words. Documents are mixtures of topics.\n"
                    "4. Document-topic theta and topic-word phi distributions map documents "
                    "and aspect terms to topics.\n"
                    "5. After extracting aspects, classify sentiment per aspect with context "
                    "windows or dependency parses using VADER, an SVM, or a transformer "
                    "to assign polarity."
                ),
                "latency_ms": 200,
                "cost": 0.002,
            },
            {
                "model": "model-b",
                "output": "LDA finds topics.",
                "latency_ms": 100,
                "cost": 0.001,
            },
        ],
        ground_truth=(
            "ABSA identifies aspects and sentiment polarity. LDA discovers topic and "
            "word distributions. Preprocessing uses tokenization, stop words, POS tagging, "
            "noun phrases, and lemmatization. Theta maps documents to topics and phi maps "
            "topics to words. After extracting aspects, a context-aware classifier predicts "
            "positive, negative, or neutral sentiment."
        ),
    )

    complete, partial = results
    assert complete["dual_concept_coverage"] > partial["dual_concept_coverage"]
    assert complete["technical_pipeline_completeness"] > partial["technical_pipeline_completeness"]
    assert complete["structural_formatting"] == 1.0
    assert complete["cost_latency_tradeoff"] == 0.45
    assert complete["absa_lda_composite_score"] > partial["absa_lda_composite_score"]
    assert complete["absa_coverage"] == 1.0
    assert complete["lda_coverage"] == 1.0


def test_benchmark_rejects_missing_reference_and_invalid_tier():
    profiler = BenchmarkProfiler()
    candidate = [{"model": "model-a", "output": "answer"}]

    try:
        profiler.benchmark_models(candidate, ground_truth=" ")
    except ValueError as exc:
        assert "ground-truth" in str(exc)
    else:
        raise AssertionError("Empty reference rubric should be rejected.")

    try:
        profiler.benchmark_models(
            candidate,
            ground_truth="answer",
            auto_update_tier=4,
        )
    except ValueError as exc:
        assert "auto_update_tier" in str(exc)
    else:
        raise AssertionError("Invalid benchmark tier should be rejected.")


def test_profiler_and_matrix_reject_invalid_configuration():
    try:
        BenchmarkProfiler(max_latency_ms=0)
    except ValueError as exc:
        assert "max_latency_ms" in str(exc)
    else:
        raise AssertionError("Non-positive latency baseline should be rejected.")

    matrix = CapabilityMatrix()
    try:
        matrix.update_matrix(4, "unsupported")
    except ValueError as exc:
        assert "Unknown tier" in str(exc)
    else:
        raise AssertionError("Invalid capability tier should be rejected.")


if __name__ == "__main__":
    for name, test in list(globals().items()):
        if name.startswith("test_") and callable(test):
            test()
