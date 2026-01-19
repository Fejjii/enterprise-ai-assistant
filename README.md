What this project does
This AI Business Analyst Assistant answers business questions from structured sales data using AI-generated insights.

Why this matters
Managers often lack time or SQL skills. This system converts data into explainable insights.

How it works
• Data is summarized programmatically
• AI reasons over business context
• Natural language questions drive analysis

Example questions
• Which region performs best?
• Which product should be prioritized?

This is interview-grade documentation.

API Usage

Endpoint:
POST /analyze

Example request:

{
  "question": "Which region is underperforming?"
}


Example response:

{
  "insight": "Asia shows lower total revenue compared to other regions..."