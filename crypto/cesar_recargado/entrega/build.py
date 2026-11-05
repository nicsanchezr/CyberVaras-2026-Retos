#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cifra la flag con César (shift fijo) + texto señuelo. Salida: mensaje.txt"""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
flag = open(os.path.join(HERE, "..", "flag.txt")).read().strip()
SHIFT = 7

def cesar(s, k):
    out = []
    for c in s:
        if 'a' <= c <= 'z': out.append(chr((ord(c)-97+k) % 26 + 97))
        elif 'A' <= c <= 'Z': out.append(chr((ord(c)-65+k) % 26 + 65))
        else: out.append(c)
    return "".join(out)

texto = ("Nota del operador: el mensaje importante viaja cifrado abajo.\n"
         "Recuerda que este metodo de cifrado es muy antiguo.\n\n" + flag)
open(os.path.join(HERE, "mensaje.txt"), "w").write(cesar(texto, SHIFT) + "\n")
assert cesar(cesar(flag, SHIFT), 26 - SHIFT) == flag
print(f"[ok] mensaje.txt generado (shift={SHIFT})")
