# Crypto · XOR de Bolsillo

| | |
|---|---|
| **Categoría** | Crypto |
| **Dificultad** | fácil |
| **Puntaje** | 125 (fijo: minimum == initial) |
| **Despliegue** | estático (archivo de entrega) |
| **Flag** | `CITT{xor_un_byte_es_trivial}` |

## Enunciado (para el jugador)

Cifrado XOR con una clave de un solo byte. 256 posibilidades. Tú puedes.

## Solución (writeup — NO publicar)

Fuerza bruta de los 256 bytes de clave; el candidato legible (empieza con `CITT{`) es la flag. CyberChef 'XOR Brute Force' o script en Python.

## Construcción del reto

Generador XOR de la flag con un byte fijo, salida en hex. Ver build/build.py.

**Archivos de entrega:** `entrega/cipher.hex`

