import importlib
import matplotlib
matplotlib.use('Agg')

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.clean import clean_dataframe
import src.classify
importlib.reload(src.classify)
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

def youtube_url(video_id):
    return f"https://www.youtube.com/watch?v={video_id}"

def safe(val):
    if not isinstance(val, str):
        val = str(val)
    return val.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&#x27;")

COL_LABELS = {
    "titulo": "Título", "titulo_original": "Título Original",
    "canal": "Canal", "categoria": "Categoria",
    "tags": "Tags", "category_id_nativo": "Categ. YouTube",
    "visualizacoes": "Visualizações", "curtidas": "Curtidas",
    "comentarios": "Comentários", "engajamento_total": "Eng. Total",
    "taxa_engajamento": "Tx. Engajamento", "data_publicacao": "Publicação"
}

def style_ax(ax):
    ax.set_facecolor("#0d1a26")
    ax.tick_params(colors="#b0c8dd", labelsize=9)
    ax.spines["bottom"].set_color((1, 1, 1, 0.12))
    ax.spines["left"].set_color((1, 1, 1, 0.12))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.xaxis.label.set_color("#b0c8dd")
    ax.yaxis.label.set_color("#b0c8dd")
    ax.title.set_color("#e8eef5")
    ax.grid(True, alpha=0.08, color=(1, 1, 1, 0.1))
    return ax

def html_video_table(df, columns):
    cols = [c for c in columns if c in df.columns]
    has_link = "video_id" in df.columns and ("titulo" in cols or "titulo_original" in cols)
    titulo_col = "titulo_original" if "titulo_original" in cols else "titulo" if "titulo" in cols else None
    out = '<table class="video-link-table"><thead><tr>'
    for c in cols:
        if c == "video_id":
            out += "<th>Link</th>"
        else:
            label = "Título" if c == "titulo_original" else COL_LABELS.get(c, c)
            out += f"<th>{label}</th>"
    out += '</tr></thead><tbody>'
    for _, row in df.iterrows():
        out += "<tr>"
        for c in cols:
            val = row[c]
            if c == "video_id":
                url = youtube_url(val)
                out += f'<td><a href="{url}" target="_blank" style="color:#ff6b35;font-weight:600;text-decoration:none;">▶ YouTube</a></td>'
            elif c in ("titulo", "titulo_original") and has_link and titulo_col:
                url = youtube_url(row["video_id"])
                titulo = safe(row[titulo_col])
                out += f'<td><a href="{url}" target="_blank">{titulo}</a> <a href="{url}" target="_blank" style="color:#ff6b35;font-size:0.7rem;font-weight:600;text-decoration:none;margin-left:6px;white-space:nowrap;">▶ Assistir</a></td>'
            elif isinstance(val, (int, float)):
                out += f"<td>{val:,.0f}</td>" if abs(val) >= 1000 else f"<td>{val}</td>"
            else:
                out += f"<td>{safe(val)}</td>"
        out += "</tr>"
    out += "</tbody></table>"
    return out

