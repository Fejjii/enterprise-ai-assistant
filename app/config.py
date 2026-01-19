from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "sales_data.csv"

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
