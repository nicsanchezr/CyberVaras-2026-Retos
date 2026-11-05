#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""XOR de un solo byte sobre la flag. Salida: cipher.hex"""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
flag = open(os.path.join(HERE, "..", "flag.txt")).read().strip().encode()
KEY = 0x5A
ct = bytes(b ^ KEY for b in flag)
open(os.path.join(HERE, "cipher.hex"), "w").write(ct.hex() + "\n")
assert bytes(b ^ KEY for b in ct) == flag
print(f"[ok] cipher.hex generado (key=0x{KEY:02x})")
