import pandas as pd
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load env
load_dotenv()

# Client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load data
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "sales_data.csv"
df = pd.read_csv(DATA_PATH)

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

def ask_ai(summary: str, question: str) -> str:
    prompt = f"""
You are a senior business analyst.

Here is the data summary:
{summary}

Business question:
{question}

Provide a concise insight.
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content


data_summary = summarize_data(df)
question = "Which region is performing best and why?"

print("\nDATA SUMMARY SENT TO AI:")
print(data_summary)

insight = ask_ai(data_summary, question)

print("\nAI BUSINESS INSIGHT:")
print(insight)
