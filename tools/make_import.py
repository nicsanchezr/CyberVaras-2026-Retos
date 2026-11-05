#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera import/retos_estaticos.csv (importable en CTFd) para los retos NO-whale,
y import/indice_retos.csv con el panorama completo (incluye web).
Parser minimo de challenge.yml (sin dependencias)."""
import os, csv, glob, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "import"); os.makedirs(OUT, exist_ok=True)
CATS = ["warmup", "web", "crypto", "forense", "redes", "osint", "reversing"]

def parse_yaml(path):
    """Parser muy simple para nuestros challenge.yml (plano + description '|' + listas '- ')."""
    d = {"flags": [], "tags": [], "extra": {}}
    lines = open(path, encoding="utf-8").read().split("\n")
    i = 0
    while i < len(lines):
        ln = lines[i]
        m = re.match(r'^(\w+):\s*(.*)$', ln)
        if ln.strip().startswith("description: |"):
            desc = []
            i += 1
            while i < len(lines) and (lines[i].startswith("  ") or lines[i] == ""):
                if lines[i].startswith("  "): desc.append(lines[i][2:])
                elif lines[i] == "": desc.append("")
                i += 1
            d["description"] = "\n".join(desc).strip()
            continue
        if ln.strip() in ("flags:", "tags:"):
            key = ln.strip()[:-1]; i += 1
            while i < len(lines) and lines[i].startswith("  - "):
                d[key].append(lines[i][4:].strip()); i += 1
            continue
        if m:
            k, v = m.group(1), m.group(2).strip().strip('"')
            if k in ("name", "category", "value", "type", "state"):
                d[k] = v
        i += 1
    return d

rows_static, rows_all = [], []
for cat in CATS:
    for ymlp in sorted(glob.glob(os.path.join(ROOT, cat, "*", "challenge.yml"))):
        d = parse_yaml(ymlp)
        slug = os.path.basename(os.path.dirname(ymlp))
        is_whale = d.get("type") == "dynamic_docker"
        flag = d["flags"][0] if d["flags"] else ""
        tag = d["tags"][0] if d["tags"] else ""
        desc1 = d.get("description", "").split("\n")[0]
        rows_all.append([cat, slug, d.get("name"), d.get("category"),
                         d.get("value"), "whale" if is_whale else "static", flag, tag])
        if not is_whale:
            # columnas compatibles con el importador CSV de CTFd (un flag/tag por reto)
            rows_static.append([d.get("name"), d.get("description"), d.get("category"),
                                d.get("value"), "dynamic", "hidden", flag, tag])

with open(os.path.join(OUT, "retos_estaticos.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["name", "description", "category", "value", "type", "state", "flags", "tags"])
    w.writerows(rows_static)

with open(os.path.join(OUT, "indice_retos.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["carpeta", "slug", "nombre", "categoria", "puntaje", "despliegue", "flag", "dificultad"])
    w.writerows(rows_all)

print(f"[ok] import/retos_estaticos.csv ({len(rows_static)} retos estaticos)")
print(f"[ok] import/indice_retos.csv ({len(rows_all)} retos en total)")
