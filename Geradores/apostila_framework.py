# -*- coding: utf-8 -*-
"""
FRAMEWORK DE PRODUÇÃO DE APOSTILAS — Escola Bíblica Epignósis (EBE)

Gera, a partir de um dicionário de conteúdo (um ficheiro por apostila em
Geradores/conteudos/), as versões .docx e .pdf de cada apostila, gravando-as
na árvore oficial:

    Apostilas/Instituto_XX_Nome/Escola_XX_Nome/Curso_XX_Nome/Modulo_X_Nome/

O formato editorial é fixo (padrão da Apostila Piloto EBE-APO-001);
o conteúdo de cada apostila é 100% próprio e fiel ao seu tema.

Extensão alvo: 15–20 páginas por apostila.

Marcações aceites no texto dos blocos:
    **negrito**  →  negrito no DOCX e no PDF

Tipos de bloco aceites em "blocos":
    ("p", texto)
    ("h3", texto)
    ("cit", texto, referência)
    ("destaque", rótulo, texto)
    ("tabela", [cabeçalhos], [[linhas]], [larguras_cm])
    ("lista", [itens], ordenada: bool)
    ("pb",)                      → quebra de página
"""
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))       # .../Geradores
RAIZ = os.path.dirname(BASE)                             # raiz do repositório
sys.path.insert(0, BASE)

from _estilos import *                                    # noqa: F401,F403
from _estilos import _shade_cell, _add_horizontal_line    # noqa: F401

# ============================================================
# UTILIDADES COMUNS
# ============================================================

_BOLD_RE = re.compile(r"\*\*(.+?)\*\*")


def _segmentos(texto):
    """Divide o texto em segmentos (texto, é_negrito)."""
    out, pos = [], 0
    for m in _BOLD_RE.finditer(texto):
        if m.start() > pos:
            out.append((texto[pos:m.start()], False))
        out.append((m.group(1), True))
        pos = m.end()
    if pos < len(texto):
        out.append((texto[pos:], False))
    return out


def _pdf_markup(texto):
    """Converte **x** em <b>x</b> e escapa & < >."""
    texto = texto.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return _BOLD_RE.sub(r"<b>\1</b>", texto)


def pasta_destino(meta):
    d = os.path.join(RAIZ, "Apostilas", meta["pasta"])
    os.makedirs(d, exist_ok=True)
    return d


def nome_ficheiro(meta):
    return f"EBE-APO-{meta['numero_global']}_{meta['slug']}"


# ============================================================
# GERADOR DOCX
# ============================================================

def _p_docx(doc, texto, size=12, italic=False):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    for seg, bold in _segmentos(texto):
        r = p.add_run(seg)
        r.font.name = FONTE_CORPO
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.italic = italic
    return p


def _lista_docx(doc, itens, ordenada=False):
    for i, item in enumerate(itens, 1):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.left_indent = Cm(0.8)
        p.paragraph_format.first_line_indent = Cm(-0.5)
        p.paragraph_format.space_after = Pt(2)
        marca = f"{i}. " if ordenada else "•  "
        r = p.add_run(marca)
        r.font.name = FONTE_TITULO; r.font.size = Pt(12)
        r.font.bold = True; r.font.color.rgb = COR_SECUNDARIA
        for seg, bold in _segmentos(item):
            r2 = p.add_run(seg)
            r2.font.name = FONTE_CORPO; r2.font.size = Pt(12)
            r2.font.bold = bold


def _destaque_docx(doc, rotulo, texto):
    tbl = doc.add_table(rows=1, cols=1)
    cell = tbl.rows[0].cells[0]
    _shade_cell(cell, "E8F1EC")
    p = cell.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(f"✦ {rotulo}:  ")
    r.font.bold = True; r.font.color.rgb = COR_SECUNDARIA
    r.font.name = FONTE_TITULO; r.font.size = Pt(11)
    for seg, bold in _segmentos(texto):
        r2 = p.add_run(seg)
        r2.font.name = FONTE_CORPO; r2.font.size = Pt(11)
        r2.font.italic = True; r2.font.bold = bold


