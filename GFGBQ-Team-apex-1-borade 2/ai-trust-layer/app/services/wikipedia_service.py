"""
Wikipedia Service
=================
This service verifies claims by searching Wikipedia for relevant information.
Uses the Wikipedia API to fetch real data for fact-checking.
"""

import re
from typing import Any, Dict, List, Optional

import requests

# Wikipedia API endpoint
WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"

# Request timeout in seconds
REQUEST_TIMEOUT = 10

# Headers for API requests
HEADERS = {"User-Agent": "AITrustLayer/1.0 (Educational Project; Python/requests)"}


def search_wikipedia(query: str, limit: int = 3) -> List[Dict[str, Any]]:
    """
    Search Wikipedia for articles matching the query.

    Args:
        query: Search term
        limit: Maximum number of results to return

    Returns:
        List of search results with title and snippet
    """
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srlimit": limit,
        "format": "json",
        "utf8": 1,
    }

    try:
        response = requests.get(
            WIKIPEDIA_API_URL, params=params, headers=HEADERS, timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        data = response.json()

        results = []
        for item in data.get("query", {}).get("search", []):
            # Clean HTML tags from snippet
            snippet = re.sub(r"<[^>]+>", "", item.get("snippet", ""))
            results.append(
                {
                    "title": item.get("title", ""),
                    "snippet": snippet,
                    "page_id": item.get("pageid"),
                }
            )
        return results

    except requests.exceptions.RequestException as e:
        print(f"Wikipedia search error: {e}")
        return []
    except Exception as e:
        print(f"Wikipedia search unexpected error: {e}")
        return []


def get_wikipedia_summary(title: str) -> Optional[str]:
    """
    Get the summary/extract of a Wikipedia article.

    Args:
        title: Wikipedia article title

    Returns:
        Article summary text or None if not found
    """
    params = {
        "action": "query",
        "titles": title,
        "prop": "extracts",
        "exintro": True,  # Only get intro section
        "explaintext": True,  # Plain text, no HTML
        "format": "json",
        "utf8": 1,
    }

    try:
        response = requests.get(
            WIKIPEDIA_API_URL, params=params, headers=HEADERS, timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        data = response.json()

        pages = data.get("query", {}).get("pages", {})
        for page_id, page_data in pages.items():
            if page_id != "-1":  # -1 means page not found
                return page_data.get("extract", "")
        return None

    except requests.exceptions.RequestException as e:
        print(f"Wikipedia summary error: {e}")
        return None
    except Exception as e:
        print(f"Wikipedia summary unexpected error: {e}")
        return None


def extract_main_subject(claim: str) -> str:
    """
    Extract the main subject/topic from a claim for Wikipedia search.

    This focuses on finding proper nouns and key entities.

    Args:
        claim: The claim text

    Returns:
        Main search term
    """
    # Common words to filter out
    stop_words = {
        "the",
        "a",
        "an",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "being",
        "have",
        "has",
        "had",
        "do",
        "does",
        "did",
        "will",
        "would",
        "could",
        "should",
        "may",
        "might",
        "must",
        "shall",
        "can",
        "to",
        "of",
        "in",
        "for",
        "on",
        "with",
        "at",
        "by",
        "from",
        "as",
        "into",
        "through",
        "during",
        "before",
        "after",
        "above",
        "below",
        "between",
        "and",
        "but",
        "or",
        "not",
        "no",
        "yes",
        "this",
        "that",
        "these",
        "those",
        "it",
        "its",
        "his",
        "her",
        "their",
        "our",
        "my",
        "your",
        "who",
        "which",
        "what",
        "where",
        "when",
        "why",
        "how",
        "all",
        "each",
        "every",
        "both",
        "few",
        "more",
        "most",
        "other",
        "some",
        "such",
        "only",
        "own",
        "same",
        "so",
        "than",
        "too",
        "very",
        "just",
        "also",
        "built",
        "made",
        "created",
        "located",
        "found",
        "discovered",
        "invented",
        "developed",
        "known",
        "called",
        "named",
        "memory",
        "honor",
        "wife",
        "husband",
        "son",
        "daughter",
        "father",
        "mother",
    }

    # Try to find proper nouns (sequences of capitalized words)
    # This pattern finds things like "Taj Mahal", "Shah Jahan", "Albert Einstein"
    proper_noun_pattern = r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b"
    proper_nouns = re.findall(proper_noun_pattern, claim)

    # Filter out single common words that might be capitalized at sentence start
    proper_nouns = [pn for pn in proper_nouns if pn.lower() not in stop_words]

    if proper_nouns:
        # Return the first (likely main subject) proper noun
        return proper_nouns[0]

    # Fallback: extract significant words
    words = re.findall(r"\b[A-Za-z]+\b", claim)
    significant = [w for w in words if w.lower() not in stop_words and len(w) > 3]

    if significant:
        return " ".join(significant[:2])

    return claim[:50]  # Last resort: first 50 chars


def extract_verification_terms(claim: str) -> List[str]:
    """
    Extract terms from the claim that we should look for in Wikipedia content.

    Args:
        claim: The claim text

    Returns:
        List of terms to verify against Wikipedia
    """
    stop_words = {
        "the",
        "a",
        "an",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "being",
        "have",
        "has",
        "had",
        "do",
        "does",
        "did",
        "will",
        "would",
        "could",
        "should",
        "to",
        "of",
        "in",
        "for",
        "on",
        "with",
        "at",
        "by",
        "from",
        "and",
        "but",
        "or",
        "not",
        "this",
        "that",
        "it",
        "its",
        "his",
        "her",
    }

    # Find all proper nouns
    proper_nouns = re.findall(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b", claim)

    # Find numbers/years
    numbers = re.findall(r"\b(\d{4}|\d+)\b", claim)

    # Find other significant words
    words = re.findall(r"\b[A-Za-z]+\b", claim)
    significant = [w for w in words if w.lower() not in stop_words and len(w) > 3]

    # Combine all terms
    all_terms = proper_nouns + numbers + significant

    # Remove duplicates while preserving order
    seen = set()
    unique_terms = []
    for term in all_terms:
        term_lower = term.lower()
        if term_lower not in seen:
            seen.add(term_lower)
            unique_terms.append(term)

    return unique_terms


def check_claim_against_wikipedia(claim: str) -> Dict[str, Any]:
    """
    Verify a claim by checking Wikipedia.

    Args:
        claim: The claim text to verify

    Returns:
        Dictionary with verification result
    """
    # Step 1: Extract the main subject for searching
    main_subject = extract_main_subject(claim)

    if not main_subject:
        return {
            "status": "UNKNOWN",
            "confidence": 0.3,
            "reason": "Could not extract searchable subject from claim",
            "wikipedia_source": None,
            "wikipedia_snippet": None,
        }

    print(f"[Wikipedia] Searching for: '{main_subject}'")

    # Step 2: Search Wikipedia
    search_results = search_wikipedia(main_subject)

    if not search_results:
        # Try a broader search with just the first word if it's a proper noun
        fallback = main_subject.split()[0] if " " in main_subject else None
        if fallback:
            print(f"[Wikipedia] Trying fallback search: '{fallback}'")
            search_results = search_wikipedia(fallback)

    if not search_results:
        return {
            "status": "UNKNOWN",
            "confidence": 0.3,
            "reason": f"No Wikipedia articles found for: '{main_subject}'",
            "wikipedia_source": None,
            "wikipedia_snippet": None,
        }

    # Step 3: Get the summary of the top result
    top_result = search_results[0]
    print(f"[Wikipedia] Found article: '{top_result['title']}'")

    summary = get_wikipedia_summary(top_result["title"])

    if not summary:
        # Use the search snippet as fallback
        summary = top_result.get("snippet", "")

    if not summary:
        return {
            "status": "UNKNOWN",
            "confidence": 0.4,
            "reason": f"Found article '{top_result['title']}' but could not retrieve content",
            "wikipedia_source": top_result["title"],
            "wikipedia_snippet": None,
        }

    # Step 4: Extract terms to verify from the claim
    verification_terms = extract_verification_terms(claim)
    print(f"[Wikipedia] Verification terms: {verification_terms}")

    # Step 5: Check how many terms appear in Wikipedia content
    summary_lower = summary.lower()

    matches = []
    for term in verification_terms:
        if term.lower() in summary_lower:
            matches.append(term)

    match_count = len(matches)
    total_terms = len(verification_terms)
    match_ratio = match_count / total_terms if total_terms > 0 else 0

    print(f"[Wikipedia] Matches found: {matches}")
    print(f"[Wikipedia] Match ratio: {match_ratio:.2f}")

    # Step 6: Determine verification status
    snippet = summary[:500] + "..." if len(summary) > 500 else summary

    if match_ratio >= 0.5:
        # Good match - claim appears to be supported
        confidence = min(0.6 + (match_ratio * 0.3), 0.95)
        return {
            "status": "VERIFIED",
            "confidence": round(confidence, 2),
            "reason": f"Claim supported by Wikipedia article '{top_result['title']}'. Found terms: {', '.join(matches)}",
            "wikipedia_source": top_result["title"],
            "wikipedia_snippet": snippet,
        }
    elif match_ratio >= 0.25:
        # Partial match
        return {
            "status": "UNKNOWN",
            "confidence": 0.5,
            "reason": f"Partial match in Wikipedia article '{top_result['title']}'. Found terms: {', '.join(matches) if matches else 'none'}",
            "wikipedia_source": top_result["title"],
            "wikipedia_snippet": snippet,
        }
    else:
        # Low match - claim might be incorrect or unrelated
        main_subject_found = main_subject.lower() in summary_lower

        if main_subject_found:
            return {
                "status": "UNKNOWN",
                "confidence": 0.4,
                "reason": f"Found '{main_subject}' in Wikipedia but claim details could not be verified",
                "wikipedia_source": top_result["title"],
                "wikipedia_snippet": snippet,
            }
        else:
            return {
                "status": "UNKNOWN",
                "confidence": 0.3,
                "reason": f"Claim could not be verified against Wikipedia article '{top_result['title']}'",
                "wikipedia_source": top_result["title"],
                "wikipedia_snippet": snippet,
            }


def verify_claims_with_wikipedia(claims: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Verify a list of claims using Wikipedia.

    Args:
        claims: List of claim dictionaries with 'text' field

    Returns:
        List of claims with Wikipedia verification results
    """
    verified_claims = []

    for claim in claims:
        claim_text = claim.get("text", "")

        # Get Wikipedia verification
        wiki_result = check_claim_against_wikipedia(claim_text)

        # Build enriched claim object
        verified_claim = {
            "text": claim_text,
            "index": claim.get("index", 0),
            "status": wiki_result["status"],
            "confidence": wiki_result["confidence"],
            "reason": wiki_result["reason"],
            "has_citation": claim.get("has_citation", False),
            "citation_valid": claim.get("citation_valid", None),
            "wikipedia_source": wiki_result.get("wikipedia_source"),
            "wikipedia_snippet": wiki_result.get("wikipedia_snippet"),
        }

        verified_claims.append(verified_claim)

    return verified_claims
