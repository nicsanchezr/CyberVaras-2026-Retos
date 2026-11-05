#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Incrusta la flag en el LSB del canal rojo de un PNG. Salida: secreto.png
Compatible con zsteg (lee LSB, canal r, orden b, xy)."""
import os
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
flag = open(os.path.join(HERE, "..", "flag.txt")).read().strip()
payload = (flag + "\x00").encode()            # terminador nulo
bits = "".join(f"{b:08b}" for b in payload)

W, H = 200, 120
img = Image.new("RGB", (W, H))
px = img.load()
import random; random.seed(7)
for y in range(H):
    for x in range(W):
        px[x, y] = (random.randint(0,255), random.randint(0,255), random.randint(0,255))

i = 0
for y in range(H):
    for x in range(W):
        if i < len(bits):
            r, g, b = px[x, y]
            r = (r & ~1) | int(bits[i])
            px[x, y] = (r, g, b)
            i += 1
img.save(os.path.join(HERE, "secreto.png"))

# verificación: releer LSB
img2 = Image.open(os.path.join(HERE, "secreto.png")); p2 = img2.load()
out = []
for y in range(H):
    for x in range(W):
        out.append(str(p2[x, y][0] & 1))
bitstr = "".join(out)
rec = bytes(int(bitstr[k:k+8], 2) for k in range(0, len(payload)*8, 8))
assert rec.split(b"\x00")[0].decode() == flag
print("[ok] secreto.png generado (LSB canal R) y verificado")
