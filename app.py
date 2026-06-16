import matplotlib
matplotlib.use('Agg')

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.clean import clean_dataframe
from src.classify import classificar_dataframe
from src.metrics import calcular_metricas, resumo_por_categoria, top_videos, extrair_tempo, engajamento_por_dia, tendencias_categoria_ao_longo_tempo


st.set_page_config(
    page_title="Analytics Esportivo - YouTube",
    page_icon="⚽",
    layout="wide"
)

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #0f1724 0%, #152238 50%, #0d1a26 100%);
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1a26 0%, #0f1724 100%);
        border-right: 1px solid rgba(0, 200, 200, 0.08);
        padding: 1.5rem 0.5rem;
    }

    section[data-testid="stSidebar"] .stMarkdown {
        color: #c8d6e5;
    }

    .sidebar-title {
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #00bcd4;
        margin-bottom: 0.25rem;
        padding-left: 0.5rem;
    }

    .sidebar-label {
        font-size: 0.8rem;
        font-weight: 600;
        color: #8faabe;
        margin-bottom: 0.15rem;
        padding-left: 0.5rem;
    }

    h1 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 800 !important;
        font-size: 2rem !important;
        color: #e8eef5 !important;
        letter-spacing: -0.02em;
        margin-bottom: 0.25rem !important;
    }

    h2, h3, h4 {
        font-family: 'Inter', sans-serif !important;
        color: #dce6f0 !important;
    }

    .stRadio > div {
        gap: 0 !important;
        background: rgba(255,255,255,0.04);
        border-radius: 10px;
        padding: 3px;
        display: flex;
    }

    .stRadio > div > label {
        flex: 1;
        text-align: center;
        padding: 0.5rem 0.8rem !important;
        margin: 0 !important;
        border-radius: 8px !important;
        background: transparent !important;
        color: #8faabe !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        transition: all 0.25s ease;
        border: none !important;
    }

    .stRadio > div > label:hover {
        color: #e8eef5 !important;
        background: rgba(0, 188, 212, 0.08) !important;
    }

    .stRadio > div > label[data-testid="stWidgetLabel"] {
        padding: 0 !important;
    }

    div[role="radiogroup"] > label[data-baseweb="radio"] {
        flex: 1;
        text-align: center;
        padding: 0.5rem 0.8rem !important;
        margin: 0 !important;
        border-radius: 8px !important;
        background: transparent !important;
        color: #8faabe !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        transition: all 0.25s ease;
    }

    div[role="radiogroup"] > label[data-baseweb="radio"]:hover {
        color: #e8eef5 !important;
        background: rgba(0, 188, 212, 0.08) !important;
    }

    div[role="radiogroup"] > label[aria-checked="true"] {
        background: linear-gradient(135deg, #ff4d4d 0%, #ff6b35 100%) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 14px rgba(255, 77, 77, 0.35) !important;
    }

    div[role="radiogroup"] input {
        display: none !important;
    }

    .stSlider > div > div > div {
        background: rgba(255,255,255,0.08) !important;
    }

    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #ff4d4d, #ff6b35) !important;
    }

    .stSlider div[data-testid="stThumb"] {
        background: #ff4d4d !important;
        box-shadow: 0 2px 8px rgba(255, 77, 77, 0.4) !important;
    }

    div.stButton > button {
        background: linear-gradient(135deg, #ff4d4d 0%, #ff6b35 100%) !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.7rem 1.5rem !important;
        box-shadow: 0 6px 20px rgba(255, 77, 77, 0.3) !important;
        transition: all 0.3s ease !important;
        letter-spacing: 0.02em;
    }

    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 28px rgba(255, 77, 77, 0.45) !important;
        background: linear-gradient(135deg, #ff3333 0%, #ff5a1f 100%) !important;
    }

    div.stButton > button:active {
        transform: translateY(0px) !important;
    }

    div.stButton > button > div {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .stTextInput > div > div {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 10px !important;
        color: #e8eef5 !important;
    }

    .stTextInput > div > div:focus-within {
        border-color: #00bcd4 !important;
        box-shadow: 0 0 0 2px rgba(0, 188, 212, 0.15) !important;
    }

    .stTextInput input {
        color: #e8eef5 !important;
        font-family: 'Inter', sans-serif !important;
    }

    .stSelectbox > div > div {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 10px !important;
        color: #e8eef5 !important;
    }

    .stMultiSelect > div > div {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 10px !important;
        color: #e8eef5 !important;
    }

    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 14px;
        padding: 1.2rem 1rem;
        backdrop-filter: blur(8px);
        transition: all 0.3s ease;
    }

    div[data-testid="stMetric"]:hover {
        border-color: rgba(0, 188, 212, 0.2);
        background: rgba(255,255,255,0.06);
    }

    div[data-testid="stMetric"] label {
        color: #8faabe !important;
        font-weight: 500 !important;
        font-size: 0.8rem !important;
    }

    div[data-testid="stMetric"] div {
        color: #e8eef5 !important;
        font-weight: 700 !important;
        font-size: 1.5rem !important;
    }

    .stDataFrame {
        border-radius: 12px !important;
        overflow: hidden !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
    }

    .stDataFrame table {
        background: rgba(255,255,255,0.02) !important;
    }

    .stDataFrame th {
        background: rgba(0, 188, 212, 0.12) !important;
        color: #00bcd4 !important;
        font-weight: 600 !important;
        font-size: 0.75rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
    }

    .stDataFrame td {
        color: #c8d6e5 !important;
        font-size: 0.8rem !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.06) !important;
        margin: 1.5rem 0 !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0.25rem !important;
        background: rgba(255,255,255,0.03);
        border-radius: 12px;
        padding: 4px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 10px !important;
        padding: 0.5rem 1rem !important;
        color: #8faabe !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.8rem !important;
        transition: all 0.25s ease !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: #e8eef5 !important;
        background: rgba(0, 188, 212, 0.06) !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #ff4d4d 0%, #ff6b35 100%) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 14px rgba(255, 77, 77, 0.3) !important;
    }

    .stSpinner > div {
        border-color: #ff4d4d !important;
        border-top-color: transparent !important;
    }

    .stAlert {
        border-radius: 12px !important;
        border: none !important;
        background: rgba(255,255,255,0.04) !important;
        color: #e8eef5 !important;
    }

    .stAlert [data-testid="stAlert"] {
        background: rgba(255, 77, 77, 0.1) !important;
        border-left: 3px solid #ff4d4d !important;
    }

    div[data-testid="stNotificationContent"] {
        color: #e8eef5 !important;
    }

    .stDownloadButton > button {
        background: linear-gradient(135deg, #00bcd4 0%, #0097a7 100%) !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 16px rgba(0, 188, 212, 0.3) !important;
        transition: all 0.3s ease !important;
    }

    .stDownloadButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 188, 212, 0.45) !important;
    }

    .stSubheader {
        color: #dce6f0 !important;
        font-weight: 600 !important;
    }

    .divider-teal {
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(0, 188, 212, 0.3), transparent);
        margin: 0.75rem 0 1.5rem 0;
        border: none;
    }

    .video-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 14px;
        padding: 1.2rem 1rem;
        height: 100%;
        transition: all 0.3s ease;
        display: flex;
        flex-direction: column;
        gap: 0.4rem;
    }

    .video-card:hover {
        border-color: rgba(0, 188, 212, 0.2);
        background: rgba(255,255,255,0.06);
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.2);
    }

    .video-card .rank {
        font-size: 0.65rem;
        font-weight: 700;
        color: #4a667a;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .video-card .title {
        font-size: 0.85rem;
        font-weight: 600;
        line-height: 1.3;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }

    .video-card .title a {
        color: #e8eef5;
        text-decoration: none;
        transition: color 0.2s ease;
    }

    .video-card .title a:hover {
        color: #ff6b35;
        text-decoration: underline;
    }

    .video-card .meta {
        font-size: 0.72rem;
        color: #6a8aa0;
        display: flex;
        flex-wrap: wrap;
        gap: 0.6rem;
        margin-top: auto;
    }

    .video-card .meta span {
        display: flex;
        align-items: center;
        gap: 0.25rem;
    }

    .video-card .channel {
        font-size: 0.72rem;
        color: #8faabe;
    }

    .video-link-table {
        width: 100%;
        border-collapse: collapse;
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
    }

    .video-link-table thead th {
        background: rgba(0, 188, 212, 0.12);
        color: #00bcd4;
        font-weight: 600;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        padding: 0.7rem 0.8rem;
        text-align: left;
        white-space: nowrap;
    }

    .video-link-table tbody td {
        color: #c8d6e5;
        padding: 0.6rem 0.8rem;
        border-bottom: 1px solid rgba(255,255,255,0.04);
    }

    .video-link-table tbody tr:hover td {
        background: rgba(255,255,255,0.03);
    }

    .video-link-table a {
        color: #e8eef5;
        text-decoration: none;
        font-weight: 500;
        transition: color 0.2s ease;
    }

    .video-link-table a:hover {
        color: #ff6b35;
        text-decoration: underline;
    }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

