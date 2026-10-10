"""Model client infrastructure for Groq LLMs.

Supports:
- Tier 1: 'llama-3.1-8b-instant' (Meta via Groq)
- Tier 2: 'qwen/qwen3.8-27b' (Alibaba via Groq)
- Tier 3 / Fallback: 'llama-3.3-70b-versatile' (Meta via Groq)

Provides wall-clock latency tracking and safe mock fallback when
GROQ_API_KEY is not configured or in case of client/network errors.
"""

from __future__ import annotations

import logging
import os
import time
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

logger = logging.getLogger(__name__)

# Supported Groq model identifiers across different account provisions
SUPPORTED_MODELS: List[str] = [
    "llama-3.1-8b-instant",
    "qwen/qwen3.8-27b",
    "llama-3.3-70b-versatile",
    "openai/gpt-oss-20b",
    "openai/gpt-oss-120b",
]

# Architectural equivalents across Groq endpoints
ARCHITECTURE_EQUIVALENTS: Dict[str, List[str]] = {
    "llama-3.1-8b-instant": ["openai/gpt-oss-20b", "llama-3.1-8b-instant"],
    "openai/gpt-oss-20b": ["openai/gpt-oss-20b", "llama-3.1-8b-instant"],
    "qwen/qwen3.8-27b": ["qwen/qwen3.8-27b"],
    "llama-3.3-70b-versatile": ["openai/gpt-oss-120b", "llama-3.3-70b-versatile"],
    "openai/gpt-oss-120b": ["openai/gpt-oss-120b", "llama-3.3-70b-versatile"],
}

# Legacy alias mappings
MODEL_ALIASES: Dict[str, str] = {
    "llama-8b": "llama-3.1-8b-instant",
    "qwen-27b": "qwen/qwen3.8-27b",
    "llama-70b": "llama-3.3-70b-versatile",
}

MAX_COMPLETION_TOKENS = 900

_cached_client: Any = None
_available_groq_models: Optional[set] = None


def get_available_groq_models(groq_client: Any) -> set:
    """Retrieve the set of models actually provisioned on the active Groq account."""
    global _available_groq_models
    if _available_groq_models is not None:
        return _available_groq_models

    if groq_client is None:
        return set()

    try:
        models_data = groq_client.models.list()
        _available_groq_models = {m.id for m in models_data.data}
        logger.info("Discovered available Groq models on account: %s", _available_groq_models)
    except Exception as exc:
        logger.debug("Could not query Groq models.list(): %s", exc)
        _available_groq_models = set()

    return _available_groq_models


def resolve_model_for_account(model_name: str, groq_client: Any) -> str:
    """Resolve requested model to one that is active and accessible on this Groq account."""
    if groq_client is None:
        return model_name

    available = get_available_groq_models(groq_client)
    if not available:
        return model_name

    # If directly available on the account, use it
    if model_name in available:
        return model_name

    # Search architecture equivalents
    candidates = ARCHITECTURE_EQUIVALENTS.get(model_name, [model_name])
    for cand in candidates:
        if cand in available:
            logger.info("Auto-routing model '%s' -> provisioned Groq model '%s'", model_name, cand)
            return cand

    return model_name


def get_groq_client() -> Any:
    """Retrieve or initialize the Groq client instance if API key is present."""
    global _cached_client
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or not api_key.strip():
        return None

    if _cached_client is None:
        try:
            from groq import Groq
            _cached_client = Groq(api_key=api_key.strip())
        except Exception as exc:
            logger.warning("Failed to initialize Groq client: %s", exc)
            return None

    return _cached_client


# Module-level client initialization as requested in specifications
client = get_groq_client()


