import re
import pandas as pd

ESPORTES = [
    dict(
        nome="Futebol Americano",
        detectar=[r"\bfutebol americano\b", r"\bfootball americano\b", r"\bnfl\b"],
        sub=[
            ("Futebol Americano - Melhores Momentos", [
                r"\btouchdown\b", r"\btd\b", r"\bfield goal\b",
                r"\bintercepta[çc][ãa]o\b", r"\binterceptacao\b",
                r"\bpasse\b", r"\bcorrida\b",
                r"\bhighlights?\b", r"\blances?\b",
                r"\bsuper bowl\b", r"\bsuperbowl\b", r"\bsack\b",
                r"\bmelhores momentos\b", r"\bjogadas?\b",
            ]),
            ("Futebol Americano - Análise", [
                r"\ban[áa]lise\b", r"\banalise\b", r"\bt[áa]tica\b",
                r"\bplay\b", r"\bplaybook\b", r"\bestratégia\b",
                r"\bquarterback\b", r"\bqb\b", r"\bdefense\b",
                r"\boffense\b", r"\bdraft\b", r"\branking\b",
                r"\bmock draft\b", r"\bpoder[áa]rio\b",
            ]),
        ],
    ),
    dict(
        nome="Futebol",
        detectar=[r"\bfutebol\b"],
        sub=[
            ("Futebol - Gols / Melhores Momentos", [
                r"\bgol\b", r"\bgols\b", r"\bgola[çc]o\b",
                r"\bhat[-\s]?trick\b", r"\bmelhores momentos\b",
                r"\bhighlights?\b", r"\blances?\b", r"\blances? do jogo\b",
                r"\btodos os gols\b", r"\bresumo\b", r"\bcompacto\b",
                r"\blances? emocionantes\b", r"\bjogada[ s]?\b",
                r"\bdefesa[ s]?\b", r"\bfinaliza[çc][ãa]o\b",
            ]),
            ("Futebol - Análise Tática", [
                r"\b[áa]nalise t[áa]tica\b", r"\bt[áa]tica\b",
                r"\besquema t[áa]tico\b", r"\bforma[çc][ãa]o\b",
                r"\b4[-\s]?4[-\s]?2\b", r"\b4[-\s]?3[-\s]?3\b",
                r"\bposse de bola\b", r"\bmarca[çc][ãa]o\b",
                r"\bpressing\b", r"\blinha defensiva\b",
                r"\bescalação\b", r"\bescalacao\b",
                r"\btransi[çc][ãa]o\b", r"\bbreakdown\b",
                r"\bxg\b", r"\bexpected goals\b", r"\bestat[íi]sticas?\b",
                r"\bdados\b", r"\bm[ée]tricas?\b", r"\bmapa de calor\b",
                r"\bdesempenho\b", r"\bperformance\b",
            ]),
            ("Futebol - Notícias / Mercado", [
                r"\bnot[íi]cias?\b", r"\bnews\b", r"\bbreaking\b",
                r"\bcontrata[çc][ãa]o\b", r"\btransfer[eê]ncia\b",
                r"\bmercado\b", r"\bnegocia[çc][ãa]o\b",
                r"\brenova[çc][ãa]o\b", r"\bcl[áa]usula\b",
                r"\bmulta\b", r"\bsa[íi]da\b", r"\bchegada\b",
                r"\brefor[çc]o\b", r"\bdispensa\b",
                r"\bempre[ée]stimo\b", r"\brumor\b",
            ]),
            ("Futebol - Entrevista / Coletiva", [
                r"\bentrevista\b", r"\bcoletiva\b",
                r"\bcoletiva de imprensa\b", r"\bdeclara[çc][ãa]o\b",
                r"\bdepoimento\b", r"\bexclusivo\b",
                r"\bperguntas?\b", r"\bafirma\b", r"\bcomenta\b",
            ]),
            ("Futebol - Vlog de Estádio / Bastidores", [
                r"\bvlog\b", r"\bbastidores\b", r"\bbackstage\b",
                r"\bdia[-\s]?a[-\s]?dia\b", r"\brotina\b",
                r"\bvesti[áa]rio\b", r"\bconcentra[çc][ãa]o\b",
                r"\bnoite de jogo\b", r"\bmatch[-\s]?day\b",
                r"\bdentro de campo\b", r"\btreino\b", r"\btraining\b",
                r"\bcct\b", r"\baquecimento\b",
                r"\best[áa]dio\b", r"\barena\b",
            ]),
            ("Futebol - Humor / Memes", [
                r"\bhumor\b", r"\bmeme\b", r"\bmemes\b",
                r"\bengra[çc]ado\b", r"\bpiada\b", r"\bfunny\b",
                r"\bcom[ée]dia\b", r"\bzuera\b", r"\bzueira\b",
                r"\bpar[ôo]dia\b", r"\bgafe\b", r"\bfail\b",
                r"\bpegadinha\b", r"\bmomentos engra[çc]ados\b",
            ]),
        ],
    ),
    dict(
        nome="Basquete",
        detectar=[r"\bbasquete\b", r"\bbasketball\b", r"\bnba\b"],
        sub=[
            ("Basquete - Melhores Momentos", [
                r"\bcesta\b", r"\bcestas?\b", r"\benterrada\b",
                r"\bdunk\b", r"\bala[-\s]?o\b",
                r"\bhighlights?\b", r"\blance[ s]?\b",
                r"\bpontos\b", r"\btriplo\b",
                r"\bthree[-\s]?pointer?\b", r"\bbandeja\b",
                r"\bgarrafao\b", r"\btabela\b",
                r"\bmelhor do jogo\b", r"\bresumo\b",
                r"\bmelhores momentos\b",
            ]),
            ("Basquete - Análise Tática", [
                r"\bt[áa]tica\b", r"\bestrat[ée]gia\b",
                r"\bdefesa\b", r"\bataque\b",
                r"\bpick[-\s]?and[-\s]?roll\b",
                r"\bala[-\s]?piv[ôo]\b", r"\barremesso\b",
                r"\besquema\b", r"\bplay\b",
            ]),
            ("Basquete - Notícias", [
                r"\bnot[íi]cias?\b", r"\btrade\b", r"\bdraft\b",
                r"\bcontrata[çc][ãa]o\b", r"\bfree agency\b",
                r"\btemporada\b", r"\bplayoffs?\b",
            ]),
        ],
    ),
    dict(
        nome="Esportes Radicais / Ação",
        detectar=[
            r"\besportes? radical\w*\b", r"\bskate\b",
            r"\bsurf\b", r"\bparkour\b", r"\bescalada\b",
            r"\bclimbing\b", r"\brapel\b", r"\bwingsuit\b",
            r"\bparaquedas\b", r"\bparapente\b",
            r"\bsnowboard\b", r"\besqui\b", r"\bski\b",
            r"\bmotocross\b", r"\bfreestyle\b", r"\bdownhill\b",
            r"\bbmx\b", r"\bmtb\b",
        ],
        sub=[],
    ),
    dict(
        nome="MMA / UFC / Boxe",
        detectar=[
            r"\bmm[aã]\b", r"\bufc\b", r"\bboxe\b", r"\bboxing\b",
            r"\bluta\b", r"\bluta livre\b", r"\bjiu[-\s]?jitsu\b",
            r"\bbjj\b", r"\bnocaute\b", r"\bknockout\b",
            r"\bfinaliza[çc][ãa]o\b", r"\bcintur[ãa]o\b",
            r"\bcampe[ãa]o\b", r"\bbelt\b", r"\bcombate\b",
            r"\bweight[-\s]?in\b", r"\bpesagem\b",
        ],
        sub=[],
    ),
    dict(
        nome="Tênis",
        detectar=[
            r"\bt[êe]nis\b", r"\btenis\b", r"\btennis\b",
            r"\bgrand slam\b", r"\bwimbledon\b",
            r"\bfrench open\b", r"\broland[-\s]?garros\b",
            r"\bustralian open\b", r"\bus open\b",
        ],
        sub=[],
    ),
    dict(
        nome="Vôlei",
        detectar=[
            r"\bv[ôo]lei\b", r"\bvolei\b", r"\bvolleyball\b",
            r"\bcortada\b", r"\bbloqueio\b", r"\brede\b",
            r"\blevantamento\b",
        ],
        sub=[],
    ),
    dict(
        nome="Automobilismo",
        detectar=[
            r"\bautomobilismo\b", r"\bf[óo]rmula[-\s]?1\b",
            r"\bf1\b", r"\bfórmula 1\b", r"\bformula 1\b",
            r"\bnascar\b", r"\bmoto gp\b", r"\bmotogp\b",
            r"\bworld rally\b", r"\bindy[-\s]?car\b",
            r"\bpole position\b", r"\bgrid\b",
            r"\bpit stop\b", r"\bgrande pr[êe]mio\b",
            r"\bgrand prix\b", r"\bcircuito\b",
            r"\blewis hamilton\b", r"\bverstappen\b",
        ],
        sub=[],
    ),
    dict(
        nome="Atletismo / Olimpíadas",
        detectar=[
            r"\batletismo\b", r"\bolimp[íi]ada\b",
            r"\bjogos ol[íi]mpicos\b", r"\bolympic\b",
            r"\bolympics?\b", r"\bmaratona\b",
            r"\bsalto\b", r"\blan[çc]amento\b",
            r"\barremesso\b", r"\brevezamento\b",
            r"\bheptatlo\b", r"\bdecatlo\b", r"\btriatlo\b",
            r"\bmedalha\b", r"\bp[óo]dio\b",
            r"\bnatação\b", r"\bnatacao\b", r"\bswimming\b",
            r"\bgin[áa]stica\b", r"\bginastica\b",
        ],
        sub=[],
    ),
    dict(
        nome="E-sports / Gameplay Esportivo",
        detectar=[
            r"\be[-\s]?sports?\b", r"\besports?\b",
            r"\bgaming\b", r"\bgameplay\b", r"\bfifa\b",
            r"\be[-\s]?football\b", r"\bpro[-\s]?evolution\b",
            r"\bpes\b", r"\bnba 2k\b", r"\bmadden\b",
            r"\btorneio de games?\b", r"\bstreamer\b",
            r"\bpartida de\b", r"\branked\b",
        ],
        sub=[],
    ),
    dict(
        nome="Outros Esportes",
        detectar=[
            r"\bgolfe?\b", r"\bgolf\b", r"\br[úu]gbi\b",
            r"\brugby\b", r"\bhandebol\b", r"\bhandball\b",
            r"\bbaseball\b", r"\bsoftball\b",
            r"\bcr[íi]quete\b", r"\bcricket\b",
            r"\bh[óo]quei\b", r"\bhockey\b",
            r"\bp[óo]lo aqu[áa]tico\b", r"\bwater polo\b",
            r"\bbadminton\b", r"\besgrima\b", r"\bfencing\b",
            r"\bhipismo\b",
        ],
        sub=[],
    ),
]

