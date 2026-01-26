# AI Business Analyst Assistant

**Production-grade AI service with observability, MLOps, CI/CD, and cloud deployment**

---

## Overview

The **AI Business Analyst Assistant** is a production-ready AI system that answers business questions from structured data using a Large Language Model (LLM).

Unlike typical AI demos or notebooks, this project focuses on **how AI systems are built, deployed, observed, and operated in real production environments**.

The goal is not just to generate answers, but to make AI **traceable, debuggable, auditable, and reliable**.

---

## What the System Does

The system exposes a REST API that:

1. Loads structured business data (sales dataset)
2. Computes a deterministic analytical summary
3. Builds a controlled prompt from that summary
4. Queries an LLM to generate a business insight
5. Returns the answer via an API
6. Tracks the entire AI decision lifecycle

### Example

**Request**
```json
{
  "question": "Which region is underperforming?"
}

## Example Response

```json
{
  "request_id": "e8b4c5f2-6a4b-4d6c-9b89-8d2b8f3a7c21",
  "insight": "Asia shows lower total revenue compared to other regions..."
}

## Architecture Overview

Client (Swagger / API Consumer)
        |
        v
FastAPI Application
        |
        v
Business Logic Layer
  - Data loading
  - Data aggregation
  - Summary generation
  - Prompt construction
        |
        v
LLM (OpenAI API)
        |
        v
Observability Layer
  - Structured logs (request_id)
  - MLflow tracking
  - Latency metrics
  - Output artifacts

## Project Structure

enterprise_ai_assistant/
│
├── app/
│   ├── api.py                # FastAPI routes
│   ├── business_analyst.py   # Core data + AI logic
│   ├── mlflow_config.py      # MLflow initialization
│   ├── config.py             # Application configuration
│   └── logger.py             # Structured logging setup
│
├── data/
│   └── sales_data.csv
│
├── tests/
│   └── test_health.py        # API health test
│
├── .github/workflows/
│   └── ci.yml                # CI pipeline
│
├── Dockerfile
├── requirements.txt
├── pytest.ini
└── README.md