def _generate_realistic_mock_text(model_name: str, prompt: str, system_prompt: str) -> str:
    """Generate realistic educational mock response tailored to the model tier and prompt."""
    p_lower = prompt.lower()

    # Tier 1: Fast factual recall / vocabulary / definition
    if "llama-3.1-8b" in model_name or "20b" in model_name:
        if "dna" in p_lower:
            return (
                f"[Mock Fallback ({model_name})]: Deoxyribonucleic acid (DNA) is a molecule that carries the "
                "genetic instructions used in the growth, development, functioning, and reproduction of all known "
                "living organisms and many viruses. Most DNA molecules consist of two biopolymer strands coiled around "
                "each other to form a double helix."
            )
        elif "photosynthesis" in p_lower:
            return (
                f"[Mock Fallback ({model_name})]: Photosynthesis is the biochemical process by which green plants and "
                "certain organisms convert solar light energy into chemical energy, synthesizing glucose from carbon "
                "dioxide and water while releasing oxygen."
            )
        elif "speed of light" in p_lower:
            return (
                f"[Mock Fallback ({model_name})]: The speed of light in a vacuum is exactly 299,792,458 meters per "
                "second (approximately 3.00 × 10^8 m/s). Ole Rømer first demonstrated that light travels at a finite "
                "speed in 1676 through observations of Jupiter's moon Io."
            )
        elif "water" in p_lower:
            return (
                f"[Mock Fallback ({model_name})]: Water is composed of two hydrogen atoms covalently bonded to one "
                "oxygen atom, with the chemical formula H2O. It is essential for all known forms of life."
            )
        elif "prove" in p_lower or "induction" in p_lower or "theorem" in p_lower:
            return (
                f"[Mock Fallback ({model_name})]: The arithmetic series sum formula n(n+1)/2 calculates the sum. "
                "For n=1 it equals 1, and for n=2 it equals 3."
            )
        else:
            return (
                f"[Mock Fallback ({model_name})]: Factual summary: {prompt.strip()[:60]}... "
                "Key definition: foundational educational concept."
            )

    # Tier 2: Conceptual Explanation & Synthesis
    elif "qwen" in model_name:
        if "mitosis" in p_lower and "meiosis" in p_lower:
            return (
                f"[Mock Fallback ({model_name})]:\n\n"
                "### Conceptual Synthesis: Mitosis vs. Meiosis\n\n"
                "1. **Biological Purpose**: Mitosis functions for asexual growth, tissue maintenance, and repair in somatic cells. "
                "Meiosis is specialized for gametogenesis in germ cells to enable sexual reproduction.\n"
                "2. **Division Cycles & Daughter Cells**: Mitosis involves one single nuclear division yielding two identical diploid (2n) daughter cells. "
                "Meiosis involves two consecutive nuclear divisions (Meiosis I & II) producing four genetically diverse haploid (n) cells.\n"
                "3. **Genetic Recombination**: Crossing over and independent assortment occur exclusively during Meiosis I, creating genetic variation, "
                "whereas mitosis preserves exact genomic fidelity without recombination."
            )
        elif "absa" in p_lower or "lda" in p_lower:
            return (
                f"[Mock Fallback ({model_name})]:\n\n"
                "### Aspect-Based Sentiment Analysis with LDA\n\n"
                "1. **Preprocessing**: The corpus undergoes tokenization, stop-word removal, POS tagging to identify candidate nouns/noun phrases, and lemmatization.\n"
                "2. **LDA Topic Modeling**: Latent Dirichlet Allocation models documents as mixtures of topics (theta distribution) and topics as distributions over words (phi distribution).\n"
                "3. **Aspect Extraction & Mapping**: Discovered topic clusters are mapped to aspect terms representing targeted entities.\n"
                "4. **Per-Aspect Sentiment Classification**: Context windows surrounding each extracted aspect term are evaluated using a classifier (VADER or Transformer) to determine polarity (positive, negative, or neutral)."
            )
        else:
            return (
                f"[Mock Fallback ({model_name})]:\n\n"
                f"### Structured Conceptual Overview: {prompt[:50]}...\n\n"
                "1. **Core Mechanism**: Explains the fundamental relationships and theoretical framework.\n"
                "2. **Comparative Dynamics**: Evaluates primary distinctions, trade-offs, and curriculum context.\n"
                "3. **Practical Implications**: Illustrates educational applications through concrete structured examples."
            )

    # Tier 3 / Fallback: Frontier-Class Multi-step Reasoning / Proofs / Code
    else:
        if "induction" in p_lower or "prove" in p_lower or "proof" in p_lower:
            return (
                f"[Mock Fallback ({model_name})]:\n\n"
                "### Rigorous Mathematical Proof by Induction\n\n"
                "**Proposition**: For all positive integers n ≥ 1, 1 + 2 + ... + n = n(n + 1)/2.\n\n"
                "**Step 1: Base Case**\n"
                "Let n = 1. LHS = 1. RHS = 1(1 + 1)/2 = 1. Therefore, the base case holds.\n\n"
                "**Step 2: Inductive Hypothesis**\n"
                "Assume the statement holds for an arbitrary positive integer k ≥ 1:\n"
                "1 + 2 + ... + k = k(k + 1)/2.\n\n"
                "**Step 3: Inductive Step**\n"
                "We must prove the statement holds for n = k + 1. Adding (k + 1) to both sides:\n"
                "1 + 2 + ... + k + (k + 1) = [k(k + 1)/2] + (k + 1)\n"
                "= (k + 1) * [k/2 + 1]\n"
                "= (k + 1)(k + 2)/2.\n\n"
                "Hence, because both the base case and inductive step hold, the formula is proven true for all positive integers n by the Principle of Mathematical Induction. Q.E.D."
            )
        elif "code" in p_lower or "python" in p_lower or "binary search" in p_lower:
            return (
                f"[Mock Fallback ({model_name})]:\n\n"
                "### Step-by-Step Algorithmic Implementation\n\n"
                "```python\n"
                "def binary_search(arr: list[int], target: int) -> int:\n"
                "    \"\"\"Perform binary search with O(log n) time complexity.\"\"\"\n"
                "    left, right = 0, len(arr) - 1\n"
                "    while left <= right:\n"
                "        mid = left + (right - left) // 2\n"
                "        if arr[mid] == target:\n"
                "            return mid\n"
                "        elif arr[mid] < target:\n"
                "            left = mid + 1\n"
                "        else:\n"
                "            right = mid - 1\n"
                "    return -1\n"
                "```\n\n"
                "**Analysis**:\n"
                "- Step 1: Initialize two pointers for searching the sorted sequence.\n"
                "- Step 2: In each iteration, divide search space in half, achieving O(log n) time complexity and O(1) space complexity."
            )
        else:
            return (
                f"[Mock Fallback ({model_name})]:\n\n"
                "### Comprehensive Frontier Reasoning Solution\n\n"
                "**Step 1: Problem Decomposition**\n"
                f"Analyzing prompt: '{prompt[:80]}...'\n\n"
                "**Step 2: Methodological Derivation**\n"
                "Applying first-principles multi-step pedagogical reasoning. Hence, we establish the underlying formal mechanics.\n\n"
                "**Step 3: Verification & Conclusion**\n"
                "Therefore, the solution meets all curriculum rigor and pedagogical completeness criteria."
            )


