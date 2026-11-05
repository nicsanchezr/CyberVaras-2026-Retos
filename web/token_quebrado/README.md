# Web · Token Quebrado

| | |
|---|---|
| **Categoría** | Web |
| **Dificultad** | difícil |
| **Puntaje** | 350 (fijo: minimum == initial) |
| **Despliegue** | instancia web fija · https://jwt.retos.cybervaras.xyz (droplet retos, vía Caddy) |
| **Flag** | `CITT{jwt_alg_none_es_peligroso}` |

## Enunciado (para el jugador)

La API entrega un JWT al iniciar sesión. El endpoint /admin exige un token de administrador. Falsifica uno.

Objetivo en: https://jwt.retos.cybervaras.xyz

## Pista (configurable en CTFd)

> El header de un JWT dice qué algoritmo usar para verificarlo. ¿Qué pasa si el servidor le cree al header?

## Solución (writeup — NO publicar)

El verificador acepta `alg: none` (o una clave HS256 débil de diccionario). Forjar un JWT con payload `{'user':'admin','role':'admin'}` y alg none (firma vacía), o crackear el secreto con jwt_tool/hashcat y re-firmar. /admin devuelve la flag.

## Construcción del reto

App Flask, verificación JWT mal configurada (acepta none / secreto 'secret'). Ver app/.

