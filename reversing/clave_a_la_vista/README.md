# Reversing · Clave a la Vista

| | |
|---|---|
| **Categoría** | Reversing |
| **Dificultad** | medio |
| **Puntaje** | 200 (fijo: minimum == initial) |
| **Despliegue** | estático (archivo de entrega) |
| **Flag** | `CITT{strings_revela_la_clave}` |

## Enunciado (para el jugador)

Un binario te pide una contraseña. Si aciertas, te da la flag. La contraseña está más a la vista de lo que crees.

## Solución (writeup — NO publicar)

`strings crackme | less` muestra la contraseña comparada en claro. Ingresarla devuelve la flag. También se ve en Ghidra en la comparación strcmp.

## Construcción del reto

Fuente C compara input con password en claro; si coincide imprime la flag. Compilar con tools. Ver src/ y build.sh.

**Archivos de entrega:** `entrega/crackme`

