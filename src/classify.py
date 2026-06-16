import re
import pandas as pd

CATEGORIAS_ESPECIFICAS = {
    "Futebol - Gols / Melhores Momentos": [
        r"\bgol\b", r"\bgols\b", r"\bgola[çc]o\b", r"\bhat[-\s]?trick\b",
        r"\bmelhores momentos\b", r"\bhighlights?\b", r"\blances?\b",
        r"\blances? do jogo\b", r"\btodos os gols\b", r"\bresumo\b",
        r"\bcompacto\b", r"\blances? emocionantes\b", r"\bjogada[ s]?\b",
        r"\bdefesa[ s]?\b", r"\bfinaliza[çc][ãa]o\b",
    ],
    "Futebol - Análise Tática": [
        r"\b[áa]nalise t[áa]tica\b", r"\bt[áa]tica\b", r"\bt[áa]tico\b",
        r"\besquema t[áa]tico\b", r"\bforma[çc][ãa]o\b", r"\b4[-\s]?4[-\s]?2\b",
        r"\b4[-\s]?3[-\s]?3\b", r"\bposse de bola\b", r"\btriangula[çc][ãa]o\b",
        r"\bmarca[çc][ãa]o\b", r"\bpressing\b", r"\blinha defensiva\b",
        r"\bescalação\b", r"\bescalacao\b", r"\btransi[çc][ãa]o\b",
        r"\blance[-\s]?a[-\s]?lance\b", r"\bbreakdown\b",
        r"\bdata[-\s]?driven\b", r"\bestat[íi]sticas?\b", r"\bdados\b",
        r"\bm[ée]tricas?\b", r"\bxg\b", r"\bexpected goals\b",
        r"\bexpected assists\b", r"\bmapa de calor\b",
        r"\bdesempenho\b", r"\bperformance\b",
    ],
    "Futebol - Notícias / Mercado": [
        r"\bnot[íi]cias?\b", r"\bnot[íi]cia\b", r"\bnews\b", r"\bbreaking\b",
        r"\b[úu]ltima hora\b", r"\boficial\b", r"\bconfirmado\b",
        r"\bcontrata[çc][ãa]o\b", r"\bcontratacao\b", r"\btransfer[eê]ncia\b",
        r"\btransferencia\b", r"\bmercado\b", r"\bnegocia[çc][ãa]o\b",
        r"\bnegociacao\b", r"\brenova[çc][ãa]o\b", r"\brenovacao\b",
        r"\bcl[áa]usula\b", r"\bmulta\b", r"\bsa[íi]da\b", r"\bsaida\b",
        r"\bchegada\b", r"\brefor[çc]o\b", r"\breforco\b", r"\bcontratação\b",
        r"\bdispensa\b", r"\bempre[ée]stimo\b", r"\bemprestimo\b",
        r"\bapresenta[çc][ãa]o\b", r"\bapresentacao\b",
        r"\brumor\b", r"\brumors?\b", r"\bspeculation\b",
    ],
    "Futebol - Entrevista / Coletiva": [
        r"\bentrevista\b", r"\binterview\b", r"\bcoletiva\b",
        r"\bcoletiva de imprensa\b", r"\bpression\s?conference\b",
        r"\bfala [a-zà-ú]+", r"\bdeclara[çc][ãa]o\b", r"\bdeclaracao\b",
        r"\bdepoimento\b", r"\bperguntas?\b", r"\brespostas?\b",
        r"\bexclusivo\b", r"\bconversa\b", r"\bpapo[^s]?\b",
        r"\bdiz [a-zà-ú]+", r"\bafirma\b", r"\bcomenta\b",
    ],
    "Futebol - Vlog de Estádio / Bastidores": [
        r"\bvlog\b", r"\bbastidores\b", r"\bbackstage\b", r"\bdia[-\s]?a[-\s]?dia\b",
        r"\brotina\b", r"\bvesti[áa]rio\b", r"\bvestiario\b",
        r"\bconcentra[çc][ãa]o\b", r"\bconcentracao\b",
        r"\bnoite de jogo\b", r"\bmatch[-\s]?day\b", r"\bgameday\b",
        r"\bdentro de campo\b", r"\bpreparação\b", r"\bpreparacao\b",
        r"\baquecimento\b", r"\btreino\b", r"\btraining\b",
        r"\bcct\b", r"\bcentro de treinamento\b",
        r"\best[áa]dio\b", r"\bestadio\b", r"\barena\b",
        r"\btour pelo est[áa]dio\b", r"\btour pelo estadio\b",
    ],
    "Futebol - Humor / Memes": [
        r"\bhumor\b", r"\bmeme\b", r"\bmemes\b", r"\bengra[çc]ado\b",
        r"\bengracado\b", r"\bhil[áa]rio\b", r"\bhilario\b", r"\bpiada\b",
        r"\bfunny\b", r"\bcom[ée]dia\b", r"\bcomedia\b", r"\bzuera\b",
        r"\bzueira\b", r"\bzoação\b", r"\bzoacao\b", r"\bbesteirol\b",
        r"\bpar[ôo]dia\b", r"\bparodia\b", r"\bgafe\b", r"\bfail\b",
        r"\bpegadinha\b", r"\bcortina[^s]?\b", r"\bcompila[çc][ãa]o\b",
        r"\bcompilacao\b", r"\bmomentos engra[çc]ados\b",
    ],
    "Basquete - Melhores Momentos": [
        r"\bbasquete\b", r"\bbasketball\b", r"\bnba\b", r"\bcesta\b",
        r"\bcestas?\b", r"\benterrada\b", r"\bdunk\b", r"\bala\b",
        r"\blance[ s]?\b", r"\bhighlights?\b", r"\bpontos\b",
        r"\btriplo\b", r"\bthree[-\s]?pointer?\b",
        r"\bbandeja\b", r"\bgarrafao\b", r"\btabela\b",
        r"\bmelhor do jogo\b", r"\bresumo\b",
    ],
    "Basquete - Análise Tática": [
        r"\bbasquete\b", r"\bbasketball\b", r"\bnba\b",
        r"\bt[áa]tica\b", r"\bestrat[ée]gia\b", r"\bestrategia\b",
        r"\bdefesa\b", r"\bataque\b", r"\boffense\b", r"\bdefense\b",
        r"\bpick[-\s]?and[-\s]?roll\b", r"\bbola[-\s]?alta\b",
        r"\bala[-\s]?piv[ôo]\b", r"\barremesso\b",
        r"\besquema\b", r"\bplay\b", r"\bplaybook\b",
    ],
    "Basquete - Notícias": [
        r"\bbasquete\b", r"\bbasketball\b", r"\bnba\b",
        r"\bnot[íi]cias?\b", r"\btrade\b", r"\bdraft\b",
        r"\bcontrata[çc][ãa]o\b", r"\bfree agency\b",
        r"\btemporada\b", r"\bplayoffs?\b", r"\bfinals?\b",
    ],
    "Futebol Americano - Melhores Momentos": [
        r"\bfutebol americano\b", r"\bfootball americano\b",
        r"\bnfl\b", r"\btouchdown\b", r"\btd\b",
        r"\bfield goal\b", r"\bintercepta[çc][ãa]o\b",
        r"\binterceptacao\b", r"\bpasse\b", r"\bcorrida\b",
        r"\bhighlights?\b", r"\blances?\b",
        r"\bsuper bowl\b", r"\bsuperbowl\b", r"\bsack\b",
    ],
    "Futebol Americano - Análise": [
        r"\bfutebol americano\b", r"\bnfl\b",
        r"\ban[áa]lise\b", r"\bt[áa]tica\b", r"\bplay\b",
        r"\bplaybook\b", r"\bestratégia\b", r"\bestrategia\b",
        r"\bquarterback\b", r"\bqb\b", r"\bdefense\b", r"\boffense\b",
        r"\bdraft\b", r"\branking\b", r"\bmock draft\b",
        r"\bpoder[áa]rio\b", r"\bpoderario\b",
    ],
    "Esportes Radicais / Ação": [
        r"\besportes? radical\w*\b", r"\bskate\b", r"\bskateboarding\b",
        r"\bsurf\b", r"\bsurfing\b", r"\bparkour\b",
        r"\bescalada\b", r"\bclimbing\b", r"\brapel\b",
        r"\bwingsuit\b", r"\bbase jump\b", r"\bparaquedas\b",
        r"\bparapente\b", r"\basa delta\b", r"\bsnowboard\b",
        r"\besqui\b", r"\bski\b", r"\bmoto[^r]\b",
        r"\bmotocross\b", r"\bfreestyle\b", r"\bmanobra\b",
        r"\bradical\b", r"\bdownhill\b", r"\bbmx\b", r"\bmtb\b",
    ],
    "MMA / UFC / Boxe": [
        r"\bmm[aã]\b", r"\bufc\b", r"\bboxe\b", r"\bboxing\b",
        r"\bluta\b", r"\bluta livre\b", r"\bjiu[-\s]?jitsu\b",
        r"\bbjj\b", r"\bnocaute\b", r"\bknockout\b", r"\bko\b",
        r"\bfinaliza[çc][ãa]o\b", r"\bfinalizacao\b", r"\bweight[-\s]?in\b",
        r"\bpesagem\b", r"\bcintur[ãa]o\b", r"\bcinturao\b",
        r"\bcampe[ãa]o\b", r"\bcampeao\b", r"\bbelt\b",
        r"\bcard\b", r"\bluta[ s]?\b", r"\bcombate\b",
    ],
    "Tênis": [
        r"\bt[êe]nis\b", r"\btenis\b", r"\btennis\b",
        r"\bgrand slam\b", r"\bwimbledon\b", r"\bustralian open\b",
        r"\bfrench open\b", r"\b Roland[-\s]?Garros\b", r"\bUS open\b",
        r"\bsaques?\b", r"\brace\b", r"\bbackhand\b", r"\bforehand\b",
        r"\b match point\b", r"\bset point\b", r"\bbreak point\b",
    ],
    "Vôlei": [
        r"\bv[ôo]lei\b", r"\bvolei\b", r"\bvolleyball\b",
        r"\bsaque\b", r"\bcortada\b", r"\bbloqueio\b", r"\bdefesa\b",
        r"\bmatch point\b", r"\bset\b", r"\brede\b",
        r"\blevantamento\b", r"\bataque\b",
    ],
    "Automobilismo": [
        r"\bautomobilismo\b", r"\bf[óo]rmula[-\s]?1\b", r"\bf1\b",
        r"\bfórmula 1\b", r"\bformula 1\b", r"\bnascar\b",
        r"\bmoto gp\b", r"\bmotogp\b", r"\bworld rally\b",
        r"\bwr[cê]\b", r"\bindi[áa]polis?\b", r"\bindy[-\s]?car\b",
        r"\bpole position\b", r"\bgrid\b", r"\bvolta r[áa]pida\b",
        r"\bpit stop\b", r"\box\b", r"\btemporada\b",
        r"\bgrande pr[êe]mio\b", r"\bgrand prix\b",
        r"\bcorrida\b", r"\bcircuito\b", r"\bpista\b",
        r"\blewis hamilton\b", r"\bverstappen\b", r"\bsenna\b",
    ],
    "Atletismo / Olimpíadas": [
        r"\batletismo\b", r"\bolimp[íi]ada\b", r"\bolimpiada\b",
        r"\bjogos ol[íi]mpicos\b", r"\bolympic\b", r"\bolympics?\b",
        r"\bcorrida\b", r"\bmaratona\b", r"\b100m\b", r"\b200m\b",
        r"\bsalto\b", r"\blan[çc]amento\b", r"\blancamento\b",
        r"\barremesso\b", r"\brevezamento\b", r"\breveza[çc][ãa]o\b",
        r"\bheptatlo\b", r"\bdecatlo\b", r"\btriatlo\b",
        r"\bmedalha\b", r"\bpódio\b", r"\bpodio\b",
        r"\bnatação\b", r"\bnatacao\b", r"\bswimming\b",
        r"\bgin[áa]stica\b", r"\bginastica\b",
    ],
    "E-sports / Gameplay Esportivo": [
        r"\be[-\s]?sports?\b", r"\besports?\b", r"\bgaming\b",
        r"\bgameplay\b", r"\bfifa\b", r"\be[-\s]?football\b",
        r"\bpro[-\s]?evolution\b", r"\bpes\b", r"\bnba 2k\b",
        r"\bmadden\b", r"\bcampeonato de games?\b",
        r"\btorneio de games?\b", r"\bstreamer\b",
        r"\blive\b", r"\bjogando\b", r"\bjogar\b",
        r"\bpartida de\b", r"\branked\b",
    ],
    "Entrevista / Podcast Esportivo": [
        r"\bpodcast\b", r"\bpodcast esportivo\b",
        r"\bentrevista\b", r"\binterview\b", r"\bconversa\b",
        r"\bpap[oõ]\b", r"\bbate[-\s]?papo\b", r"\bdiscuss[ãa]o\b",
        r"\bdiscussao\b", r"\bdebate\b", r"\bmesa redonda\b",
        r"\broundtable\b", r"\bparticipa[çc][ãa]o\b",
        r"\bbate bola\b", r"\bprograma\b", r"\blive\b",
        r"\bstream\b", r"\bcortes?\b", r"\bpodpah\b",
        r"\bflow podcast\b", r"\binteligência [lL]tda\b",
    ],
    "Vlog / Bastidores Esportivos": [
        r"\bvlog\b", r"\bbastidores\b", r"\bbackstage\b",
        r"\bdia[-\s]?a[-\s]?dia\b", r"\brotina\b", r"\btreinos?\b",
        r"\btraining\b", r"\bprepara[çc][ãa]o\b", r"\bpreparacao\b",
        r"\bvida de atleta\b", r"\bcct\b", r"\bconcentração\b",
        r"\bconcentracao\b", r"\bviagem\b", r"\bdelegação\b",
        r"\bdelegacao\b", r"\bvestiário\b", r"\bvestiario\b",
        r"\bnoite de jogos?\b", r"\bmatchday\b",
    ],
    "Notícias Gerais Esportivas": [
        r"\bnot[íi]cias?\b", r"\bnews?\b", r"\b[úu]ltimas?\b",
        r"\bbreaking\b", r"\boficial\b", r"\bconfirmado\b",
        r"\bagora\b", r"\bao vivo\b", r"\bplantão\b", r"\bplantao\b",
        r"\bflash\b", r"\bupdate\b", r"\bround[-\s]?up\b",
        r"\broundup\b", r"\bresumo\b", r"\bmanchetes?\b",
        r"\bjornal\b", r"\btudo sobre\b",
    ],
    "Humor / Memes Esportivos": [
        r"\bhumor\b", r"\bmeme\b", r"\bmemes\b", r"\bengra[çc]ado\b",
        r"\bengracado\b", r"\bhil[áa]rio\b", r"\bhilario\b",
        r"\bpiada\b", r"\bfunny\b", r"\bcom[ée]dia\b", r"\bcomedia\b",
        r"\bzuera\b", r"\bzueira\b", r"\bpar[ôo]dia\b", r"\bparodia\b",
        r"\bgafe\b", r"\bfail\b", r"\btroll\b", r"\bs[ée]rie\b",
        r"\bserie\b", r"\btop 5\b", r"\btop 10\b",
        r"\bmelhores momentos engra[çc]ados\b",
    ],
    "Outros Esportes": [
        r"\bgolfe?\b", r"\bgolf\b", r"\br[úu]gbi\b", r"\brugby\b",
        r"\bhandebol\b", r"\bhandball\b", r"\bbaseball\b", r"\bsoftball\b",
        r"\bcr[íi]quete\b", r"\bcricket\b", r"\bh[óo]quei\b", r"\bhockey\b",
        r"\bp[óo]lo aqu[áa]tico\b", r"\bwater polo\b",
        r"\bpeteca\b", r"\bbadminton\b", r"\besgrima\b", r"\bfencing\b",
        r"\bhipismo\b", r"\bcorrida de cavalos?\b", r"\bcurling\b",
    ],
}

def classificar_video_inteligente(titulo, descricao, tags):
    texto = f"{titulo} {descricao} {tags}".lower()
    for categoria, padroes in CATEGORIAS_ESPECIFICAS.items():
        for padrao in padroes:
            if re.search(padrao, texto):
                return categoria
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
# PROMPT_TEMPLATE = '''
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
# '''
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
