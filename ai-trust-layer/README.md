# AI Trust Layer Backend

A beginner-friendly FastAPI backend that verifies AI-generated content by analyzing claims and citations.

## System Overview

This backend accepts AI-generated text and returns a trust score with detailed explanations:

1. **Claim Extraction** - Breaks text into individual factual claims
2. **Citation Checking** - Identifies and validates any citations in the text
3. **Claim Verification** - Verifies each claim against mock knowledge base
4. **Trust Scoring** - Aggregates results into a 0-100 trust score
5. **Response** - Returns explainable results via REST API

> **Note:** This uses mock/placeholder logic for educational purposes. No real ML models or external APIs are used.

## Project Structure

```
ai-trust-layer/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app, CORS, routes
│   ├── orchestrator.py      # Central workflow controller
│   ├── schemas.py           # Request/response models
│   ├── scoring.py           # Trust score calculation
│   └── services/
│       ├── __init__.py
│       ├── claim_service.py       # Extract claims from text
│       ├── citation_service.py    # Check citations
│       └── verification_service.py # Verify claims
├── requirements.txt
├── Dockerfile
└── README.md
```

## API Endpoints

### POST /verify

Verify AI-generated text and get a trust score.

**Request:**
```json
{
  "text": "The Eiffel Tower is 330 meters tall. Python was created in 1991."
}
```

**Response:**
```json
{
  "trust_score": 75,
  "reliability_label": "MOSTLY RELIABLE",
  "claims": [
    {
      "claim_text": "The Eiffel Tower is 330 meters tall",
      "status": "VERIFIED",
      "reason": "Claim matches known facts in knowledge base"
    },
    {
      "claim_text": "Python was created in 1991",
      "status": "VERIFIED",
      "reason": "Claim matches known facts in knowledge base"
    }
  ],
  "citation_report": {
    "total_citations": 0,
    "valid_citations": 0,
    "citations": []
  }
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "ai-trust-layer"
}
```

## Running Locally

### Prerequisites

- Python 3.10+
- pip

### Installation

1. Clone the repository and navigate to the project:
   ```bash
   cd ai-trust-layer
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. Open your browser and go to:
   - API docs: http://localhost:8000/docs
   - Health check: http://localhost:8000/health

## Running with Docker

### Build the image:
```bash
docker build -t ai-trust-layer .
```

### Run the container:
```bash
docker run -p 8000:8000 ai-trust-layer
```

## Testing the API

Using curl:
```bash
curl -X POST http://localhost:8000/verify \
  -H "Content-Type: application/json" \
  -d '{"text": "The Earth orbits the Sun. Water boils at 100 degrees Celsius."}'
```

Using Python requests:
```python
import requests

response = requests.post(
    "http://localhost:8000/verify",
    json={"text": "The Earth orbits the Sun. Water boils at 100 degrees Celsius."}
)
print(response.json())
```

## Tech Stack

- **Python 3.10+** - Programming language
- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **Docker** - Containerization

## License

MIT License