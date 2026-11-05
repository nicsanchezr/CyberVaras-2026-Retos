# Web · Cazador de Agentes

| | |
|---|---|
| **Categoría** | Web |
| **Dificultad** | fácil |
| **Puntaje** | 125 (fijo: minimum == initial) |
| **Despliegue** | instancia web fija · https://ua.retos.cybervaras.xyz (droplet retos, vía Caddy) |
| **Flag** | `CITT{el_user_agent_te_delata}` |

## Enunciado (para el jugador)

El feed de inteligencia de Sentinel solo responde a su cliente oficial. Las peticiones desde un navegador son rechazadas. Hazte pasar por el cliente.

Objetivo en: https://ua.retos.cybervaras.xyz

## Solución (writeup — NO publicar)

Control de acceso basado solo en el User-Agent. El sitio revela que el cliente oficial usa el UA 'SentinelCLI/2.0'. Enviarlo a /feed entrega la flag: `curl -A "SentinelCLI/2.0" https://ua.retos.cybervaras.xyz/feed`.

## Construcción del reto

App Flask: /feed devuelve la flag solo si el header User-Agent contiene 'SentinelCLI/2.0'. Flag por variable FLAG. Ver app/.