QUERIES_SUGERIDAS = [
    "esportes melhores momentos", "análise esportiva", "humor esportivo",
    "notícias esportivas", "futebol gols", "basquete cestas",
    "futebol americano touchdown", "memes esportes", "debate esportivo",
    "esportes radicais"
]

def youtube_url(video_id):
    return f"https://www.youtube.com/watch?v={video_id}"

COL_LABELS = {
    "titulo": "Título", "canal": "Canal", "categoria": "Categoria",
    "visualizacoes": "Visualizações", "curtidas": "Curtidas",
    "comentarios": "Comentários", "engajamento_total": "Eng. Total",
    "taxa_engajamento": "Tx. Engajamento", "data_publicacao": "Publicação"
}

def html_video_table(df, columns):
    cols = [c for c in columns if c != "video_id" and c in df.columns]
    has_link = "video_id" in df.columns and "titulo" in cols
    html = '<table class="video-link-table"><thead><tr>'
    for c in cols:
        html += f"<th>{COL_LABELS.get(c, c)}</th>"
    html += '</tr></thead><tbody>'
    for _, row in df.iterrows():
        html += "<tr>"
        for c in cols:
            val = row[c]
            if c == "titulo" and has_link:
                url = youtube_url(row["video_id"])
                html += f'<td><a href="{url}" target="_blank">{val}</a></td>'
            elif isinstance(val, (int, float)):
                html += f"<td>{val:,.0f}</td>" if abs(val) >= 1000 else f"<td>{val}</td>"
            else:
                html += f"<td>{val}</td>"
        html += "</tr>"
    html += "</tbody></table>"
    return html

