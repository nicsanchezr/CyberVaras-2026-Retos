#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# robots_traviesos :: information disclosure via robots.txt + backup expuesto.
import os
from flask import Flask, Response

FLAG = os.environ.get("FLAG", "CITT{nunca_confies_en_robots_txt}")
app = Flask(__name__)

@app.route("/")
def index():
    return "<title>CyberVaras Corp</title><h2>Sitio corporativo</h2><p>Nada que ver por aqui.</p>"

@app.route("/robots.txt")
def robots():
    body = ("User-agent: *\n"
            "Disallow: /panel-interno/\n"
            "Disallow: /backup/\n")
    return Response(body, mimetype="text/plain")

@app.route("/backup/app.py.bak")
def bak():
    # "copia de seguridad" olvidada con la flag en el codigo
    code = ("# backup del sitio - NO SUBIR A PROD\n"
            "SECRET_CONFIG = {\n"
            f"    'flag': '{FLAG}',\n"
            "    'db': 'postgres://interno'\n"
            "}\n")
    return Response(code, mimetype="text/plain")

@app.route("/panel-interno/")
def panel():
    return "<h3>Panel interno</h3><p>Acceso restringido. Revisa los respaldos.</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
