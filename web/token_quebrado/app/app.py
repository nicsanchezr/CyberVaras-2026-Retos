#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# token_quebrado :: JWT mal verificado. Acepta alg=none Y secreto debil 'secret'.
# El rediseño toca SOLO la presentacion de / (portada de la API). La verificacion
# vulnerable (make_jwt/verify_jwt), el secreto debil, la ruta /admin, el header
# Authorization: Bearer / ?token= y el JSON de respuesta se mantienen identicos.
import os, json, base64, hmac, hashlib
from flask import Flask, request

FLAG = os.environ.get("FLAG", "CITT{jwt_alg_none_es_peligroso}")
SECRET = b"secret"            # secreto debil (crackeable por diccionario)
app = Flask(__name__)

def b64u(b):  return base64.urlsafe_b64encode(b).rstrip(b"=").decode()
def b64ud(s): return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))

def make_jwt(payload, alg="HS256"):
    h = {"alg": alg, "typ": "JWT"}
    seg = b64u(json.dumps(h).encode()) + "." + b64u(json.dumps(payload).encode())
    if alg == "none":
        sig = ""
    else:
        sig = b64u(hmac.new(SECRET, seg.encode(), hashlib.sha256).digest())
    return seg + "." + sig

def verify_jwt(tok):
    try:
        hs, ps, sig = tok.split(".")
        header = json.loads(b64ud(hs))
        payload = json.loads(b64ud(ps))
    except Exception:
        return None
    alg = header.get("alg", "")
    # VULNERABLE: confia en el alg del header
    if alg == "none":
        return payload
    if alg == "HS256":
        want = b64u(hmac.new(SECRET, f"{hs}.{ps}".encode(), hashlib.sha256).digest())
        if hmac.compare_digest(want, sig):
            return payload
    return None

CSS = r"""
:root{--bg:#0d1117;--panel:#161b22;--line:#273040;--txt:#e6edf3;--mut:#8b98a9;--acc:#58a6ff;--acc2:#3fb950;--code:#0b0f16}
*{box-sizing:border-box}
body{margin:0;min-height:100vh;font-family:'Space Grotesk',system-ui,Segoe UI,sans-serif;color:var(--txt);background:var(--bg)}
.top{display:flex;align-items:center;gap:12px;padding:14px 24px;border-bottom:1px solid var(--line);position:sticky;top:0;background:rgba(13,17,23,.85);backdrop-filter:blur(6px)}
.brand{display:flex;align-items:center;gap:10px;font-weight:700}
.brand .o{width:24px;height:24px;border-radius:50%;border:3px solid var(--acc);position:relative}
.brand .o::after{content:"";position:absolute;width:7px;height:7px;background:var(--acc2);border-radius:50%;top:-5px;left:7px}
.top nav{margin-left:auto;display:flex;gap:20px;color:var(--mut);font-size:14px}
.layout{max-width:980px;margin:0 auto;display:grid;grid-template-columns:200px 1fr;gap:30px;padding:34px 22px}
.side{color:var(--mut);font-size:14px;border-right:1px solid var(--line);padding-right:10px}
.side h4{color:var(--txt);font-size:12px;text-transform:uppercase;letter-spacing:1px;margin:0 0 10px}
.side a{display:block;color:var(--mut);text-decoration:none;padding:6px 0}
.side a.on{color:var(--acc)}
h1{margin:0 0 6px;font-size:26px}
.sub{color:var(--mut);margin:0 0 24px}
h2{font-size:18px;margin:26px 0 10px;border-bottom:1px solid var(--line);padding-bottom:8px}
p{line-height:1.6;color:#c9d4e0}
code.inline{background:var(--code);border:1px solid var(--line);padding:2px 7px;border-radius:6px;font-family:ui-monospace,Consolas,monospace;color:var(--acc)}
pre{background:var(--code);border:1px solid var(--line);border-radius:10px;padding:16px;overflow:auto;
font-family:ui-monospace,Consolas,monospace;font-size:13px;line-height:1.55;color:#d7e2ef;word-break:break-all;white-space:pre-wrap}
.pill{display:inline-block;background:rgba(63,185,80,.14);color:var(--acc2);border:1px solid rgba(63,185,80,.35);
font-size:12px;font-weight:700;padding:3px 9px;border-radius:999px;margin-right:8px}
.get{background:rgba(88,166,255,.14);color:var(--acc);border-color:rgba(88,166,255,.35)}
@media(max-width:760px){.layout{grid-template-columns:1fr}.side{border-right:0;border-bottom:1px solid var(--line);padding-bottom:10px}}
"""

@app.route("/")
def index():
    tok = make_jwt({"user": "invitado", "role": "user"})
    body = f"""<!doctype html><html lang=es><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1"><title>OrbitAPI · Docs</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&display=swap" rel=stylesheet>
<style>{CSS}</style></head><body>
<header class=top><div class=brand><span class=o></span>Orbit<span style="color:#58a6ff">API</span></div>
<nav><span>Docs</span><span>Referencia</span><span>Estado</span></nav></header>
<div class=layout>
  <aside class=side><h4>Guía</h4>
    <a href="#">Introducción</a><a class=on href="#quick">Quickstart</a>
    <a href="#auth">Autenticación</a><a href="#admin">Endpoint /admin</a>
  </aside>
  <main>
    <h1>OrbitAPI — Documentación</h1>
    <p class=sub>API REST para gestionar tus recursos en la nube Orbit.</p>

    <h2 id=quick>Quickstart</h2>
    <p>Al entrar te emitimos un <b>token de invitado</b> (JWT). Úsalo para llamar a los
    endpoints protegidos:</p>
    <pre>{tok}</pre>

    <h2 id=auth>Autenticación</h2>
    <p>Envía el token en la cabecera <code class=inline>Authorization: Bearer &lt;token&gt;</code>.
    El servidor valida el JWT y resuelve tu rol a partir del payload.</p>

    <h2 id=admin>Endpoint</h2>
    <p><span class="pill get">GET</span><code class=inline>/admin</code> — requiere un token con rol
    de administrador. Con tu token de invitado responde <code class=inline>403</code>.</p>
    <pre>curl -H "Authorization: Bearer &lt;token&gt;" https://jwt.retos.cybervaras.xyz/admin</pre>
  </main>
</div></body></html>"""
    return body

@app.route("/admin")
def admin():
    auth = request.headers.get("Authorization", "")
    tok = auth[7:] if auth.startswith("Bearer ") else request.args.get("token", "")
    payload = verify_jwt(tok)
    if payload and payload.get("role") == "admin":
        return {"ok": True, "flag": FLAG}
    return {"ok": False, "error": "token invalido o sin privilegios"}, 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
