#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ssrf_interno :: SSRF. Un "verificador de servicios internos" trae por el servidor
# la URL que le pidas; apuntandolo al metadata interno se filtra la flag.
# SEGURIDAD: el fetcher SOLO permite destinos loopback (no es un proxy abierto a
# internet); el endpoint de metadata solo responde a peticiones loopback, que es lo
# que ocurre cuando el servidor se consulta a si mismo via SSRF.
import os, urllib.request, urllib.parse
from flask import Flask, request, Response

FLAG = os.environ.get("FLAG", "CITT{ssrf_al_metadata_interno}")
app = Flask(__name__)
ALLOWED = {"127.0.0.1", "localhost", "0.0.0.0", "::1"}
LOOPBACK = {"127.0.0.1", "::1"}

CSS = r"""
:root{--bg:#0a0f14;--panel:#111a22;--line:#1f2d39;--txt:#dbe7ef;--mut:#7f95a6;--acc:#19b6c9;--acc2:#6ee7b7}
*{box-sizing:border-box}
body{margin:0;min-height:100vh;font-family:'IBM Plex Sans',system-ui,Segoe UI,sans-serif;color:var(--txt);
background:radial-gradient(900px 500px at 85% -10%,#10323a 0,transparent 60%),var(--bg)}
.top{display:flex;align-items:center;gap:12px;padding:15px 26px;border-bottom:1px solid var(--line)}
.brand{display:flex;align-items:center;gap:10px;font-weight:700}
.brand .m{width:26px;height:26px;border-radius:7px;border:2px solid var(--acc);position:relative}
.brand .m::after{content:"";position:absolute;inset:5px;border-radius:3px;background:var(--acc2)}
.top nav{margin-left:auto;display:flex;gap:20px;color:var(--mut);font-size:14px}
.wrap{max-width:760px;margin:0 auto;padding:40px 20px}
.kick{color:var(--acc2);font-size:12px;letter-spacing:2px;text-transform:uppercase;font-weight:700}
h1{margin:6px 0 6px;font-size:26px}.sub{color:var(--mut);margin:0 0 24px}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:24px}
label{display:block;color:var(--mut);font-size:13px;margin:0 0 8px}
.rowf{display:flex;gap:10px}
input{flex:1;padding:12px 14px;border-radius:10px;border:1px solid var(--line);background:#0b141b;color:var(--txt);font-size:14px}
button{padding:12px 18px;border:0;border-radius:10px;font-weight:700;color:#06141a;cursor:pointer;
background:linear-gradient(135deg,var(--acc),var(--acc2))}
.note{color:var(--mut);font-size:13px;margin-top:14px;line-height:1.6}
.note code{background:#0b141b;border:1px solid var(--line);padding:2px 7px;border-radius:6px;color:var(--acc)}
pre{margin-top:20px;background:#0b141b;border:1px solid var(--line);border-radius:10px;padding:16px;
font-family:ui-monospace,Consolas,monospace;font-size:13px;line-height:1.55;white-space:pre-wrap;word-break:break-word;color:#cfe3ef}
.foot{color:var(--mut);font-size:12px;text-align:center;padding:22px}
"""

def page(body):
    return f"""<!doctype html><html lang=es><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1"><title>InfraCloud · Healthcheck</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600;700&display=swap" rel=stylesheet>
<style>{CSS}</style></head><body>
<header class=top><div class=brand><span class=m></span>Infra<span style="color:#19b6c9">Cloud</span></div>
<nav><span>Consola</span><span>Servicios</span><span>Docs</span></nav></header>
<main class=wrap>{body}</main>
<footer class=foot>InfraCloud · panel de operaciones — verificador de servicios internos</footer>
</body></html>"""

def home(result=""):
    return page(f"""<div class=kick>Operaciones</div>
<h1>Healthcheck de servicios internos</h1>
<p class=sub>Verifica el estado de un servicio de la red interna indicando su URL.</p>
<div class=panel>
  <form method=get action="/fetch">
    <label for=url>URL del servicio interno</label>
    <div class=rowf>
      <input id=url name=url placeholder="http://127.0.0.1:5000/" value="">
      <button>Consultar</button>
    </div>
  </form>
  <div class=note>Por política de seguridad este verificador <b>solo alcanza servicios internos</b>
  (loopback). Servicio base: <code>http://127.0.0.1:5000/</code>. La metadata de la instancia
  queda en un endpoint interno bajo <code>/internal/…</code>.</div>
  {result}
</div>""")

@app.route("/")
def index():
    return home()

@app.route("/fetch")
def fetch():
    url = request.args.get("url", "")
    if not url:
        return home()
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return home("<pre>error: esquema no soportado (usa http://)</pre>")
    host = (parsed.hostname or "").lower()
    if host not in ALLOWED:
        return home("<pre>destino no permitido: este verificador solo consulta servicios internos (loopback)</pre>")
    try:
        with urllib.request.urlopen(url, timeout=3) as r:
            body = r.read(8192).decode("utf-8", "replace")
        out = f"<pre>HTTP {r.status} desde {host}\n\n{body}</pre>"
    except Exception as e:
        out = f"<pre>error al consultar: {e}</pre>"
    return home(out)

@app.route("/internal/metadata")
def metadata():
    # solo responde a peticiones loopback (red interna). Alcanzable via SSRF cuando
    # el propio servidor hace la consulta a 127.0.0.1.
    if request.remote_addr in LOOPBACK:
        txt = ("# metadata de la instancia (uso interno)\n"
               "service = infracloud-node\n"
               "region  = cv-south-1\n"
               f"flag    = {FLAG}\n")
        return Response(txt, mimetype="text/plain")
    return Response("403 forbidden: metadata solo accesible desde la red interna\n",
                    status=403, mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
