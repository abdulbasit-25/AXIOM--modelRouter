"""Educational query classification infrastructure.

Classifies incoming student/educational prompts into 3 distinct complexity tiers:
- Tier 1: Vocab / Flashcard / Micro Factual Recall -> Meta Llama 3.1 8B Instant (llama-3.1-8b-instant)
- Tier 2: Conceptual Explanation & Structured Synthesis -> Alibaba Qwen 27B (qwen/qwen3.8-27b)
- Tier 3: Complex STEM / Code / Heavy Multi-step Reasoning -> Meta Llama 3.3 70B Versatile (llama-3.3-70b-versatile)
"""

from __future__ import annotations

import re
from typing import Any, Dict


class TierClassificationResult(dict):
    """Dictionary holding classification result with integer casting and attribute access support."""

    def __init__(
        self,
        tier: int,
        tier_name: str,
        target_model: str,
        reason: str = "",
        confidence: float = 0.95,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            tier=tier,
            tier_name=tier_name,
            target_model=target_model,
            reason=reason,
            confidence=confidence,
            **kwargs,
        )
        self.tier = tier
        self.tier_name = tier_name
        self.target_model = target_model
        self.reason = reason
        self.confidence = confidence

    def __int__(self) -> int:
        return self.tier

    def __index__(self) -> int:
        return self.tier

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, int):
            return self.tier == other
        return super().__eq__(other)

    def __hash__(self) -> int:
        return hash(self.tier)


