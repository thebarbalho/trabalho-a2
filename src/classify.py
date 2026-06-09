import pandas as pd

CATEGORIAS = {
    "Gols / Melhores Momentos": [
        "gol", "gols", "cesta", "cestas", "touchdown", "melhores momentos",
        "highlight", "lances", "jogada", "pontos", "hat trick", "hat-trick",
        "bicicleta", "enterrada", "defesa", "finalização", "finalizacao",
        "assistência", "assistencia", "lance", "golaço", "golaco"
    ],
    "Análises Esportivas": [
        "análise", "analise", "análise técnica", "analise tecnica",
        "tática", "tatica", "preview", "review", "debate", "discussão",
        "discussao", "opinião", "opiniao", "palpite", "prognóstico",
        "prognostico", "breakdown", "deep dive", "técnico", "tecnico",
        "estatística", "estatistica", "desempenho", "ranking", "top 10",
        "comparação", "comparacao", "quem é melhor"
    ],
    "Humor / Memes": [
        "humor", "meme", "memes", "engraçado", "hilário", "hilario",
        "piada", "funny", "lol", "comédia", "comedia", "zuera", "zueira",
        "zoação", "zoacao", "melhores momentos engraçados", "cortina",
        "fail", "erro", "cuspe", "gafe", "besteirol"
    ],
    "Notícias": [
        "notícia", "noticia", "notícias", "noticias", "news", "breaking",
        "anúncio", "anuncio", "oficial", "confirmado", "contratação",
        "contratacao", "transferência", "transferencia", "rumor",
        "bastidores", "novidade", "última hora", "ultima hora",
        "ao vivo", "agora", "urgente", "mercado", "negociação", "negociacao"
    ]
}

def classificar_video(titulo, descricao):
    texto = f"{titulo} {descricao}".lower()
    for categoria, keywords in CATEGORIAS.items():
        for kw in keywords:
            if kw in texto:
                return categoria
    return "Outros"

def classificar_dataframe(df):
    df = df.copy()
    df["categoria"] = df.apply(
        lambda row: classificar_video(row["titulo"], row["descricao"]), axis=1
    )
    return df
