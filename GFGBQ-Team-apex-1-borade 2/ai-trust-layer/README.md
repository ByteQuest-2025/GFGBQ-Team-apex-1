# AI Trust Layer Backend

A beginner-friendly FastAPI backend that verifies AI-generated content by analyzing claims and citations.

## System Overview

This backend accepts AI-generated text and returns a trust score with detailed explanations:

1. *Claim Extraction* - Breaks text into individual factual claims
2. *Citation Checking* - Identifies and validates any citations in the text
3. *Claim Verification* - Verifies each claim against mock knowledge base
4. *Trust Scoring* - Aggregates results into a 0-100 trust score
5. *Response* - Returns explainable results via REST API

> *Note:* This uses mock/placeholder logic for educational purposes. No real ML models or external APIs are used.

## Project Structure


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


## API Endpoints

### POST /verify

Verify AI-generated text and get a trust score.

*Request:*
json
{
  "text": "The Eiffel Tower is 330 meters tall. Python was created in 1991."
}
### Summary 
The system acts as an automated "fact-checker" through five distinct stages:
•	1. Claim Extraction (The Breakdown): The engine uses Natural Language Processing (NLP) to dissect a paragraph into specific, testable assertions (e.g., names, dates, or scientific facts).
•	2. Citation Checking (The Source Audit): It isolates any provided references, checking for "dead links," valid DOIs (Digital Object Identifiers), and source authority (e.g., .gov or .edu domains).
•	3. Claim Verification (The Cross-Reference): Each individual claim is compared against a trusted knowledge base to see if the information is supported or contradicted.
•	4. Trust Scoring (The Final Grade): It aggregates the findings from the previous steps into a single Trust Score (0–100), providing a clear "Red/Yellow/Green" signal to the user.
•	5. Response (The Integration): Finally, it delivers these results via a REST API, ensuring the data is not only verified but also explainable—showing exactly why a piece of information was flagged.

### Installation

1. Clone the repository and navigate to the project:
   bash
   cd ai-trust-layer
2. Create a virtual environment (optional but recommended):
   bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install dependencies:
   bash
   pip install -r requirements.txt
4. Run the server:
   bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
5. Open your browser and go to:
   - API docs: http://localhost:8000/docs
   - Health check: http://localhost:8000/health

## Running with Docker

### Build the image:
bash
docker build -t ai-trust-layer .


### Run the container:
bash
docker run -p 8000:8000 ai-trust-layer


## Testing the API

Using curl:
bash
curl -X POST http://localhost:8000/verify \
  -H "Content-Type: application/json" \
  -d '{"text": "The Earth orbits the Sun. Water boils at 100 degrees Celsius."}'

Using Python requests:
python
import requests
response = requests.post(
    "http://localhost:8000/verify",
    json={"text": "The Earth orbits the Sun. Water boils at 100 degrees Celsius."}
)
print(response.json())

## Tech Stack
- *Python 3.10+* - Programming language
- *FastAPI* - Web framework
- *Uvicorn* - ASGI server
- *Pydantic* - Data validation
- *Docker* - Containerization
