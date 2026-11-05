#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Crea usb.img: imagen de ~4 MB con un archivo 'borrado' recuperable.
Se incrusta un JPEG valido (con la flag en EXIF) para que foremost/photorec lo
carven por firma, y una copia en texto para que `strings usb.img | grep CITT`
tambien funcione. No requiere montar ni mkfs."""
import os, io, piexif
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "entrega"); os.makedirs(OUT, exist_ok=True)
flag = open(os.path.join(OUT, "..", "flag.txt")).read().strip()

# JPEG con la flag en EXIF
img = Image.new("RGB", (480, 300), (40, 40, 60))
ImageDraw.Draw(img).text((30, 140), "archivo recuperado", fill=(220,220,220))
buf = io.BytesIO(); img.save(buf, "JPEG", quality=80)
exif = {"0th": {}, "Exif": {piexif.ExifIFD.UserComment: b"ASCII\x00\x00\x00"+flag.encode()},
        "GPS": {}, "1st": {}, "thumbnail": None}
# piexif.insert requiere archivo de salida: escribir, insertar, releer.
tmp = os.path.join(OUT, "_tmp.jpg"); open(tmp, "wb").write(buf.getvalue())
piexif.insert(piexif.dump(exif), tmp)
jpg = open(tmp, "rb").read(); os.remove(tmp)

SIZE = 4 * 1024 * 1024
data = bytearray(b"\x00" * SIZE)
# relleno pseudo-aleatorio ligero para realismo
import random; random.seed(11)
for i in range(0, SIZE, 4096):
    if random.random() < 0.15:
        chunk = bytes(random.getrandbits(8) for _ in range(64))
        data[i:i+64] = chunk

# "archivo de texto borrado" (recuperable por strings)
note = (b"=== notas.txt (borrado) ===\n"
        b"credencial del laboratorio\n" + flag.encode() + b"\n=== fin ===\n")
off_txt = 512 * 100
data[off_txt:off_txt+len(note)] = note

# JPEG carvable, alineado a sector
off_jpg = 512 * 2000
data[off_jpg:off_jpg+len(jpg)] = jpg

open(os.path.join(OUT, "usb.img"), "wb").write(data)
print(f"[ok] usb.img generado ({SIZE//1024} KB) — JPEG carvable + notas.txt recuperable")