def _mock_generate(
    model_name: str,
    prompt: str,
    system_prompt: str = "",
    start_time: Optional[float] = None,
    note: str = "GROQ_API_KEY not configured",
) -> Dict[str, Any]:
    """Generate safe mock response without throwing unhandled crashes."""
    if start_time is None:
        start_time = time.perf_counter()

    # Small simulated wall-clock delay for realism
    time.sleep(0.005)
    latency_ms = (time.perf_counter() - start_time) * 1000.0

    full_input = f"{system_prompt}\n{prompt}".strip() if system_prompt else prompt
    input_tokens = max(1, len(full_input.split()))

    mock_text = _generate_realistic_mock_text(model_name, prompt, system_prompt)
    output_tokens = max(1, len(mock_text.split()))

    return {
        "text": mock_text,
        "latency_ms": round(latency_ms, 2),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "model": model_name,
        "mock_fallback": True,
    }


def generate(
    model_name: str,
    prompt: str,
    system_prompt: str = "",
) -> Dict[str, Any]:
    """Generate completion using Groq LLM or safe mock fallback.

    Args:
        model_name: Target model identifier ('llama-3.1-8b-instant',
            'qwen/qwen3.8-27b', 'llama-3.3-70b-versatile').
        prompt: User prompt content.
        system_prompt: Optional system prompt instructions.

    Returns:
        dict: {"text": str, "latency_ms": float, "input_tokens": int, "output_tokens": int, "model": str}
    """
    start_time = time.perf_counter()

    # Resolve model alias if provided
    canonical_model = MODEL_ALIASES.get(model_name, model_name)

    # Verify or refresh client
    groq_client = get_groq_client()

    if groq_client is None:
        logger.info(
            "GROQ_API_KEY is not configured or invalid. Using safe mock fallback for %s.",
            canonical_model,
        )
        return _mock_generate(
            model_name=canonical_model,
            prompt=prompt,
            system_prompt=system_prompt,
            start_time=start_time,
            note="Safe mock fallback (GROQ_API_KEY not configured)",
        )

    # Prepare chat completion messages
    messages: List[Dict[str, str]] = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    target_model = resolve_model_for_account(canonical_model, groq_client)

    try:
        response = groq_client.chat.completions.create(
            model=target_model,
            messages=messages,
            max_completion_tokens=MAX_COMPLETION_TOKENS,
        )
        latency_ms = (time.perf_counter() - start_time) * 1000.0

        content = ""
        if response.choices and len(response.choices) > 0:
            content = response.choices[0].message.content or ""

        input_tokens = (
            response.usage.prompt_tokens
            if response.usage and response.usage.prompt_tokens is not None
            else max(1, len((f"{system_prompt} {prompt}").split()))
        )
        output_tokens = (
            response.usage.completion_tokens
            if response.usage and response.usage.completion_tokens is not None
            else max(1, len(content.split()))
        )

        return {
            "text": content,
            "latency_ms": round(latency_ms, 2),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "model": canonical_model,
            "executed_model": target_model,
            "mock_fallback": False,
        }

    except Exception as exc:
        # If target model failed with 404 / model not found, try alternative equivalent models
        if "does not exist" in str(exc) or "404" in str(exc) or getattr(exc, "status_code", None) == 404:
            for alt_model in ARCHITECTURE_EQUIVALENTS.get(canonical_model, []):
                if alt_model != target_model:
                    try:
                        logger.info("Attempting fallback equivalent model '%s' for '%s'", alt_model, target_model)
                        alt_resp = groq_client.chat.completions.create(
                            model=alt_model,
                            messages=messages,
                            max_completion_tokens=MAX_COMPLETION_TOKENS,
                        )
                        latency_ms = (time.perf_counter() - start_time) * 1000.0
                        alt_content = alt_resp.choices[0].message.content or "" if alt_resp.choices else ""
                        in_tok = alt_resp.usage.prompt_tokens if alt_resp.usage and alt_resp.usage.prompt_tokens else max(1, len((f"{system_prompt} {prompt}").split()))
                        out_tok = alt_resp.usage.completion_tokens if alt_resp.usage and alt_resp.usage.completion_tokens else max(1, len(alt_content.split()))
                        return {
                            "text": alt_content,
                            "latency_ms": round(latency_ms, 2),
                            "input_tokens": in_tok,
                            "output_tokens": out_tok,
                            "model": canonical_model,
                            "executed_model": alt_model,
                            "mock_fallback": False,
                        }
                    except Exception:
                        pass

        logger.warning(
            "Encountered error while calling Groq API (%s: %s). Falling back to mock response.",
            exc.__class__.__name__,
            exc,
        )
        return _mock_generate(
            model_name=canonical_model,
            prompt=prompt,
            system_prompt=system_prompt,
            start_time=start_time,
            note=f"Fallback due to {exc.__class__.__name__}",
        )


class ModelClient:
    """Convenience class wrapper for model client invocations."""

    def __init__(self, api_key: Optional[str] = None):
        if api_key:
            os.environ["GROQ_API_KEY"] = api_key
        self.client = get_groq_client()

    def generate(
        self,
        model_name: str,
        prompt: str,
        system_prompt: str = "",
    ) -> Dict[str, Any]:
        return generate(
            model_name=model_name,
            prompt=prompt,
            system_prompt=system_prompt,
        )
