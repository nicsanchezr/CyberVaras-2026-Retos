# Warmup · Terminal Básica

| | |
|---|---|
| **Categoría** | Warmup |
| **Dificultad** | fácil |
| **Puntaje base** | 75 (dinámico) |
| **Despliegue** | estático (archivo de entrega) |
| **Flag** | `CITT{grep_es_tu_amigo}` |

## Enunciado (para el jugador)

Te dejamos un montón de archivos en un .tar.gz. En uno de ellos, en alguna línea perdida, está la flag. Descomprime y busca con las herramientas de siempre.

## Solución (writeup — NO publicar)

`tar xzf pistas.tar.gz` y luego `grep -rao 'CITT{[^}]*}' .` (recursivo, texto). La flag está dentro de uno de ~200 archivos de ruido.

## Construcción del reto

Generador crea 200 archivos .txt de basura y mete la flag en una línea de uno. Empaqueta en pistas.tar.gz. Ver entrega/build.sh.

**Archivos de entrega:** `entrega/pistas.tar.gz`

