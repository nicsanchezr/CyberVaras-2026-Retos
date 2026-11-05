#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# galleta_falsa :: cookie de sesion casera (base64 JSON SIN firmar) manipulable.
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

@app.route("/")
def index():
    s = get_session()
    if not s:
        resp = make_response(
            "<title>CyberVaras App</title><h2>// APP</h2>"
            "<p>Te asignamos una sesion de invitado.</p>"
            '<p><a href="/admin">ir al panel admin</a></p>')
        set_session(resp, {"user": "invitado", "role": "user"})
        return resp
    return (f"<h2>// APP</h2><p>Hola {s.get('user')} (rol: {s.get('role')}).</p>"
            '<p><a href="/admin">ir al panel admin</a></p>')

@app.route("/admin")
def admin():
    s = get_session() or {}
    if s.get("role") == "admin":
        return f"<h2>Panel admin</h2><p>Flag: {FLAG}</p>"
    return "<h3>403</h3><p>Solo administradores.</p>", 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
