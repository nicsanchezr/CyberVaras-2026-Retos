#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# login_injectado :: SQLi de autenticacion. VULNERABLE A PROPOSITO (reto CTF).
# NOTA: el rediseño toca SOLO la presentacion (HTML/CSS). La consulta vulnerable,
# los campos del formulario (user/pass), la ruta (/ POST) y la entrega de flag
# se mantienen identicos.
import os, sqlite3
from flask import Flask, request

FLAG = os.environ.get("FLAG", "CITT{sql_injection_101}")
app = Flask(__name__)

def db():
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE users(user TEXT, pass TEXT, role TEXT)")
    c.execute("INSERT INTO users VALUES('admin','S3cr3t_aDm1n_2026','admin')")
    c.execute("INSERT INTO users VALUES('invitado','invitado','user')")
    return c

CSS = r"""
:root{--bg:#0b1020;--panel:#121a33;--line:#24335e;--txt:#e7ecfb;--mut:#93a0c7;
--acc:#4f8cff;--acc2:#27e0b3;--err:#ff6b8b}
*{box-sizing:border-box}
body{margin:0;min-height:100vh;font-family:'Inter',system-ui,Segoe UI,Roboto,sans-serif;
color:var(--txt);background:radial-gradient(1200px 600px at 80% -10%,#1b2a55 0,transparent 60%),var(--bg);
display:flex;flex-direction:column}
.topbar{display:flex;align-items:center;gap:12px;padding:16px 28px;border-bottom:1px solid var(--line);
background:rgba(10,15,32,.6);backdrop-filter:blur(6px)}
.logo{display:flex;align-items:center;gap:10px;font-weight:700;letter-spacing:.3px}
.logo .mark{width:26px;height:26px;border-radius:7px;background:linear-gradient(135deg,var(--acc),var(--acc2));
display:grid;place-items:center;color:#06122b;font-weight:900;font-size:14px}
.topnav{margin-left:auto;display:flex;gap:22px;color:var(--mut);font-size:14px}
.topnav span{cursor:default}
.wrap{flex:1;display:grid;place-items:center;padding:40px 16px}
.card{width:100%;max-width:420px;background:var(--panel);border:1px solid var(--line);
border-radius:16px;padding:34px 30px;box-shadow:0 30px 70px rgba(0,0,0,.45)}
.kicker{color:var(--acc2);font-size:12px;letter-spacing:2px;text-transform:uppercase;font-weight:700}
h1{margin:6px 0 4px;font-size:22px}
.sub{color:var(--mut);font-size:14px;margin-bottom:22px}
label{display:block;font-size:13px;color:var(--mut);margin:14px 0 6px}
input{width:100%;padding:12px 14px;border-radius:10px;border:1px solid var(--line);
background:#0c1430;color:var(--txt);font-size:15px}
input:focus{outline:none;border-color:var(--acc)}
button{margin-top:22px;width:100%;padding:12px;border:0;border-radius:10px;cursor:pointer;
font-weight:700;font-size:15px;color:#06122b;background:linear-gradient(135deg,var(--acc),var(--acc2))}
.msg{margin-top:20px;padding:12px 14px;border-radius:10px;font-size:14px}
.msg.err{background:rgba(255,107,139,.12);color:var(--err);border:1px solid rgba(255,107,139,.3)}
.msg.ok{background:rgba(39,224,179,.10);color:var(--acc2);border:1px solid rgba(39,224,179,.3)}
.flag{margin-top:14px;font-family:ui-monospace,Menlo,Consolas,monospace;background:#0c1430;
border:1px dashed var(--acc2);color:var(--acc2);padding:12px;border-radius:10px;text-align:center;word-break:break-all}
.foot{color:var(--mut);font-size:12px;text-align:center;padding:16px}
"""

def page(body):
    return f"""<!doctype html><html lang=es><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Núcleo Corp · Intranet</title>
<link rel=preconnect href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel=stylesheet>
<style>{CSS}</style></head><body>
<header class=topbar>
  <div class=logo><span class=mark>N</span> Núcleo<span style="color:#27e0b3">Corp</span></div>
  <nav class=topnav><span>Servicios</span><span>Personas</span><span>Soporte TI</span></nav>
</header>
<main class=wrap>{body}</main>
<footer class=foot>© 2026 Núcleo Corp — Portal interno de colaboradores · uso exclusivo autorizado</footer>
</body></html>"""

def card(msg_html=""):
    return f"""<section class=card>
  <div class=kicker>Acceso corporativo</div>
  <h1>Iniciar sesión</h1>
  <div class=sub>Ingresa con tus credenciales de red Núcleo Corp.</div>
  <form method=post>
    <label for=user>Usuario</label>
    <input id=user name=user autocomplete=username placeholder="nombre.apellido">
    <label for=pass>Contraseña</label>
    <input id=pass name=pass type=password autocomplete=current-password placeholder="••••••••">
    <button>Entrar</button>
  </form>
  {msg_html}
</section>"""

@app.route("/", methods=["GET", "POST"])
def index():
    msg_html = ""
    if request.method == "POST":
        u = request.form.get("user", "")
        p = request.form.get("pass", "")
        # VULNERABLE: concatenacion directa, sin parametrizar
        q = f"SELECT role FROM users WHERE user='{u}' AND pass='{p}'"
        try:
            row = db().execute(q).fetchone()
        except Exception as e:
            row = None
            msg_html = f"<div class='msg err'>Error del sistema: {e}</div>"
        if row:
            if row[0] == "admin":
                msg_html = ("<div class='msg ok'>Bienvenido admin. Acceso concedido al panel de TI.</div>"
                            f"<div class=flag>Flag: {FLAG}</div>")
            else:
                msg_html = "<div class='msg ok'>Sesión iniciada (usuario sin privilegios).</div>"
        elif not msg_html:
            msg_html = "<div class='msg err'>Credenciales inválidas.</div>"
    return page(card(msg_html))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
