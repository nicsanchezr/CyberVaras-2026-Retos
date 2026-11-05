#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera capas.txt: la flag envuelta en base64(hex(base64(rot13))).
Resolver: rot13 <- base64 -d <- unhex <- base64 -d."""
import base64, codecs, os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "entrega"); os.makedirs(OUT, exist_ok=True)
flag = open(os.path.join(OUT, "..", "flag.txt")).read().strip()

l0 = codecs.encode(flag, "rot13")                 # rot13
l1 = base64.b64encode(l0.encode()).decode()       # base64
l2 = l1.encode().hex()                             # hex
l3 = base64.b64encode(l2.encode()).decode()        # base64

open(os.path.join(OUT, "capas.txt"), "w").write(l3 + "\n")

# verificación (desenvolver)
d = base64.b64decode(l3).decode()
d = bytes.fromhex(d).decode()
d = base64.b64decode(d).decode()
d = codecs.decode(d, "rot13")
assert d == flag, "round-trip falló"
print("[ok] capas.txt generado y verificado")
