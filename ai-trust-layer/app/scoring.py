"""
Scoring Module
--------------
Calculates the overall trust score based on claim verification results.
Uses a simple weighted average approach for beginner-friendliness.
"""

from typing import Any, Dict, List

# Status weights for scoring (higher = more trustworthy)
STATUS_WEIGHTS = {
    "VERIFIED": 100,  # Claim appears to be true
    "UNKNOWN": 50,  # Cannot determine truth
    "CONTRADICTED": 0,  # Claim appears to be false
}


def calculate_trust_score(verified_claims: List[Dict[str, Any]]) -> int:
    """
    Calculate overall trust score from verified claims.

    Args:
        verified_claims: List of claims with their verification status

    Returns:
        Trust score from 0 to 100
    """
    # Handle edge case: no claims found
    if not verified_claims:
        return 50  # Neutral score when nothing to verify

    # Calculate weighted average of all claim scores
    total_score = 0
    for claim in verified_claims:
        status = claim.get("status", "UNKNOWN")
        total_score += STATUS_WEIGHTS.get(status, 50)

    # Return average score (integer)
    return total_score // len(verified_claims)


def get_reliability_label(trust_score: int) -> str:
    """
    Convert numeric trust score to human-readable label.

    Args:
        trust_score: Score from 0 to 100

    Returns:
        Human-readable reliability label
    """
    if trust_score >= 80:
        return "HIGH - Content appears reliable"
    elif trust_score >= 60:
        return "MEDIUM - Some claims need verification"
    elif trust_score >= 40:
        return "LOW - Multiple unverified claims"
    else:
        return "VERY LOW - Content contains contradicted claims"


def get_score_breakdown(verified_claims: List[Dict[str, Any]]) -> Dict[str, int]:
    """
    Get count of claims by status for transparency.

    Args:
        verified_claims: List of claims with their verification status

    Returns:
        Dictionary with counts per status
    """
    breakdown = {
        "verified_count": 0,
        "contradicted_count": 0,
        "unknown_count": 0,
        "total_claims": len(verified_claims),
    }

    for claim in verified_claims:
        status = claim.get("status", "UNKNOWN")
        if status == "VERIFIED":
            breakdown["verified_count"] += 1
        elif status == "CONTRADICTED":
            breakdown["contradicted_count"] += 1
        else:
            breakdown["unknown_count"] += 1

    return breakdown
