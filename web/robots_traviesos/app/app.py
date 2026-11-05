#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# robots_traviesos :: information disclosure via robots.txt + backup expuesto.
# El rediseño toca SOLO la presentacion de / y /panel-interno/.
# /robots.txt y /backup/app.py.bak se sirven IDENTICOS (text/plain) — son la
# superficie del reto y no se tocan.
import os
from flask import Flask, Response

FLAG = os.environ.get("FLAG", "CITT{nunca_confies_en_robots_txt}")
app = Flask(__name__)

CSS = r"""
:root{--bg:#f4f7fb;--ink:#0b2545;--mut:#5b6b85;--acc:#0a6e78;--acc2:#0b7d4f;--line:#e2e8f2}
*{box-sizing:border-box}
body{margin:0;font-family:'Manrope',system-ui,Segoe UI,Roboto,sans-serif;color:var(--ink);background:var(--bg)}
header{background:#fff;border-bottom:1px solid var(--line)}
.bar{max-width:1040px;margin:0 auto;display:flex;align-items:center;gap:14px;padding:18px 22px}
.brand{display:flex;align-items:center;gap:10px;font-weight:800;font-size:19px;letter-spacing:-.2px}
.brand .d{width:28px;height:28px;border-radius:8px;background:linear-gradient(135deg,var(--acc),var(--acc2))}
nav{margin-left:auto;display:flex;gap:24px;color:var(--mut);font-weight:600;font-size:14px}
.hero{max-width:1040px;margin:0 auto;padding:70px 22px 40px}
.tag{color:var(--acc);font-weight:700;letter-spacing:2px;text-transform:uppercase;font-size:12px}
h1{font-size:40px;line-height:1.1;margin:10px 0 14px;max-width:16ch}
.lead{color:var(--mut);font-size:18px;max-width:52ch;line-height:1.6}
.cta{margin-top:26px;display:inline-block;background:var(--ink);color:#fff;text-decoration:none;
padding:13px 22px;border-radius:10px;font-weight:700}
.grid{max-width:1040px;margin:30px auto;padding:0 22px 70px;display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.cardx{background:#fff;border:1px solid var(--line);border-radius:14px;padding:22px}
.cardx h3{margin:6px 0 8px;font-size:17px}
.cardx p{margin:0;color:var(--mut);font-size:14px;line-height:1.55}
.dot{width:34px;height:34px;border-radius:9px;background:#eaf5f3;display:grid;place-items:center;color:var(--acc);font-weight:900}
.foot{border-top:1px solid var(--line);background:#fff;color:var(--mut);font-size:13px}
.foot .bar{justify-content:space-between}
.panel{max-width:720px;margin:60px auto;padding:0 22px}
.panel .box{background:#fff;border:1px solid var(--line);border-left:4px solid var(--acc);border-radius:12px;padding:26px}
.muted{color:var(--mut)}
@media(max-width:780px){.grid{grid-template-columns:1fr}h1{font-size:30px}}
"""

def page(body, title="Veltra Solutions"):
    return f"""<!doctype html><html lang=es><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1"><title>{title}</title>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&display=swap" rel=stylesheet>
<style>{CSS}</style></head><body>
<header><div class=bar>
  <div class=brand><span class=d></span>Veltra<span style="color:#0a6e78">Solutions</span></div>
  <nav><span>Plataforma</span><span>Industrias</span><span>Nosotros</span><span>Contacto</span></nav>
</div></header>
{body}
<footer class=foot><div class=bar><span>© 2026 Veltra Solutions SpA</span><span>Santiago · Chile</span></div></footer>
</body></html>"""

HOME = """
<section class=hero>
  <div class=tag>Infraestructura digital</div>
  <h1>Automatizamos la operación de tu empresa</h1>
  <p class=lead>Veltra Solutions integra procesos, datos y personas en una sola plataforma.
  Más de 120 empresas confían en nosotros para operar sin fricción.</p>
  <a class=cta href="#">Solicitar demo</a>
</section>
<section class=grid>
  <div class=cardx><div class=dot>◈</div><h3>Integración</h3><p>Conecta tus sistemas legados con APIs modernas en semanas, no meses.</p></div>
  <div class=cardx><div class=dot>▲</div><h3>Analítica</h3><p>Tableros en tiempo real para decidir con datos y no con intuición.</p></div>
  <div class=cardx><div class=dot>●</div><h3>Soporte 24/7</h3><p>Acompañamiento continuo con SLA y respaldo de nuestro equipo.</p></div>
</section>"""

PANEL = """
<section class=panel><div class=box>
  <h1 style="font-size:24px;margin:0 0 10px">Panel interno</h1>
  <p class=muted>Acceso restringido al personal de Veltra Solutions.</p>
  <p class=muted>Si buscas una versión anterior del sitio o un respaldo de configuración,
  consulta con el equipo de infraestructura. Los respaldos quedan en su ubicación habitual.</p>
</div></section>"""

@app.route("/")
def index():
    return page(HOME)

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
    return page(PANEL, title="Veltra · Panel interno")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
