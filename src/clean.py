import re
import pandas as pd

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^\w\sáéíóúâêîôûàèìòùãõçñÁÉÍÓÚÂÊÎÔÛÀÈÌÒÙÃÕÇÑ\w]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text.lower()

def clean_dataframe(df):
    df = df.copy()
    df["titulo"] = df["titulo"].apply(clean_text)
    df["descricao"] = df["descricao"].apply(clean_text)
    df["data_publicacao"] = pd.to_datetime(df["data_publicacao"], errors="coerce")
    df["visualizacoes"] = pd.to_numeric(df["visualizacoes"], errors="coerce").fillna(0).astype(int)
    df["curtidas"] = pd.to_numeric(df["curtidas"], errors="coerce").fillna(0).astype(int)
    df["comentarios"] = pd.to_numeric(df["comentarios"], errors="coerce").fillna(0).astype(int)
    df = df.dropna(subset=["data_publicacao"])
    return df
