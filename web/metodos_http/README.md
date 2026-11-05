# Web · Métodos HTTP

| | |
|---|---|
| **Categoría** | Web |
| **Dificultad** | fácil |
| **Puntaje** | 150 (fijo: minimum == initial) |
| **Despliegue** | instancia web fija · https://methods.retos.cybervaras.xyz (droplet retos, vía Caddy) |
| **Flag** | `CITT{metodo_http_olvidado}` |

## Enunciado (para el jugador)

La consola heredada de LegacyDB deshabilitó el método GET en su endpoint de exportación, pero la exportación sigue viva por otro método. Encuéntralo.

Objetivo en: https://methods.retos.cybervaras.xyz

## Solución (writeup — NO publicar)

GET /export responde 405 con la cabecera 'Allow: POST', que delata el método vigente. `curl -X POST https://methods.retos.cybervaras.xyz/export` devuelve la flag.

## Construcción del reto

App Flask: /export acepta GET y POST; con GET responde 405 + Allow: POST, con POST entrega la flag. Flag por variable FLAG. Ver app/.

