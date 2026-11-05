#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# login_injectado :: SQLi de autenticacion. VULNERABLE A PROPOSITO (reto CTF).
import os, sqlite3
from flask import Flask, request, render_template_string

FLAG = os.environ.get("FLAG", "CITT{sql_injection_101}")
app = Flask(__name__)

def db():
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE users(user TEXT, pass TEXT, role TEXT)")
    c.execute("INSERT INTO users VALUES('admin','S3cr3t_aDm1n_2026','admin')")
    c.execute("INSERT INTO users VALUES('invitado','invitado','user')")
    return c

PAGE = """
<!doctype html><title>Intranet CyberVaras</title>
<h2>// LOGIN</h2>
<form method=post>
  usuario: <input name=user><br>
  clave: <input name=pass type=password><br>
  <button>entrar</button>
</form>
{% if msg %}<p><b>{{msg}}</b></p>{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def index():
    msg = ""
    if request.method == "POST":
        u = request.form.get("user", "")
        p = request.form.get("pass", "")
        # VULNERABLE: concatenacion directa, sin parametrizar
        q = f"SELECT role FROM users WHERE user='{u}' AND pass='{p}'"
        try:
            row = db().execute(q).fetchone()
        except Exception as e:
            row, msg = None, f"SQL error: {e}"
        if row:
            if row[0] == "admin":
                msg = f"Bienvenido admin. Flag: {FLAG}"
            else:
                msg = "Sesion iniciada (usuario sin privilegios)."
        elif not msg:
            msg = "Credenciales invalidas."
    return render_template_string(PAGE, msg=msg)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
