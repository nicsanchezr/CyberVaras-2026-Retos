# Crypto · César Recargado

| | |
|---|---|
| **Categoría** | Crypto |
| **Dificultad** | fácil |
| **Puntaje** | 100 (fijo: minimum == initial) |
| **Despliegue** | estático (archivo de entrega) |
| **Flag** | `CITT{el_cesar_no_protege_nada}` |

## Enunciado (para el jugador)

Un mensaje cifrado con un método que tiene 2000 años. Rómpelo.

## Solución (writeup — NO publicar)

Cifrado César con desplazamiento fijo. Probar los 25 corrimientos (brute force) o análisis de frecuencia. El prefijo `CITT{` ayuda a encontrar el shift.

## Construcción del reto

Generador cifra la flag (y un texto señuelo) con César shift fijo. Ver build/build.py.

**Archivos de entrega:** `entrega/mensaje.txt`

