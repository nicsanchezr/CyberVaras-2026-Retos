# Crypto · RSA Frágil

| | |
|---|---|
| **Categoría** | Crypto |
| **Dificultad** | medio |
| **Puntaje base** | 250 (dinámico) |
| **Despliegue** | estático (archivo de entrega) |
| **Flag** | `CITT{primos_pequenos_rsa_roto}` |

## Enunciado (para el jugador)

Te damos n, e y c de un cifrado RSA. El problema: eligieron primos demasiado pequeños.

## Pista (configurable en CTFd)

> n es pequeño. ¿Qué pasa si lo factorizas? Prueba factordb.

## Solución (writeup — NO publicar)

Factorizar n (pequeño) con factordb o sympy.factorint → p,q. Calcular φ=(p-1)(q-1), d=inverse(e,φ), m=c^d mod n. Convertir m a bytes → flag.

## Construcción del reto

Generador crea RSA con p,q pequeños, cifra la flag. Guarda n,e,c. Ver entrega/build.py.

**Archivos de entrega:** `entrega/rsa.txt`

