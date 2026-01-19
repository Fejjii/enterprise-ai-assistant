from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app.logger import logger
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
        logger.info(f"Received analysis request: {request.question}")

        df = load_data()
        summary = summarize_data(df)
        insight = ask_ai(summary, request.question)

        logger.info("Analysis completed successfully")
        return {"insight": insight}

    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Analysis failed")
