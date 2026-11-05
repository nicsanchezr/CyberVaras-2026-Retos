#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# token_quebrado :: JWT mal verificado. Acepta alg=none Y secreto debil 'secret'.
# Implementacion manual a proposito para exponer la vulnerabilidad del reto.
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

@app.route("/")
def index():
    tok = make_jwt({"user": "invitado", "role": "user"})
    return (f"<title>API CyberVaras</title><h2>// API</h2>"
            f"<p>Tu token de invitado:</p><code>{tok}</code>"
            f'<p>Usa el header <b>Authorization: Bearer &lt;token&gt;</b> en <a href="/admin">/admin</a>.</p>')

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
