# -*- coding: utf-8 -*-
"""
PRODUÇÃO EM LOTE DE APOSTILAS — Escola Bíblica Epignósis

Uso:
    python3 produzir.py                 # produz todas as apostilas em conteudos/
    python3 produzir.py 0002 0003       # produz apenas os números indicados

Cada ficheiro conteudos/apo_XXXX.py define um dicionário APOSTILA.
O framework gera .docx e .pdf na árvore Apostilas/Instituto/Escola/Curso/Módulo.
"""
import glob
import importlib.util
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

from apostila_framework import gerar_apostila


def carregar(caminho):
    spec = importlib.util.spec_from_file_location(
        os.path.basename(caminho)[:-3], caminho)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.APOSTILA


def main():
    apenas = set(sys.argv[1:])
    ficheiros = sorted(glob.glob(os.path.join(BASE, "conteudos", "apo_*.py")))
    if not ficheiros:
        print("Nenhum conteúdo encontrado em conteudos/.")
        return
    total = 0
    for f in ficheiros:
        numero = os.path.basename(f)[4:-3]
        if apenas and numero not in apenas:
            continue
        A = carregar(f)
        docx, pdf = gerar_apostila(A)
        rel = os.path.relpath(os.path.dirname(docx), os.path.dirname(BASE))
        print(f"✔ EBE-APO-{A['meta']['numero_global']} — {A['meta']['titulo']}")
        print(f"   → {rel}/")
        total += 1
    print(f"\n{total} apostila(s) produzida(s).")


if __name__ == "__main__":
    main()
