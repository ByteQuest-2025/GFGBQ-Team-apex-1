"""
Claim Extraction Service
------------------------
This service breaks AI-generated text into individual factual claims.
Uses mock/placeholder logic - no real NLP models.
"""

import re
from typing import List


def extract_claims(text: str) -> List[str]:
    """
    Extract factual claims from AI-generated text.

    In a real system, this would use NLP models to identify
    and extract factual statements. Here we use simple rules:
    - Split by sentences
    - Filter out questions and very short sentences
    - Keep statements that look like factual claims

    Args:
        text: The AI-generated text to analyze

    Returns:
        List of extracted claim strings
    """
    if not text or not text.strip():
        return []

    # Simple sentence splitting (handles ., !, ?)
    # In production, use proper NLP sentence tokenizer
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())

    claims = []
    for sentence in sentences:
        sentence = sentence.strip()

        # Skip empty or very short sentences
        if len(sentence) < 10:
            continue

        # Skip questions (not factual claims)
        if sentence.endswith("?"):
            continue

        # Skip sentences that are clearly opinions (mock logic)
        opinion_markers = ["i think", "i believe", "in my opinion", "maybe", "perhaps"]
        if any(marker in sentence.lower() for marker in opinion_markers):
            continue

        # Keep sentences that contain factual indicators (mock heuristic)
        # In reality, this would be much more sophisticated
        factual_indicators = [
            "is",
            "are",
            "was",
            "were",
            "has",
            "have",
            "had",
            "percent",
            "%",
            "million",
            "billion",
            "year",
            "founded",
            "located",
            "discovered",
            "invented",
            "created",
            "published",
        ]

        # If sentence contains numbers or factual indicators, likely a claim
        has_numbers = bool(re.search(r"\d+", sentence))
        has_factual_words = any(word in sentence.lower() for word in factual_indicators)

        if has_numbers or has_factual_words or len(sentence) > 30:
            claims.append(sentence)

    # If no claims found but text exists, treat whole text as one claim
    if not claims and text.strip():
        claims = [text.strip()[:500]]  # Limit length

    return claims


def count_claims(text: str) -> int:
    """
    Quick count of claims without full extraction.

    Args:
        text: The AI-generated text

    Returns:
        Number of claims found
    """
    return len(extract_claims(text))
