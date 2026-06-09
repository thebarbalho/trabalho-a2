import pandas as pd
import numpy as np

def extrair_tempo(df):
    df = df.copy()
    df["ano"] = df["data_publicacao"].dt.year
    df["mes"] = df["data_publicacao"].dt.month
    df["dia_da_semana"] = df["data_publicacao"].dt.day_name()
    df["hora"] = df["data_publicacao"].dt.hour
    df["semana_ano"] = df["data_publicacao"].dt.isocalendar().week.astype(int)
    return df

def engajamento_por_dia(df):
    ordem = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    nomes = {
        "Monday": "Segunda", "Tuesday": "Terça", "Wednesday": "Quarta",
        "Thursday": "Quinta", "Friday": "Sexta", "Saturday": "Sábado", "Sunday": "Domingo"
    }
    result = df.groupby("dia_da_semana").agg(
        total_engajamento=("engajamento_total", "sum"),
        media_engajamento=("engajamento_total", "mean"),
        total_visualizacoes=("visualizacoes", "sum"),
        contagem=("video_id", "count")
    ).reset_index()
    result["dia_pt"] = result["dia_da_semana"].map(nomes)
    result["ordem"] = result["dia_da_semana"].map({v: i for i, v in enumerate(ordem)})
    result = result.sort_values("ordem").drop(columns=["ordem"])
    return result

def engajamento_ao_longo_do_tempo(df):
    return df.groupby("ano").agg(
        total_engajamento=("engajamento_total", "sum"),
        total_visualizacoes=("visualizacoes", "sum"),
        total_videos=("video_id", "count")
    ).reset_index()

def tendencias_categoria_ao_longo_tempo(df):
    df["mes_ano"] = df["data_publicacao"].dt.to_period("M").astype(str)
    return df.groupby(["mes_ano", "categoria"]).agg(
        engajamento=("engajamento_total", "sum"),
        visualizacoes=("visualizacoes", "sum"),
        videos=("video_id", "count")
    ).reset_index()
