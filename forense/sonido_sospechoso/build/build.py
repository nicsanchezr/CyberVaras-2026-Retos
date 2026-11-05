#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sintetiza senal.wav cuyo ESPECTROGRAMA dibuja el texto de la flag.
Requiere numpy + Pillow. Visible en Audacity/Sonic Visualiser (vista espectral)."""
import os, wave, struct
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "entrega"); os.makedirs(OUT, exist_ok=True)
flag = open(os.path.join(OUT, "..", "flag.txt")).read().strip()

SR = 22050
F_LO, F_HI = 800, 7000          # rango de frecuencias donde se "dibuja"
COL_DUR = 0.035                 # segundos por columna de la imagen

# 1) renderizar el texto a una imagen binaria
try:
    font = ImageFont.truetype("DejaVuSans-Bold.ttf", 28)
except Exception:
    font = ImageFont.load_default()
tmp = Image.new("L", (10, 10))
dd = ImageDraw.Draw(tmp)
bbox = dd.textbbox((0, 0), flag, font=font)
tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
pad = 6
img = Image.new("L", (tw + pad*2, th + pad*2), 0)
ImageDraw.Draw(img).text((pad-bbox[0], pad-bbox[1]), flag, fill=255, font=font)
img = img.transpose(Image.FLIP_TOP_BOTTOM)     # fila 0 abajo = freq baja
arr = np.array(img) > 128
H, W = arr.shape

# 2) por columna, sumar sinusoides en las filas encendidas
col_n = int(COL_DUR * SR)
t = np.arange(col_n) / SR
freqs = np.linspace(F_LO, F_HI, H)
samples = []
for x in range(W):
    rows = np.where(arr[:, x])[0]
    seg = np.zeros(col_n)
    for r in rows:
        seg += np.sin(2*np.pi*freqs[r]*t)
    if len(rows):
        seg /= len(rows)
    # ventana suave para evitar clicks
    seg *= np.hanning(col_n)
    samples.append(seg)
sig = np.concatenate(samples) if samples else np.zeros(col_n)
sig = sig / (np.max(np.abs(sig)) + 1e-9) * 0.8
pcm = (sig * 32767).astype(np.int16)

out = os.path.join(OUT, "senal.wav")
with wave.open(out, "w") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print(f"[ok] senal.wav generado ({len(pcm)/SR:.1f}s) — ver espectrograma")
