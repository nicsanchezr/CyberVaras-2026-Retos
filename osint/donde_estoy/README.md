# OSINT · ¿Dónde Estoy?

| | |
|---|---|
| **Categoría** | OSINT |
| **Dificultad** | fácil |
| **Puntaje base** | 150 (dinámico) |
| **Despliegue** | estático (archivo de entrega) |
| **Flag** | `CITT{geolocalizado_sin_exif}` |

## Enunciado (para el jugador)

Esta foto NO tiene metadatos de ubicación. Pero se reconoce el lugar. Identifícalo: la flag es el nombre del lugar en el formato que indica la pista.

## Solución (writeup — NO publicar)

Reconocer el hito visible (edificio/monumento reconocible de Santiago o del campus). Búsqueda inversa de imagen (Google Lens/Yandex). La flag se arma con el nombre del lugar normalizado según pista.txt.

## Construcción del reto

MANUAL: elegir una foto propia/libre de un lugar reconocible SIN EXIF de GPS, y fijar la flag como su nombre. pista.txt explica el formato. Ver README para el montaje.

**Archivos de entrega:** `entrega/lugar.jpg`, `entrega/pista.txt`

