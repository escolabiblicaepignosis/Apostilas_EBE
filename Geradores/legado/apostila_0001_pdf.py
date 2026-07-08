# -*- coding: utf-8 -*-
"""
Versão PDF da APOSTILA 0001 — Escola Bíblica Epignósis
«O Estado de Perdição do Ser Humano»

Gera EBE-APO-0001_O_Estado_de_Perdicao_do_Ser_Humano.pdf com o mesmo
conteúdo e identidade visual da versão .docx (EBE-APO-0001).

Nota técnica: neste ambiente não há LibreOffice para conversão directa
do .docx; o PDF é composto com ReportLab. A fonte usada é DejaVu Serif
(serifada, com suporte ao grego politónico), substituindo o Garamond
apenas nesta pré-visualização.
"""
import os

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table,
    TableStyle, Image, PageBreak, HRFlowable, KeepTogether,
)

BASE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(BASE, "_assets", "fonts")
LOGO = os.path.join(BASE, "_assets", "logo_ebe.png")

CODIGO = "EBE-APO-0001"
TITULO_DOC = "Apostila — O Estado de Perdição do Ser Humano"

# === Paleta institucional ===
AZUL = HexColor("#1B3A5C")
VERDE = HexColor("#2E7D4F")
DOURADO = HexColor("#C9A14B")
TEXTO = HexColor("#1A1A1A")
CINZA = HexColor("#555555")
VERDE_CLARO = HexColor("#E8F1EC")
CINZA_LINHA = HexColor("#C8C8C8")

# === Fontes ===
pdfmetrics.registerFont(TTFont("Serif", os.path.join(FONTS, "DejaVuSerif.ttf")))
pdfmetrics.registerFont(TTFont("Serif-Bold", os.path.join(FONTS, "DejaVuSerif-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Serif-Italic", os.path.join(FONTS, "DejaVuSerif-Italic.ttf")))
pdfmetrics.registerFont(TTFont("Serif-BoldItalic", os.path.join(FONTS, "DejaVuSerif-BoldItalic.ttf")))
pdfmetrics.registerFontFamily(
    "Serif", normal="Serif", bold="Serif-Bold",
    italic="Serif-Italic", boldItalic="Serif-BoldItalic")

# === Estilos ===
def st(name, **kw):
    base = dict(fontName="Serif", fontSize=10.5, leading=15.5,
                textColor=TEXTO, alignment=TA_JUSTIFY, spaceAfter=6)
    base.update(kw)
    return ParagraphStyle(name, **base)

S = {
    "corpo":      st("corpo"),
    "lema":       st("lema", fontName="Serif-Italic", fontSize=9.5, textColor=VERDE, alignment=TA_CENTER),
    "capa_inst":  st("capa_inst", fontName="Serif-Bold", fontSize=11, textColor=VERDE, alignment=TA_CENTER, spaceBefore=6),
    "capa_curso": st("capa_curso", fontSize=9, textColor=CINZA, alignment=TA_CENTER),
    "capa_num":   st("capa_num", fontName="Serif-Bold", fontSize=12, textColor=VERDE, alignment=TA_CENTER, spaceBefore=14),
    "capa_tit":   st("capa_tit", fontName="Serif-Bold", fontSize=24, leading=30, textColor=AZUL, alignment=TA_CENTER, spaceBefore=8),
    "capa_sub":   st("capa_sub", fontName="Serif-Italic", fontSize=12, leading=16, alignment=TA_CENTER, spaceBefore=6),
    "capa_cod":   st("capa_cod", fontSize=8.5, textColor=CINZA, alignment=TA_CENTER),
    "h1":         st("h1", fontName="Serif-Bold", fontSize=13.5, leading=17, textColor=AZUL, alignment=TA_LEFT, spaceBefore=16, spaceAfter=2, keepWithNext=1),
    "h2":         st("h2", fontName="Serif-Bold", fontSize=12, leading=15, textColor=AZUL, alignment=TA_LEFT, spaceBefore=11, spaceAfter=4, keepWithNext=1),
    "h3":         st("h3", fontName="Serif-Bold", fontSize=10.5, leading=14, textColor=VERDE, alignment=TA_LEFT, spaceBefore=8, spaceAfter=2, keepWithNext=1),
    "citacao":    st("citacao", fontName="Serif-Italic", fontSize=9.5, leading=14, textColor=CINZA, leftIndent=1.5*cm, rightIndent=1.0*cm, spaceBefore=5, spaceAfter=5),
    "lista":      st("lista", leftIndent=0.8*cm, firstLineIndent=-0.5*cm, spaceAfter=3),
    "marco_tit":  st("marco_tit", fontName="Serif-Bold", fontSize=12, textColor=VERDE, alignment=TA_CENTER),
    "marco_txt":  st("marco_txt", fontName="Serif-Italic", fontSize=13, leading=19, textColor=AZUL, alignment=TA_CENTER, leftIndent=1.5*cm, rightIndent=1.5*cm),
    "marco_ass":  st("marco_ass", fontSize=9.5, textColor=CINZA, alignment=TA_CENTER),
    "marco_ef":   st("marco_ef", fontName="Serif-Italic", fontSize=9.5, leading=13.5, textColor=CINZA, alignment=TA_CENTER, leftIndent=1.5*cm, rightIndent=1.5*cm),
    "selo1":      st("selo1", fontName="Serif-Bold", fontSize=11, textColor=AZUL, alignment=TA_CENTER),
    "selo2":      st("selo2", fontName="Serif-Italic", fontSize=10, textColor=VERDE, alignment=TA_CENTER),
    "selo3":      st("selo3", fontName="Serif-Italic", fontSize=9, textColor=CINZA, alignment=TA_CENTER),
    "tbl":        st("tbl", fontSize=9, leading=12.5, spaceAfter=0),
    "tbl_hdr":    st("tbl_hdr", fontName="Serif-Bold", fontSize=9, leading=12, textColor=white, alignment=TA_CENTER, spaceAfter=0),
    "destaque":   st("destaque", fontSize=9.5, leading=14, spaceAfter=0),
    "texto_base": st("texto_base", fontName="Serif-Bold", fontSize=13, textColor=VERDE, alignment=TA_CENTER, spaceBefore=6),
}


def linha(color=VERDE, width=0.8, space_b=2, space_a=6):
    return HRFlowable(width="100%", thickness=width, color=color,
                      spaceBefore=space_b, spaceAfter=space_a)


def h1(texto):
    return [Paragraph(texto.upper(), S["h1"]), linha(AZUL, 0.9, 1, 8)]


def cit(texto, ref=None):
    extra = f'  <font size="8.5" color="#2E7D4F">({ref}, ARC)</font>' if ref else ""
    return Paragraph(f"“{texto}”{extra}", S["citacao"])


def lista(itens, ordenada=False):
    out = []
    for i, item in enumerate(itens, 1):
        marca = f"{i}." if ordenada else "•"
        out.append(Paragraph(
            f'<font color="#2E7D4F"><b>{marca}</b></font>&nbsp;&nbsp;{item}',
            S["lista"]))
    return out


def quadro_destaque(rotulo, texto):
    p = Paragraph(
        f'<font color="#2E7D4F"><b>◆ {rotulo}:</b></font>&nbsp; <i>{texto}</i>',
        S["destaque"])
    t = Table([[p]], colWidths=[15.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), VERDE_CLARO),
        ("BOX", (0, 0), (-1, -1), 0.5, CINZA_LINHA),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return [Spacer(1, 4), t, Spacer(1, 6)]


def tabela(headers, rows, widths):
    data = [[Paragraph(h, S["tbl_hdr"]) for h in headers]]
    for r in rows:
        data.append([Paragraph(c, S["tbl"]) for c in r])
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), AZUL),
        ("GRID", (0, 0), (-1, -1), 0.5, CINZA_LINHA),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def logo_img(largura_cm):
    ir = ImageReader(LOGO)
    iw, ih = ir.getSize()
    w = largura_cm * cm
    return Image(LOGO, width=w, height=w * ih / iw)


