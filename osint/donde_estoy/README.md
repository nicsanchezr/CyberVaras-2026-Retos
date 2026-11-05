# OSINT · ¿Dónde Estoy?

| | |
|---|---|
| **Categoría** | OSINT |
| **Dificultad** | fácil |
| **Puntaje** | 150 (fijo: minimum == initial) |
| **Despliegue** | estático (archivo de entrega) |
| **Flag** | `CITT{definir_ciudad_lugar}` |

## Enunciado (para el jugador)

Esta foto NO tiene metadatos de ubicación. Pero se reconoce el lugar. Identifícalo: la flag es el nombre del lugar en el formato que indica la pista.

## Solución (writeup — NO publicar)

Reconocer el hito visible (edificio/monumento reconocible). Búsqueda inversa de imagen (Google Lens/Yandex). La flag se arma con el nombre del lugar normalizado según pista.txt: CITT{ciudad_lugar}.

## Construcción del reto

MANUAL (OBLIGATORIO antes de publicar): 1) reemplazar lugar.jpg (hoy es un placeholder de prueba, NO geolocalizable) por una foto real de un lugar reconocible SIN EXIF de GPS; 2) fijar la flag en flag.txt al formato CITT{ciudad_lugar} de ESE lugar (reemplaza el placeholder CITT{definir_ciudad_lugar}). El enunciado y pista.txt ya prometen ese formato. Verificar que la flag coincide con lo que da una búsqueda inversa.

**Archivos de entrega:** `entrega/lugar.jpg`, `entrega/pista.txt`

