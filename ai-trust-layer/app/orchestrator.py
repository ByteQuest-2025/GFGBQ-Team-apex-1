"""
Orchestrator Module
-------------------
This is the central workflow controller that coordinates all services.
It manages the flow: text → claims → citation check → verification → scoring
"""

from typing import Any, Dict, List

from app import scoring
from app.schemas import ClaimResult, ClaimStatus, ReliabilityLabel, VerifyResponse
from app.services import citation_service, claim_service, verification_service


class TrustOrchestrator:
    """
    Central orchestrator that coordinates the verification workflow.

    This class manages the entire process of:
    1. Extracting claims from text
    2. Checking citations
    3. Verifying each claim
    4. Calculating the trust score
    """

    def process(self, text: str) -> VerifyResponse:
        """
        Main orchestration method that processes AI-generated text.

        Args:
            text: The AI-generated text to verify

        Returns:
            VerifyResponse containing trust score, label, and claim details
        """
        # Step 1: Extract factual claims from the text
        extracted_claims = claim_service.extract_claims(text)

        # Step 2: Analyze citations in the text
        citation_analysis = citation_service.analyze_citations(text)
        citation_map = self._build_citation_map(citation_analysis)

        # Step 3: Build claim objects with citation info
        claims_with_citations = []
        for idx, claim_text in enumerate(extracted_claims):
            # Check if this claim has a citation nearby (simplified logic)
            has_citation = self._claim_has_citation(claim_text, citation_map)
            claims_with_citations.append(
                {
                    "text": claim_text,
                    "index": idx,
                    "has_citation": has_citation,
                    "citation_valid": citation_map.get("has_valid", False)
                    if has_citation
                    else None,
                }
            )

        # Step 4: Verify each claim
        verified_claims = verification_service.verify_claims(claims_with_citations)

        # Step 5: Calculate trust score
        trust_score = scoring.calculate_trust_score(verified_claims)

        # Step 6: Get reliability label based on score
        reliability_label = self._get_reliability_label(trust_score)

        # Step 7: Get breakdown statistics
        breakdown = scoring.get_score_breakdown(verified_claims)

        # Step 8: Build claim results for response
        claim_results = self._build_claim_results(verified_claims)

        # Step 9: Build and return the final response
        return VerifyResponse(
            trust_score=trust_score,
            reliability_label=reliability_label,
            total_claims=breakdown["total_claims"],
            verified_count=breakdown["verified_count"],
            contradicted_count=breakdown["contradicted_count"],
            unknown_count=breakdown["unknown_count"],
            claims=claim_results,
        )

    def _build_citation_map(self, citation_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build a map of citation information for quick lookup.
        """
        return {
            "citations": citation_analysis.get("citations", []),
            "has_citations": citation_analysis.get("citation_count", 0) > 0,
            "has_valid": citation_analysis.get("valid_count", 0) > 0,
            "citation_score": citation_analysis.get("citation_score", 50),
        }

    def _claim_has_citation(
        self, claim_text: str, citation_map: Dict[str, Any]
    ) -> bool:
        """
        Check if a claim appears to have a citation.
        This is simplified mock logic - in reality would be more sophisticated.
        """
        # If there are citations in the text, assume some claims are cited
        # This is a simplification for the mock implementation
        if not citation_map.get("has_citations", False):
            return False

        # Check if claim contains citation markers
        citation_markers = ["[", "(", "http", "www", "according to", "source:"]
        claim_lower = claim_text.lower()
        return any(marker in claim_lower for marker in citation_markers)

    def _get_reliability_label(self, trust_score: int) -> ReliabilityLabel:
        """
        Convert numeric trust score to reliability label enum.
        """
        if trust_score >= 80:
            return ReliabilityLabel.HIGHLY_RELIABLE
        elif trust_score >= 60:
            return ReliabilityLabel.MOSTLY_RELIABLE
        elif trust_score >= 40:
            return ReliabilityLabel.QUESTIONABLE
        else:
            return ReliabilityLabel.UNRELIABLE

    def _build_claim_results(
        self, verified_claims: List[Dict[str, Any]]
    ) -> List[ClaimResult]:
        """
        Convert verified claim dictionaries to ClaimResult schema objects.
        """
        results = []
        for claim in verified_claims:
            # Map status string to enum
            status_str = claim.get("status", "UNKNOWN")
            status = ClaimStatus(status_str)

            result = ClaimResult(
                claim_text=claim.get("text", ""),
                status=status,
                reason=claim.get("reason", "No reason provided"),
                confidence=claim.get("confidence", 0.5),
                has_citation=claim.get("has_citation", False),
            )
            results.append(result)

        return results


# For backwards compatibility, also provide a function interface
def process_text(text: str) -> VerifyResponse:
    """
    Convenience function to process text without instantiating orchestrator.
    """
    orchestrator = TrustOrchestrator()
    return orchestrator.process(text)
