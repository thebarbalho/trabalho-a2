import matplotlib
matplotlib.use('Agg')

pip install -r requirements.txt
streamlit run src/app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.collect import search_videos, collect_multiple_queries
from src.clean import clean_dataframe
from src.classify import classificar_dataframe
from src.metrics import calcular_metricas, resumo_por_categoria, top_videos
from src.analyze import extrair_tempo, engajamento_por_dia, engajamento_ao_longe_do_tempo, tendencias_categoria_ao_longo_tempo
from src.utils import save_dataframe, load_dataframe

st.set_page_config(
    page_title="Analytics Esportivo - YouTube",
    page_icon="⚽",
    layout="wide"
)

with sns.axes_style("darkgrid")

QUERIES_SUGERIDAS = [
    "esportes melhores momentos", "análise esportiva", "humor esportivo",
    "notícias esportivas", "futebol gols", "basquete cestas",
    "futebol americano touchdown", "memes esportes", "debate esportivo",
    "esportes radicais"
]

with st.sidebar:
    st.header("Configuração")
    modo = st.radio("Fonte dos dados", ["Coletar da API", "Usar dados salvos"])

    if modo == "Coletar da API":
        opcao_busca = st.radio("Busca", ["Palavra-chave única", "Múltiplas consultas"])

        if opcao_busca == "Palavra-chave única":
            query = st.text_input("Palavra-chave", "futebol gols")
            max_results = st.slider("Quantidade de vídeos", 5, 50, 20)
        else:
            queries_selecionadas = st.multiselect(
                "Consultas", QUERIES_SUGERIDAS,
                default=QUERIES_SUGERIDAS[:4]
            )
            videos_por_query = st.slider("Vídeos por consulta", 10, 50, 25)

        coletar = st.button("Coletar Dados", type="primary", use_container_width=True)
    else:
        arquivos = []
        try:
            from pathlib import Path
            data_dir = Path(__file__).resolve().parent.parent / "data"
            if data_dir.exists():
                arquivos = [f.name for f in data_dir.glob("*.csv")]
        except:
            pass
        arquivo = st.selectbox("Arquivo", arquivos) if arquivos else None
        if arquivo:
            carregar = st.button("Carregar", type="primary", use_container_width=True)

    st.markdown("---")
    st.caption("Projeto A2 - Programação")

if "df" not in st.session_state:
    st.session_state.df = None
    st.session_state.processado = None

if modo == "Coletar da API" and coletar:
    with st.spinner("Coletando dados da YouTube API..."):
        try:
            if opcao_busca == "Palavra-chave única":
                df_raw = search_videos(query, max_results=max_results)
            else:
                df_raw = collect_multiple_queries(queries_selecionadas, videos_per_query=videos_por_query)

            if df_raw.empty:
                st.error("Nenhum vídeo encontrado. Tente outras palavras-chave.")
            else:
                st.session_state.df = df_raw
                st.success(f"{len(df_raw)} vídeos coletados com sucesso!")
        except Exception as e:
            st.error(f"Erro na coleta: {e}")

elif modo == "Usar dados salvos":
    if arquivo and carregar:
        df_raw = load_dataframe(arquivo)
        if df_raw is not None:
            st.session_state.df = df_raw
            st.success(f"Dados carregados: {len(df_raw)} vídeos")
        else:
            st.error("Arquivo não encontrado.")
    elif not arquivos:
        st.info("Nenhum dado salvo encontrado. Colete dados primeiro.")

