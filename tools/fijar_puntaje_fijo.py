#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fijar_puntaje_fijo.py — Plan B de scoring.
Normaliza TODOS los challenge.yml del repo a puntaje FIJO: deja
extra.minimum == extra.initial (decay queda inerte). Idempotente.

Uso:  python3 tools/fijar_puntaje_fijo.py
"""
import os, glob, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATS = ["warmup", "web", "crypto", "forense", "redes", "osint", "reversing"]

def fijar(path):
    lines = open(path, encoding="utf-8").read().split("\n")
    initial = None
    for ln in lines:
        m = re.match(r'^\s*initial:\s*(\d+)', ln)
        if m:
            initial = int(m.group(1)); break
    if initial is None:
        return False, "sin initial"
    out, changed = [], False
    for ln in lines:
        m = re.match(r'^(\s*minimum:\s*)(\d+)(.*)$', ln)
        if m:
            nuevo = f"{m.group(1)}{initial}        # == initial -> puntaje fijo"
            if ln != nuevo:
                changed = True
            out.append(nuevo)
        else:
            out.append(ln)
    open(path, "w", encoding="utf-8").write("\n".join(out))
    return changed, f"minimum={initial}"

def main():
    total = cambiados = 0
    for cat in CATS:
        for p in sorted(glob.glob(os.path.join(ROOT, cat, "*", "challenge.yml"))):
            total += 1
            ch, info = fijar(p)
            cambiados += 1 if ch else 0
            slug = os.path.basename(os.path.dirname(p))
            print(f"  {'FIX ' if ch else 'ok  '}{cat}/{slug:20s} {info}")
    print(f"[ok] {total} challenge.yml revisados · {cambiados} ajustados")

if __name__ == "__main__":
    main()
