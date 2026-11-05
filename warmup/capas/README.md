# Warmup · Capas

| | |
|---|---|
| **Categoría** | Warmup |
| **Dificultad** | fácil |
| **Puntaje** | 100 (fijo: minimum == initial) |
| **Despliegue** | estático (archivo de entrega) |
| **Flag** | `CITT{capa_tras_capa_tras_capa}` |

## Enunciado (para el jugador)

La flag está envuelta en varias capas de codificación (base64, hexadecimal y un corrimiento de letras). Ve pelando una a una hasta llegar al centro.

## Solución (writeup — NO publicar)

Cadena exacta: base64 → hex → base64 → rot13. Resolver con CyberChef 'Magic' (recursivo), o a mano: `base64 -d`, `xxd -r -p`, `base64 -d`, y finalmente rot13.

## Construcción del reto

Generador aplica base64(hex(base64(rot13(flag)))) y guarda en capas.txt. Ver build/build.py.

**Archivos de entrega:** `entrega/capas.txt`