with st.sidebar:
    st.markdown('<div class="sidebar-title">Configuração</div>', unsafe_allow_html=True)
    st.markdown('<div class="divider-teal"></div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-label">Tipo de busca</div>', unsafe_allow_html=True)
    opcao_busca = st.radio("Busca", ["Palavra-chave única", "Múltiplas consultas"], label_visibility="collapsed")

    if opcao_busca == "Palavra-chave única":
        st.markdown('<div class="sidebar-label">Palavra-chave</div>', unsafe_allow_html=True)
        query = st.text_input("Palavra-chave", "futebol gols", label_visibility="collapsed")
        st.markdown('<div class="sidebar-label">Quantidade de vídeos</div>', unsafe_allow_html=True)
        max_results = st.slider("Quantidade de vídeos", 5, 50, 20, label_visibility="collapsed")
    else:
        st.markdown('<div class="sidebar-label">Consultas</div>', unsafe_allow_html=True)
        queries_selecionadas = st.multiselect(
            "Consultas", QUERIES_SUGERIDAS,
            default=QUERIES_SUGERIDAS[:4],
            label_visibility="collapsed"
        )
        st.markdown('<div class="sidebar-label">Vídeos por consulta</div>', unsafe_allow_html=True)
        videos_por_query = st.slider("Vídeos por consulta", 10, 50, 25, label_visibility="collapsed")

    coletar = st.button("🔍  Coletar Dados", type="primary", use_container_width=True)

    st.markdown("---")
    st.markdown(
        '<p style="color: #4a667a; font-size: 0.7rem; text-align: center; '
        'letter-spacing: 0.05em;">Projeto A2 — Programação</p>',
        unsafe_allow_html=True
    )

if "df" not in st.session_state:
    st.session_state.df = None
    st.session_state.processado = None

if coletar:
    with st.spinner("Coletando dados da YouTube API..."):
        try:
            from src.collect import search_videos, collect_multiple_queries
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

