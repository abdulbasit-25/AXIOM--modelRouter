"""Shared, non-secret application configuration."""

from pathlib import Path

BRAND_NAME = "Axiom"
BRAND_WORDMARK = "AXIOM"
BRAND_EXPANSION = "AI eXcellence in Optimized Mentoring"
BRAND_TAGLINE = "Intelligence, routed with purpose."
BRAND_SHORT_DESCRIPTION = "Educational AI routing for learning support."
BRAND_DESCRIPTION = (
    "Axiom is an educational AI routing prototype that classifies questions, routes them "
    "to suitable AI models, verifies responses, and tracks session-scoped routing and "
    "estimated cost metrics."
)

ASSETS_DIR = Path(__file__).resolve().parent / "assets"
BRAND_LOGO_PATH = ASSETS_DIR / "axiom-logo.svg"
BRAND_MARK_PATH = ASSETS_DIR / "axiom-mark.svg"

PAGE_TITLE = "Axiom — Intelligence, Routed with Purpose"
PAGE_ICON = str(BRAND_MARK_PATH)

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

GETTING_STARTED = (
    ("Open Production AI Tutor.", "This is the primary workspace for the integrated tutoring workflow."),
    ("Select an educational scenario.", "Choose from Vocabulary Flashcard, Curriculum Synthesis, STEM Reasoning, or Fallback Demonstration."),
    ("Review or edit the suggested question.", "The prompt reflects a sample learning task that can be refined before running the demonstration."),
    ("Run the question.", "The routing engine selects a model, checks the response, and reports the route and estimated cost."),
)

MAX_QUESTION_CHARS = 600
