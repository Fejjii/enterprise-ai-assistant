import pandas as pd
from pathlib import Path
from app.config import DATA_PATH, OPENAI_MODEL
from app.logger import logger
from openai import OpenAI
from dotenv import load_dotenv
import os
import time
import mlflow
from app.mlflow_config import init_mlflow

PROMPT_VERSION = "v1.0"

PROMPT_TEMPLATE = """
You are a senior business analyst.
Based on the following summary, answer the user's question clearly and concisely.

Summary:
{summary}

Question:
{question}
"""

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "sales_data.csv"

def load_data():
    logger.info("Loading sales data")
    df = pd.read_csv(DATA_PATH)
    logger.info(f"Sales data loaded successfully ({len(df)} rows)")
    return df

def summarize_data(df: pd.DataFrame) -> str:
    summary = []
    summary.append(f"The dataset has {len(df)} rows.")
    summary.append(f"Regions: {df['region'].unique().tolist()}")
    summary.append(f"Products: {df['product'].unique().tolist()}")

    revenue_by_region = df.groupby("region")["revenue"].sum()
    summary.append("Total revenue by region:")
    for region, value in revenue_by_region.items():
        summary.append(f"- {region}: {value}")

    return "\n".join(summary)

def build_prompt(summary: str, question: str) -> str:
    return f"""
You are a senior business analyst.

Here is the data summary:
{summary}

Business question:
{question}

Provide a concise, data-driven business insight.
"""

def ask_ai(summary: str, question: str, request_id: str) -> str:
    logger.info(
        "calling_openai",
        extra={
            "request_id": request_id,
            "prompt_version": PROMPT_VERSION,
            "model": OPENAI_MODEL,
        },
    )

    # Initialize MLflow (safe to call multiple times)
    init_mlflow()

    start_time = time.time()

    with mlflow.start_run():
        # --- MLflow: configuration ---
        mlflow.log_param("prompt_version", PROMPT_VERSION)
        mlflow.log_param("model", OPENAI_MODEL)
        mlflow.log_param("temperature", 0.2)

        # --- MLflow: safe input metadata ---
        mlflow.log_param("question_length", len(question))
        mlflow.log_param("summary_length", len(summary))

        # --- Build prompt ---
        prompt = build_prompt(summary, question)

        # --- Call OpenAI safely ---
        try:
            response = client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
            )
            content = response.choices[0].message.content

        except Exception as e:
            logger.error(
                "openai_call_failed",
                extra={
                    "request_id": request_id,
                    "error": str(e),
                },
            )
            raise RuntimeError("AI service temporarily unavailable")

        # --- Log success ---
        logger.info(
            "analysis_completed",
            extra={
                "request_id": request_id,
            },
        )

        # --- MLflow: output + metrics ---
        mlflow.log_text(content, "response.txt")

        latency = time.time() - start_time
        mlflow.log_metric("latency_seconds", latency)

        return content
