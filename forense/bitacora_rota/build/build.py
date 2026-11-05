#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera access.log (formato combined) con ruido legitimo + la secuencia del
atacante: fuzzing (404s) y una peticion final que exfiltra la flag en base64
dentro de un parametro de query. Salida: access.log"""
import os, base64, random, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "entrega"); os.makedirs(OUT, exist_ok=True)
flag = open(os.path.join(OUT, "..", "flag.txt")).read().strip()
random.seed(2026)

UAS = [
 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0 Safari/537.36",
 "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
 "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1",
]
PAGES = ["/", "/index.html", "/css/app.css", "/js/main.js", "/img/logo.png",
         "/productos", "/contacto", "/blog/ctf-2026", "/favicon.ico"]
def ip_norm(): return f"190.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
ATTACKER = "45.138.12.207"

t = datetime.datetime(2026, 10, 20, 9, 0, 0)
lines = []
def ts(dt): return dt.strftime("%d/%b/%Y:%H:%M:%S -0300")

# 400 lineas de trafico legitimo
for _ in range(400):
    t += datetime.timedelta(seconds=random.randint(1, 20))
    p = random.choice(PAGES); code = random.choice([200,200,200,304,200])
    sz = random.randint(180, 5000)
    lines.append(f'{ip_norm()} - - [{ts(t)}] "GET {p} HTTP/1.1" {code} {sz} "-" "{random.choice(UAS)}"')

# secuencia del atacante: fuzzing de rutas (muchos 404)
FUZZ = ["/admin","/.env","/backup.zip","/wp-login.php","/config.php","/.git/config",
        "/phpinfo.php","/server-status","/api/v1/users","/old","/test.php","/shell.php"]
for f in FUZZ:
    t += datetime.timedelta(seconds=random.randint(1, 4))
    lines.append(f'{ATTACKER} - - [{ts(t)}] "GET {f} HTTP/1.1" 404 199 "-" "curl/8.4.0"')

# hallazgo: 200 en endpoint vulnerable y exfiltracion en base64
b64 = base64.b64encode(flag.encode()).decode()
t += datetime.timedelta(seconds=3)
lines.append(f'{ATTACKER} - - [{ts(t)}] "GET /api/v1/export?data={b64} HTTP/1.1" 200 512 "-" "curl/8.4.0"')

# un poco mas de ruido despues
for _ in range(60):
    t += datetime.timedelta(seconds=random.randint(1, 15))
    lines.append(f'{ip_norm()} - - [{ts(t)}] "GET {random.choice(PAGES)} HTTP/1.1" 200 {random.randint(180,5000)} "-" "{random.choice(UAS)}"')

open(os.path.join(OUT, "access.log"), "w").write("\n".join(lines) + "\n")
print(f"[ok] access.log generado ({len(lines)} lineas, atacante {ATTACKER})")
