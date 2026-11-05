#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RSA con primos pequeños (factorizable). Cifra la flag. Salida: rsa.txt (n,e,c).
La flag debe caber en un bloque: usamos n suficientemente grande pero factorizable."""
import os, random
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "entrega"); os.makedirs(OUT, exist_ok=True)
flag = open(os.path.join(OUT, "..", "flag.txt")).read().strip().encode()
m = int.from_bytes(flag, "big")

def is_prime(n):
    if n < 2: return False
    for p in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n % p == 0: return n == p
    d, r = n-1, 0
    while d % 2 == 0: d //= 2; r += 1
    for a in (2,3,5,7,11,13,17,19,23,29,31,37):
        x = pow(a, d, n)
        if x in (1, n-1): continue
        for _ in range(r-1):
            x = x*x % n
            if x == n-1: break
        else: return False
    return True

def gen_prime(bits):
    while True:
        p = random.getrandbits(bits) | (1 << (bits-1)) | 1
        if is_prime(p): return p

# n debe superar a m pero seguir siendo factorizable (primos "pequeños" ~ 64 bits c/u)
bits = max(80, (m.bit_length() // 2) + 8)
random.seed(2026)
while True:
    p = gen_prime(bits); q = gen_prime(bits)
    n = p*q
    if n > m and p != q:
        break
e = 65537
phi = (p-1)*(q-1)
d = pow(e, -1, phi)
c = pow(m, e, n)
# verificación
assert pow(c, d, n) == m
with open(os.path.join(OUT, "rsa.txt"), "w") as fh:
    fh.write(f"n = {n}\ne = {e}\nc = {c}\n")
print(f"[ok] rsa.txt generado (n de {n.bit_length()} bits, factorizable)")
print("    pista: factordb / sympy.factorint resuelven n")
