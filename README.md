# Apostilas EBE — Escola Bíblica Epignósis

Repositório oficial de produção das **1.029 apostilas** da Escola Bíblica
Epignósis, organizadas segundo a Arquitectura Oficial (EBE-DOC-005):
**Nível → Instituto → Escola → Curso → Módulo → Apostila**.

## Estrutura do repositório

| Pasta | Conteúdo |
|---|---|
| `Apostilas/` | As apostilas (.docx + .pdf), organizadas por Instituto / Escola / Curso / Módulo |
| `Documentos_Institucionais/` | EBE-DOC-001 a 008, Compêndios |
| `Manuais/` | Manual do Aluno e Manual do Docente |
| `Formularios/` | Formulários da Secretaria Acadêmica (FRM/HIS) |
| `Modelos/` | Modelos de apostila, certificados, TCC e Apostila Piloto |
| `Planeamento/` | Mapa Completo das 1.029 Apostilas (EBE-PLAN-APO) |
| `Geradores/` | Sistema de produção (framework + conteúdos) |

## Como produzir apostilas

```bash
cd Geradores
python3 produzir.py            # todas
python3 produzir.py 0002 0003  # apenas as indicadas
```

Cada apostila tem o seu conteúdo próprio e original em
`Geradores/conteudos/apo_XXXX.py`; o framework (`apostila_framework.py`)
aplica o padrão editorial oficial (15–20 páginas) e grava o .docx na
árvore `Apostilas/`.

## Progresso — 9 / 1.029

### Instituto 1 — Formação Cristã · Escola de Fundamentos da Fé

**Curso 1 — Salvação e Novo Nascimento (25 h) — ✅ COMPLETO (9/9)**

Módulo 1 — Fundamentos da Salvação:
- [x] EBE-APO-0001 — O Estado de Perdição do Ser Humano
- [x] EBE-APO-0002 — A Graça de Deus em Cristo
- [x] EBE-APO-0003 — Fé e Arrependimento como Resposta

Módulo 2 — O Novo Nascimento:
- [x] EBE-APO-0004 — O Significado Bíblico de Nascer de Novo
- [x] EBE-APO-0005 — A Obra do Espírito Santo na Regeneração
- [x] EBE-APO-0006 — Sinais de uma Vida Regenerada

Módulo 3 — Vivendo a Nova Vida:
- [x] EBE-APO-0007 — Segurança da Salvação
- [x] EBE-APO-0008 — Crescendo Após o Novo Nascimento
- [x] EBE-APO-0009 — Testemunho e Confissão da Fé

**Próximo: Curso 2 — Arrependimento e Fé (20 h)**, começando por
EBE-APO-0010 — Metanoia: Mudança de Mente e Direção.

- [ ] … 1.020 restantes, segundo o Mapa (Planeamento/)

*Soli Deo Gloria.*
