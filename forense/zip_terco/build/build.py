#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PNG con un ZIP (protegido) anexado al final. La contraseña del ZIP va en un
chunk tEXt del PNG (comentario). Salida: portada.png
binwalk portada.png revela el ZIP; la pass está en los metadatos del PNG."""
import os, subprocess, tempfile, shutil
from PIL import Image
from PIL.PngImagePlugin import PngInfo
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "entrega"); os.makedirs(OUT, exist_ok=True)
flag = open(os.path.join(OUT, "..", "flag.txt")).read().strip()
ZIP_PASS = "c1tt_v6"

# 1) PNG base con la pass escondida en metadatos tEXt
img = Image.new("RGB", (480, 300), (10, 110, 120))
meta = PngInfo()
meta.add_text("Comment", f"backup interno. pass del adjunto: {ZIP_PASS}")
png_tmp = os.path.join(OUT, "_base.png")
img.save(png_tmp, pnginfo=meta)

# 2) ZIP protegido con flag.txt
work = tempfile.mkdtemp()
with open(os.path.join(work, "flag.txt"), "w") as f:
    f.write(flag + "\n")
zip_tmp = os.path.join(OUT, "_secret.zip")
if os.path.exists(zip_tmp): os.remove(zip_tmp)
subprocess.run(["zip", "-j", "-P", ZIP_PASS, zip_tmp, os.path.join(work, "flag.txt")],
               check=True, stdout=subprocess.DEVNULL)

# 3) concatenar PNG + ZIP
out = os.path.join(OUT, "portada.png")
with open(out, "wb") as o:
    o.write(open(png_tmp, "rb").read())
    o.write(open(zip_tmp, "rb").read())

os.remove(png_tmp); os.remove(zip_tmp); shutil.rmtree(work)
print(f"[ok] portada.png generado (ZIP anexado, pass '{ZIP_PASS}' en tEXt Comment)")