GENERICAS = [
    ("Entrevista / Podcast Esportivo", [
        r"\bpodcast\b", r"\bentrevista\b", r"\binterview\b",
        r"\bconversa\b", r"\bpap[oõ]\b", r"\bbate[-\s]?papo\b",
        r"\bdiscuss[ãa]o\b", r"\bdebate\b", r"\bmesa redonda\b",
        r"\broundtable\b", r"\bbate bola\b", r"\bstream\b",
        r"\bcortes?\b", r"\bpodpah\b", r"\bflow podcast\b",
    ]),
    ("Vlog / Bastidores Esportivos", [
        r"\bvlog\b", r"\bbastidores\b", r"\bbackstage\b",
        r"\bdia[-\s]?a[-\s]?dia\b", r"\brotina\b",
        r"\btreinos?\b", r"\btraining\b",
        r"\bprepara[çc][ãa]o\b", r"\bvida de atleta\b",
        r"\bviagem\b", r"\bdelega[çc][ãa]o\b",
        r"\bnoite de jogos?\b", r"\bmatchday\b",
    ]),
    ("Notícias Gerais Esportivas", [
        r"\bnot[íi]cias?\b", r"\bnews?\b",
        r"\b[úu]ltimas?\b", r"\bbreaking\b",
        r"\boficial\b", r"\bconfirmado\b",
        r"\bplantão\b", r"\bflash\b", r"\bupdate\b",
        r"\bmanchetes?\b", r"\btudo sobre\b",
    ]),
    ("Humor / Memes Esportivos", [
        r"\bhumor\b", r"\bmeme\b", r"\bmemes\b",
        r"\bengra[çc]ado\b", r"\bhil[áa]rio\b",
        r"\bpiada\b", r"\bfunny\b", r"\bcom[ée]dia\b",
        r"\bzuera\b", r"\bzueira\b", r"\bpar[ôo]dia\b",
        r"\bgafe\b", r"\bfail\b", r"\btroll\b",
        r"\btop 5\b", r"\btop 10\b",
    ]),
]


