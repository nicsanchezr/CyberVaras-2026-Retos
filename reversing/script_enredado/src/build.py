#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera reto.py: script Python ofuscado (base64 + marshal + rot) que valida la
flag. Desofuscar reemplazando exec->print o pelando capas. Salida: ../entrega/reto.py"""
import os, base64, marshal, codecs
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "entrega"))
flag = open(os.path.join(HERE, "..", "flag.txt")).read().strip()

# código interno que compara input con la flag
inner = f'''
import sys
FLAG = {flag!r}
try:
    g = input("flag? ")
except EOFError:
    g = ""
print("Correcto!" if g == FLAG else "Nope.")
'''
code_obj = compile(inner, "<reto>", "exec")
payload = base64.b64encode(marshal.dumps(code_obj)).decode()
# capa extra: rot13 sobre el nombre de los módulos para despistar
loader = (
 "import base64 as _a, marshal as _b\n"
 f"_d = {payload!r}\n"
 "exec(_b.loads(_a.b64decode(_d)))\n"
)
# una vuelta más: todo el loader en base64 dentro de un exec
outer = base64.b64encode(loader.encode()).decode()
final = (
 "#!/usr/bin/env python3\n"
 "# CyberVaras 2026 :: rev :: script_enredado\n"
 "import base64\n"
 f"exec(base64.b64decode({outer!r}).decode())\n"
)
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, "reto.py"), "w").write(final)
print("[ok] reto.py generado (capas: base64 -> base64 -> marshal)")
print("    writeup: reemplazar el exec externo por print para ver la capa interna")