if st.session_state.df is None:
    st.markdown("""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center;
                    min-height: 65vh; text-align: center; gap: 1.5rem;">
            <div style="font-size: 4rem; line-height: 1;">⚽</div>
            <h1 style="font-size: 2.2rem !important; margin: 0 !important;">
                Ferramenta Analítica de Engajamento Social
            </h1>
            <p style="color: #6a8aa0; font-size: 1.05rem; font-weight: 400; margin: 0;
                      max-width: 480px;">
                Conteúdos Esportivos no YouTube
            </p>
            <div style="margin: 0.5rem 0;">
                <svg width="200" height="80" viewBox="0 0 200 80" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="10" y="50" width="30" height="20" rx="4" fill="rgba(0,188,212,0.15)"/>
                    <rect x="50" y="30" width="30" height="40" rx="4" fill="rgba(0,188,212,0.20)"/>
                    <rect x="90" y="15" width="30" height="55" rx="4" fill="rgba(0,188,212,0.25)"/>
                    <rect x="130" y="35" width="30" height="35" rx="4" fill="rgba(0,188,212,0.20)"/>
                    <rect x="170" y="45" width="30" height="25" rx="4" fill="rgba(0,188,212,0.15)"/>
                    <line x1="10" y1="72" x2="200" y2="72" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>
                    <path d="M10 55 Q 35 40, 65 50 Q 95 20, 120 40 Q 145 30, 170 50 Q 185 45, 200 48"
                          stroke="rgba(255,77,77,0.25)" stroke-width="2" fill="none" stroke-linecap="round"/>
                </svg>
            </div>
            <p style="color: #4a667a; font-size: 0.85rem; font-weight: 400; margin: 0;
                      letter-spacing: 0.04em;">
                Aguardando coleta de dados...
            </p>
        </div>
    """, unsafe_allow_html=True)

