# Warmup · insert_coin

| | |
|---|---|
| **Categoría** | Warmup |
| **Dificultad** | fácil |
| **Puntaje base** | 50 (dinámico) |
| **Despliegue** | estático (archivo de entrega) |
| **Flag** | `CITT{bienvenido_a_cybervaras_2026}` |

## Enunciado (para el jugador)

Toda buena partida empieza metiendo una ficha. La flag está escondida a plena vista en la propia web del campeonato (https://2026.cybervaras.xyz). Mira donde nadie mira.

## Solución (writeup — NO publicar)

En el pie de la página aparece el texto `insert_coin_to_continue_`. La flag está como comentario HTML / atributo data cerca de ese elemento (o en el CSS `::after`). Ver código fuente con Ctrl+U o DevTools.

## Construcción del reto

Sembrar la flag como comentario HTML en el footer del repo de la web pública (nicsanchezr/CyberVaras-2026), p. ej. `<!-- CITT{...} -->` junto a insert_coin_to_continue_.

