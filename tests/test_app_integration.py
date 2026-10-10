"""End-to-end test for the Streamlit tutor-to-router integration."""

from collections.abc import Generator
from contextlib import contextmanager
import os
from pathlib import Path

from streamlit.testing.v1 import AppTest

PROJECT_ROOT = Path(__file__).resolve().parents[1]


@contextmanager
def _without_api_key() -> Generator[None, None, None]:
    previous_key = os.environ.get("GROQ_API_KEY")
    os.environ["GROQ_API_KEY"] = ""
    try:
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

        app.radio(key="active_destination").set_value("Production AI Tutor").run()
        assert not app.exception

        app.text_area(key="question_input").set_value("What is DNA?")
        app.button(key="run_tutor").click().run()

        assert not app.exception
        assert any("Simulated response" in item.value for item in app.info)
        assert any("Estimated cost" in item.value for item in app.markdown)


def test_fallback_scenario_runs_both_models_and_records_one_query():
    with _without_api_key():
        app = AppTest.from_file(str(PROJECT_ROOT / "app" / "main.py")).run(timeout=10)
        app.radio(key="active_destination").set_value("Production AI Tutor").run()
        app.button(key="scenario_3").click().run()
        app.button(key="run_tutor").click().run()

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


if __name__ == "__main__":
    test_tutor_submits_question_and_displays_router_result()
    test_fallback_scenario_runs_both_models_and_records_one_query()