def _detectar_esporte(texto):
    for esporte in ESPORTES:
        for padrao in esporte["detectar"]:
            if re.search(padrao, texto):
                return esporte
    return None


def classificar_video_inteligente(titulo, descricao, tags):
    texto = f"{titulo} {descricao} {tags}".lower()

    esporte = _detectar_esporte(texto)
    if esporte is not None and esporte["sub"]:
        for nome_sub, padroes in esporte["sub"]:
            for padrao in padroes:
                if re.search(padrao, texto):
                    return nome_sub
        return esporte["nome"]

    if esporte is not None:
        return esporte["nome"]

    for nome_gen, padroes in GENERICAS:
        for padrao in padroes:
            if re.search(padrao, texto):
                return nome_gen

    return "Outros Esportes"


def classificar_dataframe(df):
    df = df.copy()
    df["categoria"] = df.apply(
        lambda row: classificar_video_inteligente(
            row.get("titulo", ""),
            row.get("descricao", ""),
            row.get("tags", ""),
        ),
        axis=1,
    )
    return df


# ─── Abordagem LLM (Gemini API) ───
# Descomente e configure a chave GEMINI_API_KEY no .env para usar.
#
# import google.generativeai as genai
# import os
#
# CATEGORIAS_LLM = [
#     "Futebol - Gols / Melhores Momentos",
#     "Futebol - Análise Tática",
#     "Futebol - Notícias / Mercado",
#     "Futebol - Entrevista / Coletiva",
#     "Futebol - Vlog de Estádio / Bastidores",
#     "Futebol - Humor / Memes",
#     "Basquete - Melhores Momentos",
#     "Basquete - Análise Tática",
#     "Basquete - Notícias",
#     "Futebol Americano - Melhores Momentos",
#     "Futebol Americano - Análise",
#     "Esportes Radicais / Ação",
#     "MMA / UFC / Boxe",
#     "Tênis",
#     "Vôlei",
#     "Automobilismo",
#     "Atletismo / Olimpíadas",
#     "E-sports / Gameplay Esportivo",
#     "Entrevista / Podcast Esportivo",
#     "Vlog / Bastidores Esportivos",
#     "Notícias Gerais Esportivas",
#     "Humor / Memes Esportivos",
#     "Outros Esportes",
# ]
#
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# modelo = genai.GenerativeModel("gemini-2.0-flash")
#
# PROMPT_TEMPLATE = """
# Classifique o vídeo esportivo abaixo em UMA das categorias da lista.
# Responda APENAS com o nome exato da categoria, sem explicações.
#
# Categorias:
# {categorias}
#
# Título: {titulo}
# Descrição: {descricao}
# Tags: {tags}
#
# Categoria:
# """
#
# def classificar_video_llm(titulo, descricao, tags):
#     prompt = PROMPT_TEMPLATE.format(
#         categorias="\n".join(f"- {c}" for c in CATEGORIAS_LLM),
#         titulo=titulo,
#         descricao=descricao[:500],
#         tags=tags,
#     )
#     try:
#         resposta = modelo.generate_content(prompt)
#         cat = resposta.text.strip()
#         return cat if cat in CATEGORIAS_LLM else "Outros Esportes"
#     except Exception:
#         return "Outros Esportes"
