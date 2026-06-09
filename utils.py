import os
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def get_api_key():
    key = os.getenv("YOUTUBE_API_KEY")
    if not key:
        raise ValueError("YOUTUBE_API_KEY não encontrada. Verifique o arquivo .env")
    return key

def save_dataframe(df, filename="videos.csv"):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = DATA_DIR / filename
    df.to_csv(path, index=False, encoding="utf-8")
    return path

def load_dataframe(filename="videos.csv"):
    path = DATA_DIR / filename
    if path.exists():
        return pd.read_csv(path, encoding="utf-8")
    return None
