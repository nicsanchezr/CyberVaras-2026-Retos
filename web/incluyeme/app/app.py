#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# incluyeme :: LFI. ?page= se abre como archivo sin sanitizar (path traversal).
# El rediseño toca SOLO la presentacion (chrome del CMS). Se mantiene IDENTICO el
# mecanismo vulnerable: se arma la ruta VIEWS/<page>.html y, si no existe, se abre
# el valor crudo de ?page= (traversal). El contenido se sigue mostrando tal cual
# (en un visor monoespaciado) para que la salida del traversal sea legible.
import os
from flask import Flask, request

app = Flask(__name__)
VIEWS = os.path.join(os.path.dirname(__file__), "views")

CSS = r"""
:root{--bg:#faf7f2;--ink:#20242b;--mut:#6b7280;--acc:#b5530f;--line:#eadfce;--paper:#fff}
*{box-sizing:border-box}
body{margin:0;font-family:'Fraunces',Georgia,serif;color:var(--ink);background:var(--bg)}
.masthead{border-bottom:2px solid var(--ink);background:var(--paper)}
.mh{max-width:860px;margin:0 auto;padding:22px 20px;display:flex;align-items:baseline;gap:14px}
.title{font-size:30px;font-weight:900;letter-spacing:-.5px}
.title .dot{color:var(--acc)}
.tagline{color:var(--mut);font-style:italic;font-size:15px}
.nav{background:var(--ink)}
.nav .in{max-width:860px;margin:0 auto;padding:10px 20px;display:flex;gap:20px}
.nav a{color:#f3ece0;text-decoration:none;font-family:ui-sans-serif,system-ui,sans-serif;font-size:14px;font-weight:600;letter-spacing:.3px}
.nav a:hover{color:#ffcf99}
.wrap{max-width:860px;margin:0 auto;padding:40px 20px}
.kicker{font-family:ui-sans-serif,system-ui,sans-serif;text-transform:uppercase;letter-spacing:2px;
font-size:12px;color:var(--acc);font-weight:700}
.article{background:var(--paper);border:1px solid var(--line);border-radius:4px;padding:30px;margin-top:10px;
box-shadow:0 10px 30px rgba(50,30,0,.06)}
.viewer{margin:0;font-family:ui-monospace,Consolas,monospace;font-size:14px;line-height:1.6;
white-space:pre-wrap;word-break:break-word;color:#2b2f36}
.meta{color:var(--mut);font-family:ui-sans-serif,system-ui,sans-serif;font-size:13px;margin-top:8px}
.foot{border-top:1px solid var(--line);color:var(--mut);font-size:13px;text-align:center;
padding:22px;font-family:ui-sans-serif,system-ui,sans-serif}
"""

def page(view_name, content_html):
    return f"""<!doctype html><html lang=es><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1"><title>Bitácora · {view_name}</title>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,900&display=swap" rel=stylesheet>
<style>{CSS}</style></head><body>
<header class=masthead><div class=mh>
  <span class=title>Bitácora<span class=dot>.</span></span>
  <span class=tagline>notas de un equipo que construye en público</span>
</div></header>
<nav class=nav><div class=in>
  <a href="/?page=home">Inicio</a><a href="/?page=about">Acerca de</a>
  <a href="/?page=home">Artículos</a><a href="/?page=home">Archivo</a>
</div></nav>
<main class=wrap>
  <div class=kicker>Vista: {view_name}</div>
  <article class=article>{content_html}</article>
  <div class=meta>Bitácora CMS · contenido servido desde la carpeta de vistas</div>
</main>
<footer class=foot>© 2026 Bitácora — hecho con nuestro CMS artesanal</footer>
</body></html>"""

@app.route("/")
def index():
    page_param = request.args.get("page", "home")
    # VULNERABLE: se concatena y se abre sin validar -> traversal
    path = os.path.join(VIEWS, page_param + ".html")
    try:
        with open(path, "r", errors="replace") as f:
            content = f.read()
    except Exception:
        # permite tambien rutas absolutas/traversal crudas si .html no existe
        try:
            with open(request.args.get("page", ""), "r", errors="replace") as f:
                content = f.read()
        except Exception as e:
            return page("error", f"<pre class=viewer>no se pudo cargar la vista: {e}</pre>"), 404
    return page(page_param, f"<pre class=viewer>{content}</pre>")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
