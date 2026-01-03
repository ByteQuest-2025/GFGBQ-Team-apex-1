"""
Citation Service
================
This service checks AI-generated text for citations and validates them.
Uses MOCK logic - no real URL checking or database lookups.
"""

import re
from typing import Any, Dict, List


def extract_citations(text: str) -> List[Dict[str, Any]]:
    """
    Extract citation-like patterns from text.

    Looks for common citation patterns:
    - URLs (http/https)
    - Academic-style citations like [1], (Smith, 2023)
    - Quoted sources like "according to..."

    Args:
        text: The input text to scan for citations

    Returns:
        List of citation dictionaries with text and type
    """
    citations = []

    # Pattern 1: URLs
    url_pattern = r'https?://[^\s<>"\']+|www\.[^\s<>"\']+'
    urls = re.findall(url_pattern, text)
    for url in urls:
        citations.append({"text": url, "type": "url", "position": text.find(url)})

    # Pattern 2: Bracketed references like [1], [2, 3], [Smith 2023]
    bracket_pattern = r"\[([^\]]+)\]"
    brackets = re.findall(bracket_pattern, text)
    for bracket in brackets:
        # Skip if it looks like a URL or code
        if not any(x in bracket.lower() for x in ["http", "www", "://"]):
            citations.append(
                {
                    "text": f"[{bracket}]",
                    "type": "reference",
                    "position": text.find(f"[{bracket}]"),
                }
            )

    # Pattern 3: Parenthetical citations like (Author, Year) or (Author Year)
    paren_pattern = (
        r"\(([A-Z][a-z]+(?:\s+(?:et\s+al\.?|and|&)\s+[A-Z][a-z]+)*[\s,]+\d{4}[a-z]?)\)"
    )
    paren_cites = re.findall(paren_pattern, text)
    for cite in paren_cites:
        citations.append(
            {
                "text": f"({cite})",
                "type": "academic",
                "position": text.find(f"({cite})"),
            }
        )

    return citations


def check_citation_validity(citation: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mock validation of a single citation.

    In a real system, this would:
    - Check if URLs are accessible
    - Verify academic citations against databases
    - Cross-reference with trusted sources

    For this mock version, we use simple heuristics.

    Args:
        citation: Citation dict with text and type

    Returns:
        Citation dict with added validity info
    """
    citation_text = citation.get("text", "")
    citation_type = citation.get("type", "unknown")

    # Mock validation logic based on type
    if citation_type == "url":
        # Mock: Check if URL looks legitimate
        is_valid = _mock_url_check(citation_text)
        reason = (
            "URL structure appears valid"
            if is_valid
            else "URL appears malformed or suspicious"
        )

    elif citation_type == "academic":
        # Mock: Academic citations are assumed valid if properly formatted
        is_valid = True
        reason = "Academic citation format recognized"

    elif citation_type == "reference":
        # Mock: Numbered references are assumed valid
        is_valid = True
        reason = "Reference marker found"

    else:
        is_valid = False
        reason = "Unknown citation type"

    return {
        **citation,
        "is_valid": is_valid,
        "confidence": 0.8 if is_valid else 0.3,  # Mock confidence score
        "reason": reason,
    }


def _mock_url_check(url: str) -> bool:
    """
    Mock URL validation.

    In production, this would make HTTP requests to verify URLs.
    Here we just check for common patterns of legitimate URLs.
    """
    # List of domains we "trust" for mock purposes
    trusted_domains = [
        "wikipedia.org",
        "nature.com",
        "science.org",
        "arxiv.org",
        "github.com",
        "gov",
        ".edu",
        "reuters.com",
        "bbc.com",
        "nytimes.com",
        "who.int",
        "cdc.gov",
        "nih.gov",
    ]

    # Check if URL contains a trusted domain
    url_lower = url.lower()
    for domain in trusted_domains:
        if domain in url_lower:
            return True

    # Basic structure check
    if url.startswith("http") and "." in url and len(url) > 10:
        return True  # Assume valid for mock

    return False


def analyze_citations(text: str) -> Dict[str, Any]:
    """
    Main function to analyze all citations in text.

    This is the primary entry point for the citation service.

    Args:
        text: The AI-generated text to analyze

    Returns:
        Dictionary containing:
        - citations: List of found citations with validity info
        - citation_count: Total number of citations found
        - valid_count: Number of valid citations
        - citation_score: Overall citation quality score (0-100)
    """
    # Extract all citations from text
    citations = extract_citations(text)

    # Validate each citation
    validated_citations = [check_citation_validity(c) for c in citations]

    # Calculate statistics
    total_count = len(validated_citations)
    valid_count = sum(1 for c in validated_citations if c.get("is_valid", False))

    # Calculate citation score
    # - Having citations is good
    # - Having valid citations is better
    # - No citations = neutral (50)
    if total_count == 0:
        citation_score = 50  # Neutral - no citations to verify
        quality_label = "NO_CITATIONS"
    else:
        validity_ratio = valid_count / total_count
        # Score ranges from 40 (all invalid) to 100 (all valid)
        citation_score = int(40 + (validity_ratio * 60))

        if validity_ratio >= 0.8:
            quality_label = "WELL_CITED"
        elif validity_ratio >= 0.5:
            quality_label = "PARTIALLY_CITED"
        else:
            quality_label = "POORLY_CITED"

    return {
        "citations": validated_citations,
        "citation_count": total_count,
        "valid_count": valid_count,
        "citation_score": citation_score,
        "quality_label": quality_label,
    }