# ====== Cabeçalho / rodapé ======
def _pagina(canvas, doc_, com_cabecalho=True):
    canvas.saveState()
    W, H = A4
    if com_cabecalho:
        canvas.setFont("Serif-Italic", 8)
        canvas.setFillColor(VERDE)
        canvas.drawRightString(W - 2.5*cm, H - 1.6*cm,
                               f"Escola Bíblica Epignósis  ·  {TITULO_DOC}")
    canvas.setFont("Serif", 8)
    canvas.setFillColor(CINZA)
    canvas.drawCentredString(W / 2, 1.4*cm, f"{CODIGO}  ·  {doc_.page}")
    canvas.restoreState()


def pagina_normal(canvas, doc_):
    _pagina(canvas, doc_, com_cabecalho=True)


def pagina_capa(canvas, doc_):
    _pagina(canvas, doc_, com_cabecalho=False)


def gerar():
    out = os.path.join(BASE, "EBE-APO-0001_O_Estado_de_Perdicao_do_Ser_Humano.pdf")
    doc = BaseDocTemplate(
        out, pagesize=A4,
        topMargin=2.5*cm, bottomMargin=2.5*cm,
        leftMargin=3.0*cm, rightMargin=2.5*cm,
        title=TITULO_DOC, author="Escola Bíblica Epignósis",
        subject="Material didáctico oficial · EBE-APO-0001",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
    doc.addPageTemplates([
        PageTemplate(id="Capa", frames=[frame], onPage=pagina_capa),
        PageTemplate(id="Normal", frames=[frame], onPage=pagina_normal),
    ])

    E = []  # elementos

    # ================= CAPA =================
    E.append(Spacer(1, 10))
    E.append(logo_img(5.0))
    E.append(Spacer(1, 6))
    E.append(Paragraph("Conhecer a Deus. Viver a Palavra. Manifestar o Reino.", S["lema"]))
    E.append(linha(VERDE, 1.0, 4, 8))
    E.append(Paragraph("INSTITUTO DE FORMAÇÃO CRISTÃ", S["capa_inst"]))
    E.append(Paragraph(
        "Escola de Fundamentos da Fé  ·  Curso «Salvação e Novo Nascimento»  ·  "
        "Módulo 1 — Fundamentos da Salvação", S["capa_curso"]))
    E.append(Paragraph("APOSTILA N.º  01", S["capa_num"]))
    E.append(Paragraph("O Estado de Perdição do Ser Humano", S["capa_tit"]))
    E.append(Paragraph(
        "Compreender a nossa condição sem Cristo para valorizar a salvação em Cristo",
        S["capa_sub"]))
    E.append(Spacer(1, 22))

    ident = [
        ("Autor / Docente", "Direcção Pedagógica · Escola Bíblica Epignósis"),
        ("Carga horária estimada", "2 horas de estudo"),
        ("Nível formativo", "Nível 1 — Discípulo (Conhecer)"),
        ("Edição / Ano", "1.ª edição — 2026"),
    ]
    rows = [[Paragraph(f'<font color="#1B3A5C"><b>{k}</b></font>', S["tbl"]),
             Paragraph(v, S["tbl"])] for k, v in ident]
    t = Table(rows, colWidths=[5.2*cm, 9.3*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), VERDE_CLARO),
        ("GRID", (0, 0), (-1, -1), 0.5, CINZA_LINHA),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    t.hAlign = "CENTER"
    E.append(t)
    E.append(Spacer(1, 20))
    E.append(linha(VERDE, 0.8, 2, 6))
    E.append(Paragraph(f"Material didáctico oficial · Código {CODIGO} · 2026", S["capa_cod"]))
    E.append(PageBreak())

    # ================= MARCO FILOSÓFICO =================
    E.append(Spacer(1, 130))
    E.append(Paragraph("MARCO FILOSÓFICO", S["marco_tit"]))
    E.append(linha(VERDE, 0.8, 4, 16))
    E.append(Paragraph(
        "“Acreditamos que o verdadeiro conhecimento de Deus transforma "
        "a mente pela verdade das Escrituras, o coração pela acção do "
        "Espírito Santo e a vida pelo compromisso de viver e anunciar "
        "o Evangelho de Jesus Cristo.”", S["marco_txt"]))
    E.append(Spacer(1, 14))
    E.append(Paragraph("— Escola Bíblica Epignósis —", S["marco_ass"]))
    E.append(Spacer(1, 20))
    E.append(Paragraph(
        "“Até que todos cheguemos à unidade da fé e ao pleno conhecimento "
        "(ἐπίγνωσις) do Filho de Deus, a homem perfeito, à medida da estatura "
        "completa de Cristo.”<br/>Efésios 4.13", S["marco_ef"]))
    E.append(PageBreak())

    # ================= FICHA TÉCNICA =================
    E += h1("Ficha Técnica")
    E.append(Paragraph(
        "Este material didáctico é propriedade intelectual da Escola Bíblica "
        "Epignósis (EBE), produzido para uso exclusivo no âmbito dos seus "
        "programas de formação. A sua reprodução, no todo ou em parte, "
        "depende de autorização institucional escrita.", S["corpo"]))
    E += lista([
        "Título da apostila: O Estado de Perdição do Ser Humano.",
        "Curso: Salvação e Novo Nascimento (25 h).",
        "Módulo: 1 — Fundamentos da Salvação (Apostila 1 de 3).",
        "Escola: Escola de Fundamentos da Fé · Instituto de Formação Cristã.",
        "Nível formativo: Nível 1 — Discípulo (Conhecer).",
        "Autor / Docente: Direcção Pedagógica da Escola Bíblica Epignósis.",
        "Revisão pedagógica: Coordenação Acadêmica.",
        "Revisão doutrinária: Conselho Doutrinário (cf. EBE-DOC-002, Art. 6.º e 7.º).",
        "Versão bíblica de referência: Almeida Revista e Corrigida (ARC).",
        "Edição: 1.ª — 2026.",
        f"Código institucional: {CODIGO}.",
    ])
    E.append(cit("Porque o Filho do Homem veio buscar e salvar o que se havia perdido.",
                 "Lucas 19.10"))
    E.append(PageBreak())

    # ================= SUMÁRIO =================
    E += h1("Sumário")
    E += lista([
        "Apresentação da apostila",
        "Objectivos de aprendizagem",
        "Versículo-chave",
        "Texto-base para leitura",
        "1. Introdução — Por que começar pela má notícia",
        "2. Desenvolvimento do conceito central",
        "&nbsp;&nbsp;&nbsp;2.1 Fundamentos bíblicos",
        "&nbsp;&nbsp;&nbsp;2.2 O que significa estar «perdido»",
        "&nbsp;&nbsp;&nbsp;2.3 As quatro dimensões da perdição humana",
        "&nbsp;&nbsp;&nbsp;2.4 Dúvidas e equívocos comuns",
        "&nbsp;&nbsp;&nbsp;2.5 Quadro de destaque — para reter",
        "3. Aplicação prática",
        "4. Síntese e conclusão",
        "Exercícios de revisão",
        "Estudo bíblico complementar — Lucas 15: o perdido aos olhos de Deus",
        "Para a próxima apostila",
        "Glossário",
        "Bibliografia recomendada",
        "Anotações pessoais",
    ])
    E.append(PageBreak())

    # ================= APRESENTAÇÃO =================
    E += h1("Apresentação da Apostila")
    E.append(Paragraph(
        "Esta apostila abre o Módulo 1 — Fundamentos da Salvação — do Curso "
        "«Salvação e Novo Nascimento», o primeiro curso da Escola de "
        "Fundamentos da Fé. É, por isso, a porta de entrada de toda a "
        "jornada formativa Epignósis: antes de aprender qualquer doutrina, "
        "o discípulo precisa de compreender de onde Deus o resgatou.", S["corpo"]))
    E.append(Paragraph(
        "O Evangelho é uma boa notícia. Mas nenhuma boa notícia é "
        "plenamente entendida sem se conhecer a má notícia que a precede: "
        "fora de Cristo, o ser humano está perdido, separado de Deus pelo "
        "pecado e incapaz de se salvar por esforço próprio. Nesta apostila "
        "estudaremos o que a Escritura ensina sobre esse estado de "
        "perdição — a sua origem, a sua extensão e as suas consequências —, "
        "não para nos deixar no desespero, mas para nos conduzir, com "
        "gratidão e humildade, à graça de Deus em Cristo, tema da próxima "
        "apostila.", S["corpo"]))
    E.append(Paragraph(
        "Ao final do estudo, o aluno terá alicerces firmes para compreender "
        "por que a salvação é inteiramente obra da graça de Deus, e estará "
        "preparado para testemunhar do Evangelho com clareza e compaixão.", S["corpo"]))

    # ================= OBJECTIVOS =================
    E += h1("Objectivos de Aprendizagem")
    E.append(Paragraph("Ao concluir o estudo desta apostila, o(a) aluno(a) será capaz de:", S["corpo"]))
    E += lista([
        "<b>CONHECER</b> — explicar, a partir das Escrituras, a origem do pecado "
        "(Génesis 3), a sua extensão universal (Romanos 3.23; 5.12) e as quatro "
        "dimensões da perdição humana.",
        "<b>CRER</b> — interiorizar a convicção de que nenhuma obra, mérito ou "
        "religiosidade humana pode remover o pecado, e de que a salvação só é "
        "possível pela graça de Deus em Cristo.",
        "<b>VIVER</b> — cultivar humildade e gratidão diante de Deus, abandonando "
        "toda a autossuficiência espiritual e reconhecendo diariamente a "
        "dependência da graça.",
        "<b>SERVIR</b> — apresentar o Evangelho a outros de forma fiel, começando "
        "pela real condição humana, com verdade e com a compaixão de Cristo, sem "
        "dureza nem condenação farisaica.",
    ], ordenada=True)

    # ================= VERSÍCULO-CHAVE =================
    E += h1("Versículo-Chave")
    E.append(cit("Porque todos pecaram e destituídos estão da glória de Deus.",
                 "Romanos 3.23"))

    # ================= TEXTO-BASE =================
    E += h1("Texto-Base para Leitura")
    E.append(Paragraph(
        "Antes de iniciar o estudo, leia atentamente, em sua Bíblia "
        "(Almeida Revista e Corrigida), a seguinte passagem, observando "
        "como Paulo descreve o que éramos sem Cristo e o que Deus fez por nós:",
        S["corpo"]))
    E.append(Paragraph("Efésios 2.1-10", S["texto_base"]))
    E.append(PageBreak())

    # ================= 1. INTRODUÇÃO =================
    E += h1("1. Introdução — Por que Começar pela Má Notícia")
    E.append(Paragraph(
        "Ninguém procura um médico enquanto se julga saudável. Da mesma "
        "forma, ninguém corre para o Salvador enquanto não compreende que "
        "está perdido. Foi o próprio Jesus quem o disse: «Os sãos não "
        "necessitam de médico, mas sim os que estão doentes» (Mateus 9.12). "
        "Por isso, todo o ensino bíblico sobre a salvação começa pelo "
        "diagnóstico: a condição real do ser humano diante de Deus.", S["corpo"]))
    E.append(Paragraph(
        "Este ponto de partida distingue o Evangelho de todas as "
        "religiões e filosofias humanas. Estas partem do princípio de que "
        "o homem pode, por esforço, disciplina ou mérito, elevar-se até "
        "Deus. A Escritura, pelo contrário, revela que o ser humano, "
        "criado à imagem de Deus e para comunhão com Ele, caiu pelo "
        "pecado e tornou-se incapaz de se restaurar a si mesmo. A "
        "iniciativa da salvação, do princípio ao fim, pertence a Deus.", S["corpo"]))
    E.append(cit("Porque o Filho do Homem veio buscar e salvar o que se havia perdido.",
                 "Lucas 19.10"))
    E.append(Paragraph(
        "Note-se: Jesus não veio ajudar quem já se estava a salvar; veio "
        "buscar e salvar o que se havia perdido. Compreender a perdição é, "
        "portanto, o primeiro passo para compreender — e amar — a salvação.",
        S["corpo"]))

    # ================= 2. DESENVOLVIMENTO =================
    E += h1("2. Desenvolvimento do Conceito Central")

    E.append(Paragraph("2.1. Fundamentos bíblicos", S["h2"]))
    E.append(Paragraph(
        "A doutrina do estado de perdição não se apoia num único "
        "versículo, mas atravessa toda a Escritura. Observemos três "
        "passagens-chave:", S["corpo"]))

    E.append(Paragraph("a) A queda — a entrada do pecado no mundo (Génesis 3)", S["h3"]))
    E.append(Paragraph(
        "Deus criou o ser humano — homem e mulher — à Sua imagem e "
        "semelhança, com dignidade, propósito e vocação (Génesis 1.27). "
        "Mas, pela desobediência voluntária dos nossos primeiros pais, o "
        "pecado entrou no mundo. As consequências foram imediatas: "
        "vergonha (Génesis 3.7), medo e fuga da presença de Deus "
        "(Génesis 3.8-10), transferência de culpa (Génesis 3.12-13) e, "
        "por fim, a expulsão do Éden — figura da separação entre o homem "
        "e o seu Criador (Génesis 3.23-24).", S["corpo"]))
    E.append(cit("E chamou o Senhor Deus a Adão e disse-lhe: Onde estás?", "Génesis 3.9"))
    E.append(Paragraph(
        "A primeira pergunta de Deus ao homem caído — «Onde estás?» — não "
        "é a pergunta de quem procura informação, mas de quem procura o "
        "perdido. Já em Génesis 3, a perdição humana é acompanhada pela "
        "busca amorosa de Deus.", S["corpo"]))

    E.append(Paragraph("b) A extensão universal do pecado (Romanos 3 e 5)", S["h3"]))
    E.append(Paragraph(
        "Paulo, na Epístola aos Romanos, demonstra que a perdição não é "
        "problema de alguns, mas condição de todos — judeus e gentios, "
        "religiosos e pagãos:", S["corpo"]))
    E.append(cit(
        "Como está escrito: Não há um justo, nem um sequer. Não há ninguém "
        "que entenda; não há ninguém que busque a Deus.", "Romanos 3.10-11"))
    E.append(cit(
        "Pelo que, como por um homem entrou o pecado no mundo, e pelo "
        "pecado, a morte, assim também a morte passou a todos os homens, "
        "por isso que todos pecaram.", "Romanos 5.12"))
    E.append(Paragraph(
        "Pecamos por natureza (herdámos de Adão uma natureza inclinada ao "
        "mal) e pecamos por prática (escolhas concretas de desobediência). "
        "Por isso ninguém pode apontar o dedo a outrem: «todos pecaram e "
        "destituídos estão da glória de Deus» (Romanos 3.23).", S["corpo"]))

    E.append(Paragraph("c) Mortos em delitos e pecados (Efésios 2.1-3)", S["h3"]))
    E.append(Paragraph(
        "No texto-base desta apostila, Paulo usa a imagem mais forte "
        "possível para descrever a condição humana sem Cristo: morte "
        "espiritual. O homem natural não está apenas doente ou enfraquecido "
        "— está morto para Deus, andando segundo o curso deste mundo, "
        "sujeito às paixões da carne e, por natureza, sob a ira divina.", S["corpo"]))
    E.append(cit("E vos vivificou, estando vós mortos em ofensas e pecados.", "Efésios 2.1"))
    E.append(Paragraph(
        "Um morto não se ressuscita a si mesmo. Esta imagem elimina, pela "
        "raiz, toda a esperança de autossalvação — e prepara o coração "
        "para a gloriosa expressão que se segue no versículo 4: «Mas Deus…».",
        S["corpo"]))

    E.append(Paragraph("2.2. O que significa estar «perdido»", S["h2"]))
    E.append(Paragraph(
        "Na linguagem bíblica, «perdido» não é um insulto, mas um "
        "diagnóstico. Descreve quem está fora do lugar para o qual foi "
        "criado: longe de Deus, sem paz verdadeira, sem direcção última e "
        "sem vida eterna. O pecado não é apenas a transgressão de regras; "
        "é a ruptura de uma relação — a relação para a qual fomos criados.",
        S["corpo"]))
    E += quadro_destaque(
        "Definição",
        "Estado de perdição é a condição de todo o ser humano fora de "
        "Cristo: separado de Deus pelo pecado (Isaías 59.2), espiritualmente "
        "morto (Efésios 2.1), escravo do pecado (João 8.34), incapaz de se "
        "salvar por obras (Efésios 2.8-9) e sujeito ao juízo de Deus "
        "(Hebreus 9.27). Responde à pergunta: «de que precisa exactamente "
        "o ser humano de ser salvo?»")
    E.append(PageBreak())

    E.append(Paragraph("2.3. As quatro dimensões da perdição humana", S["h2"]))
    E.append(Paragraph(
        "Para estudar com clareza, é útil distinguir quatro dimensões da "
        "perdição, todas ensinadas nas Escrituras:", S["corpo"]))
    E.append(tabela(
        ["Dimensão", "O que a Escritura afirma", "Referência-chave"],
        [
            ["<b>1. Separação</b>",
             "O pecado separa o homem de Deus; a comunhão foi quebrada.",
             "Isaías 59.2; Génesis 3.23-24"],
            ["<b>2. Morte espiritual</b>",
             "Sem Cristo, o homem está morto em ofensas e pecados.",
             "Efésios 2.1; Colossenses 2.13"],
            ["<b>3. Escravidão</b>",
             "Quem comete pecado é servo do pecado; não há libertação própria.",
             "João 8.34; Romanos 6.16-17"],
            ["<b>4. Condenação</b>",
             "O salário do pecado é a morte; aos homens está ordenado morrerem "
             "uma vez, vindo depois o juízo.",
             "Romanos 6.23; Hebreus 9.27; João 3.18"],
        ],
        [3.6*cm, 6.9*cm, 5.0*cm]))
    E.append(Spacer(1, 8))
    E.append(Paragraph(
        "Estas quatro dimensões mostram que a perdição atinge o ser humano "
        "por inteiro: a sua relação com Deus (separação), a sua vida "
        "interior (morte espiritual), a sua vontade (escravidão) e o seu "
        "destino eterno (condenação). Por isso a salvação que Deus oferece "
        "em Cristo é igualmente completa: reconciliação, regeneração, "
        "libertação e justificação.", S["corpo"]))

    E.append(Paragraph("2.4. Dúvidas e equívocos comuns", S["h2"]))

    E.append(Paragraph("Equívoco 1 — “Mas eu sou uma boa pessoa.”", S["h3"]))
    E.append(Paragraph(
        "A bondade relativa — ser melhor do que o vizinho — não é o padrão "
        "de Deus. O padrão é a Sua própria glória e santidade, da qual "
        "todos estamos destituídos (Romanos 3.23). As nossas melhores "
        "obras, diante da santidade divina, são como trapo da imundícia "
        "(Isaías 64.6). O problema não é a ausência de boas acções, mas a "
        "presença do pecado, que nenhuma boa acção apaga.", S["corpo"]))

    E.append(Paragraph("Equívoco 2 — “A religião resolve.”", S["h3"]))
    E.append(Paragraph(
        "Práticas religiosas — cultos, ofertas, tradições — não removem o "
        "pecado. Nicodemos era mestre religioso em Israel e ouviu de Jesus: "
        "«necessário vos é nascer de novo» (João 3.7). Paulo era irrepreensível "
        "na justiça da lei, e considerou tudo perda por amor de Cristo "
        "(Filipenses 3.6-8). A religiosidade sem regeneração é apenas a "
        "perdição bem vestida.", S["corpo"]))

    E.append(Paragraph("Equívoco 3 — “Falar de pecado é falta de amor.”", S["h3"]))
    E.append(Paragraph(
        "É exactamente o contrário. Ocultar o diagnóstico de um doente "
        "grave não é amor — é crueldade. O médico fiel diz a verdade para "
        "poder aplicar a cura. Jesus, que é amor encarnado, foi quem mais "
        "claramente falou da perdição humana — e chorou sobre Jerusalém "
        "(Lucas 19.41). A verdade sobre o pecado, dita com compaixão, é a "
        "porta da graça.", S["corpo"]))

    E.append(Paragraph("Equívoco 4 — “Se estou perdido, não há esperança.”", S["h3"]))
    E.append(Paragraph(
        "A doutrina da perdição nunca aparece sozinha na Escritura. Em "
        "Génesis 3, Deus já promete o descendente que feriria a serpente "
        "(Génesis 3.15). Em Efésios 2, os «mortos em ofensas» são vivificados "
        "com Cristo. O diagnóstico existe por causa do remédio: «Mas Deus, "
        "que é riquíssimo em misericórdia…» (Efésios 2.4). A má notícia é "
        "real, mas a última palavra é da graça.", S["corpo"]))

    E.append(Paragraph("2.5. Quadro de Destaque — para reter", S["h2"]))
    E += quadro_destaque(
        "Para reter",
        "Fora de Cristo, todo o ser humano está separado de Deus, morto "
        "espiritualmente, escravo do pecado e sujeito ao juízo — e nenhuma "
        "obra humana pode mudar essa condição. Por isso a salvação é, do "
        "princípio ao fim, obra da graça de Deus, recebida pela fé em "
        "Jesus Cristo (Efésios 2.8-9).")
    E.append(PageBreak())

    # ================= 3. APLICAÇÃO =================
    E += h1("3. Aplicação Prática")
    E.append(Paragraph(
        "A doutrina do estado de perdição não é apenas para ser sabida — é "
        "para transformar o coração, a oração e o testemunho do discípulo "
        "Epignósis. Vejamos cinco esferas de aplicação:", S["corpo"]))
    E += lista([
        "<b>Na vida pessoal e devocional</b> — recorde diariamente de onde Deus o "
        "tirou (Efésios 2.11-13). A memória da perdição alimenta a gratidão, "
        "quebra o orgulho espiritual e renova o primeiro amor.",
        "<b>Na família</b> — ore pelos familiares que ainda não conhecem a Cristo "
        "com a consciência de que estão perdidos e de que Deus os busca; "
        "interceda com perseverança e testemunhe com mansidão.",
        "<b>Na igreja local</b> — trate os novos convertidos e os visitantes sem "
        "superioridade: a única diferença entre o salvo e o perdido é a "
        "graça recebida, não o mérito alcançado.",
        "<b>No trabalho e na sociedade</b> — veja colegas e vizinhos como Jesus "
        "via as multidões: «como ovelhas que não têm pastor» (Mateus 9.36). "
        "A compaixão, e não o juízo, deve marcar o olhar do discípulo.",
        "<b>No exercício ministerial</b> — ao evangelizar e ensinar, apresente o "
        "diagnóstico bíblico completo antes de oferecer o remédio. Um "
        "evangelho sem consciência de pecado produz decisões sem conversão.",
    ], ordenada=True)

    # ================= 4. SÍNTESE =================
    E += h1("4. Síntese e Conclusão")
    E.append(Paragraph(
        "Estudámos, nesta apostila, que o ser humano foi criado à imagem "
        "de Deus, para comunhão com Ele, mas que, pela desobediência "
        "voluntária dos nossos primeiros pais, o pecado entrou no mundo e "
        "alcançou toda a humanidade. Vimos que a perdição tem quatro "
        "dimensões — separação, morte espiritual, escravidão e condenação — "
        "e que nenhuma obra, mérito ou religiosidade humana pode remover o "
        "pecado.", S["corpo"]))
    E.append(Paragraph(
        "Este diagnóstico, longe de nos lançar no desespero, prepara-nos "
        "para receber e anunciar a maior de todas as notícias: Deus, que é "
        "riquíssimo em misericórdia, tomou a iniciativa de nos buscar em "
        "Cristo. É esse o tema da próxima apostila — A Graça de Deus em "
        "Cristo.", S["corpo"]))
    E.append(cit(
        "Mas Deus, que é riquíssimo em misericórdia, pelo seu muito amor "
        "com que nos amou, estando nós ainda mortos em nossas ofensas, nos "
        "vivificou juntamente com Cristo (pela graça sois salvos).",
        "Efésios 2.4-5"))
    E.append(PageBreak())

    # ================= EXERCÍCIOS =================
    E += h1("Exercícios de Revisão")
    E.append(Paragraph(
        "Responda às questões a seguir com base no conteúdo desta apostila "
        "e na sua leitura bíblica.", S["corpo"]))

    E.append(Paragraph("I — Verifique a sua compreensão", S["h3"]))
    E += lista([
        "Explique, com as suas próprias palavras, o que a Bíblia quer dizer "
        "quando afirma que o ser humano está “perdido”.",
        "Quais são as quatro dimensões da perdição humana? Indique uma "
        "referência bíblica para cada uma.",
        "Que consequências imediatas da queda observamos em Génesis 3.7-13?",
        "O que significa a expressão “mortos em ofensas e pecados” (Efésios 2.1)? "
        "Por que essa imagem exclui a autossalvação?",
        "Explique a diferença entre pecar “por natureza” e pecar “por prática”.",
    ], ordenada=True)

    E.append(Paragraph("II — Reflexão pessoal", S["h3"]))
    E += lista([
        "Antes de conhecer a Cristo, em que “dimensão da perdição” você mais "
        "sentia o peso do pecado? Como a graça de Deus o(a) alcançou?",
        "Há alguma área da sua vida em que ainda confia mais no próprio esforço "
        "do que na graça de Deus? Qual?",
        "Escreva uma breve oração de gratidão a Deus por o(a) ter buscado "
        "quando estava perdido(a).",
    ], ordenada=True)

    E.append(Paragraph("III — Ministério e serviço", S["h3"]))
    E += lista([
        "Como você explicaria, em 3 minutos e com amor, a um amigo não crente, "
        "que “ser boa pessoa” não resolve o problema do pecado?",
        "Faça uma lista de três pessoas do seu convívio que ainda não conhecem "
        "a Cristo e comprometa-se a orar por elas durante este módulo.",
    ], ordenada=True)

    # ================= ESTUDO BÍBLICO =================
    E += h1("Estudo Bíblico Complementar — Lucas 15: o Perdido aos Olhos de Deus")
    E.append(Paragraph(
        "Em Lucas 15, respondendo à murmuração dos fariseus — «Este recebe "
        "pecadores e come com eles» —, Jesus conta três parábolas sobre o "
        "que se perdeu: a ovelha, a dracma e o filho. Nelas aprendemos como "
        "Deus vê o perdido — e como o céu reage quando ele é encontrado. "
        "Leia atentamente Lucas 15.1-32 e responda:", S["corpo"]))
    E += lista([
        "Nas três parábolas, quem toma a iniciativa de buscar (ou receber) o "
        "que estava perdido? O que isso revela sobre o coração de Deus?",
        "O filho pródigo «caiu em si» (v. 17). Que passos concretos se seguiram "
        "a esse despertar? (vv. 18-20)",
        "Compare a atitude do pai (vv. 20-24) com a do filho mais velho "
        "(vv. 25-30). Qual das duas atitudes se parece mais com a nossa diante "
        "dos perdidos?",
        "Que frase se repete no final das três parábolas sobre a alegria? "
        "(vv. 7, 10, 32) O que ela ensina sobre o valor de cada pecador que se "
        "arrepende?",
        "À luz de Lucas 15, como deve a igreja tratar quem chega “perdido” aos "
        "nossos cultos e células?",
    ], ordenada=True)

    # ================= PRÓXIMA APOSTILA =================
    E += h1("Para a Próxima Apostila")
    E.append(Paragraph(
        "Na próxima apostila — Apostila 2 — estudaremos A Graça de Deus "
        "em Cristo: a resposta divina ao estado de perdição humana. Para "
        "se preparar, leia previamente Efésios 2.4-10 e Tito 2.11-14, e "
        "reflicta sobre as seguintes perguntas:", S["corpo"]))
    E += lista([
        "Em Efésios 2.4-5, que palavras descrevem o carácter de Deus que "
        "motivou a nossa salvação?",
        "Segundo Tito 2.11-12, o que a graça de Deus faz, além de salvar?",
    ])
    E.append(PageBreak())

    # ================= GLOSSÁRIO =================
    E += h1("Glossário")
    E.append(Paragraph("Definições breves dos termos-chave utilizados nesta apostila.", S["corpo"]))
    E.append(tabela(
        ["Termo", "Definição"],
        [
            ["<b><font color='#1B3A5C'>Pecado (hamartia, ἁμαρτία)</font></b>",
             "Literalmente, “errar o alvo”. Toda a desconformidade com o carácter "
             "e a vontade de Deus, em pensamento, palavra, acção ou omissão."],
            ["<b><font color='#1B3A5C'>Queda</font></b>",
             "O acto de desobediência voluntária de Adão e Eva (Génesis 3), pelo "
             "qual o pecado e a morte entraram no mundo e alcançaram toda a "
             "humanidade."],
            ["<b><font color='#1B3A5C'>Perdição</font></b>",
             "Condição do ser humano fora de Cristo: separado de Deus, "
             "espiritualmente morto, escravo do pecado e sujeito ao juízo divino."],
            ["<b><font color='#1B3A5C'>Morte espiritual</font></b>",
             "Estado de incapacidade e insensibilidade para com Deus (Efésios 2.1), "
             "distinto da morte física; só é revertido pela regeneração."],
            ["<b><font color='#1B3A5C'>Imagem de Deus (imago Dei)</font></b>",
             "Dignidade e vocação originais do ser humano, criado para reflectir o "
             "carácter de Deus e viver em comunhão com Ele (Génesis 1.27)."],
            ["<b><font color='#1B3A5C'>Graça</font></b>",
             "Favor imerecido de Deus para com o pecador; fonte exclusiva da "
             "salvação (Efésios 2.8-9). Tema da próxima apostila."],
            ["<b><font color='#1B3A5C'>Epígnosis (ἐπίγνωσις)</font></b>",
             "Conhecimento pleno, profundo e experimental de Deus — meta de todo o "
             "ensino da Escola Bíblica Epignósis."],
        ],
        [5.4*cm, 10.1*cm]))

    # ================= BIBLIOGRAFIA =================
    E += h1("Bibliografia Recomendada")
    E += lista([
        "Bíblia Sagrada. Tradução de João Ferreira de Almeida, Revista e Corrigida.",
        "Declaração de Fé Institucional da Escola Bíblica Epignósis "
        "(EBE-DOC-002), Art. 6.º e 7.º.",
        "STOTT, John. A cruz de Cristo. São Paulo: Vida.",
        "PACKER, J. I. O conhecimento de Deus. São Paulo: Cultura Cristã.",
        "GRUDEM, Wayne. Teologia sistemática (capítulos sobre o pecado e a "
        "condição humana). São Paulo: Vida Nova.",
        "RYLE, J. C. Santidade (capítulo «Pecado»). São José dos Campos: Fiel.",
    ])

    # ================= ANOTAÇÕES =================
    E += h1("Anotações Pessoais")
    for _ in range(12):
        E.append(Spacer(1, 16))
        E.append(HRFlowable(width="100%", thickness=0.5, color=CINZA_LINHA))

    # ================= SELO FINAL =================
    E.append(Spacer(1, 24))
    E.append(linha(VERDE, 0.8, 2, 10))
    E.append(Paragraph("ESCOLA BÍBLICA EPIGNÓSIS", S["selo1"]))
    E.append(Paragraph("Conhecer a Deus. Viver a Palavra. Manifestar o Reino.", S["selo2"]))
    E.append(Paragraph("Soli Deo Gloria", S["selo3"]))

    # primeira página usa template Capa; as demais, Normal
    from reportlab.platypus import NextPageTemplate
    E.insert(0, NextPageTemplate("Normal"))
    doc.build(E)
    print("OK:", out)


if __name__ == "__main__":
    gerar()
