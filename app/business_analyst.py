import pandas as pd
from pathlib import Path
from app.config import DATA_PATH, OPENAI_MODEL
from app.logger import logger
from openai import OpenAI
from dotenv import load_dotenv
import os

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


def ask_ai(summary: str, question: str) -> str:
    logger.info("Calling OpenAI model for analysis")

    prompt = build_prompt(summary, question)

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    logger.info("Received response from OpenAI")

    return response.choices[0].message.content
