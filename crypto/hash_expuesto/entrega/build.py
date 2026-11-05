#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hashea las palabras débiles que, unidas con '_', forman el interior de la flag.
Salida: hashes.txt (un hash MD5 por línea, en orden)."""
import os, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
flag = open(os.path.join(HERE, "..", "flag.txt")).read().strip()
inner = flag[len("CITT{"):-1]          # rockyou_lo_tenia
words = inner.split("_")               # ['rockyou','lo','tenia']  (todas en rockyou)
lines = [hashlib.md5(w.encode()).hexdigest() for w in words]
open(os.path.join(HERE, "hashes.txt"), "w").write("\n".join(lines) + "\n")
print("[ok] hashes.txt generado")
print("    palabras:", words)
print("    la flag se arma como CITT{" + "_".join(words) + "}")
