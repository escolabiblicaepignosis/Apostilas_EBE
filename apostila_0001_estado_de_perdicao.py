"""
APOSTILA 0001 — Escola Bíblica Epignósis
«O Estado de Perdição do Ser Humano»

Posição no Mapa Completo de Apostilas (EBE-PLAN-APO):
  Nível 1 — Discípulo (Conhecer)
  Instituto 1 — Instituto de Formação Cristã
  Escola de Fundamentos da Fé
  Curso: Salvação e Novo Nascimento · 25 h
  Módulo 1 — Fundamentos da Salvação · Apostila 1 de 3

Primeira apostila da série de produção segundo o Mapa Completo
de Apostilas da EBE (1.029 apostilas). Padrão editorial conforme
a Apostila Piloto (EBE-APO-001) e o Modelo de Apostila oficial.

Fundamentação doutrinária: Declaração de Fé Institucional
(EBE-DOC-002), Art. 6.º — O Ser Humano e o Pecado; Art. 7.º — A Salvação.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _estilos import *
from _estilos import _shade_cell, _add_horizontal_line

CODIGO = "EBE-APO-0001"


def quadro_destaque(doc, rotulo, texto):
    tbl = doc.add_table(rows=1, cols=1)
    cell = tbl.rows[0].cells[0]
    _shade_cell(cell, "E8F1EC")
    p = cell.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(f"✦ {rotulo}:  ")
    r.font.bold = True; r.font.color.rgb = COR_SECUNDARIA
    r.font.name = FONTE_TITULO; r.font.size = Pt(11)
    r2 = p.add_run(texto)
    r2.font.name = FONTE_CORPO; r2.font.size = Pt(11); r2.font.italic = True


def gerar():
    doc = novo_documento("Apostila — O Estado de Perdição do Ser Humano", CODIGO)

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
    r = p.add_run("INSTITUTO DE FORMAÇÃO CRISTÃ")
    r.font.name = FONTE_TITULO; r.font.size = Pt(11); r.font.bold = True
    r.font.color.rgb = COR_SECUNDARIA

    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Escola de Fundamentos da Fé  ·  Curso «Salvação e Novo Nascimento»  ·  Módulo 1 — Fundamentos da Salvação")
    r.font.name = FONTE_CORPO; r.font.size = Pt(10); r.font.color.rgb = COR_CITACAO

    doc.add_paragraph()
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("APOSTILA N.º  01")
    r.font.name = FONTE_TITULO; r.font.size = Pt(13); r.font.bold = True
    r.font.color.rgb = COR_SECUNDARIA

    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("O Estado de Perdição do Ser Humano")
    r.font.name = FONTE_TITULO; r.font.size = Pt(28); r.font.bold = True
    r.font.color.rgb = COR_PRIMARIA

    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Compreender a nossa condição sem Cristo para valorizar a salvação em Cristo")
    r.font.name = FONTE_TITULO; r.font.size = Pt(13)
    r.font.italic = True; r.font.color.rgb = COR_TEXTO

    doc.add_paragraph(); doc.add_paragraph()

    # quadro de identificação
    tbl = doc.add_table(rows=4, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    dados = [
        ("Autor / Docente", "Direcção Pedagógica · Escola Bíblica Epignósis"),
        ("Carga horária estimada", "2 horas de estudo"),
        ("Nível formativo", "Nível 1 — Discípulo (Conhecer)"),
        ("Edição / Ano", "1.ª edição — 2026"),
    ]
    for i, (k, v) in enumerate(dados):
        row = tbl.rows[i].cells
        row[0].text = k; row[1].text = v
        _shade_cell(row[0], "E8F1EC")
        for p in row[0].paragraphs:
            for r in p.runs:
                r.font.bold = True; r.font.name = FONTE_TITULO; r.font.size = Pt(10)
                r.font.color.rgb = COR_PRIMARIA
        for p in row[1].paragraphs:
            for r in p.runs:
                r.font.name = FONTE_CORPO; r.font.size = Pt(10)

    doc.add_paragraph()
    p = doc.add_paragraph(); _add_horizontal_line(p, color=HEX_SECUNDARIA, size=4)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(f"Material didáctico oficial · Código {CODIGO} · 2026")
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
    lista(doc, [
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
    citacao(doc,
        "Porque o Filho do Homem veio buscar e salvar o que se havia perdido.",
        "Lucas 19.10")

    page_break(doc)

    # ====== SUMÁRIO ======
    h1(doc, "Sumário")
    lista(doc, [
        "Apresentação da apostila",
        "Objectivos de aprendizagem",
        "Versículo-chave",
        "Texto-base para leitura",
        "1. Introdução — Por que começar pela má notícia",
        "2. Desenvolvimento do conceito central",
        "   2.1 Fundamentos bíblicos",
        "   2.2 O que significa estar «perdido»",
        "   2.3 As quatro dimensões da perdição humana",
        "   2.4 Dúvidas e equívocos comuns",
        "   2.5 Quadro de destaque — para reter",
        "3. Aplicação prática",
        "4. Síntese e conclusão",
        "Exercícios de revisão",
        "Estudo bíblico complementar — Lucas 15: o perdido aos olhos de Deus",
        "Para a próxima apostila",
        "Glossário",
        "Bibliografia recomendada",
        "Anotações pessoais",
    ])

    page_break(doc)

    # ====== APRESENTAÇÃO ======
    h1(doc, "Apresentação da Apostila")
    paragrafo(doc,
        "Esta apostila abre o Módulo 1 — Fundamentos da Salvação — do Curso "
        "«Salvação e Novo Nascimento», o primeiro curso da Escola de "
        "Fundamentos da Fé. É, por isso, a porta de entrada de toda a "
        "jornada formativa Epignósis: antes de aprender qualquer doutrina, "
        "o discípulo precisa de compreender de onde Deus o resgatou.")
    paragrafo(doc,
        "O Evangelho é uma boa notícia. Mas nenhuma boa notícia é "
        "plenamente entendida sem se conhecer a má notícia que a precede: "
        "fora de Cristo, o ser humano está perdido, separado de Deus pelo "
        "pecado e incapaz de se salvar por esforço próprio. Nesta apostila "
        "estudaremos o que a Escritura ensina sobre esse estado de "
        "perdição — a sua origem, a sua extensão e as suas consequências —, "
        "não para nos deixar no desespero, mas para nos conduzir, com "
        "gratidão e humildade, à graça de Deus em Cristo, tema da próxima apostila.")
    paragrafo(doc,
        "Ao final do estudo, o aluno terá alicerces firmes para compreender "
        "por que a salvação é inteiramente obra da graça de Deus, e estará "
        "preparado para testemunhar do Evangelho com clareza e compaixão.")

    # ====== OBJECTIVOS ======
    h1(doc, "Objectivos de Aprendizagem")
    paragrafo(doc, "Ao concluir o estudo desta apostila, o(a) aluno(a) será capaz de:")
    lista(doc, [
        "CONHECER — explicar, a partir das Escrituras, a origem do pecado (Génesis 3), a sua extensão universal (Romanos 3.23; 5.12) e as quatro dimensões da perdição humana.",
        "CRER — interiorizar a convicção de que nenhuma obra, mérito ou religiosidade humana pode remover o pecado, e de que a salvação só é possível pela graça de Deus em Cristo.",
        "VIVER — cultivar humildade e gratidão diante de Deus, abandonando toda a autossuficiência espiritual e reconhecendo diariamente a dependência da graça.",
        "SERVIR — apresentar o Evangelho a outros de forma fiel, começando pela real condição humana, com verdade e com a compaixão de Cristo, sem dureza nem condenação farisaica.",
    ], ordenada=True)

    # ====== VERSÍCULO-CHAVE ======
    h1(doc, "Versículo-Chave")
    citacao(doc,
        "Porque todos pecaram e destituídos estão da glória de Deus.",
        "Romanos 3.23")

    # ====== TEXTO-BASE ======
    h1(doc, "Texto-Base para Leitura")
    paragrafo(doc,
        "Antes de iniciar o estudo, leia atentamente, em sua Bíblia "
        "(Almeida Revista e Corrigida), a seguinte passagem, observando "
        "como Paulo descreve o que éramos sem Cristo e o que Deus fez por nós:")
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Efésios 2.1-10")
    r.font.name = FONTE_TITULO; r.font.size = Pt(14); r.font.bold = True
    r.font.color.rgb = COR_SECUNDARIA

    page_break(doc)

    # ====== 1. INTRODUÇÃO ======
    h1(doc, "Introdução — Por que Começar pela Má Notícia", numero=1)
    paragrafo(doc,
        "Ninguém procura um médico enquanto se julga saudável. Da mesma "
        "forma, ninguém corre para o Salvador enquanto não compreende que "
        "está perdido. Foi o próprio Jesus quem o disse: «Os sãos não "
        "necessitam de médico, mas sim os que estão doentes» (Mateus 9.12). "
        "Por isso, todo o ensino bíblico sobre a salvação começa pelo "
        "diagnóstico: a condição real do ser humano diante de Deus.")
    paragrafo(doc,
        "Este ponto de partida distingue o Evangelho de todas as "
        "religiões e filosofias humanas. Estas partem do princípio de que "
        "o homem pode, por esforço, disciplina ou mérito, elevar-se até "
        "Deus. A Escritura, pelo contrário, revela que o ser humano, "
        "criado à imagem de Deus e para comunhão com Ele, caiu pelo "
        "pecado e tornou-se incapaz de se restaurar a si mesmo. A "
        "iniciativa da salvação, do princípio ao fim, pertence a Deus.")
    citacao(doc,
        "Porque o Filho do Homem veio buscar e salvar o que se havia perdido.",
        "Lucas 19.10")
    paragrafo(doc,
        "Note-se: Jesus não veio ajudar quem já se estava a salvar; veio "
        "buscar e salvar o que se havia perdido. Compreender a perdição é, "
        "portanto, o primeiro passo para compreender — e amar — a salvação.")

    # ====== 2. DESENVOLVIMENTO ======
    h1(doc, "Desenvolvimento do Conceito Central", numero=2)

    h2(doc, "Fundamentos bíblicos", numero="2.1")
    paragrafo(doc,
        "A doutrina do estado de perdição não se apoia num único "
        "versículo, mas atravessa toda a Escritura. Observemos três "
        "passagens-chave:")

    h3(doc, "a) A queda — a entrada do pecado no mundo (Génesis 3)")
    paragrafo(doc,
        "Deus criou o ser humano — homem e mulher — à Sua imagem e "
        "semelhança, com dignidade, propósito e vocação (Génesis 1.27). "
        "Mas, pela desobediência voluntária dos nossos primeiros pais, o "
        "pecado entrou no mundo. As consequências foram imediatas: "
        "vergonha (Génesis 3.7), medo e fuga da presença de Deus "
        "(Génesis 3.8-10), transferência de culpa (Génesis 3.12-13) e, "
        "por fim, a expulsão do Éden — figura da separação entre o homem "
        "e o seu Criador (Génesis 3.23-24).")
    citacao(doc,
        "E chamou o Senhor Deus a Adão e disse-lhe: Onde estás?",
        "Génesis 3.9")
    paragrafo(doc,
        "A primeira pergunta de Deus ao homem caído — «Onde estás?» — não "
        "é a pergunta de quem procura informação, mas de quem procura o "
        "perdido. Já em Génesis 3, a perdição humana é acompanhada pela "
        "busca amorosa de Deus.")

    h3(doc, "b) A extensão universal do pecado (Romanos 3 e 5)")
    paragrafo(doc,
        "Paulo, na Epístola aos Romanos, demonstra que a perdição não é "
        "problema de alguns, mas condição de todos — judeus e gentios, "
        "religiosos e pagãos:")
    citacao(doc,
        "Como está escrito: Não há um justo, nem um sequer. Não há ninguém "
        "que entenda; não há ninguém que busque a Deus.",
        "Romanos 3.10-11")
    citacao(doc,
        "Pelo que, como por um homem entrou o pecado no mundo, e pelo "
        "pecado, a morte, assim também a morte passou a todos os homens, "
        "por isso que todos pecaram.",
        "Romanos 5.12")
    paragrafo(doc,
        "Pecamos por natureza (herdámos de Adão uma natureza inclinada ao "
        "mal) e pecamos por prática (escolhas concretas de desobediência). "
        "Por isso ninguém pode apontar o dedo a outrem: «todos pecaram e "
        "destituídos estão da glória de Deus» (Romanos 3.23).")

    h3(doc, "c) Mortos em delitos e pecados (Efésios 2.1-3)")
    paragrafo(doc,
        "No texto-base desta apostila, Paulo usa a imagem mais forte "
        "possível para descrever a condição humana sem Cristo: morte "
        "espiritual. O homem natural não está apenas doente ou enfraquecido "
        "— está morto para Deus, andando segundo o curso deste mundo, "
        "sujeito às paixões da carne e, por natureza, sob a ira divina.")
    citacao(doc,
        "E vos vivificou, estando vós mortos em ofensas e pecados.",
        "Efésios 2.1")
    paragrafo(doc,
        "Um morto não se ressuscita a si mesmo. Esta imagem elimina, pela "
        "raiz, toda a esperança de autossalvação — e prepara o coração "
        "para a gloriosa expressão que se segue no versículo 4: «Mas Deus…».")

    h2(doc, "O que significa estar «perdido»", numero="2.2")
    paragrafo(doc,
        "Na linguagem bíblica, «perdido» não é um insulto, mas um "
        "diagnóstico. Descreve quem está fora do lugar para o qual foi "
        "criado: longe de Deus, sem paz verdadeira, sem direcção última e "
        "sem vida eterna. O pecado não é apenas a transgressão de regras; "
        "é a ruptura de uma relação — a relação para a qual fomos criados.")
    quadro_destaque(doc, "Definição",
        "Estado de perdição é a condição de todo o ser humano fora de "
        "Cristo: separado de Deus pelo pecado (Isaías 59.2), espiritualmente "
        "morto (Efésios 2.1), escravo do pecado (João 8.34), incapaz de se "
        "salvar por obras (Efésios 2.8-9) e sujeito ao juízo de Deus "
        "(Hebreus 9.27). Responde à pergunta: «de que precisa exactamente "
        "o ser humano de ser salvo?»")

    page_break(doc)

    h2(doc, "As quatro dimensões da perdição humana", numero="2.3")
    paragrafo(doc,
        "Para estudar com clareza, é útil distinguir quatro dimensões da "
        "perdição, todas ensinadas nas Escrituras:")

    # Tabela de dimensões
    tbl = doc.add_table(rows=1, cols=3)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = tbl.rows[0].cells
    for i, t in enumerate(["Dimensão", "O que a Escritura afirma", "Referência-chave"]):
        hdr[i].text = ""
        _shade_cell(hdr[i], HEX_PRIMARIA)
        p = hdr[i].paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(t)
        r.font.bold = True; r.font.name = FONTE_TITULO; r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    dimensoes = [
        ("1. Separação",
         "O pecado separa o homem de Deus; a comunhão foi quebrada.",
         "Isaías 59.2; Génesis 3.23-24"),
        ("2. Morte espiritual",
         "Sem Cristo, o homem está morto em ofensas e pecados.",
         "Efésios 2.1; Colossenses 2.13"),
        ("3. Escravidão",
         "Quem comete pecado é servo do pecado; não há libertação própria.",
         "João 8.34; Romanos 6.16-17"),
        ("4. Condenação",
         "O salário do pecado é a morte; aos homens está ordenado morrerem uma vez, vindo depois o juízo.",
         "Romanos 6.23; Hebreus 9.27; João 3.18"),
    ]
    for c in dimensoes:
        row = tbl.add_row().cells
        for i, v in enumerate(c):
            row[i].text = v
            for p in row[i].paragraphs:
                for r in p.runs:
                    r.font.name = FONTE_CORPO; r.font.size = Pt(10)

    paragrafo(doc,
        "Estas quatro dimensões mostram que a perdição atinge o ser humano "
        "por inteiro: a sua relação com Deus (separação), a sua vida "
        "interior (morte espiritual), a sua vontade (escravidão) e o seu "
        "destino eterno (condenação). Por isso a salvação que Deus oferece "
        "em Cristo é igualmente completa: reconciliação, regeneração, "
        "libertação e justificação.")

    h2(doc, "Dúvidas e equívocos comuns", numero="2.4")

    h3(doc, "Equívoco 1 — “Mas eu sou uma boa pessoa.”")
    paragrafo(doc,
        "A bondade relativa — ser melhor do que o vizinho — não é o padrão "
        "de Deus. O padrão é a Sua própria glória e santidade, da qual "
        "todos estamos destituídos (Romanos 3.23). As nossas melhores "
        "obras, diante da santidade divina, são como trapo da imundícia "
        "(Isaías 64.6). O problema não é a ausência de boas acções, mas a "
        "presença do pecado, que nenhuma boa acção apaga.")

    h3(doc, "Equívoco 2 — “A religião resolve.”")
    paragrafo(doc,
        "Práticas religiosas — cultos, ofertas, tradições — não removem o "
        "pecado. Nicodemos era mestre religioso em Israel e ouviu de Jesus: "
        "«necessário vos é nascer de novo» (João 3.7). Paulo era irrepreensível "
        "na justiça da lei, e considerou tudo perda por amor de Cristo "
        "(Filipenses 3.6-8). A religiosidade sem regeneração é apenas a "
        "perdição bem vestida.")

    h3(doc, "Equívoco 3 — “Falar de pecado é falta de amor.”")
    paragrafo(doc,
        "É exactamente o contrário. Ocultar o diagnóstico de um doente "
        "grave não é amor — é crueldade. O médico fiel diz a verdade para "
        "poder aplicar a cura. Jesus, que é amor encarnado, foi quem mais "
        "claramente falou da perdição humana — e chorou sobre Jerusalém "
        "(Lucas 19.41). A verdade sobre o pecado, dita com compaixão, é a "
        "porta da graça.")

    h3(doc, "Equívoco 4 — “Se estou perdido, não há esperança.”")
    paragrafo(doc,
        "A doutrina da perdição nunca aparece sozinha na Escritura. Em "
        "Génesis 3, Deus já promete o descendente que feriria a serpente "
        "(Génesis 3.15). Em Efésios 2, os «mortos em ofensas» são vivificados "
        "com Cristo. O diagnóstico existe por causa do remédio: «Mas Deus, "
        "que é riquíssimo em misericórdia…» (Efésios 2.4). A má notícia é "
        "real, mas a última palavra é da graça.")

    # Quadro destaque
    h2(doc, "Quadro de Destaque — para reter", numero="2.5")
    quadro_destaque(doc, "Para reter",
        "Fora de Cristo, todo o ser humano está separado de Deus, morto "
        "espiritualmente, escravo do pecado e sujeito ao juízo — e nenhuma "
        "obra humana pode mudar essa condição. Por isso a salvação é, do "
        "princípio ao fim, obra da graça de Deus, recebida pela fé em "
        "Jesus Cristo (Efésios 2.8-9).")

    page_break(doc)

    # ====== 3. APLICAÇÃO ======
    h1(doc, "Aplicação Prática", numero=3)
    paragrafo(doc,
        "A doutrina do estado de perdição não é apenas para ser sabida — é "
        "para transformar o coração, a oração e o testemunho do discípulo "
        "Epignósis. Vejamos cinco esferas de aplicação:")
    lista(doc, [
        "Na vida pessoal e devocional — recorde diariamente de onde Deus o "
        "tirou (Efésios 2.11-13). A memória da perdição alimenta a gratidão, "
        "quebra o orgulho espiritual e renova o primeiro amor.",
        "Na família — ore pelos familiares que ainda não conhecem a Cristo "
        "com a consciência de que estão perdidos e de que Deus os busca; "
        "interceda com perseverança e testemunhe com mansidão.",
        "Na igreja local — trate os novos convertidos e os visitantes sem "
        "superioridade: a única diferença entre o salvo e o perdido é a "
        "graça recebida, não o mérito alcançado.",
        "No trabalho e na sociedade — veja colegas e vizinhos como Jesus "
        "via as multidões: «como ovelhas que não têm pastor» (Mateus 9.36). "
        "A compaixão, e não o juízo, deve marcar o olhar do discípulo.",
        "No exercício ministerial — ao evangelizar e ensinar, apresente o "
        "diagnóstico bíblico completo antes de oferecer o remédio. Um "
        "evangelho sem consciência de pecado produz decisões sem conversão.",
    ], ordenada=True)

    # ====== 4. SÍNTESE ======
    h1(doc, "Síntese e Conclusão", numero=4)
    paragrafo(doc,
        "Estudámos, nesta apostila, que o ser humano foi criado à imagem "
        "de Deus, para comunhão com Ele, mas que, pela desobediência "
        "voluntária dos nossos primeiros pais, o pecado entrou no mundo e "
        "alcançou toda a humanidade. Vimos que a perdição tem quatro "
        "dimensões — separação, morte espiritual, escravidão e condenação — "
        "e que nenhuma obra, mérito ou religiosidade humana pode remover o pecado.")
    paragrafo(doc,
        "Este diagnóstico, longe de nos lançar no desespero, prepara-nos "
        "para receber e anunciar a maior de todas as notícias: Deus, que é "
        "riquíssimo em misericórdia, tomou a iniciativa de nos buscar em "
        "Cristo. É esse o tema da próxima apostila — A Graça de Deus em Cristo.")
    citacao(doc,
        "Mas Deus, que é riquíssimo em misericórdia, pelo seu muito amor "
        "com que nos amou, estando nós ainda mortos em nossas ofensas, nos "
        "vivificou juntamente com Cristo (pela graça sois salvos).",
        "Efésios 2.4-5")

    page_break(doc)

    # ====== EXERCÍCIOS ======
    h1(doc, "Exercícios de Revisão")
    paragrafo(doc,
        "Responda às questões a seguir com base no conteúdo desta apostila "
        "e na sua leitura bíblica.")

    h3(doc, "I — Verifique a sua compreensão")
    lista(doc, [
        "Explique, com as suas próprias palavras, o que a Bíblia quer dizer quando afirma que o ser humano está “perdido”.",
        "Quais são as quatro dimensões da perdição humana? Indique uma referência bíblica para cada uma.",
        "Que consequências imediatas da queda observamos em Génesis 3.7-13?",
        "O que significa a expressão “mortos em ofensas e pecados” (Efésios 2.1)? Por que essa imagem exclui a autossalvação?",
        "Explique a diferença entre pecar “por natureza” e pecar “por prática”.",
    ], ordenada=True)

    h3(doc, "II — Reflexão pessoal")
    lista(doc, [
        "Antes de conhecer a Cristo, em que “dimensão da perdição” você mais sentia o peso do pecado? Como a graça de Deus o(a) alcançou?",
        "Há alguma área da sua vida em que ainda confia mais no próprio esforço do que na graça de Deus? Qual?",
        "Escreva uma breve oração de gratidão a Deus por o(a) ter buscado quando estava perdido(a).",
    ], ordenada=True)

    h3(doc, "III — Ministério e serviço")
    lista(doc, [
        "Como você explicaria, em 3 minutos e com amor, a um amigo não crente, que “ser boa pessoa” não resolve o problema do pecado?",
        "Faça uma lista de três pessoas do seu convívio que ainda não conhecem a Cristo e comprometa-se a orar por elas durante este módulo.",
    ], ordenada=True)

    # ====== ESTUDO BÍBLICO ======
    h1(doc, "Estudo Bíblico Complementar — Lucas 15: o Perdido aos Olhos de Deus")
    paragrafo(doc,
        "Em Lucas 15, respondendo à murmuração dos fariseus — «Este recebe "
        "pecadores e come com eles» —, Jesus conta três parábolas sobre o "
        "que se perdeu: a ovelha, a dracma e o filho. Nelas aprendemos como "
        "Deus vê o perdido — e como o céu reage quando ele é encontrado. "
        "Leia atentamente Lucas 15.1-32 e responda:")
    lista(doc, [
        "Nas três parábolas, quem toma a iniciativa de buscar (ou receber) o que estava perdido? O que isso revela sobre o coração de Deus?",
        "O filho pródigo «caiu em si» (v. 17). Que passos concretos se seguiram a esse despertar? (vv. 18-20)",
        "Compare a atitude do pai (vv. 20-24) com a do filho mais velho (vv. 25-30). Qual das duas atitudes se parece mais com a nossa diante dos perdidos?",
        "Que frase se repete no final das três parábolas sobre a alegria? (vv. 7, 10, 32) O que ela ensina sobre o valor de cada pecador que se arrepende?",
        "À luz de Lucas 15, como deve a igreja tratar quem chega “perdido” aos nossos cultos e células?",
    ], ordenada=True)

    # ====== PRÓXIMA APOSTILA ======
    h1(doc, "Para a Próxima Apostila")
    paragrafo(doc,
        "Na próxima apostila — Apostila 2 — estudaremos A Graça de Deus "
        "em Cristo: a resposta divina ao estado de perdição humana. Para "
        "se preparar, leia previamente Efésios 2.4-10 e Tito 2.11-14, e "
        "reflicta sobre as seguintes perguntas:")
    lista(doc, [
        "Em Efésios 2.4-5, que palavras descrevem o carácter de Deus que motivou a nossa salvação?",
        "Segundo Tito 2.11-12, o que a graça de Deus faz, além de salvar?",
    ])

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
    termos = [
        ("Pecado (hamartia, ἁμαρτία)", "Literalmente, “errar o alvo”. Toda a desconformidade com o carácter e a vontade de Deus, em pensamento, palavra, acção ou omissão."),
        ("Queda", "O acto de desobediência voluntária de Adão e Eva (Génesis 3), pelo qual o pecado e a morte entraram no mundo e alcançaram toda a humanidade."),
        ("Perdição", "Condição do ser humano fora de Cristo: separado de Deus, espiritualmente morto, escravo do pecado e sujeito ao juízo divino."),
        ("Morte espiritual", "Estado de incapacidade e insensibilidade para com Deus (Efésios 2.1), distinto da morte física; só é revertido pela regeneração."),
        ("Imagem de Deus (imago Dei)", "Dignidade e vocação originais do ser humano, criado para reflectir o carácter de Deus e viver em comunhão com Ele (Génesis 1.27)."),
        ("Graça", "Favor imerecido de Deus para com o pecador; fonte exclusiva da salvação (Efésios 2.8-9). Tema da próxima apostila."),
        ("Epígnosis (ἐπίγνωσις)", "Conhecimento pleno, profundo e experimental de Deus — meta de todo o ensino da Escola Bíblica Epignósis."),
    ]
    for termo, defin in termos:
        row = tbl.add_row().cells
        row[0].text = termo; row[1].text = defin
        for c in row:
            for p in c.paragraphs:
                for r in p.runs:
                    r.font.name = FONTE_CORPO; r.font.size = Pt(10)
        for p in row[0].paragraphs:
            for r in p.runs:
                r.font.bold = True; r.font.color.rgb = COR_PRIMARIA

    # ====== BIBLIOGRAFIA ======
    h1(doc, "Bibliografia Recomendada")
    lista(doc, [
        "Bíblia Sagrada. Tradução de João Ferreira de Almeida, Revista e Corrigida.",
        "Declaração de Fé Institucional da Escola Bíblica Epignósis (EBE-DOC-002), Art. 6.º e 7.º.",
        "STOTT, John. A cruz de Cristo. São Paulo: Vida.",
        "PACKER, J. I. O conhecimento de Deus. São Paulo: Cultura Cristã.",
        "GRUDEM, Wayne. Teologia sistemática (capítulos sobre o pecado e a condição humana). São Paulo: Vida Nova.",
        "RYLE, J. C. Santidade (capítulo «Pecado»). São José dos Campos: Fiel.",
    ])

    # ====== ANOTAÇÕES ======
    h1(doc, "Anotações Pessoais")
    for _ in range(12):
        p = doc.add_paragraph(); _add_horizontal_line(p, color="C8C8C8", size=4)

    selo_final(doc)

    out = os.path.join(os.path.dirname(__file__),
                       "EBE-APO-0001_O_Estado_de_Perdicao_do_Ser_Humano.docx")
    doc.save(out); print("OK:", out)


if __name__ == "__main__":
    gerar()
