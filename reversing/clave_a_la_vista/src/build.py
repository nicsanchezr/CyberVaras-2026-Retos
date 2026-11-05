#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera y compila 'crackme'. La contraseña está en claro (strings la revela);
la flag va XOR-eada con la contraseña y se imprime solo si el input coincide.
Salida: ../entrega/crackme"""
import os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "entrega"))
flag = open(os.path.join(HERE, "..", "flag.txt")).read().strip().encode()
PASS = b"v6_acceso_total"
enc = bytes(flag[i] ^ PASS[i % len(PASS)] for i in range(len(flag)))
arr = ", ".join(str(b) for b in enc)

c = f'''#include <stdio.h>
#include <string.h>
int main(void) {{
    char input[128];
    const char *pass = "{PASS.decode()}";
    unsigned char enc[] = {{ {arr} }};
    int n = sizeof(enc);
    printf("Ingrese la contrasena: ");
    if (!fgets(input, sizeof input, stdin)) return 1;
    input[strcspn(input, "\\n")] = 0;
    if (strcmp(input, pass) == 0) {{
        char out[256]; int pl = strlen(pass);
        for (int i = 0; i < n; i++) out[i] = enc[i] ^ pass[i % pl];
        out[n] = 0;
        printf("Acceso concedido: %s\\n", out);
    }} else {{
        printf("Acceso denegado.\\n");
    }}
    return 0;
}}
'''
src = os.path.join(HERE, "crackme.c")
open(src, "w").write(c)
os.makedirs(OUT, exist_ok=True)
subprocess.run(["gcc", "-O0", "-no-pie", "-o", os.path.join(OUT, "crackme"), src], check=True)
# verificación
r = subprocess.run([os.path.join(OUT, "crackme")], input=PASS + b"\n",
                   capture_output=True)
assert flag in r.stdout, r.stdout
print("[ok] crackme compilado y verificado (contrasena en claro, flag XOR)")
