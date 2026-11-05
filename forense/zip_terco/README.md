# Forense · ZIP Terco

| | |
|---|---|
| **Categoría** | Forense |
| **Dificultad** | medio |
| **Puntaje** | 225 (fijo: minimum == initial) |
| **Despliegue** | estático (archivo de entrega) |
| **Flag** | `CITT{binwalk_siempre_gana}` |

## Enunciado (para el jugador)

Una imagen inocente... que pesa demasiado. Algo trae pegado detrás.

## Solución (writeup — NO publicar)

`binwalk portada.png` revela un ZIP anexado. `binwalk -e` o `unzip` lo extrae. El ZIP pide contraseña; la pista está en un comentario del PNG o en los metadatos. Dentro, la flag.

## Construcción del reto

Generador concatena un ZIP (con flag.txt, protegido) al final de un PNG; pone la pass en un chunk tEXt. Ver build/build.py.

**Archivos de entrega:** `entrega/portada.png`

