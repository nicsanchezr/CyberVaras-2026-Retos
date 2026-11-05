# Forense · Bitácora Rota

| | |
|---|---|
| **Categoría** | Forense |
| **Dificultad** | medio |
| **Puntaje base** | 250 (dinámico) |
| **Despliegue** | estático (archivo de entrega) |
| **Flag** | `CITT{el_log_delata_al_atacante}` |

## Enunciado (para el jugador)

Alguien atacó este servidor web. Entre miles de líneas de log hay una serie de peticiones sospechosas. Reconstruye el ataque y encuentra la flag.

## Solución (writeup — NO publicar)

Filtrar el access.log: una IP hace fuzzing (muchos 404) y luego 200 en una ruta rara. Esa IP, en una petición, exfiltra la flag codificada en base64 dentro de un parámetro/User-Agent. Decodificar.

## Construcción del reto

Generador crea un access.log realista con ruido + la secuencia del atacante; la flag va en base64 en un parámetro. Ver entrega/build.py.

**Archivos de entrega:** `entrega/access.log`

