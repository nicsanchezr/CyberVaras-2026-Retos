# Web · Robots Traviesos

| | |
|---|---|
| **Categoría** | Web |
| **Dificultad** | fácil |
| **Puntaje** | 125 (fijo: minimum == initial) |
| **Despliegue** | instancia web fija · https://robots.retos.cybervaras.xyz (droplet retos, vía Caddy) |
| **Flag** | `CITT{nunca_confies_en_robots_txt}` |

## Enunciado (para el jugador)

El administrador creyó que esconder rutas en robots.txt bastaba. Spoiler: no basta.

Objetivo en: https://robots.retos.cybervaras.xyz

## Solución (writeup — NO publicar)

Leer `/robots.txt` → lista rutas 'Disallow' como `/panel-oculto/` y `/backup/`. En `/backup/app.py.bak` (o `/.git/`) queda expuesto el código con la flag, o un endpoint oculto la devuelve.

## Construcción del reto

App Flask sirve robots.txt con Disallow a /backup/. En /backup/ hay un .bak con la flag. Ver app/.

