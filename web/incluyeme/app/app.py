#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# incluyeme :: LFI. ?page= se abre como archivo sin sanitizar (path traversal).
import os
from flask import Flask, request

app = Flask(__name__)
VIEWS = os.path.join(os.path.dirname(__file__), "views")

@app.route("/")
def index():
    page = request.args.get("page", "home")
    # VULNERABLE: se concatena y se abre sin validar -> traversal
    path = os.path.join(VIEWS, page + ".html")
    try:
        with open(path, "r", errors="replace") as f:
            content = f.read()
    except Exception:
        # permite tambien rutas absolutas/traversal crudas si .html no existe
        try:
            with open(request.args.get("page", ""), "r", errors="replace") as f:
                content = f.read()
        except Exception as e:
            return f"<p>no se pudo cargar la vista: {e}</p>", 404
    menu = ('<nav>[<a href="/?page=home">home</a>] '
            '[<a href="/?page=about">about</a>]</nav><hr>')
    return menu + f"<pre>{content}</pre>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
