"""
Verification Service
====================
Mock service that verifies individual claims against a simulated knowledge base.
In production, this would connect to fact-checking APIs or knowledge graphs.
"""

import random
from typing import Literal

# Define possible verification statuses
VerificationStatus = Literal["VERIFIED", "CONTRADICTED", "UNKNOWN"]


# Mock knowledge base of "known facts" for demonstration
MOCK_KNOWLEDGE_BASE = {
    "earth": {"fact": "Earth is round", "verified": True},
    "sun": {"fact": "The Sun is a star", "verified": True},
    "water": {"fact": "Water boils at 100°C at sea level", "verified": True},
    "moon": {"fact": "The Moon orbits Earth", "verified": True},
    "python": {"fact": "Python is a programming language", "verified": True},
    "gravity": {"fact": "Gravity pulls objects toward each other", "verified": True},
}

# Keywords that might indicate false claims (for mock purposes)
CONTRADICTION_KEYWORDS = ["never", "impossible", "fake", "myth", "false"]


def verify_single_claim(claim_text: str) -> dict:
    """
    Verify a single claim using mock logic.

    Args:
        claim_text: The claim text to verify

    Returns:
        Dictionary with status, confidence, and reason
    """
    claim_lower = claim_text.lower()

    # Check for contradiction keywords (mock logic)
    for keyword in CONTRADICTION_KEYWORDS:
        if keyword in claim_lower:
            return {
                "status": "CONTRADICTED",
                "confidence": random.uniform(0.6, 0.9),
                "reason": f"Claim contains potentially misleading language ('{keyword}')",
            }

    # Check against mock knowledge base
    for key, data in MOCK_KNOWLEDGE_BASE.items():
        if key in claim_lower:
            return {
                "status": "VERIFIED",
                "confidence": random.uniform(0.75, 0.95),
                "reason": f"Claim aligns with known fact: '{data['fact']}'",
            }

    # Default: Unknown - cannot verify with available data
    return {
        "status": "UNKNOWN",
        "confidence": random.uniform(0.3, 0.5),
        "reason": "Insufficient data to verify this claim",
    }


def verify_claims(claims: list[dict]) -> list[dict]:
    """
    Verify a list of claims.

    Args:
        claims: List of claim dictionaries with 'text' field

    Returns:
        List of claims with verification results added
    """
    verified_claims = []

    for claim in claims:
        claim_text = claim.get("text", "")

        # Get verification result
        verification = verify_single_claim(claim_text)

        # Build enriched claim object
        verified_claim = {
            "text": claim_text,
            "index": claim.get("index", 0),
            "status": verification["status"],
            "confidence": round(verification["confidence"], 2),
            "reason": verification["reason"],
            # Preserve citation info if present
            "has_citation": claim.get("has_citation", False),
            "citation_valid": claim.get("citation_valid", None),
        }

        verified_claims.append(verified_claim)

    return verified_claims


def get_verification_summary(verified_claims: list[dict]) -> dict:
    """
    Generate a summary of verification results.

    Args:
        verified_claims: List of verified claim dictionaries

    Returns:
        Summary statistics dictionary
    """
    total = len(verified_claims)

    if total == 0:
        return {
            "total_claims": 0,
            "verified_count": 0,
            "contradicted_count": 0,
            "unknown_count": 0,
            "verification_rate": 0.0,
        }

    verified_count = sum(1 for c in verified_claims if c["status"] == "VERIFIED")
    contradicted_count = sum(
        1 for c in verified_claims if c["status"] == "CONTRADICTED"
    )
    unknown_count = sum(1 for c in verified_claims if c["status"] == "UNKNOWN")

    return {
        "total_claims": total,
        "verified_count": verified_count,
        "contradicted_count": contradicted_count,
        "unknown_count": unknown_count,
        "verification_rate": round(verified_count / total, 2),
    }
