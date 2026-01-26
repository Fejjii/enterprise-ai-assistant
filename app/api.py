from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import uuid


from app.business_analyst import load_data, summarize_data, ask_ai
from app.logger import logger

# 1️⃣ Create app
app = FastAPI(
    title="AI Business Analyst Assistant",
    description="Answers business questions from structured data using AI",
    version="0.1.0",
)

# 2️⃣ Health check (infrastructure endpoint)
@app.get("/health")
def health():
    return {"status": "ok"}

# 3️⃣ Request / Response models
class AnalyzeRequest(BaseModel):
    question: str = Field(..., min_length=5, max_length=500)

class AnalyzeResponse(BaseModel):
    insight: str

# 4️⃣ Business endpoint
@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    request_id = str(uuid.uuid4())

    try:
        logger.info(
            "analysis_request_received",
            extra={
                "request_id": request_id,
                "question_length": len(request.question),
            },
        )

        df = load_data()
        summary = summarize_data(df)

        insight = ask_ai(
            summary,
            request.question,
            request_id=request_id
        )

        logger.info(
            "analysis_completed_successfully",
            extra={
                "request_id": request_id,
            },
        )

        return {
            "request_id": request_id,
            "insight": insight,
        }

    except Exception as e:
        logger.error(
            "analysis_failed",
            extra={
                "request_id": request_id,
                "error": str(e),
            },
        )
        raise HTTPException(status_code=500, detail="Analysis failed")
