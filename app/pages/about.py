"""About page."""

from app.components import info_section, page_header


def render() -> None:
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
