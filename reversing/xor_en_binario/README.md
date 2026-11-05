# Reversing · XOR en Binario

| | |
|---|---|
| **Categoría** | Reversing |
| **Dificultad** | difícil |
| **Puntaje** | 400 (fijo: minimum == initial) |
| **Despliegue** | estático (archivo de entrega) |
| **Flag** | `CITT{xor_en_tiempo_de_ejecucion}` |

## Enunciado (para el jugador)

La flag no aparece con strings porque el binario la arma en tiempo de ejecución, byte a byte, con XOR. Tienes que analizarlo.

## Pista (configurable en CTFd)

> La flag no está en strings: se construye en memoria. Pon un breakpoint después del bucle XOR.

## Solución (writeup — NO publicar)

En Ghidra se ve un arreglo de bytes XOR-eados con una clave y un bucle que reconstruye la flag. Opciones: replicar el XOR en Python con los bytes y la clave del binario, o en gdb poner breakpoint tras el bucle y leer memoria.

## Construcción del reto

Fuente C guarda la flag XOR-eada y la descifra en runtime (no la imprime directo). Compilar. Ver src/ y build.sh.

**Archivos de entrega:** `entrega/xorme`

