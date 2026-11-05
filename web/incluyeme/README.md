# Web · Inclúyeme

| | |
|---|---|
| **Categoría** | Web |
| **Dificultad** | difícil |
| **Puntaje** | 400 (fijo: minimum == initial) |
| **Despliegue** | instancia web fija · https://lfi.retos.cybervaras.xyz (droplet retos, vía Caddy) |
| **Flag** | `CITT{lfi_hasta_la_raiz}` |

## Enunciado (para el jugador)

La página carga 'vistas' según un parámetro. Parece inofensivo, pero el servidor incluye el archivo que le pidas. Lee la flag del sistema.

Objetivo en: https://lfi.retos.cybervaras.xyz

## Pista (configurable en CTFd)

> El parámetro de idioma termina siendo una ruta de archivo. ¿Hasta dónde puedes subir?

## Solución (writeup — NO publicar)

LFI en `/?page=home`. Path traversal `?page=../../../../etc/passwd` confirma. La flag está en un archivo fuera del webroot, p. ej. `?page=../../../../flag.txt` o vía filtros php/wrappers. Para el reto, la flag vive en /flag.txt dentro del contenedor.

## Construcción del reto

App Flask incluye plantillas por nombre sin sanitizar (open(path).read()). flag.txt en / del contenedor. Ver app/.