if st.session_state.df is not None:
    df_raw = st.session_state.df

    df_clean = clean_dataframe(df_raw)
    df_class = classificar_dataframe(df_clean)
    df_metrics = calcular_metricas(df_class)
    df_analyze = extrair_tempo(df_metrics)

    st.session_state.processado = df_analyze

    st.sidebar.markdown("---")
    st.sidebar.subheader("Filtros")
    categorias_disponiveis = ["Todas"] + sorted(df_analyze["categoria"].unique().tolist())
    categoria_filtro = st.sidebar.multiselect(
        "Categorias", categorias_disponiveis, default="Todas"
    )
    if "Todas" in categoria_filtro or not categoria_filtro:
        df_filtered = df_analyze
    else:
        df_filtered = df_analyze[df_analyze["categoria"].isin(categoria_filtro)]

    abas = st.tabs(["Visão Geral", "Por Categoria", "Análise Temporal", "Tabela de Dados"])

    with abas[0]:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total de Vídeos", len(df_filtered))
        with col2:
            st.metric("Total de Visualizações", f"{df_filtered['visualizacoes'].sum():,}")
        with col3:
            st.metric("Engajamento Total", f"{df_filtered['engajamento_total'].sum():,}")
        with col4:
            media_taxa = df_filtered["taxa_engajamento"].mean()
            st.metric("Taxa de Engajamento Média", f"{media_taxa:.2f}%")

        st.markdown("### Top 10 Vídeos por Engajamento")
        top10 = top_videos(df_filtered)
        st.dataframe(top10, use_container_width=True, hide_index=True)

    with abas[1]:
        st.subheader("Resumo por Categoria")
        resumo = resumo_por_categoria(df_filtered)

        col_a, col_b = st.columns(2)

        with col_a:
            fig1, ax1 = plt.subplots(figsize=(10, 5))
            bars = ax1.bar(resumo["categoria"], resumo["engajamento_medio"])
            ax1.set_xlabel("Categoria")
            ax1.set_ylabel("Engajamento Médio")
            ax1.tick_params(axis="x", rotation=45)
            for bar in bars:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width() / 2., height,
                         f"{height:.0f}", ha="center", va="bottom")
            fig1.tight_layout()
            st.pyplot(fig1)

        with col_b:
            fig2, ax2 = plt.subplots(figsize=(10, 5))
            cores = sns.color_palette("viridis", len(resumo))
            wedges, texts, autotexts = ax2.pie(
                resumo["total_visualizacoes"],
                labels=resumo["categoria"],
                autopct="%1.1f%%",
                colors=cores,
                startangle=90
            )
            ax2.set_title("Distribuição de Visualizações por Categoria")
            st.pyplot(fig2)

        st.dataframe(resumo, use_container_width=True, hide_index=True)

    with abas[2]:
        st.subheader("Engajamento por Dia da Semana")

        dias = engajamento_por_dia(df_filtered)
        fig3, ax3 = plt.subplots(figsize=(10, 5))
        ax3.plot(dias["dia_pt"], dias["media_engajamento"], marker="o", linewidth=2)
        ax3.set_xlabel("Dia da Semana")
        ax3.set_ylabel("Engajamento Médio")
        ax3.grid(True, alpha=0.3)
        fig3.tight_layout()
        st.pyplot(fig3)

        st.subheader("Tendências das Categorias ao Longo do Tempo")
        tendencias = tendencias_categoria_ao_longo_tempo(df_filtered)
        if not tendencias.empty:
            fig4, ax4 = plt.subplots(figsize=(12, 5))
            for cat in tendencias["categoria"].unique():
                dados_cat = tendencias[tendencias["categoria"] == cat]
                ax4.plot(dados_cat["mes_ano"], dados_cat["engajamento"],
                         marker="o", label=cat, linewidth=2)
            ax4.set_xlabel("Mês / Ano")
            ax4.set_ylabel("Engajamento Total")
            ax4.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
            ax4.tick_params(axis="x", rotation=45)
            fig4.tight_layout()
            st.pyplot(fig4)

    with abas[3]:
        colunas_exibir = ["titulo", "canal", "categoria", "visualizacoes",
                          "curtidas", "comentarios", "engajamento_total",
                          "taxa_engajamento", "data_publicacao"]
        colunas_exibir = [c for c in colunas_exibir if c in df_filtered.columns]
        st.dataframe(
            df_filtered[colunas_exibir].sort_values("engajamento_total", ascending=False),
            use_container_width=True,
            hide_index=True
        )

        csv = df_filtered.to_csv(index=False, encoding="utf-8")
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="dados_esportivos_youtube.csv",
            mime="text/csv"
        )
