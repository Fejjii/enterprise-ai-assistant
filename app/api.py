from fastapi import FastAPI
from pydantic import BaseModel

from app.business_analyst import load_data, summarize_data, ask_ai

app = FastAPI(
    title="AI Business Analyst Assistant",
    description="Answers business questions from structured data using AI",
    version="0.1.0",
)

class AnalyzeRequest(BaseModel):
    question: str

class AnalyzeResponse(BaseModel):
    insight: str

@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    try:
        df = load_data()
        summary = summarize_data(df)
        insight = ask_ai(summary, request.question)
        return {"insight": insight}
    except Exception as e:
        return {"insight": f"Error during analysis: {str(e)}"}
