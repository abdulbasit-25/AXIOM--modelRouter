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
        assert any("Estimated cost" in item.value for item in app.markdown)


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
            "openai/gpt-oss-20b",
            "openai/gpt-oss-120b",
        ]
        telemetry_row = router.telemetry.query_history[0]
        assert telemetry_row["tier"] == 1
        assert telemetry_row["fallback_triggered"] is True
        assert telemetry_row["mock_fallback"] is True
        assert telemetry_row["latency_ms"] > 0
        assert telemetry_row["timestamp"]

        app.radio(key="active_destination").set_value("SDG Analytics").run(timeout=10)
        assert not app.exception
        assert any("Routed questions" in item.value for item in app.markdown)


def test_calibration_evaluates_route_and_records_tier_agreement():
    with _without_api_key():
        app = AppTest.from_file(str(PROJECT_ROOT / "app" / "main.py")).run(timeout=10)
        app.radio(key="active_destination").set_value("Calibration Studio").run(timeout=10)
        app.text_area(key="calibration_prompt").set_value("What is DNA?")
        app.selectbox(key="calibration_expected_tier").set_value(1)
        app.button(key="run_calibration").click().run(timeout=10)

        assert not app.exception
        calibration = app.session_state["calibration_results"]
        assert len(calibration) == 1
        assert calibration[0]["expected_tier"] == 1
        assert calibration[0]["actual_tier"] == 1
        assert calibration[0]["tier_match"] is True
        assert app.session_state["production_router"].telemetry.total_queries == 1


if __name__ == "__main__":
    test_tutor_submits_question_and_displays_router_result()
    test_fallback_scenario_runs_both_models_and_records_one_query()
    test_calibration_evaluates_route_and_records_tier_agreement()
