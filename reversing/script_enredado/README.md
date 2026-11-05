# Reversing · Script Enredado

| | |
|---|---|
| **Categoría** | Reversing |
| **Dificultad** | medio |
| **Puntaje** | 250 (fijo: minimum == initial) |
| **Despliegue** | estático (archivo de entrega) |
| **Flag** | `CITT{ofuscar_no_es_cifrar}` |

## Enunciado (para el jugador)

Un script de Python ofuscado que, al ejecutarse, valida una flag. Pero ofuscar no es cifrar: desenrédalo.

## Solución (writeup — NO publicar)

El script tiene la flag como base64/rot/marshal anidado. En vez de ejecutarlo a ciegas, reemplazar el `exec/eval` final por `print`, o ir decodificando las capas a mano, para revelar la flag.

## Construcción del reto

Generador produce reto.py con la flag ofuscada en varias capas (base64 + marshal). Ver src/build.py.

**Archivos de entrega:** `entrega/reto.py`

