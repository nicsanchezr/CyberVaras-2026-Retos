# Web · SSRF Interno

| | |
|---|---|
| **Categoría** | Web |
| **Dificultad** | difícil |
| **Puntaje** | 350 (fijo: minimum == initial) |
| **Despliegue** | instancia web fija · https://ssrf.retos.cybervaras.xyz (droplet retos, vía Caddy) |
| **Flag** | `CITT{ssrf_al_metadata_interno}` |

## Enunciado (para el jugador)

InfraCloud tiene un verificador que consulta por ti el estado de un servicio interno a partir de su URL. Hazlo consultar la metadata interna de la instancia.

Objetivo en: https://ssrf.retos.cybervaras.xyz

## Solución (writeup — NO publicar)

SSRF: el verificador solo alcanza destinos loopback, y la metadata (/internal/metadata) solo responde a peticiones loopback. Pedir url=http://127.0.0.1:5000/internal/metadata hace que el servidor se consulte a sí mismo (remote_addr loopback) y devuelva la flag. Seguro: no es un proxy abierto a internet (no_network).

## Construcción del reto

App Flask: /fetch?url= solo permite hosts loopback y hace la consulta server-side; /internal/metadata responde la flag solo a remote_addr loopback. threaded=True para la auto-consulta. Flag por variable FLAG. Ver app/.

