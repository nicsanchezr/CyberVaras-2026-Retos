# Warmup · Capas

| | |
|---|---|
| **Categoría** | Warmup |
| **Dificultad** | fácil |
| **Puntaje base** | 100 (dinámico) |
| **Despliegue** | estático (archivo de entrega) |
| **Flag** | `CITT{capa_tras_capa_tras_capa}` |

## Enunciado (para el jugador)

Base64 sobre hex sobre base64... la flag está envuelta en varias codificaciones. Ve pelando una a una.

## Solución (writeup — NO publicar)

Cadena: base64 → hex → base64 → rot13 (o similar). Resolver con CyberChef 'Magic', o a mano: `base64 -d`, `xxd -r -p`, etc.

## Construcción del reto

Generador aplica base64(hex(base64(rot13(flag)))) y guarda en capas.txt. Ver entrega/build.py.

**Archivos de entrega:** `entrega/capas.txt`

