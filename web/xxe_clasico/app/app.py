#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# xxe_clasico :: XXE. Un importador de facturas XML parsea con resolucion de
# entidades externas activada; con una entidad file:// se lee un archivo local
# (la flag vive en /flag.txt dentro del contenedor).
# SEGURIDAD: el parser usa no_network=True -> no hay SSRF a internet via XXE;
# solo lectura de archivos locales del contenedor (aislado/efimero), como el LFI.
import os
from flask import Flask, request
from markupsafe import escape
from lxml import etree

app = Flask(__name__)

SAMPLE = ('<?xml version="1.0"?>\n'
          '<factura>\n'
          '  <cliente>\n'
          '    <nombre>Empresa Demo SpA</nombre>\n'
          '  </cliente>\n'
          '  <monto>19990</monto>\n'
          '</factura>')

CSS = r"""
:root{--bg:#f5f7fb;--ink:#111a2e;--mut:#5a6b86;--acc:#3b56d6;--acc2:#6b4ef0;--card:#fff;--line:#e4e9f3}
*{box-sizing:border-box}
body{margin:0;font-family:'Inter',system-ui,Segoe UI,sans-serif;color:var(--ink);background:var(--bg)}
.top{background:#fff;border-bottom:1px solid var(--line)}
.bar{max-width:900px;margin:0 auto;display:flex;align-items:center;gap:12px;padding:16px 22px}
.brand{display:flex;align-items:center;gap:10px;font-weight:800;font-size:19px}
.brand .m{width:27px;height:27px;border-radius:8px;background:linear-gradient(135deg,var(--acc),var(--acc2))}
nav{margin-left:auto;display:flex;gap:22px;color:var(--mut);font-weight:600;font-size:14px}
.wrap{max-width:900px;margin:0 auto;padding:40px 22px}
.kick{color:var(--acc);font-weight:700;letter-spacing:2px;text-transform:uppercase;font-size:12px}
h1{margin:6px 0 6px;font-size:26px}.sub{color:var(--mut);margin:0 0 22px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:24px;box-shadow:0 10px 30px rgba(30,40,80,.05)}
label{display:block;color:var(--mut);font-size:13px;margin:0 0 8px;font-weight:600}
textarea{width:100%;min-height:180px;padding:14px;border:1px solid var(--line);border-radius:10px;
font-family:ui-monospace,Consolas,monospace;font-size:13px;line-height:1.5;color:#1a2440;background:#fbfcff;resize:vertical}
button{margin-top:14px;padding:12px 20px;border:0;border-radius:10px;font-weight:700;color:#fff;cursor:pointer;
background:linear-gradient(135deg,var(--acc),var(--acc2))}
.res{margin-top:20px;padding:16px 18px;border-radius:10px;border:1px solid var(--line);background:#f3f6ff}
.res.ok{border-left:4px solid var(--acc)}
.res.err{border-left:4px solid #d64545;background:#fff5f5}
.res pre{margin:6px 0 0;font-family:ui-monospace,Consolas,monospace;white-space:pre-wrap;word-break:break-word;font-size:13px}
.foot{color:var(--mut);font-size:13px;text-align:center;padding:22px}
"""

def page(body):
    return f"""<!doctype html><html lang=es><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1"><title>DocFlow · Importar factura</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel=stylesheet>
<style>{CSS}</style></head><body>
<header class=top><div class=bar>
  <div class=brand><span class=m></span>Doc<span style="color:#3b56d6">Flow</span></div>
  <nav><span>Facturas</span><span>Clientes</span><span>Reportes</span></nav>
</div></header>
<main class=wrap>{body}</main>
<footer class=foot>DocFlow · gestión documental — importación de facturas en formato XML</footer>
</body></html>"""

def form(result=""):
    return page(f"""<div class=kick>Importador</div>
<h1>Importar factura (XML)</h1>
<p class=sub>Pega el XML de la factura y el sistema registrará el cliente.</p>
<div class=card>
  <form method=post action="/import">
    <label for=xml>Documento XML</label>
    <textarea id=xml name=xml spellcheck=false>{escape(SAMPLE)}</textarea>
    <button>Importar factura</button>
  </form>
  {result}
</div>""")

@app.route("/")
def index():
    return form()

@app.route("/import", methods=["POST"])
def do_import():
    data = request.form.get("xml") or request.get_data(as_text=True) or ""
    try:
        # VULNERABLE: resolucion de entidades externas activada (load_dtd + resolve_entities)
        parser = etree.XMLParser(resolve_entities=True, load_dtd=True,
                                 no_network=True, dtd_validation=False)
        root = etree.fromstring(data.encode("utf-8"), parser)
        nombre_el = root.find(".//nombre")
        nombre = nombre_el.text if nombre_el is not None else "(sin nombre)"
        res = (f"<div class='res ok'><b>Factura importada correctamente.</b>"
               f"<pre>cliente registrado: {escape(nombre)}</pre></div>")
    except Exception as e:
        res = f"<div class='res err'><b>Error al procesar el XML</b><pre>{escape(str(e))}</pre></div>"
    return form(res)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
