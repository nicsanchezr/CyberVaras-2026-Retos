#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# galleta_falsa :: cookie de sesion casera (base64 JSON SIN firmar) manipulable.
# El rediseño toca SOLO la presentacion. Se mantienen: nombre de cookie 'sesion',
# formato base64(JSON) SIN firma (la vulnerabilidad), rutas / y /admin, y la
# condicion role == 'admin' para entregar la flag.
import os, json, base64
from flask import Flask, request, make_response

FLAG = os.environ.get("FLAG", "CITT{cookies_no_son_para_confiar}")
app = Flask(__name__)

def set_session(resp, data):
    raw = base64.b64encode(json.dumps(data).encode()).decode()
    resp.set_cookie("sesion", raw)

def get_session():
    raw = request.cookies.get("sesion")
    if not raw:
        return None
    try:
        return json.loads(base64.b64decode(raw).decode())  # VULNERABLE: sin verificar firma
    except Exception:
        return None

CSS = r"""
:root{--bg:#fff7ed;--ink:#3b2412;--mut:#8a6b52;--acc:#e8590c;--acc2:#f08c00;--card:#fff;--line:#f1e0cf}
*{box-sizing:border-box}
body{margin:0;min-height:100vh;font-family:'Nunito',system-ui,Segoe UI,sans-serif;color:var(--ink);
background:radial-gradient(800px 400px at 90% -5%,#ffe8cc 0,transparent 60%),var(--bg)}
.nav{display:flex;align-items:center;gap:12px;padding:16px 26px}
.brand{display:flex;align-items:center;gap:10px;font-weight:900;font-size:20px}
.brand .c{width:30px;height:30px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#ffd8a8,#e8590c);
position:relative}
.brand .c::after{content:"";position:absolute;inset:0;border-radius:50%;
box-shadow:7px 6px 0 -4px #7a3b0e,-6px 9px 0 -4px #7a3b0e,9px -5px 0 -5px #7a3b0e inset}
.nav .sp{margin-left:auto;display:flex;gap:10px;align-items:center;color:var(--mut);font-weight:700;font-size:14px}
.badge{background:#fff;border:1px solid var(--line);border-radius:999px;padding:7px 13px}
.wrap{max-width:720px;margin:0 auto;padding:40px 18px}
.hero{background:linear-gradient(135deg,var(--acc),var(--acc2));color:#fff;border-radius:20px;padding:34px 30px;
box-shadow:0 24px 50px rgba(232,89,12,.25)}
.hero h1{margin:0 0 8px;font-size:28px}
.hero p{margin:0;opacity:.95}
.card{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:26px;margin-top:22px}
.card h2{margin:0 0 6px;font-size:18px}
.mut{color:var(--mut)}
.btn{display:inline-block;margin-top:16px;text-decoration:none;font-weight:800;color:#fff;
background:var(--ink);padding:12px 20px;border-radius:12px}
.flag{margin-top:14px;font-family:ui-monospace,Consolas,monospace;background:#fff4e6;border:1px dashed var(--acc);
color:var(--acc);padding:14px;border-radius:12px;text-align:center;word-break:break-all;font-weight:700}
.deny{background:#fff;border:1px solid var(--line);border-left:4px solid var(--acc);border-radius:14px;padding:24px;margin-top:22px}
.foot{color:var(--mut);text-align:center;font-size:13px;padding:24px}
"""

def page(body, title="Galletta"):
    return f"""<!doctype html><html lang=es><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1"><title>{title}</title>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;900&display=swap" rel=stylesheet>
<style>{CSS}</style></head><body>
<div class=nav><div class=brand><span class=c></span>Galletta</div>
<div class=sp><span class=badge>🍪 Mis puntos</span></div></div>
<main class=wrap>{body}</main>
<div class=foot>Galletta · tu app de recompensas — endúlzate el día</div>
</body></html>"""

@app.route("/")
def index():
    s = get_session()
    if not s:
        resp = make_response(page(
            """<div class=hero><h1>¡Bienvenido a Galletta!</h1>
            <p>Acumula puntos, canjea premios y lleva el control de tu cuenta.</p></div>
            <div class=card><h2>Tu sesión</h2>
            <p class=mut>Te asignamos una sesión de <b>invitado</b> para que explores la app.</p>
            <a class=btn href="/admin">Ir al panel de administración →</a></div>"""))
        set_session(resp, {"user": "invitado", "role": "user"})
        return resp
    body = f"""<div class=hero><h1>Hola, {s.get('user')}</h1>
    <p>Rol actual: <b>{s.get('role')}</b>. ¡Sigue sumando puntos!</p></div>
    <div class=card><h2>Tu sesión</h2>
    <p class=mut>Gestiona tu cuenta y revisa tus recompensas.</p>
    <a class=btn href="/admin">Ir al panel de administración →</a></div>"""
    return page(body)

@app.route("/admin")
def admin():
    s = get_session() or {}
    if s.get("role") == "admin":
        body = ("<div class=card><h2>Panel de administración</h2>"
                "<p class=mut>Acceso concedido. Bienvenido, administrador.</p>"
                f"<div class=flag>Flag: {FLAG}</div></div>")
        return page(body, title="Galletta · Admin")
    body = ("<div class=deny><h2 style='margin:0 0 6px'>403 — Acceso denegado</h2>"
            "<p class=mut>Esta sección es solo para administradores.</p></div>")
    return page(body, title="Galletta · 403"), 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
