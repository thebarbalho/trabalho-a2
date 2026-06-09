import pandas as pd
import numpy as np

def calcular_metricas(df):
    df = df.copy()
    df["engajamento_total"] = df["curtidas"] + df["comentarios"]
    df["taxa_engajamento"] = np.where(
        df["visualizacoes"] > 0,
        ((df["curtidas"] + df["comentarios"]) / df["visualizacoes"]) * 100,
        0
    )
    df["curtidas_por_comentario"] = np.where(
        df["comentarios"] > 0,
        df["curtidas"] / df["comentarios"],
        df["curtidas"]
    )
    return df

def resumo_por_categoria(df):
    return df.groupby("categoria").agg(
        total_videos=("video_id", "count"),
        total_visualizacoes=("visualizacoes", "sum"),
        total_curtidas=("curtidas", "sum"),
        total_comentarios=("comentarios", "sum"),
        engajamento_medio=("engajamento_total", "mean"),
        taxa_engajamento_media=("taxa_engajamento", "mean")
    ).reset_index().sort_values("engajamento_medio", ascending=False)

def top_videos(df, metrica="engajamento_total", n=10):
    return df.nlargest(n, metrica)[
        ["titulo", "canal", "categoria", metrica, "visualizacoes"]
    ]
