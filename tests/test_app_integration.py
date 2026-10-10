"""End-to-end test for the Streamlit tutor-to-router integration."""

from collections.abc import Generator
from contextlib import contextmanager
import os
from pathlib import Path
import sys
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.config import (
    BRAND_EXPANSION,
    BRAND_LOGO_PATH,
    BRAND_MARK_PATH,
    BRAND_TAGLINE,
    PAGE_ICON,
)


@contextmanager
def _without_api_key() -> Generator[None, None, None]:
    previous_key = os.environ.get("GROQ_API_KEY")
    os.environ["GROQ_API_KEY"] = ""
    try:
        with patch("engine.model_client.get_groq_client", return_value=None):
            yield
    finally:
        if previous_key is not None:
            os.environ["GROQ_API_KEY"] = previous_key
        else:
            os.environ.pop("GROQ_API_KEY", None)


def test_tutor_submits_question_and_displays_router_result():
    with _without_api_key():
        app = AppTest.from_file(str(PROJECT_ROOT / "app" / "main.py")).run(timeout=10)
        assert not app.exception

        app.radio(key="active_destination").set_value("Production AI Tutor").run(timeout=10)
        assert not app.exception

        app.text_area(key="question_input").set_value("What is DNA?")
        app.button(key="run_tutor").click().run(timeout=10)

        assert not app.exception
        assert any("Simulated response" in item.value for item in app.info)
        assert any("Axiom Cost" in item.value for item in app.markdown)


def test_fallback_scenario_runs_both_models_and_records_one_query():
    with _without_api_key():
        app = AppTest.from_file(str(PROJECT_ROOT / "app" / "main.py")).run(timeout=10)
        app.radio(key="active_destination").set_value("Production AI Tutor").run(timeout=10)
        app.button(key="scenario_3").click().run(timeout=10)
        app.button(key="run_tutor").click().run(timeout=10)

        assert not app.exception
        result = app.session_state["tutor_result"]
        assert result["fallback_triggered"] is True
        assert result["mock_fallback"] is True
        router = app.session_state["production_router"]
        assert router.telemetry.total_queries == 1
        assert router.telemetry.query_history[0]["models"] == [
            "llama-3.1-8b-instant",
            "llama-3.3-70b-versatile",
        ]
        telemetry_row = router.telemetry.query_history[0]
        assert telemetry_row["fallback_triggered"] is True
        assert telemetry_row["mock_fallback"] is True
        assert telemetry_row["latency_ms"] > 0
        assert telemetry_row["timestamp"]

        app.radio(key="active_destination").set_value("SDG Analytics").run(timeout=10)
        assert not app.exception
        assert any("Routed Questions" in item.value for item in app.markdown)


def test_calibration_evaluates_models_and_updates_capability_matrix():
    with _without_api_key():
        app = AppTest.from_file(str(PROJECT_ROOT / "app" / "main.py")).run(timeout=10)
        app.radio(key="active_destination").set_value("Calibration Studio").run(timeout=10)
        app.text_area(key="cal_prompt_input").set_value("Explain the difference between mitosis and meiosis.")
        app.text_area(key="cal_rubric_input").set_value("1. Mitosis produces 2 identical cells. 2. Meiosis produces 4 diverse gametes.")
        app.selectbox(key="cal_target_tier").set_value(2)
        app.multiselect(key="cal_models_select").set_value(["llama-3.1-8b-instant", "qwen/qwen3.8-27b"])
        app.button(key="run_calibration").click().run(timeout=10)

        assert not app.exception
        cal = app.session_state.get("active_calibration")
        assert cal is not None
        assert cal["tier"] == 2
        assert len(cal["results"]) == 2
        assert cal["best_model"] in ["llama-3.1-8b-instant", "qwen/qwen3.8-27b"]
        profiler = app.session_state["benchmark_profiler"]
        assert profiler.capability_matrix.get_model(2) == cal["best_model"]


def test_sdg_analytics_displays_kpi_cards_and_spend_comparison():
    with _without_api_key():
        app = AppTest.from_file(str(PROJECT_ROOT / "app" / "main.py")).run(timeout=10)
        # First generate a tutor query
        app.radio(key="active_destination").set_value("Production AI Tutor").run(timeout=10)
        app.text_area(key="question_input").set_value("What is DNA?")
        app.button(key="run_tutor").click().run(timeout=10)

        # Now view analytics
        app.radio(key="active_destination").set_value("SDG Analytics").run(timeout=10)
        assert not app.exception
        assert any("EdTech Accessibility Multiplier" in item.value for item in app.markdown)
        assert any("Axiom Total Spend" in item.value for item in app.markdown)
        assert any("Comparative Spend" in item.value for item in app.markdown)


def test_all_pages_render_and_router_is_reused_across_navigation():
    destinations = (
        "Welcome",
        "Production AI Tutor",
        "Calibration Studio",
        "SDG Analytics",
        "About",
    )
    with _without_api_key():
        app = AppTest.from_file(str(PROJECT_ROOT / "app" / "main.py")).run(timeout=10)
        assert not app.exception
        app.radio(key="active_destination").set_value("SDG Analytics").run(timeout=10)
        router = app.session_state["production_router"]

        for destination in destinations:
            app.radio(key="active_destination").set_value(destination).run(timeout=10)
            assert not app.exception
            assert app.session_state["active_destination"] == destination
            assert app.session_state["production_router"] is router
            if destination == "Welcome":
                assert any(BRAND_TAGLINE in item.value for item in app.markdown)
            if destination == "About":
                assert any(BRAND_EXPANSION in item.value for item in app.markdown)
                team_credit = "\n".join(item.value for item in app.markdown)
                assert "Backend" in team_credit
                assert "Abdul Basit" in team_credit
                assert "Frontend" in team_credit
                assert "Fatima Asim" in team_credit
                assert "Classifier" in team_credit
                assert team_credit.count('<article class="ab-member">') == 3


def test_unknown_active_destination_recovers_to_welcome():
    assert BRAND_LOGO_PATH.is_file()
    assert BRAND_MARK_PATH.is_file()
    assert Path(PAGE_ICON).is_file()
    assert Path(PAGE_ICON) == BRAND_MARK_PATH

    with _without_api_key():
        app = AppTest.from_file(str(PROJECT_ROOT / "app" / "main.py"))
        app.session_state["active_destination"] = "Unknown page"
        app.run(timeout=10)

        assert not app.exception
        assert app.session_state["active_destination"] == "Welcome"
        assert any(
            "Intelligence, routed with purpose." in item.value
            for item in app.markdown
        )


def test_welcome_call_to_action_navigates_to_tutor():
    with _without_api_key():
        app = AppTest.from_file(str(PROJECT_ROOT / "app" / "main.py")).run(timeout=10)
        app.button(key="cta_tutor").click().run(timeout=10)

        assert not app.exception
        assert app.session_state["active_destination"] == "Production AI Tutor"
        assert any("Choose a scenario" in item.value for item in app.markdown)


if __name__ == "__main__":
    test_tutor_submits_question_and_displays_router_result()
    test_fallback_scenario_runs_both_models_and_records_one_query()
    test_calibration_evaluates_models_and_updates_capability_matrix()
    test_sdg_analytics_displays_kpi_cards_and_spend_comparison()
    test_all_pages_render_and_router_is_reused_across_navigation()
    test_unknown_active_destination_recovers_to_welcome()
    test_welcome_call_to_action_navigates_to_tutor()
    print("All integration tests passed successfully!")
