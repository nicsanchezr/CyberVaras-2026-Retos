# Crypto · XOR Reciclado

| | |
|---|---|
| **Categoría** | Crypto |
| **Dificultad** | medio |
| **Puntaje base** | 275 (dinámico) |
| **Despliegue** | estático (archivo de entrega) |
| **Flag** | `CITT{clave_repetida_mala_idea}` |

## Enunciado (para el jugador)

Reusaron una clave corta para cifrar un texto largo con XOR. Ese es su error.

## Solución (writeup — NO publicar)

XOR de clave repetida (Vigenère binario). Estimar longitud de clave (Kasiski/Hamming), luego resolver byte a byte por frecuencia. xortool: `xortool cipher.bin`. La flag va embebida en el texto plano.

## Construcción del reto

Generador XOR de un texto largo (que contiene la flag) con clave de ~5-7 bytes repetida. Ver entrega/build.py.

**Archivos de entrega:** `entrega/cipher.bin`

