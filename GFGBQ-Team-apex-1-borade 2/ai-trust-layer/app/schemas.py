"""
Pydantic schemas for request/response models.
These define the structure of data flowing through the API.
"""

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

# ============================================
# Enums for Status Values
# ============================================


class ClaimStatus(str, Enum):
    """Possible verification statuses for a claim."""

    VERIFIED = "VERIFIED"
    CONTRADICTED = "CONTRADICTED"
    UNKNOWN = "UNKNOWN"


class ReliabilityLabel(str, Enum):
    """Human-readable reliability labels based on trust score."""

    HIGHLY_RELIABLE = "HIGHLY_RELIABLE"
    MOSTLY_RELIABLE = "MOSTLY_RELIABLE"
    QUESTIONABLE = "QUESTIONABLE"
    UNRELIABLE = "UNRELIABLE"


# ============================================
# Request Models
# ============================================


class VerifyRequest(BaseModel):
    """
    Input model for the /verify endpoint.
    Contains the AI-generated text to be verified.
    """

    text: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="The AI-generated text to verify",
        examples=[
            "The Eiffel Tower was built in 1889 and is located in Paris, France."
        ],
    )


# ============================================
# Internal Models (used between services)
# ============================================


class Claim(BaseModel):
    """Internal representation of an extracted claim."""

    text: str = Field(..., description="The extracted factual claim text")
    index: int = Field(default=0, description="Position of claim in original text")
    has_citation: bool = Field(
        default=False, description="Whether a citation was found for this claim"
    )
    citation_valid: Optional[bool] = Field(
        default=None, description="Whether the citation is valid (if present)"
    )


class VerifiedClaim(BaseModel):
    """Claim after verification process."""

    text: str = Field(..., description="The claim text")
    index: int = Field(default=0, description="Position in original text")
    status: ClaimStatus = Field(..., description="Verification status")
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Confidence score (0.0 to 1.0)"
    )
    reason: str = Field(..., description="Explanation for the verification result")
    has_citation: bool = Field(default=False, description="Whether citation exists")
    citation_valid: Optional[bool] = Field(
        default=None, description="Citation validity"
    )
    wikipedia_source: Optional[str] = Field(
        default=None, description="Wikipedia article used for verification"
    )
    wikipedia_snippet: Optional[str] = Field(
        default=None, description="Relevant snippet from Wikipedia"
    )


# ============================================
# Response Models
# ============================================


class ClaimResult(BaseModel):
    """
    Result for a single claim in the API response.
    Contains the claim, its verification status, and reasoning.
    """

    claim_text: str = Field(..., description="The extracted factual claim")
    status: ClaimStatus = Field(
        ..., description="Verification status: VERIFIED, CONTRADICTED, or UNKNOWN"
    )
    reason: str = Field(
        ..., description="Brief explanation for the verification result"
    )
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Confidence score for this claim (0.0 to 1.0)"
    )
    has_citation: bool = Field(
        default=False, description="Whether a citation was found for this claim"
    )
    wikipedia_source: Optional[str] = Field(
        default=None, description="Wikipedia article title used for verification"
    )
    wikipedia_snippet: Optional[str] = Field(
        default=None, description="Relevant excerpt from Wikipedia article"
    )


class VerifyResponse(BaseModel):
    """
    Output model for the /verify endpoint.
    Contains the overall trust score, reliability label, and detailed claim results.
    """

    trust_score: int = Field(
        ..., ge=0, le=100, description="Overall trust score from 0 to 100"
    )
    reliability_label: ReliabilityLabel = Field(
        ..., description="Human-readable reliability classification"
    )
    total_claims: int = Field(..., ge=0, description="Total number of claims extracted")
    verified_count: int = Field(..., ge=0, description="Number of verified claims")
    contradicted_count: int = Field(
        ..., ge=0, description="Number of contradicted claims"
    )
    unknown_count: int = Field(
        ..., ge=0, description="Number of claims with unknown status"
    )
    claims: List[ClaimResult] = Field(
        ..., description="List of individual claim verification results"
    )


class HealthResponse(BaseModel):
    """Response model for the /health endpoint."""

    status: str = Field(default="healthy", description="Service health status")
    service: str = Field(default="ai-trust-layer", description="Service name")
    version: str = Field(default="1.0.0", description="API version")
