#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera y compila 'xorme'. La flag NO aparece con strings: está XOR-eada con
una clave multibyte y se reconstruye en memoria en tiempo de ejecución, pero el
programa no la imprime directamente (pide confirmar y solo dice OK/NO).
El jugador debe leer memoria (gdb) o replicar el XOR desde el binario.
Salida: ../entrega/xorme"""
import os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "entrega"))
flag = open(os.path.join(HERE, "..", "flag.txt")).read().strip().encode()
KEY = b"\x13\x37\xAC\x5E"
enc = bytes(flag[i] ^ KEY[i % len(KEY)] for i in range(len(flag)))
enc_arr = ", ".join(str(b) for b in enc)
key_arr = ", ".join(str(b) for b in KEY)

c = f'''#include <stdio.h>
#include <string.h>
int main(void) {{
    unsigned char enc[] = {{ {enc_arr} }};
    unsigned char key[] = {{ {key_arr} }};
    int n = sizeof(enc);
    char flag[256];
    for (int i = 0; i < n; i++) flag[i] = enc[i] ^ key[i % sizeof(key)];
    flag[n] = 0;                 // <- la flag vive aqui en runtime
    char buf[64];
    printf("Clave de activacion: ");
    if (!fgets(buf, sizeof buf, stdin)) return 1;
    buf[strcspn(buf, "\\n")] = 0;
    if (strcmp(buf, flag) == 0) printf("Activado.\\n");
    else printf("Clave incorrecta.\\n");
    return 0;
}}
'''
src = os.path.join(HERE, "xorme.c")
open(src, "w").write(c)
os.makedirs(OUT, exist_ok=True)
subprocess.run(["gcc", "-O0", "-no-pie", "-o", os.path.join(OUT, "xorme"), src], check=True)
# verificación: con la flag correcta debe "Activar"
r = subprocess.run([os.path.join(OUT, "xorme")], input=flag + b"\n", capture_output=True)
assert b"Activado" in r.stdout, r.stdout
# y strings NO debe mostrar la flag
s = subprocess.run(["strings", os.path.join(OUT, "xorme")], capture_output=True)
assert flag not in s.stdout, "la flag aparece en strings (no deberia)"
print("[ok] xorme compilado — flag NO visible en strings, se arma en runtime")