with st.sidebar:
    st.markdown('<div class="sidebar-title">Configuração</div>', unsafe_allow_html=True)
    st.markdown('<div class="divider-teal"></div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-label">Palavra-chave</div>', unsafe_allow_html=True)
    query = st.text_input("Palavra-chave", "futebol gols", label_visibility="collapsed")
    st.markdown('<div class="sidebar-label">Quantidade de vídeos</div>', unsafe_allow_html=True)
    max_results = st.slider("Quantidade de vídeos", 5, 10, 10, label_visibility="collapsed")

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
            from src.collect import search_videos
            df_raw = search_videos(query, max_results=max_results)

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

    try:
        df_clean = clean_dataframe(df_raw)
        df_class = classificar_dataframe(df_clean)
        df_metrics = calcular_metricas(df_class)
        df_analyze = extrair_tempo(df_metrics)
    except Exception as e:
        st.error(f"Erro ao processar dados: {e}")
        st.stop()

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
        if "video_id" not in top10.columns:
            st.dataframe(top10, use_container_width=True, hide_index=True)
        else:
            cards_html = '<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem;">'
            for rank, (_, row) in enumerate(top10.iterrows(), start=1):
                url = youtube_url(row["video_id"])
                views = f"{row['visualizacoes']:,.0f}"
                eng = f"{row['engajamento_total']:,.0f}"
                titulo_exibir = safe(row.get("titulo_original", row.get("titulo", "")))
                categoria = safe(row.get("categoria", ""))
                canal = safe(row.get("canal", ""))
                cards_html += f"""
                    <div class="video-card">
                        <div class="rank">#{rank} — {categoria}</div>
                        <div class="title"><a href="{url}" target="_blank">{titulo_exibir}</a></div>
                        <div class="channel">{canal}</div>
                        <div class="meta">
                            <span>👁️ {views}</span>
                            <span>⚡ {eng}</span>
                            <span style="margin-left:auto;"><a href="{url}" target="_blank" style="color:#ff6b35;font-weight:600;text-decoration:none;font-size:0.75rem;">▶ Assistir</a></span>
                        </div>
                    </div>
                """
            cards_html += "</div>"
            try:
                st.markdown(cards_html, unsafe_allow_html=True)
            except Exception as e:
                st.dataframe(top10, use_container_width=True, hide_index=True)

    with abas[1]:
        st.subheader("Resumo por Categoria")
        resumo = resumo_por_categoria(df_filtered)
        sns.set_style("darkgrid")

        col_a, col_b = st.columns(2)

        with col_a:
            fig1, ax1 = plt.subplots(figsize=(10, 5.5))
            fig1.patch.set_facecolor("#0d1a26")
            ax1 = style_ax(ax1)
            cores_bar = ["#ff6b35", "#ff8c5a", "#ffa07a", "#ffb89a", "#ffd0ba"]
            bars = ax1.bar(resumo["categoria"], resumo["engajamento_medio"],
                           color=cores_bar[:len(resumo)], edgecolor="none", width=0.65)
            ax1.set_xlabel("Categoria", fontsize=10, labelpad=10)
            ax1.set_ylabel("Engajamento Médio", fontsize=10, labelpad=10)
            ax1.tick_params(axis="x", rotation=30, pad=6)
            ax1.set_title("Engajamento Médio por Categoria", fontsize=12, pad=12)
            for bar in bars:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width() / 2., height - height * 0.05,
                         f"{height:.0f}", ha="center", va="top", color="#ffffff",
                         fontsize=9, fontweight=600)
            fig1.tight_layout()
            st.pyplot(fig1)

        with col_b:
            fig2, ax2 = plt.subplots(figsize=(10, 5.5))
            fig2.patch.set_facecolor("#0d1a26")
            cores_pie = sns.color_palette("Set2", len(resumo))
            wedges, texts, autotexts = ax2.pie(
                resumo["total_visualizacoes"],
                labels=None,
                autopct="%1.1f%%",
                colors=cores_pie,
                startangle=90,
                pctdistance=0.75,
                textprops={"color": "#ffffff", "fontsize": 9, "fontweight": 600}
            )
            ax2.set_title("Distribuição de Visualizações", fontsize=12, pad=12, color="#e8eef5")
            ax2.legend(
                wedges, resumo["categoria"],
                loc="center left", bbox_to_anchor=(1, 0.5),
                frameon=False, fontsize=9,
                labelcolor="#b0c8dd"
            )
            fig2.tight_layout()
            st.pyplot(fig2)

        st.dataframe(resumo, use_container_width=True, hide_index=True)

    with abas[2]:
        st.subheader("Engajamento por Dia da Semana")

        dias = engajamento_por_dia(df_filtered)
        fig3, ax3 = plt.subplots(figsize=(10, 5))
        fig3.patch.set_facecolor("#0d1a26")
        ax3 = style_ax(ax3)
        ax3.plot(dias["dia_pt"], dias["media_engajamento"],
                 marker="o", linewidth=2.5, color="#ff6b35",
                 markerfacecolor="#ff4d4d", markeredgecolor="#ffffff",
                 markeredgewidth=1.5, markersize=9)
        for _, row in dias.iterrows():
            ax3.annotate(f"{row['media_engajamento']:.0f}",
                         xy=(row["dia_pt"], row["media_engajamento"]),
                         xytext=(0, 10), textcoords="offset points",
                         ha="center", va="bottom", fontsize=8,
                         color="#b0c8dd", fontweight=500)
        ax3.set_xlabel("Dia da Semana", fontsize=10, labelpad=10)
        ax3.set_ylabel("Engajamento Médio", fontsize=10, labelpad=10)
        ax3.set_title("Engajamento Médio por Dia da Semana", fontsize=12, pad=12)
        fig3.tight_layout()
        st.pyplot(fig3)

        st.subheader("Tendências das Categorias ao Longo do Tempo")
        tendencias = tendencias_categoria_ao_longo_tempo(df_filtered)
        if not tendencias.empty:
            fig4, ax4 = plt.subplots(figsize=(12, 5.5))
            fig4.patch.set_facecolor("#0d1a26")
            ax4 = style_ax(ax4)
            cores_linhas = ["#ff6b35", "#00bcd4", "#4ecdc4", "#ffd93d", "#ff4d4d", "#a78bfa", "#34d399"]
            for i, (cat, dados_cat) in enumerate(tendencias.groupby("categoria")):
                cor = cores_linhas[i % len(cores_linhas)]
                ax4.plot(dados_cat["mes_ano"], dados_cat["engajamento"],
                         marker="o", label=cat, linewidth=2.5, color=cor,
                         markerfacecolor=cor, markeredgecolor="none", markersize=7)
            ax4.set_xlabel("Mês / Ano", fontsize=10, labelpad=10)
            ax4.set_ylabel("Engajamento Total", fontsize=10, labelpad=10)
            ax4.set_title("Tendências de Engajamento por Categoria", fontsize=12, pad=12)
            ax4.legend(
                loc="upper left", bbox_to_anchor=(1.01, 1),
                frameon=True, facecolor=(0.08, 0.12, 0.18, 0.9),
                edgecolor=(1, 1, 1, 0.08), fontsize=9,
                labelcolor="#b0c8dd"
            )
            ax4.tick_params(axis="x", rotation=35, pad=6)
            fig4.tight_layout()
            st.pyplot(fig4)

    with abas[3]:
        colunas_exibir = ["video_id", "titulo_original", "canal", "categoria", "tags",
                          "visualizacoes", "curtidas", "comentarios",
                          "engajamento_total", "taxa_engajamento", "data_publicacao"]
        colunas_exibir = [c for c in colunas_exibir if c in df_filtered.columns]
        df_tabela = df_filtered[colunas_exibir].sort_values("engajamento_total", ascending=False)
        try:
            st.markdown(html_video_table(df_tabela, colunas_exibir), unsafe_allow_html=True)
        except Exception:
            st.dataframe(df_tabela, use_container_width=True, hide_index=True)

        csv = df_filtered.to_csv(index=False, encoding="utf-8")
        st.download_button(
            label="📥  Download CSV",
            data=csv,
            file_name="dados_esportivos_youtube.csv",
            mime="text/csv"
        )
