# Forense · Sonido Sospechoso

| | |
|---|---|
| **Categoría** | Forense |
| **Dificultad** | medio |
| **Puntaje** | 250 (fijo: minimum == initial) |
| **Despliegue** | estático (archivo de entrega) |
| **Flag** | `CITT{escucha_el_espectrograma}` |

## Enunciado (para el jugador)

Un audio con un pitido raro. La flag no está en lo que oyes, sino en lo que ves.

## Pista (configurable en CTFd)

> No se escucha, se ve. Abre el espectrograma en Audacity o Sonic Visualiser.

## Solución (writeup — NO publicar)

Abrir el WAV en Audacity/Sonic Visualiser y ver el espectrograma: la flag está 'dibujada' en las frecuencias.

## Construcción del reto

Generador sintetiza un WAV cuyo espectrograma dibuja el texto de la flag. Ver build/build.py (requiere numpy).

**Archivos de entrega:** `entrega/senal.wav`