def _tabela_docx(doc, headers, rows):
    tbl = doc.add_table(rows=1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = tbl.rows[0].cells
    for i, t in enumerate(headers):
        hdr[i].text = ""
        _shade_cell(hdr[i], HEX_PRIMARIA)
        p = hdr[i].paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(t)
        r.font.bold = True; r.font.name = FONTE_TITULO; r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    for linha_ in rows:
        row = tbl.add_row().cells
        for i, v in enumerate(linha_):
            row[i].text = ""
            p = row[i].paragraphs[0]
            for seg, bold in _segmentos(v):
                r = p.add_run(seg)
                r.font.name = FONTE_CORPO; r.font.size = Pt(10)
                r.font.bold = bold
    doc.add_paragraph()


def _blocos_docx(doc, blocos):
    for b in blocos:
        t = b[0]
        if t == "p":
            _p_docx(doc, b[1])
        elif t == "h3":
            h3(doc, b[1])
        elif t == "cit":
            citacao(doc, b[1], b[2])
        elif t == "destaque":
            _destaque_docx(doc, b[1], b[2])
        elif t == "tabela":
            _tabela_docx(doc, b[1], b[2])
        elif t == "lista":
            _lista_docx(doc, b[1], b[2] if len(b) > 2 else False)
        elif t == "pb":
            page_break(doc)


def gerar_docx(A):
    meta = A["meta"]
    codigo = f"EBE-APO-{meta['numero_global']}"
    doc = novo_documento(f"Apostila — {meta['titulo']}", codigo)

    # ====== CAPA ======
    doc.add_paragraph()
    inserir_logo(doc, LOGO_PATH, largura_cm=5.5)

    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Conhecer a Deus. Viver a Palavra. Manifestar o Reino.")
    r.font.name = FONTE_TITULO; r.font.size = Pt(10)
    r.font.italic = True; r.font.color.rgb = COR_SECUNDARIA

    p = doc.add_paragraph(); _add_horizontal_line(p, color=HEX_SECUNDARIA, size=6)

    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    r = p.add_run(meta["instituto"].upper())
    r.font.name = FONTE_TITULO; r.font.size = Pt(11); r.font.bold = True
    r.font.color.rgb = COR_SECUNDARIA

    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(f"{meta['escola']}  ·  Curso «{meta['curso']}»  ·  Módulo {meta['modulo_num']} — {meta['modulo_nome']}")
    r.font.name = FONTE_CORPO; r.font.size = Pt(10); r.font.color.rgb = COR_CITACAO

    doc.add_paragraph()
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(f"APOSTILA N.º  {meta['numero_no_curso']:02d}")
    r.font.name = FONTE_TITULO; r.font.size = Pt(13); r.font.bold = True
    r.font.color.rgb = COR_SECUNDARIA

    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(meta["titulo"])
    r.font.name = FONTE_TITULO; r.font.size = Pt(28); r.font.bold = True
    r.font.color.rgb = COR_PRIMARIA

    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(meta["subtitulo"])
    r.font.name = FONTE_TITULO; r.font.size = Pt(13)
    r.font.italic = True; r.font.color.rgb = COR_TEXTO

    doc.add_paragraph(); doc.add_paragraph()

    tbl = doc.add_table(rows=4, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    dados = [
        ("Autor / Docente", "Direcção Pedagógica · Escola Bíblica Epignósis"),
        ("Carga horária estimada", meta.get("carga", "2–3 horas de estudo")),
        ("Nível formativo", meta["nivel"]),
        ("Edição / Ano", "1.ª edição — 2026"),
    ]
    for i, (k, v) in enumerate(dados):
        row = tbl.rows[i].cells
        row[0].text = k; row[1].text = v
        _shade_cell(row[0], "E8F1EC")
        for pp in row[0].paragraphs:
            for rr in pp.runs:
                rr.font.bold = True; rr.font.name = FONTE_TITULO; rr.font.size = Pt(10)
                rr.font.color.rgb = COR_PRIMARIA
        for pp in row[1].paragraphs:
            for rr in pp.runs:
                rr.font.name = FONTE_CORPO; rr.font.size = Pt(10)

    doc.add_paragraph()
    p = doc.add_paragraph(); _add_horizontal_line(p, color=HEX_SECUNDARIA, size=4)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(f"Material didáctico oficial · Código {codigo} · 2026")
    r.font.name = FONTE_CORPO; r.font.size = Pt(9); r.font.color.rgb = COR_CITACAO

    page_break(doc)

    # ====== MARCO FILOSÓFICO ======
    add_marco_filosofico(doc)

    # ====== FICHA TÉCNICA ======
    h1(doc, "Ficha Técnica")
    paragrafo(doc,
        "Este material didáctico é propriedade intelectual da Escola Bíblica "
        "Epignósis (EBE), produzido para uso exclusivo no âmbito dos seus "
        "programas de formação. A sua reprodução, no todo ou em parte, "
        "depende de autorização institucional escrita.")
    itens_ficha = [
        f"Título da apostila: {meta['titulo']}.",
        f"Curso: {meta['curso']} ({meta['curso_carga']}).",
        f"Módulo: {meta['modulo_num']} — {meta['modulo_nome']} (Apostila {meta['apostila_no_modulo']} de {meta['apostilas_no_modulo']}).",
        f"Escola: {meta['escola']} · {meta['instituto']}.",
        f"Nível formativo: {meta['nivel']}.",
        "Autor / Docente: Direcção Pedagógica da Escola Bíblica Epignósis.",
        "Revisão pedagógica: Coordenação Acadêmica.",
        f"Revisão doutrinária: Conselho Doutrinário ({meta['base_doutrinaria']}).",
        "Versão bíblica de referência: Almeida Revista e Corrigida (ARC).",
        "Edição: 1.ª — 2026.",
        f"Código institucional: {codigo}.",
    ]
    lista(doc, itens_ficha)
    citacao(doc, A["citacao_ficha"][0], A["citacao_ficha"][1])
    page_break(doc)

    # ====== SUMÁRIO ======
    h1(doc, "Sumário")
    lista(doc, _sumario(A))
    page_break(doc)

    # ====== APRESENTAÇÃO ======
    h1(doc, "Apresentação da Apostila")
    for t in A["apresentacao"]:
        _p_docx(doc, t)

    # ====== OBJECTIVOS ======
    h1(doc, "Objectivos de Aprendizagem")
    paragrafo(doc, "Ao concluir o estudo desta apostila, o(a) aluno(a) será capaz de:")
    _lista_docx(doc, A["objectivos"], ordenada=True)

    # ====== VERSÍCULO-CHAVE ======
    h1(doc, "Versículo-Chave")
    citacao(doc, A["versiculo_chave"][0], A["versiculo_chave"][1])

    # ====== TEXTO-BASE ======
    h1(doc, "Texto-Base para Leitura")
    _p_docx(doc, A["texto_base"]["intro"])
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(A["texto_base"]["passagem"])
    r.font.name = FONTE_TITULO; r.font.size = Pt(14); r.font.bold = True
    r.font.color.rgb = COR_SECUNDARIA
    page_break(doc)

    # ====== 1. INTRODUÇÃO ======
    h1(doc, f"Introdução — {A['introducao']['titulo']}", numero=1)
    _blocos_docx(doc, A["introducao"]["blocos"])

    # ====== 2. DESENVOLVIMENTO ======
    h1(doc, "Desenvolvimento do Conceito Central", numero=2)
    for i, sec in enumerate(A["desenvolvimento"], 1):
        h2(doc, sec["titulo"], numero=f"2.{i}")
        _blocos_docx(doc, sec["blocos"])

    page_break(doc)

    # ====== 3. APLICAÇÃO ======
    h1(doc, "Aplicação Prática", numero=3)
    _p_docx(doc, A["aplicacao"]["intro"])
    _lista_docx(doc, A["aplicacao"]["itens"], ordenada=True)

    # ====== 4. SÍNTESE ======
    h1(doc, "Síntese e Conclusão", numero=4)
    for t in A["sintese"]["paragrafos"]:
        _p_docx(doc, t)
    citacao(doc, A["sintese"]["citacao"][0], A["sintese"]["citacao"][1])
    page_break(doc)

    # ====== EXERCÍCIOS ======
    h1(doc, "Exercícios de Revisão")
    paragrafo(doc,
        "Responda às questões a seguir com base no conteúdo desta apostila "
        "e na sua leitura bíblica.")
    h3(doc, "I — Verifique a sua compreensão")
    _lista_docx(doc, A["exercicios"]["compreensao"], ordenada=True)
    h3(doc, "II — Reflexão pessoal")
    _lista_docx(doc, A["exercicios"]["reflexao"], ordenada=True)
    h3(doc, "III — Ministério e serviço")
    _lista_docx(doc, A["exercicios"]["ministerio"], ordenada=True)

    # ====== ESTUDO BÍBLICO ======
    h1(doc, f"Estudo Bíblico Complementar — {A['estudo']['titulo']}")
    _p_docx(doc, A["estudo"]["intro"])
    _lista_docx(doc, A["estudo"]["perguntas"], ordenada=True)

    # ====== PRÓXIMA APOSTILA ======
    h1(doc, "Para a Próxima Apostila")
    _p_docx(doc, A["proxima"]["texto"])
    _lista_docx(doc, A["proxima"]["itens"])
    page_break(doc)

    # ====== GLOSSÁRIO ======
    h1(doc, "Glossário")
    paragrafo(doc, "Definições breves dos termos-chave utilizados nesta apostila.")
    tbl = doc.add_table(rows=1, cols=2)
    hdr = tbl.rows[0].cells
    for i, t in enumerate(["Termo", "Definição"]):
        hdr[i].text = ""
        _shade_cell(hdr[i], HEX_PRIMARIA)
        p = hdr[i].paragraphs[0]
        r = p.add_run(t)
        r.font.bold = True; r.font.name = FONTE_TITULO; r.font.size = Pt(11)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    for termo, defin in A["glossario"]:
        row = tbl.add_row().cells
        row[0].text = termo; row[1].text = defin
        for c in row:
            for pp in c.paragraphs:
                for rr in pp.runs:
                    rr.font.name = FONTE_CORPO; rr.font.size = Pt(10)
        for pp in row[0].paragraphs:
            for rr in pp.runs:
                rr.font.bold = True; rr.font.color.rgb = COR_PRIMARIA

    # ====== BIBLIOGRAFIA ======
    h1(doc, "Bibliografia Recomendada")
    lista(doc, A["bibliografia"])

    # ====== ANOTAÇÕES ======
    h1(doc, "Anotações Pessoais")
    for _ in range(12):
        p = doc.add_paragraph(); _add_horizontal_line(p, color="C8C8C8", size=4)

    selo_final(doc)

    out = os.path.join(pasta_destino(meta), nome_ficheiro(meta) + ".docx")
    doc.save(out)
    return out


def _sumario(A):
    itens = [
        "Apresentação da apostila",
        "Objectivos de aprendizagem",
        "Versículo-chave",
        "Texto-base para leitura",
        f"1. Introdução — {A['introducao']['titulo']}",
        "2. Desenvolvimento do conceito central",
    ]
    for i, sec in enumerate(A["desenvolvimento"], 1):
        itens.append(f"   2.{i} {sec['titulo']}")
    itens += [
        "3. Aplicação prática",
        "4. Síntese e conclusão",
        "Exercícios de revisão",
        f"Estudo bíblico complementar — {A['estudo']['titulo']}",
        "Para a próxima apostila",
        "Glossário",
        "Bibliografia recomendada",
        "Anotações pessoais",
    ]
    return itens


# ============================================================
# GERADOR PDF (ReportLab)
# ============================================================

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
    TableStyle, Image, PageBreak, HRFlowable, NextPageTemplate,
)

FONTS = os.path.join(BASE, "_assets", "fonts")
AZUL = HexColor("#1B3A5C"); VERDE = HexColor("#2E7D4F")
TEXTO_C = HexColor("#1A1A1A"); CINZA = HexColor("#555555")
VERDE_CLARO = HexColor("#E8F1EC"); CINZA_LINHA = HexColor("#C8C8C8")

_FONTES_OK = False


def _registar_fontes():
    global _FONTES_OK
    if _FONTES_OK:
        return
    pdfmetrics.registerFont(TTFont("Serif", os.path.join(FONTS, "DejaVuSerif.ttf")))
    pdfmetrics.registerFont(TTFont("Serif-Bold", os.path.join(FONTS, "DejaVuSerif-Bold.ttf")))
    pdfmetrics.registerFont(TTFont("Serif-Italic", os.path.join(FONTS, "DejaVuSerif-Italic.ttf")))
    pdfmetrics.registerFont(TTFont("Serif-BoldItalic", os.path.join(FONTS, "DejaVuSerif-BoldItalic.ttf")))
    pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-Bold",
                                  italic="Serif-Italic", boldItalic="Serif-BoldItalic")
    _FONTES_OK = True


