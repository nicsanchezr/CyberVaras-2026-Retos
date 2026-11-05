# Web · Login Injectado

| | |
|---|---|
| **Categoría** | Web |
| **Dificultad** | fácil |
| **Puntaje** | 100 (fijo: minimum == initial) |
| **Despliegue** | instancia web fija · https://login.retos.cybervaras.xyz (droplet retos, vía Caddy) |
| **Flag** | `CITT{sql_injection_101}` |

## Enunciado (para el jugador)

Un panel de login de lo más normal. ¿Seguro que valida bien lo que escribes? Entra como administrador.

Objetivo en: https://login.retos.cybervaras.xyz

## Solución (writeup — NO publicar)

Inyección SQL clásica de autenticación: usuario `admin' -- ` o `' OR '1'='1' -- `. La consulta concatena sin parametrizar. Al autenticarse como admin se muestra la flag.

## Construcción del reto

App Flask + SQLite en app/. Query vulnerable por f-string. Whale: imagen por equipo. Ver app/ y docker-compose.yml.

