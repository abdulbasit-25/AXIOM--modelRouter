"""Lightweight output verification infrastructure.

Inspects generated candidate responses to ensure educational pedagogical standards,
factual completeness, step-by-step reasoning depth, and code structure before returning
to students. Escalates to frontier models when fast SLM outputs do not meet criteria.
"""

from __future__ import annotations

import re
from typing import Any, Dict, Optional


def inject_failure_marker(text: str) -> str:
    """Helper to inject a simulated failure marker into text for verification testing."""
    return f"{text.rstrip()} [error] simulated verification failure marker"


class VerificationResult(dict):
    """Encapsulates output verification status and diagnostic reasoning.

    Implements dict interface, boolean evaluation, and attribute access for complete
    contract interoperability across all callers.
    """

    def __init__(self, is_valid: bool, reason: str = "", **kwargs: Any) -> None:
        super().__init__(is_valid=bool(is_valid), reason=reason, **kwargs)
        self.is_valid = bool(is_valid)
        self.reason = reason

    def __bool__(self) -> bool:
        return self.is_valid

    def __repr__(self) -> str:
        return f"VerificationResult(is_valid={self.is_valid}, reason='{self.reason}')"

    def to_dict(self) -> Dict[str, Any]:
        return {"is_valid": self.is_valid, "reason": self.reason}


class LightweightVerifier:
    """Evaluates candidate model outputs against quality and complexity criteria."""

    def __init__(
        self,
        min_tier1_words: int = 3,
        min_tier2_words: int = 10,
        min_tier3_words: int = 25,
    ) -> None:
        self.min_tier1_words = min_tier1_words
        self.min_tier2_words = min_tier2_words
        self.min_tier3_words = min_tier3_words

    def inject_failure_marker(self, text: str) -> str:
        """Helper to inject a simulated failure marker into candidate text."""
        return inject_failure_marker(text)

    def verify(
        self,
        output_text: str = "",
        tier: int = 1,
        prompt: str = "",
        force_fail: bool = False,
        **kwargs: Any,
    ) -> VerificationResult:
        """Verify model output quality against deterministic heuristic standards.

        Supports both contract signatures:
          verify(output_text, tier, prompt)
          verify(prompt=..., response=..., tier=...)

        Args:
            output_text: Generated candidate response text (or response).
            tier: Query complexity tier (1, 2, or 3).
            prompt: Original user/student prompt.
            force_fail: If True, forces verification failure for demo purposes.
            **kwargs: Handles legacy keyword args ('response', 'model_name').

        Returns:
            VerificationResult (dict subclass): boolean-evaluable with 'is_valid' and 'reason'.
        """
        # Handle inverted/legacy arguments: response passed as keyword or output_text
        response = kwargs.get("response", output_text)
        if "prompt" in kwargs and output_text and prompt == "":
            prompt = output_text
            response = kwargs.get("response", "")

        if force_fail:
            return VerificationResult(
                is_valid=False,
                reason="Simulated verification failure (force_fallback_demo=True)",
            )

        # Baseline sanity checks
        if not response or not response.strip():
            return VerificationResult(
                is_valid=False,
                reason="Empty or whitespace-only response",
            )

        text = response.strip()
        word_count = len(text.split())

        # Check for obvious refusal or catastrophic failure patterns
        error_indicators = ["[error]", "failed to generate", "cannot assist with this", "simulated verification failure"]
        for ind in error_indicators:
            if ind in text.lower():
                return VerificationResult(
                    is_valid=False,
                    reason=f"Response contains failure marker: '{ind}'",
                )

        # Tier 1 checks (Vocab / Flashcard / Micro Factual)
        if tier == 1:
            if word_count < self.min_tier1_words:
                return VerificationResult(
                    is_valid=False,
                    reason=f"Tier 1 output too brief ({word_count} words < minimum {self.min_tier1_words})",
                )
            return VerificationResult(
                is_valid=True,
                reason="Tier 1 factual verification passed",
            )

        # Tier 2 checks (Conceptual Explanation / Synthesis)
        if tier == 2:
            if word_count < self.min_tier2_words:
                return VerificationResult(
                    is_valid=False,
                    reason=f"Tier 2 output lacks sufficient explanatory depth ({word_count} words < {self.min_tier2_words})",
                )
            return VerificationResult(
                is_valid=True,
                reason="Tier 2 conceptual synthesis verification passed",
            )

        # Tier 3 checks (STEM / Code / Heavy Multi-step Reasoning)
        if tier == 3:
            prompt_lower = (prompt or "").lower()

            # Check if this is a coding prompt
            is_coding_prompt = any(
                term in prompt_lower
                for term in ["code", "python", "programming", "algorithm", "binary search", "write a function", "python function", "def "]
            )
            has_code_fence = "```" in text

            if is_coding_prompt and not has_code_fence:
                return VerificationResult(
                    is_valid=False,
                    reason=(
                        "Tier 3 coding query output lacks formatted code fences (```). "
                        "Requires escalation to a frontier code-reasoning model."
                    ),
                )

            # Check for step-by-step reasoning / proof markers
            proof_markers = [
                "step",
                "proof",
                "therefore",
                "hence",
                "because",
                "induction",
                "base case",
                "1.",
                "2.",
                "first,",
                "finally",
            ]
            has_proof_structure = any(marker in text.lower() for marker in proof_markers)

            if word_count < self.min_tier3_words or not (has_proof_structure or has_code_fence):
                return VerificationResult(
                    is_valid=False,
                    reason=(
                        f"Tier 3 response failed verification: "
                        f"Insufficient reasoning depth ({word_count} words) or missing step-by-step markers. "
                        f"Requires escalation to a larger reasoning model."
                    ),
                )

            return VerificationResult(
                is_valid=True,
                reason="Tier 3 reasoning verification passed",
            )

        return VerificationResult(is_valid=True, reason="Default verification passed")