def _st(name, **kw):
    base = dict(fontName="Serif", fontSize=10.5, leading=15.5,
                textColor=TEXTO_C, alignment=TA_JUSTIFY, spaceAfter=6)
    base.update(kw)
    return ParagraphStyle(name, **base)


def _estilos_pdf():
    return {
        "corpo":      _st("corpo"),
        "lema":       _st("lema", fontName="Serif-Italic", fontSize=9.5, textColor=VERDE, alignment=TA_CENTER),
        "capa_inst":  _st("capa_inst", fontName="Serif-Bold", fontSize=11, textColor=VERDE, alignment=TA_CENTER, spaceBefore=6),
        "capa_curso": _st("capa_curso", fontSize=9, textColor=CINZA, alignment=TA_CENTER),
        "capa_num":   _st("capa_num", fontName="Serif-Bold", fontSize=12, textColor=VERDE, alignment=TA_CENTER, spaceBefore=14),
        "capa_tit":   _st("capa_tit", fontName="Serif-Bold", fontSize=24, leading=30, textColor=AZUL, alignment=TA_CENTER, spaceBefore=8),
        "capa_sub":   _st("capa_sub", fontName="Serif-Italic", fontSize=12, leading=16, alignment=TA_CENTER, spaceBefore=6),
        "capa_cod":   _st("capa_cod", fontSize=8.5, textColor=CINZA, alignment=TA_CENTER),
        "h1":         _st("h1", fontName="Serif-Bold", fontSize=13.5, leading=17, textColor=AZUL, alignment=TA_LEFT, spaceBefore=16, spaceAfter=2, keepWithNext=1),
        "h2":         _st("h2", fontName="Serif-Bold", fontSize=12, leading=15, textColor=AZUL, alignment=TA_LEFT, spaceBefore=11, spaceAfter=4, keepWithNext=1),
        "h3":         _st("h3", fontName="Serif-Bold", fontSize=10.5, leading=14, textColor=VERDE, alignment=TA_LEFT, spaceBefore=8, spaceAfter=2, keepWithNext=1),
        "citacao":    _st("citacao", fontName="Serif-Italic", fontSize=9.5, leading=14, textColor=CINZA, leftIndent=1.5*cm, rightIndent=1.0*cm, spaceBefore=5, spaceAfter=5),
        "lista":      _st("lista", leftIndent=0.8*cm, firstLineIndent=-0.5*cm, spaceAfter=3),
        "marco_tit":  _st("marco_tit", fontName="Serif-Bold", fontSize=12, textColor=VERDE, alignment=TA_CENTER),
        "marco_txt":  _st("marco_txt", fontName="Serif-Italic", fontSize=13, leading=19, textColor=AZUL, alignment=TA_CENTER, leftIndent=1.5*cm, rightIndent=1.5*cm),
        "marco_ass":  _st("marco_ass", fontSize=9.5, textColor=CINZA, alignment=TA_CENTER),
        "marco_ef":   _st("marco_ef", fontName="Serif-Italic", fontSize=9.5, leading=13.5, textColor=CINZA, alignment=TA_CENTER, leftIndent=1.5*cm, rightIndent=1.5*cm),
        "selo1":      _st("selo1", fontName="Serif-Bold", fontSize=11, textColor=AZUL, alignment=TA_CENTER),
        "selo2":      _st("selo2", fontName="Serif-Italic", fontSize=10, textColor=VERDE, alignment=TA_CENTER),
        "selo3":      _st("selo3", fontName="Serif-Italic", fontSize=9, textColor=CINZA, alignment=TA_CENTER),
        "tbl":        _st("tbl", fontSize=9, leading=12.5, spaceAfter=0),
        "tbl_hdr":    _st("tbl_hdr", fontName="Serif-Bold", fontSize=9, leading=12, textColor=white, alignment=TA_CENTER, spaceAfter=0),
        "destaque":   _st("destaque", fontSize=9.5, leading=14, spaceAfter=0),
        "texto_base": _st("texto_base", fontName="Serif-Bold", fontSize=13, textColor=VERDE, alignment=TA_CENTER, spaceBefore=6),
    }


