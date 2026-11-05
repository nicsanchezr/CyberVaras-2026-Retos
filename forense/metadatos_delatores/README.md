# Forense · Metadatos Delatores

| | |
|---|---|
| **Categoría** | Forense |
| **Dificultad** | fácil |
| **Puntaje base** | 100 (dinámico) |
| **Despliegue** | estático (archivo de entrega) |
| **Flag** | `CITT{los_metadatos_hablan}` |

## Enunciado (para el jugador)

Una foto de lo más común. Pero las fotos guardan más de lo que muestran. Revisa sus metadatos.

## Solución (writeup — NO publicar)

`exiftool foto.jpg`. La flag está en un campo EXIF (Comment / Artist / UserComment).

## Construcción del reto

Generador crea un JPG y escribe la flag en EXIF UserComment (piexif/exiftool). Ver entrega/build.py.

**Archivos de entrega:** `entrega/foto.jpg`

