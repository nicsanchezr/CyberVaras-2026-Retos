#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# metodos_http :: control de acceso por metodo HTTP. El endpoint de exportacion
# deshabilito GET pero sigue respondiendo a otro metodo, que entrega la flag.
import os
from flask import Flask, request, Response

FLAG = os.environ.get("FLAG", "CITT{metodo_http_olvidado}")
app = Flask(__name__)

CSS = r"""
:root{--bg:#f3f4f1;--ink:#1c2321;--mut:#5f6b66;--acc:#2f6f4f;--acc2:#b5530f;--card:#fff;--line:#e0e3dc}
*{box-sizing:border-box}
body{margin:0;font-family:'Space Mono',ui-monospace,Consolas,monospace;color:var(--ink);background:var(--bg)}
.top{background:var(--ink);color:#eef1ec}
.bar{max-width:820px;margin:0 auto;display:flex;align-items:center;gap:12px;padding:14px 22px}
.brand{font-weight:700;display:flex;align-items:center;gap:10px}
.brand .m{width:12px;height:12px;background:var(--acc);box-shadow:16px 0 0 var(--acc2)}
.bar nav{margin-left:auto;display:flex;gap:18px;color:#aab6ae;font-size:13px}
.wrap{max-width:820px;margin:0 auto;padding:40px 22px}
.tag{color:var(--acc2);text-transform:uppercase;letter-spacing:2px;font-size:12px}
h1{margin:6px 0 6px;font-size:25px}.sub{color:var(--mut);margin:0 0 22px;line-height:1.6}
.card{background:var(--card);border:1px solid var(--line);border-radius:6px;padding:24px;box-shadow:4px 4px 0 rgba(28,35,33,.08)}
.card h3{margin:0 0 10px;color:var(--acc)}
.card p{color:var(--mut);line-height:1.7;font-size:14px}
.method{display:inline-block;font-weight:700;padding:2px 9px;border-radius:5px;font-size:12px}
.m-off{background:#fde8e8;color:#b02a2a;text-decoration:line-through}
code{background:#f0f2ee;border:1px solid var(--line);padding:2px 7px;border-radius:5px;color:var(--acc2)}
pre{background:#1c2321;color:#e7ece8;border-radius:6px;padding:14px;overflow:auto;font-size:13px}
.foot{color:var(--mut);font-size:13px;text-align:center;padding:22px}
"""

def page(body):
    return f"""<!doctype html><html lang=es><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1"><title>LegacyDB · Consola</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&display=swap" rel=stylesheet>
<style>{CSS}</style></head><body>
<header class=top><div class=bar><div class=brand><span class=m></span>LegacyDB</div>
<nav><span>Consola</span><span>Tablas</span><span>Jobs</span></nav></div></header>
<main class=wrap>{body}</main>
<footer class=foot>LegacyDB · consola de administración heredada — v1.4 (2019)</footer>
</body></html>"""

@app.route("/")
def index():
    return page("""<div class=tag>Mantenimiento</div>
<h1>Exportación de registros</h1>
<p class=sub>La consola heredada permite exportar la tabla de registros.</p>
<div class=card>
  <h3>GET /export</h3>
  <p>Por un incidente de seguridad, el método <span class="method m-off">GET</span> de este
  endpoint fue <b>deshabilitado</b>. La exportación se migró a otro método, pero nadie
  actualizó la documentación...</p>
  <p>Pista: revisa qué métodos acepta realmente el endpoint.</p>
  <pre>curl -i https://methods.retos.cybervaras.xyz/export</pre>
</div>""")

@app.route("/export", methods=["GET", "POST"])
def export():
    # VULNERABLE: GET quedo "deshabilitado" pero POST sigue entregando los datos.
    if request.method == "GET":
        r = Response("405 Method Not Allowed: GET fue deshabilitado para /export\n",
                     status=405, mimetype="text/plain")
        r.headers["Allow"] = "POST"        # el metodo "olvidado" queda a la vista
        return r
    txt = ("# export de registros (LegacyDB)\n"
           "rows = 4211\n"
           f"flag = {FLAG}\n")
    return Response(txt, mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