else:
    df_raw = st.session_state.df

    df_clean = clean_dataframe(df_raw)
    df_class = classificar_dataframe(df_clean)
    df_metrics = calcular_metricas(df_class)
    df_analyze = extrair_tempo(df_metrics)

    st.session_state.processado = df_analyze

    st.sidebar.markdown("---")
    st.sidebar.markdown('<div class="sidebar-title">Filtros</div>', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="divider-teal"></div>', unsafe_allow_html=True)
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
        cards_html = '<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem;">'
        for idx, (_, row) in enumerate(top10.iterrows(), 1):
            url = youtube_url(row["video_id"])
            views = f"{row['visualizacoes']:,.0f}"
            eng = f"{row['engajamento_total']:,.0f}"
            cards_html += f"""
                <div class="video-card">
                    <div class="rank">#{idx} — {row['categoria']}</div>
                    <div class="title"><a href="{url}" target="_blank">{row['titulo']}</a></div>
                    <div class="channel">{row['canal']}</div>
                    <div class="meta">
                        <span>👁️ {views}</span>
                        <span>⚡ {eng}</span>
                    </div>
                </div>
            """
        cards_html += "</div>"
        st.markdown(cards_html, unsafe_allow_html=True)

    with abas[1]:
        st.subheader("Resumo por Categoria")
        resumo = resumo_por_categoria(df_filtered)
        sns.set_style("darkgrid")

        col_a, col_b = st.columns(2)

        with col_a:
            fig1, ax1 = plt.subplots(figsize=(10, 5))
            ax1.set_facecolor("#0d1a26")
            fig1.patch.set_facecolor("#0d1a26")
            ax1.tick_params(colors="#8faabe")
            ax1.spines["bottom"].set_color((1, 1, 1, 0.08))
            ax1.spines["left"].set_color((1, 1, 1, 0.08))
            ax1.spines["top"].set_visible(False)
            ax1.spines["right"].set_visible(False)
            ax1.xaxis.label.set_color("#8faabe")
            ax1.yaxis.label.set_color("#8faabe")
            ax1.title.set_color("#dce6f0")
            bars = ax1.bar(resumo["categoria"], resumo["engajamento_medio"], color="#ff6b35")
            ax1.set_xlabel("Categoria")
            ax1.set_ylabel("Engajamento Médio")
            ax1.tick_params(axis="x", rotation=45)
            for bar in bars:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width() / 2., height,
                         f"{height:.0f}", ha="center", va="bottom", color="#8faabe")
            fig1.tight_layout()
            st.pyplot(fig1)

        with col_b:
            fig2, ax2 = plt.subplots(figsize=(10, 5))
            fig2.patch.set_facecolor("#0d1a26")
            cores = sns.color_palette("magma", len(resumo))
            wedges, texts, autotexts = ax2.pie(
                resumo["total_visualizacoes"],
                labels=resumo["categoria"],
                autopct="%1.1f%%",
                colors=cores,
                startangle=90,
                textprops={"color": "#c8d6e5"}
            )
            for t in autotexts:
                t.set_color("#ffffff")
                t.set_fontweight(600)
            ax2.set_title("Distribuição de Visualizações por Categoria", color="#dce6f0")
            st.pyplot(fig2)

        st.dataframe(resumo, use_container_width=True, hide_index=True)

    with abas[2]:
        st.subheader("Engajamento por Dia da Semana")

        dias = engajamento_por_dia(df_filtered)
        fig3, ax3 = plt.subplots(figsize=(10, 5))
        ax3.set_facecolor("#0d1a26")
        fig3.patch.set_facecolor("#0d1a26")
        ax3.tick_params(colors="#8faabe")
        ax3.spines["bottom"].set_color((1, 1, 1, 0.08))
        ax3.spines["left"].set_color((1, 1, 1, 0.08))
        ax3.spines["top"].set_visible(False)
        ax3.spines["right"].set_visible(False)
        ax3.xaxis.label.set_color("#8faabe")
        ax3.yaxis.label.set_color("#8faabe")
        ax3.title.set_color("#dce6f0")
        ax3.plot(dias["dia_pt"], dias["media_engajamento"], marker="o", linewidth=2, color="#ff6b35",
                 markerfacecolor="#ff4d4d", markeredgecolor="#ff4d4d", markersize=8)
        ax3.set_xlabel("Dia da Semana")
        ax3.set_ylabel("Engajamento Médio")
        ax3.grid(True, alpha=0.1, color=(1, 1, 1, 0.08))
        fig3.tight_layout()
        st.pyplot(fig3)

        st.subheader("Tendências das Categorias ao Longo do Tempo")
        tendencias = tendencias_categoria_ao_longo_tempo(df_filtered)
        if not tendencias.empty:
            fig4, ax4 = plt.subplots(figsize=(12, 5))
            ax4.set_facecolor("#0d1a26")
            fig4.patch.set_facecolor("#0d1a26")
            ax4.tick_params(colors="#8faabe")
            ax4.spines["bottom"].set_color((1, 1, 1, 0.08))
            ax4.spines["left"].set_color((1, 1, 1, 0.08))
            ax4.spines["top"].set_visible(False)
            ax4.spines["right"].set_visible(False)
            ax4.xaxis.label.set_color("#8faabe")
            ax4.yaxis.label.set_color("#8faabe")
            ax4.legend(labelcolor="#c8d6e5", facecolor=(0.05, 0.1, 0.15, 0.8), edgecolor=(1, 1, 1, 0.08))
            palette = sns.color_palette("magma", len(tendencias["categoria"].unique()))
            for i, (cat, dados_cat) in enumerate(tendencias.groupby("categoria")):
                ax4.plot(dados_cat["mes_ano"], dados_cat["engajamento"],
                         marker="o", label=cat, linewidth=2, color=palette[i],
                         markerfacecolor=palette[i])
            ax4.set_xlabel("Mês / Ano")
            ax4.set_ylabel("Engajamento Total")
            ax4.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
            ax4.tick_params(axis="x", rotation=45)
            fig4.tight_layout()
            st.pyplot(fig4)

    with abas[3]:
        colunas_exibir = ["video_id", "titulo", "canal", "categoria", "visualizacoes",
                          "curtidas", "comentarios", "engajamento_total",
                          "taxa_engajamento", "data_publicacao"]
        colunas_exibir = [c for c in colunas_exibir if c in df_filtered.columns]
        df_tabela = df_filtered[colunas_exibir].sort_values("engajamento_total", ascending=False)
        st.markdown(html_video_table(df_tabela, colunas_exibir), unsafe_allow_html=True)

        csv = df_filtered.to_csv(index=False, encoding="utf-8")
        st.download_button(
            label="📥  Download CSV",
            data=csv,
            file_name="dados_esportivos_youtube.csv",
            mime="text/csv"
        )
