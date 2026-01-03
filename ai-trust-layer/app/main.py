"""
AI Trust Layer - Main FastAPI Application
=========================================
This is the entry point of the application.
It sets up the FastAPI app, CORS middleware, and defines the API routes.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.orchestrator import process_text
from app.schemas import HealthResponse, VerifyRequest, VerifyResponse

# ============================================
# Create FastAPI Application
# ============================================

app = FastAPI(
    title="AI Trust Layer",
    description="A backend service to verify AI-generated content and provide trust scores",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc alternative docs
)

# ============================================
# Configure CORS Middleware
# ============================================
# CORS allows the API to be called from web browsers on different domains.
# This is essential for web deployment where frontend and backend
# might be hosted on different origins.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific domains
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


# ============================================
# API Routes
# ============================================


@app.get("/", tags=["Info"])
async def root():
    """
    Root endpoint providing basic API information.
    Useful for quick verification that the API is running.
    """
    return {
        "service": "AI Trust Layer",
        "version": "1.0.0",
        "description": "Verify AI-generated content for factual accuracy",
        "endpoints": {
            "POST /verify": "Verify AI-generated content",
            "GET /health": "Check service health",
            "GET /docs": "API documentation (Swagger UI)",
        },
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint.

    Returns the service status - useful for:
    - Container orchestration (Kubernetes, Docker Swarm)
    - Load balancers
    - Monitoring systems
    """
    return HealthResponse(status="healthy", service="ai-trust-layer", version="1.0.0")


@app.post("/verify", response_model=VerifyResponse, tags=["Verification"])
async def verify_content(request: VerifyRequest):
    """
    Main verification endpoint.

    Accepts AI-generated text and returns:
    - trust_score: 0-100 indicating overall reliability
    - reliability_label: Human-readable classification
    - claims: List of extracted claims with verification details

    Workflow:
    1. Extract factual claims from the text
    2. Check for citations and validate them
    3. Verify each claim against knowledge base
    4. Calculate aggregate trust score
    5. Return detailed results
    """
    # Validate input
    if not request.text or not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Text cannot be empty. Please provide AI-generated content to verify.",
        )

    # Process the text through our verification pipeline
    # The orchestrator coordinates all services
    try:
        result = process_text(request.text)
        return result
    except Exception as e:
        # Log the error in production
        raise HTTPException(
            status_code=500, detail=f"An error occurred during verification: {str(e)}"
        )


# ============================================
# Application Startup Event (Optional)
# ============================================


@app.on_event("startup")
async def startup_event():
    """
    Runs when the application starts.
    Useful for initialization tasks.
    """
    print("🚀 AI Trust Layer API starting up...")
    print("📚 Documentation available at /docs")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Runs when the application shuts down.
    Useful for cleanup tasks.
    """
    print("👋 AI Trust Layer API shutting down...")
