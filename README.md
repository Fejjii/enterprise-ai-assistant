# AI Business Analyst Assistant

**Production-grade AI service with observability, MLOps, CI/CD, and cloud deployment**

---

## Overview

The **AI Business Analyst Assistant** is a production-ready AI application that answers business questions from structured data using a Large Language Model (LLM).

Unlike typical AI demos or notebooks, this project is built to demonstrate **how real AI systems are engineered, deployed, observed, and operated in production**.

The focus is not only on generating answers, but on making AI systems:

- Traceable
- Debuggable
- Observable
- Auditable
- Cloud-ready

This project is designed as a **flagship AI engineering reference**, not a proof of concept.

---

## What the Project Does

The application exposes a REST API that performs the following steps for every request:

1. Loads structured business data (sales dataset)
2. Computes a deterministic analytical summary
3. Builds a controlled, versioned prompt
4. Sends the prompt to an LLM
5. Returns a business insight
6. Tracks the entire request lifecycle (logs + MLflow)

Each request is treated as a **first-class production event**.

---

## Example API Call

### Request

```json
{
  "question": "Which region is underperforming?"
}