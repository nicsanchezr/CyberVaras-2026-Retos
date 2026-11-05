#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""XOR de clave repetida (6 bytes) sobre un texto largo que contiene la flag.
Salida: cipher.bin"""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "entrega"); os.makedirs(OUT, exist_ok=True)
flag = open(os.path.join(OUT, "..", "flag.txt")).read().strip()
KEY = b"CITT26"
pt = (
 "Informe interno del equipo azul. El trafico anomalo se detecto a las 03:00. "
 "El analista reviso los logs y encontro un indicador oculto en el reporte. "
 f"La bandera del incidente es {flag} y debe reportarse al CSIRT de inmediato. "
 "Fin del informe. Recuerde rotar las claves y nunca reutilizarlas."
).encode()
ct = bytes(b ^ KEY[i % len(KEY)] for i, b in enumerate(pt))
open(os.path.join(OUT, "cipher.bin"), "wb").write(ct)
dec = bytes(b ^ KEY[i % len(KEY)] for i, b in enumerate(ct))
assert flag.encode() in dec
print(f"[ok] cipher.bin generado ({len(ct)} bytes, clave {len(KEY)} bytes)")