def _linha(color=VERDE, width=0.8, sb=2, sa=6):
    return HRFlowable(width="100%", thickness=width, color=color,
                      spaceBefore=sb, spaceAfter=sa)


def _h1_pdf(S, texto):
    return [Paragraph(_pdf_markup(texto).upper(), S["h1"]), _linha(AZUL, 0.9, 1, 8)]


def _cit_pdf(S, texto, ref=None):
    extra = f'  <font size="8.5" color="#2E7D4F">({ref}, ARC)</font>' if ref else ""
    return Paragraph(f"“{_pdf_markup(texto)}”{extra}", S["citacao"])


def _lista_pdf(S, itens, ordenada=False):
    out = []
    for i, item in enumerate(itens, 1):
        marca = f"{i}." if ordenada else "•"
        out.append(Paragraph(
            f'<font color="#2E7D4F"><b>{marca}</b></font>&nbsp;&nbsp;{_pdf_markup(item)}',
            S["lista"]))
    return out


def _destaque_pdf(S, rotulo, texto):
    p = Paragraph(
        f'<font color="#2E7D4F"><b>◆ {rotulo}:</b></font>&nbsp; <i>{_pdf_markup(texto)}</i>',
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


def _tabela_pdf(S, headers, rows, widths_cm=None):
    if widths_cm is None:
        w = 15.5 / len(headers)
        widths_cm = [w] * len(headers)
    data = [[Paragraph(_pdf_markup(h), S["tbl_hdr"]) for h in headers]]
    for r in rows:
        data.append([Paragraph(_pdf_markup(c), S["tbl"]) for c in r])
    t = Table(data, colWidths=[w*cm for w in widths_cm], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), AZUL),
        ("GRID", (0, 0), (-1, -1), 0.5, CINZA_LINHA),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return [t, Spacer(1, 8)]


