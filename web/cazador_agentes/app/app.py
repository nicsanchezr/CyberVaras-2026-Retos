#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# cazador_agentes :: control de acceso por User-Agent. El feed solo se entrega al
# "cliente oficial"; basta con enviar ese User-Agent para obtener la flag.
import os
from flask import Flask, request, Response

FLAG = os.environ.get("FLAG", "CITT{el_user_agent_te_delata}")
OFFICIAL_UA = "SentinelCLI/2.0"
app = Flask(__name__)

CSS = r"""
:root{--bg:#0b0d12;--panel:#14181f;--line:#242a35;--txt:#e9edf3;--mut:#8b94a3;--acc:#ffb020;--acc2:#ff5d5d}
*{box-sizing:border-box}
body{margin:0;min-height:100vh;font-family:'JetBrains Mono',ui-monospace,Consolas,monospace;color:var(--txt);
background:radial-gradient(800px 400px at 80% -10%,#2a1c06 0,transparent 60%),var(--bg)}
.top{display:flex;align-items:center;gap:12px;padding:15px 24px;border-bottom:1px solid var(--line)}
.brand{font-weight:700;display:flex;align-items:center;gap:10px}
.brand .m{width:24px;height:24px;border-radius:6px;background:linear-gradient(135deg,var(--acc),var(--acc2))}
.top nav{margin-left:auto;display:flex;gap:18px;color:var(--mut);font-size:13px}
.wrap{max-width:720px;margin:0 auto;padding:44px 20px}
.kick{color:var(--acc);font-size:12px;letter-spacing:2px;text-transform:uppercase}
h1{margin:8px 0 8px;font-size:26px;font-family:'Space Grotesk',system-ui,sans-serif}
.sub{color:var(--mut);margin:0 0 24px;line-height:1.6}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:24px}
.panel h3{margin:0 0 10px;font-size:15px;color:var(--acc)}
.panel p{color:var(--mut);line-height:1.7;font-size:14px}
code{background:#0b0d12;border:1px solid var(--line);padding:2px 7px;border-radius:6px;color:var(--acc)}
pre{background:#0b0d12;border:1px solid var(--line);border-radius:10px;padding:14px;overflow:auto;font-size:13px;color:#d7e0ea}
.foot{color:var(--mut);font-size:12px;text-align:center;padding:22px}
"""

LANDING = f"""<!doctype html><html lang=es><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1"><title>Sentinel Feed</title>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Space+Grotesk:wght@500;700&display=swap" rel=stylesheet>
<style>{CSS}</style></head><body>
<header class=top><div class=brand><span class=m></span>Sentinel<span style="color:#ffb020">Feed</span></div>
<nav><span>Producto</span><span>API</span><span>Precios</span></nav></header>
<main class=wrap>
  <div class=kick>Threat intel feed</div>
  <h1>Datos solo para clientes autenticados</h1>
  <p class=sub>El feed de indicadores se entrega exclusivamente a través de nuestro
  cliente oficial. Las peticiones de navegadores u otros agentes son rechazadas.</p>
  <div class=panel>
    <h3>Acceso al feed</h3>
    <p>Endpoint: <code>GET /feed</code></p>
    <p>Requiere el cliente oficial <b>SentinelCLI</b>, que se identifica con el
    User-Agent <code>{OFFICIAL_UA}</code>. Ejemplo:</p>
    <pre>curl -A "{OFFICIAL_UA}" https://ua.retos.cybervaras.xyz/feed</pre>
  </div>
</main>
<footer class=foot>Sentinel Feed · inteligencia de amenazas — acceso restringido a clientes</footer>
</body></html>"""

@app.route("/")
def index():
    return LANDING

@app.route("/feed")
def feed():
    ua = request.headers.get("User-Agent", "")
    # VULNERABLE: "autenticacion" basada solo en el User-Agent
    if OFFICIAL_UA in ua:
        txt = ("# sentinel feed v2 - OK\n"
               "indicators = 128\n"
               "updated = 2026-10-23\n"
               f"flag = {FLAG}\n")
        return Response(txt, mimetype="text/plain")
    return Response("403 cliente no reconocido: usa el cliente oficial SentinelCLI\n",
                    status=403, mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
