# Forense · Píxel Oculto

| | |
|---|---|
| **Categoría** | Forense |
| **Dificultad** | fácil |
| **Puntaje base** | 150 (dinámico) |
| **Despliegue** | estático (archivo de entrega) |
| **Flag** | `CITT{el_bit_menos_significativo}` |

## Enunciado (para el jugador)

Esta imagen esconde texto en sus bits menos significativos. Extráelo.

## Solución (writeup — NO publicar)

Esteganografía LSB. Usar zsteg (`zsteg secreto.png`) o stegsolve, o script que lee el LSB del canal R. También probar `strings`/`binwalk` primero.

## Construcción del reto

Generador incrusta la flag en el LSB del canal rojo de un PNG. Ver entrega/build.py.

**Archivos de entrega:** `entrega/secreto.png`