def _blocos_pdf(S, blocos):
    out = []
    for b in blocos:
        t = b[0]
        if t == "p":
            out.append(Paragraph(_pdf_markup(b[1]), S["corpo"]))
        elif t == "h3":
            out.append(Paragraph(_pdf_markup(b[1]), S["h3"]))
        elif t == "cit":
            out.append(_cit_pdf(S, b[1], b[2]))
        elif t == "destaque":
            out += _destaque_pdf(S, b[1], b[2])
        elif t == "tabela":
            out += _tabela_pdf(S, b[1], b[2], b[3] if len(b) > 3 else None)
        elif t == "lista":
            out += _lista_pdf(S, b[1], b[2] if len(b) > 2 else False)
        elif t == "pb":
            out.append(PageBreak())
    return out


def gerar_pdf(A):
    _registar_fontes()
    meta = A["meta"]
    codigo = f"EBE-APO-{meta['numero_global']}"
    titulo_doc = f"Apostila — {meta['titulo']}"
    S = _estilos_pdf()

    out_path = os.path.join(pasta_destino(meta), nome_ficheiro(meta) + ".pdf")

    def _pagina(canvas, doc_, cab=True):
        canvas.saveState()
        W, H = A4
        if cab:
            canvas.setFont("Serif-Italic", 8)
            canvas.setFillColor(VERDE)
            canvas.drawRightString(W - 2.5*cm, H - 1.6*cm,
                                   f"Escola Bíblica Epignósis  ·  {titulo_doc}")
        canvas.setFont("Serif", 8)
        canvas.setFillColor(CINZA)
        canvas.drawCentredString(W / 2, 1.4*cm, f"{codigo}  ·  {doc_.page}")
        canvas.restoreState()

    doc = BaseDocTemplate(
        out_path, pagesize=A4,
        topMargin=2.5*cm, bottomMargin=2.5*cm,
        leftMargin=3.0*cm, rightMargin=2.5*cm,
        title=titulo_doc, author="Escola Bíblica Epignósis",
        subject=f"Material didáctico oficial · {codigo}",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
    doc.addPageTemplates([
        PageTemplate(id="Capa", frames=[frame], onPage=lambda c, d: _pagina(c, d, False)),
        PageTemplate(id="Normal", frames=[frame], onPage=lambda c, d: _pagina(c, d, True)),
    ])

    E = [NextPageTemplate("Normal")]

    # ===== CAPA =====
    ir = ImageReader(LOGO_PATH)
    iw, ih = ir.getSize()
    E.append(Spacer(1, 10))
    E.append(Image(LOGO_PATH, width=5.0*cm, height=5.0*cm*ih/iw))
    E.append(Spacer(1, 6))
    E.append(Paragraph("Conhecer a Deus. Viver a Palavra. Manifestar o Reino.", S["lema"]))
    E.append(_linha(VERDE, 1.0, 4, 8))
    E.append(Paragraph(meta["instituto"].upper(), S["capa_inst"]))
    E.append(Paragraph(
        f"{meta['escola']}  ·  Curso «{meta['curso']}»  ·  Módulo {meta['modulo_num']} — {meta['modulo_nome']}",
        S["capa_curso"]))
    E.append(Paragraph(f"APOSTILA N.º  {meta['numero_no_curso']:02d}", S["capa_num"]))
    E.append(Paragraph(meta["titulo"], S["capa_tit"]))
    E.append(Paragraph(meta["subtitulo"], S["capa_sub"]))
    E.append(Spacer(1, 22))

    ident = [
        ("Autor / Docente", "Direcção Pedagógica · Escola Bíblica Epignósis"),
        ("Carga horária estimada", meta.get("carga", "2–3 horas de estudo")),
        ("Nível formativo", meta["nivel"]),
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
    E.append(_linha(VERDE, 0.8, 2, 6))
    E.append(Paragraph(f"Material didáctico oficial · Código {codigo} · 2026", S["capa_cod"]))
    E.append(PageBreak())

    # ===== MARCO FILOSÓFICO =====
    E.append(Spacer(1, 130))
    E.append(Paragraph("MARCO FILOSÓFICO", S["marco_tit"]))
    E.append(_linha(VERDE, 0.8, 4, 16))
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

    # ===== FICHA TÉCNICA =====
    E += _h1_pdf(S, "Ficha Técnica")
    E.append(Paragraph(
        "Este material didáctico é propriedade intelectual da Escola Bíblica "
        "Epignósis (EBE), produzido para uso exclusivo no âmbito dos seus "
        "programas de formação. A sua reprodução, no todo ou em parte, "
        "depende de autorização institucional escrita.", S["corpo"]))
    E += _lista_pdf(S, [
        f"Título da apostila: {meta['titulo']}.",
        f"Curso: {meta['curso']} ({meta['curso_carga']}).",
        f"Módulo: {meta['modulo_num']} — {meta['modulo_nome']} (Apostila {meta['apostila_no_modulo']} de {meta['apostilas_no_modulo']}).",
        f"Escola: {meta['escola']} · {meta['instituto']}.",
        f"Nível formativo: {meta['nivel']}.",
        "Autor / Docente: Direcção Pedagógica da Escola Bíblica Epignósis.",
        "Revisão pedagógica: Coordenação Acadêmica.",
        f"Revisão doutrinária: Conselho Doutrinário ({meta['base_doutrinaria']}).",
        "Versão bíblica de referência: Almeida Revista e Corrigida (ARC).",
        "Edição: 1.ª — 2026.",
        f"Código institucional: {codigo}.",
    ])
    E.append(_cit_pdf(S, A["citacao_ficha"][0], A["citacao_ficha"][1]))
    E.append(PageBreak())

    # ===== SUMÁRIO =====
    E += _h1_pdf(S, "Sumário")
    E += _lista_pdf(S, [i.replace("   ", "&nbsp;&nbsp;&nbsp;") for i in _sumario(A)])
    E.append(PageBreak())

    # ===== APRESENTAÇÃO =====
    E += _h1_pdf(S, "Apresentação da Apostila")
    for t_ in A["apresentacao"]:
        E.append(Paragraph(_pdf_markup(t_), S["corpo"]))

    # ===== OBJECTIVOS =====
    E += _h1_pdf(S, "Objectivos de Aprendizagem")
    E.append(Paragraph("Ao concluir o estudo desta apostila, o(a) aluno(a) será capaz de:", S["corpo"]))
    E += _lista_pdf(S, A["objectivos"], ordenada=True)

    # ===== VERSÍCULO-CHAVE =====
    E += _h1_pdf(S, "Versículo-Chave")
    E.append(_cit_pdf(S, A["versiculo_chave"][0], A["versiculo_chave"][1]))

    # ===== TEXTO-BASE =====
    E += _h1_pdf(S, "Texto-Base para Leitura")
    E.append(Paragraph(_pdf_markup(A["texto_base"]["intro"]), S["corpo"]))
    E.append(Paragraph(A["texto_base"]["passagem"], S["texto_base"]))
    E.append(PageBreak())

    # ===== 1. INTRODUÇÃO =====
    E += _h1_pdf(S, f"1. Introdução — {A['introducao']['titulo']}")
    E += _blocos_pdf(S, A["introducao"]["blocos"])

    # ===== 2. DESENVOLVIMENTO =====
    E += _h1_pdf(S, "2. Desenvolvimento do Conceito Central")
    for i, sec in enumerate(A["desenvolvimento"], 1):
        E.append(Paragraph(f"2.{i}. {_pdf_markup(sec['titulo'])}", S["h2"]))
        E += _blocos_pdf(S, sec["blocos"])
    E.append(PageBreak())

    # ===== 3. APLICAÇÃO =====
    E += _h1_pdf(S, "3. Aplicação Prática")
    E.append(Paragraph(_pdf_markup(A["aplicacao"]["intro"]), S["corpo"]))
    E += _lista_pdf(S, A["aplicacao"]["itens"], ordenada=True)

    # ===== 4. SÍNTESE =====
    E += _h1_pdf(S, "4. Síntese e Conclusão")
    for t_ in A["sintese"]["paragrafos"]:
        E.append(Paragraph(_pdf_markup(t_), S["corpo"]))
    E.append(_cit_pdf(S, A["sintese"]["citacao"][0], A["sintese"]["citacao"][1]))
    E.append(PageBreak())

    # ===== EXERCÍCIOS =====
    E += _h1_pdf(S, "Exercícios de Revisão")
    E.append(Paragraph(
        "Responda às questões a seguir com base no conteúdo desta apostila "
        "e na sua leitura bíblica.", S["corpo"]))
    E.append(Paragraph("I — Verifique a sua compreensão", S["h3"]))
    E += _lista_pdf(S, A["exercicios"]["compreensao"], ordenada=True)
    E.append(Paragraph("II — Reflexão pessoal", S["h3"]))
    E += _lista_pdf(S, A["exercicios"]["reflexao"], ordenada=True)
    E.append(Paragraph("III — Ministério e serviço", S["h3"]))
    E += _lista_pdf(S, A["exercicios"]["ministerio"], ordenada=True)

    # ===== ESTUDO BÍBLICO =====
    E += _h1_pdf(S, f"Estudo Bíblico Complementar — {A['estudo']['titulo']}")
    E.append(Paragraph(_pdf_markup(A["estudo"]["intro"]), S["corpo"]))
    E += _lista_pdf(S, A["estudo"]["perguntas"], ordenada=True)

    # ===== PRÓXIMA APOSTILA =====
    E += _h1_pdf(S, "Para a Próxima Apostila")
    E.append(Paragraph(_pdf_markup(A["proxima"]["texto"]), S["corpo"]))
    E += _lista_pdf(S, A["proxima"]["itens"])
    E.append(PageBreak())

    # ===== GLOSSÁRIO =====
    E += _h1_pdf(S, "Glossário")
    E.append(Paragraph("Definições breves dos termos-chave utilizados nesta apostila.", S["corpo"]))
    E += _tabela_pdf(S,
        ["Termo", "Definição"],
        [[f"<b><font color='#1B3A5C'>{t_}</font></b>", d] for t_, d in A["glossario"]],
        [5.4, 10.1])

    # ===== BIBLIOGRAFIA =====
    E += _h1_pdf(S, "Bibliografia Recomendada")
    E += _lista_pdf(S, A["bibliografia"])

    # ===== ANOTAÇÕES =====
    E += _h1_pdf(S, "Anotações Pessoais")
    for _ in range(12):
        E.append(Spacer(1, 16))
        E.append(HRFlowable(width="100%", thickness=0.5, color=CINZA_LINHA))

    # ===== SELO =====
    E.append(Spacer(1, 24))
    E.append(_linha(VERDE, 0.8, 2, 10))
    E.append(Paragraph("ESCOLA BÍBLICA EPIGNÓSIS", S["selo1"]))
    E.append(Paragraph("Conhecer a Deus. Viver a Palavra. Manifestar o Reino.", S["selo2"]))
    E.append(Paragraph("Soli Deo Gloria", S["selo3"]))

    doc.build(E)
    return out_path


def gerar_apostila(A):
    """Gera .docx e .pdf de uma apostila; devolve os caminhos."""
    return gerar_docx(A), gerar_pdf(A)
