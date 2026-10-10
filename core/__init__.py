"""Core routing, classification, and verification components."""

from core.classifier import EducationalQueryClassifier
from core.verifier import LightweightVerifier, VerificationResult

__all__ = [
    "EducationalQueryClassifier",
    "LightweightVerifier",
    "VerificationResult",
]
