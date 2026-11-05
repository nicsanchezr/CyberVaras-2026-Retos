#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# cambia_el_id :: IDOR. El perfil se consulta por ?id= sin verificar propiedad.
# El rediseño toca SOLO la presentacion. Se mantienen: ruta /profile, parametro
# ?id=, el diccionario USERS (id 1 = admin con la flag en su nota) y la ausencia
# de control de autorizacion (la vulnerabilidad).
import os
from flask import Flask, request
from markupsafe import escape

FLAG = os.environ.get("FLAG", "CITT{idor_acceso_horizontal}")
app = Flask(__name__)

USERS = {
    1:    {"user": "admin",    "nombre": "Administrador", "nota": f"FLAG: {FLAG}"},
    1001: {"user": "ana",      "nombre": "Ana Rivas",     "nota": "preferencias: modo oscuro"},
    1002: {"user": "invitado", "nombre": "Cuenta Demo",   "nota": "cuenta de prueba del CTF"},
}

CSS = r"""
:root{--bg:#0f1021;--panel:#191a33;--line:#2b2d52;--txt:#ececff;--mut:#9a9cc9;--acc:#7c5cff;--acc2:#20d3c2}
*{box-sizing:border-box}
body{margin:0;min-height:100vh;font-family:'Sora',system-ui,Segoe UI,sans-serif;color:var(--txt);
background:radial-gradient(900px 500px at 15% -10%,#2a1f63 0,transparent 55%),var(--bg)}
.nav{display:flex;align-items:center;gap:12px;padding:16px 26px;border-bottom:1px solid var(--line)}
.brand{font-weight:800;display:flex;align-items:center;gap:9px}
.brand .m{width:26px;height:26px;border-radius:50%;background:conic-gradient(from 90deg,var(--acc),var(--acc2),var(--acc));}
.pill{margin-left:auto;font-size:13px;color:var(--mut);border:1px solid var(--line);padding:7px 12px;border-radius:999px}
.wrap{max-width:760px;margin:0 auto;padding:40px 18px}
.hi{font-size:14px;color:var(--mut)}
h1{margin:4px 0 24px;font-size:26px}
.profile{background:var(--panel);border:1px solid var(--line);border-radius:16px;overflow:hidden}
.phead{display:flex;align-items:center;gap:16px;padding:24px;border-bottom:1px solid var(--line);
background:linear-gradient(180deg,rgba(124,92,255,.12),transparent)}
.avatar{width:58px;height:58px;border-radius:14px;background:linear-gradient(135deg,var(--acc),var(--acc2));
display:grid;place-items:center;font-weight:900;font-size:22px;color:#0c0c1e}
.pid{color:var(--mut);font-size:13px}
.rows{padding:10px 24px 22px}
.row{display:flex;justify-content:space-between;gap:16px;padding:14px 0;border-bottom:1px dashed var(--line)}
.row:last-child{border-bottom:0}
.row .k{color:var(--mut);font-size:14px}
.row .v{font-weight:600;text-align:right;word-break:break-word}
.btn{display:inline-block;margin-top:24px;text-decoration:none;color:#0c0c1e;font-weight:700;
background:linear-gradient(135deg,var(--acc),var(--acc2));padding:11px 18px;border-radius:10px}
.link{color:var(--acc2);text-decoration:none}
.card{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:26px}
.foot{color:var(--mut);font-size:12px;text-align:center;padding:26px}
"""

def page(body):
    return f"""<!doctype html><html lang=es><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1"><title>Mi Portal</title>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;800&display=swap" rel=stylesheet>
<style>{CSS}</style></head><body>
<div class=nav><div class=brand><span class=m></span>Mi<span style="color:#20d3c2">Portal</span></div>
<div class=pill>sesión: invitado</div></div>
<main class=wrap>{body}</main>
<div class=foot>Mi Portal · panel de cuenta — los datos mostrados pertenecen a tu sesión</div>
</body></html>"""

@app.route("/")
def index():
    body = """<div class=hi>Bienvenido de vuelta</div>
<h1>Tu cuenta</h1>
<div class=card>
  <p>Has iniciado sesión como <b>invitado</b> (id 1002).</p>
  <p style="color:#9a9cc9">Desde aquí puedes revisar la información de tu perfil.</p>
  <a class=btn href="/profile?id=1002">Ver mi perfil →</a>
</div>"""
    return page(body)

@app.route("/profile")
def profile():
    try:
        pid = int(request.args.get("id", "1002"))
    except ValueError:
        return "id invalido", 400
    u = USERS.get(pid)
    if not u:
        return "perfil no encontrado", 404
    # VULNERABLE: no se comprueba que el id pertenezca al usuario en sesion
    inicial = escape(u["user"][:1].upper())
    body = f"""<div class=hi>Perfil</div>
<h1>Detalle de cuenta</h1>
<div class=profile>
  <div class=phead>
    <div class=avatar>{inicial}</div>
    <div><div style="font-weight:700;font-size:18px">{escape(u['nombre'])}</div>
    <div class=pid>id #{pid} · @{escape(u['user'])}</div></div>
  </div>
  <div class=rows>
    <div class=row><span class=k>Usuario</span><span class=v>{escape(u['user'])}</span></div>
    <div class=row><span class=k>Nombre</span><span class=v>{escape(u['nombre'])}</span></div>
    <div class=row><span class=k>Nota</span><span class=v>{escape(u['nota'])}</span></div>
  </div>
</div>
<a class=link href="/">← volver al inicio</a>"""
    return page(body)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