class EducationalQueryClassifier:
    """Classifies educational queries into operational complexity tiers in sub-15ms."""

    # Keywords indicative of Tier 3 (STEM / Code / Heavy Reasoning / Proofs)
    TIER_3_PATTERNS = [
        # Mathematics & Proofs
        r"\bprove\b",
        r"\bproof\b",
        r"\bderive\b",
        r"\bderivation\b",
        r"\binduction\b",
        r"\btheorem\b",
        r"\bcalculate the integral\b",
        r"\bintegral\b",
        r"\bderivative\b",
        r"\bdifferential equation\b",
        r"\bmatrix\b",
        r"\beigenvalue\b",
        r"\blinear algebra\b",
        r"\bcalculus\b",
        r"\bmulti-step\b",
        r"\bformal verification\b",
        r"\bquadratic equation\b",
        r"\bcompleting the square\b",
        # Coding & Algorithms
        r"\bcode\b",
        r"\bdef\s+\w+\b",
        r"\bpython\b",
        r"\bjava\b",
        r"\bc\+\+\b",
        r"\bjavascript\b",
        r"\balgorithm\b",
        r"\btime complexity\b",
        r"\bspace complexity\b",
        r"\bdata structure\b",
        r"\brecursion\b",
        r"\bbinary search\b",
        r"\bsorting algorithm\b",
        r"\bwrite a function\b",
        r"\bpython function\b",
        r"\bcode a function\b",
        r"\bdebug\b",
        r"\bsyntax error\b",
        r"\bwrite a program\b",
        r"\bprogramming\b",
        # Hard Sciences & STEM
        r"\bphysics\b",
        r"\bchemistry\b",
        r"\bthermodynamics\b",
        r"\bquantum\b",
        r"\bstoichiometry\b",
        r"\bkinematics\b",
        r"\bcircuit\b",
        r"\bohm's law\b",
    ]

    # Keywords indicative of Tier 2 (Conceptual Explanation / Synthesis / Comparison / Essay)
    TIER_2_PATTERNS = [
        r"\bexplain\b",
        r"\bcompare\b",
        r"\bcontrast\b",
        r"\bdifference between\b",
        r"\bdifferences between\b",
        r"\bsummarize\b",
        r"\bhow does\b",
        r"\bwhy does\b",
        r"\bpros and cons\b",
        r"\boverview\b",
        r"\bbreak down\b",
        r"\banalyze\b",
        r"\bstructure of\b",
        r"\bcurriculum\b",
        r"\bessay\b",
        r"\bmitosis\b",
        r"\bmeiosis\b",
        r"\bcellular respiration\b",
        r"\bphotosynthesis\b",
        r"\blda\b",
        r"\babsa\b",
        r"\btopic model\b",
        r"\bsentiment analysis\b",
    ]

    # Keywords indicative of Tier 1 (Vocab / Flashcard / Micro Facts / Definitions)
    TIER_1_PATTERNS = [
        r"\bdefine\b",
        r"\bdefinition\b",
        r"\bmeaning of\b",
        r"\bwhat is\b",
        r"\bwhat are\b",
        r"\bwho is\b",
        r"\bwho was\b",
        r"\bwhen was\b",
        r"\bwhere is\b",
        r"\bflashcard\b",
        r"\bvocabulary\b",
        r"\bvocab\b",
        r"\bsynonym\b",
        r"\bantonym\b",
        r"\bspeed of light\b",
        r"\bcapital of\b",
    ]

    TIER_NAMES = {
        1: "Tier 1: Vocab / Flashcard / Micro Factual",
        2: "Tier 2: Conceptual Explanation & Synthesis",
        3: "Tier 3: STEM / Code / Heavy Reasoning",
    }

    TARGET_MODELS = {
        1: "llama-3.1-8b-instant",
        2: "qwen/qwen3.8-27b",
        3: "llama-3.3-70b-versatile",
    }

    def classify(self, prompt: str) -> TierClassificationResult:
        """Classify prompt into complexity tiers in sub-15ms pure standard Python.

        Args:
            prompt: Student query or educational prompt.

        Returns:
            TierClassificationResult: Dict containing 'tier', 'tier_name', 'target_model', etc.
            Also supports integer conversion `int(result)` and direct equality check `result == 1`.
        """
        clean_text = prompt.lower().strip()
        words = clean_text.split()
        word_count = len(words)

        # Check Tier 3 indicators (STEM / Code / Heavy Reasoning)
        for pattern in self.TIER_3_PATTERNS:
            if re.search(pattern, clean_text):
                return TierClassificationResult(
                    tier=3,
                    tier_name=self.TIER_NAMES[3],
                    target_model=self.TARGET_MODELS[3],
                    reason=f"Matched STEM/Code/Reasoning pattern: '{pattern}'",
                    confidence=0.96,
                    prompt_length_words=word_count,
                )

        # Check concise Tier 1 Vocab / Definition / Flashcard queries (<= 25 words)
        if word_count <= 25:
            for pattern in self.TIER_1_PATTERNS:
                if re.search(pattern, clean_text):
                    return TierClassificationResult(
                        tier=1,
                        tier_name=self.TIER_NAMES[1],
                        target_model=self.TARGET_MODELS[1],
                        reason=f"Matched Tier 1 Vocab/Definition pattern: '{pattern}'",
                        confidence=0.95,
                        prompt_length_words=word_count,
                    )

        # Check Tier 2 indicators (Conceptual Explanation / Synthesis / Comparison)
        for pattern in self.TIER_2_PATTERNS:
            if re.search(pattern, clean_text):
                return TierClassificationResult(
                    tier=2,
                    tier_name=self.TIER_NAMES[2],
                    target_model=self.TARGET_MODELS[2],
                    reason=f"Matched Conceptual/Synthesis pattern: '{pattern}'",
                    confidence=0.92,
                    prompt_length_words=word_count,
                )

        # Length heuristics
        if word_count > 60:
            return TierClassificationResult(
                tier=3,
                tier_name=self.TIER_NAMES[3],
                target_model=self.TARGET_MODELS[3],
                reason=f"Length heuristic: query contains {word_count} words (>60)",
                confidence=0.88,
                prompt_length_words=word_count,
            )
        elif word_count > 25:
            return TierClassificationResult(
                tier=2,
                tier_name=self.TIER_NAMES[2],
                target_model=self.TARGET_MODELS[2],
                reason=f"Length heuristic: query contains {word_count} words (>25)",
                confidence=0.85,
                prompt_length_words=word_count,
            )

        # Default to Tier 1 (Vocab / Flashcard / Micro)
        return TierClassificationResult(
            tier=1,
            tier_name=self.TIER_NAMES[1],
            target_model=self.TARGET_MODELS[1],
            reason="Fast factual recall / flashcard definition default",
            confidence=0.90,
            prompt_length_words=word_count,
        )

    def classify_with_metadata(self, prompt: str) -> Dict[str, Any]:
        """Classify prompt with rich metadata for debugging and telemetry."""
        return dict(self.classify(prompt))
