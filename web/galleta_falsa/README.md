# Web · Galleta Falsa

| | |
|---|---|
| **Categoría** | Web |
| **Dificultad** | medio |
| **Puntaje** | 250 (fijo: minimum == initial) |
| **Despliegue** | instancia web fija · https://cookie.retos.cybervaras.xyz (droplet retos, vía Caddy) |
| **Flag** | `CITT{cookies_no_son_para_confiar}` |

## Enunciado (para el jugador)

La aplicación recuerda quién eres con una cookie. Pero la cookie dice más de lo que debería... y nadie comprueba que no la toques.

Objetivo en: https://cookie.retos.cybervaras.xyz

## Solución (writeup — NO publicar)

La cookie `role=user` (o un valor base64 `{'user':'guest','role':'user'}`) no está firmada. Cambiarla a `role=admin` (re-codificando el base64) da acceso al panel admin con la flag.

## Construcción del reto

App Flask setea cookie de sesión casera (base64 JSON, sin firmar). /admin exige role=admin. Ver app/.

