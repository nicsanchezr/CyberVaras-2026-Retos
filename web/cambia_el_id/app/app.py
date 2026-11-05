#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# cambia_el_id :: IDOR. El perfil se consulta por ?id= sin verificar propiedad.
import os
from flask import Flask, request, render_template_string

FLAG = os.environ.get("FLAG", "CITT{idor_acceso_horizontal}")
app = Flask(__name__)

USERS = {
    1:    {"user": "admin",    "nombre": "Administrador", "nota": f"FLAG: {FLAG}"},
    1001: {"user": "ana",      "nombre": "Ana Rivas",     "nota": "preferencias: modo oscuro"},
    1002: {"user": "invitado", "nombre": "Cuenta Demo",   "nota": "cuenta de prueba del CTF"},
}

HOME = """
<!doctype html><title>Mi Portal</title>
<h2>// PORTAL</h2>
<p>Sesion iniciada como <b>invitado</b> (id 1002).</p>
<p><a href="/profile?id=1002">Ver mi perfil</a></p>
"""
PROF = """
<!doctype html><title>Perfil</title>
<h2>Perfil #{{id}}</h2>
<ul>
 <li>usuario: {{u.user}}</li>
 <li>nombre: {{u.nombre}}</li>
 <li>nota: {{u.nota}}</li>
</ul>
<p><a href="/">volver</a></p>
"""

@app.route("/")
def index():
    return HOME

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
    return render_template_string(PROF, id=pid, u=u)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
