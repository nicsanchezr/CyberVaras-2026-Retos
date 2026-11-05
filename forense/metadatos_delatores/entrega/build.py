#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Crea foto.jpg con la flag en EXIF (UserComment + Artist). Requiere Pillow + piexif."""
import os, piexif
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
flag = open(os.path.join(HERE, "..", "flag.txt")).read().strip()

img = Image.new("RGB", (640, 400), (32, 74, 120))
d = ImageDraw.Draw(img)
d.text((40, 180), "CyberVaras 2026 :: nada que ver aqui", fill=(230, 236, 242))
path = os.path.join(HERE, "foto.jpg")
img.save(path, "JPEG", quality=85)

exif = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
exif["0th"][piexif.ImageIFD.Artist] = "org_cybervaras".encode()
exif["0th"][piexif.ImageIFD.Software] = "CyberVarasCam v6".encode()
exif["Exif"][piexif.ExifIFD.UserComment] = b"\x41\x53\x43\x49\x49\x00\x00\x00" + flag.encode()
piexif.insert(piexif.dump(exif), path)
print("[ok] foto.jpg generado (flag en EXIF UserComment)")
