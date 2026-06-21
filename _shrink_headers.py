# -*- coding: utf-8 -*-
# Reduce el tamaño de los headers internos de cada resumen.
import sys

# Grupo A: Derivados (apuntes) + Portafolios -> header / tabs idénticos
GROUP_A = [
    "Derivados/Apunte 1er Parcial — U1-U4.html",
    "Derivados/Apunte 2do Parcial — U5-U6-U8.html",
    "Adm. de Portafolios/Apunte 1P - Portafolios.html",
    "Adm. de Portafolios/Apunte 2P - Portafolios.html",
]
REPL_A = [
    ("padding:28px 20px 14px", "padding:14px 20px 8px"),                 # header
    ("font-size:1.45rem", "font-size:1.1rem"),                          # h1
    ("font-size:.85rem; margin-top:6px", "font-size:.76rem; margin-top:3px"),  # p
    ("padding:14px 16px; position:sticky", "padding:8px 16px; position:sticky"),  # .tabs
    ("padding:8px 16px; border-radius:20px", "padding:6px 14px; border-radius:20px"),  # .tab
    ("font-size:.88rem; transition:.15s", "font-size:.82rem; transition:.15s"),  # .tab
]

# Grupo B: Fórmulas
GROUP_B = ["Derivados/Fórmulas — U5-U6-U8 (Opciones).html"]
REPL_B = [
    (".title{font-size:1.6rem;font-weight:700}", ".title{font-size:1.15rem;font-weight:700}"),
    (".subtitle{color:var(--text2);font-size:.95rem;margin:4px 0 18px}",
     ".subtitle{color:var(--text2);font-size:.78rem;margin:3px 0 10px}"),
]

# Grupo C: Finanzas
GROUP_C = ["Finanzas Corporativas/Teoría — U2-U3-U4 (2do Parcial).html"]
REPL_C = [
    (".top{margin-bottom:22px}", ".top{margin-bottom:12px}"),
    (".top h1{font-size:22px;font-weight:700;letter-spacing:-.3px}",
     ".top h1{font-size:17px;font-weight:700;letter-spacing:-.3px}"),
    (".top .sub{color:var(--text2);font-size:13.5px;margin-top:6px}",
     ".top .sub{color:var(--text2);font-size:12px;margin-top:3px}"),
]

def apply(files, repls):
    for f in files:
        with open(f, "r", encoding="utf-8") as fh:
            txt = fh.read()
        print(f"\n{f}")
        for old, new in repls:
            n = txt.count(old)
            txt = txt.replace(old, new)
            flag = "OK" if n > 0 else "!! 0 (no encontrado)"
            print(f"   [{flag}] {old[:42]}  x{n}")
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(txt)

apply(GROUP_A, REPL_A)
apply(GROUP_B, REPL_B)
apply(GROUP_C, REPL_C)
print("\nListo.")
