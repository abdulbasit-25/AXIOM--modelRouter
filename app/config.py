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
BRAND_LOGO_PATH = ASSETS_DIR / "Logo.png"
BRAND_MARK_PATH = ASSETS_DIR / "android-chrome-192x192.png"
FAVICON_PATH = ASSETS_DIR / "favicon-32x32.png"

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
    "Vocabulary Flashcard": "Define photosynthesis and explain its primary biological function.",
    "Curriculum Synthesis": "Explain the key differences between mitosis and meiosis for high school biology students.",
    "STEM Reasoning": "Prove by mathematical induction that for all positive integers n, 1 + 2 + ... + n = n(n + 1)/2.",
    "Fallback Demonstration": "Solve the quadratic equation 2x^2 + 5x - 3 = 0 showing step-by-step mathematical proof.",
}

SCENARIO_DESCRIPTIONS = {
    "Vocabulary Flashcard": "Tier 1: Fast SLM micro-recall (llama-3.1-8b-instant).",
    "Curriculum Synthesis": "Tier 2: Conceptual explanation & synthesis (qwen/qwen3.8-27b).",
    "STEM Reasoning": "Tier 3: Complex mathematical proof & deep STEM reasoning.",
    "Fallback Demonstration": "Tier 3: Simulated verification failure & escalation to llama-3.3-70b-versatile.",
}

GETTING_STARTED = (
    ("Open Production AI Tutor.", "This is the primary workspace for the integrated tutoring workflow."),
    ("Select an educational scenario.", "Choose from Vocabulary Flashcard, Curriculum Synthesis, STEM Reasoning, or Fallback Demonstration."),
    ("Review or edit the suggested question.", "The prompt reflects a sample learning task that can be refined before running the demonstration."),
    ("Run the question.", "The routing engine selects a model, checks the response, and reports the route and estimated cost."),
)

MAX_QUESTION_CHARS = 600
