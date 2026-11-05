# OSINT · El Repo Olvidado

| | |
|---|---|
| **Categoría** | OSINT |
| **Dificultad** | medio |
| **Puntaje** | 225 (fijo: minimum == initial) |
| **Despliegue** | estático (archivo de entrega) |
| **Flag** | `CITT{git_log_recuerda_todo}` |

## Enunciado (para el jugador)

Un desarrollador 'borró' una credencial de su repositorio público. Pero git nunca olvida. Encuentra la flag en el historial.

## Solución (writeup — NO publicar)

Clonar el repo sembrado. La flag se 'eliminó' en un commit posterior pero sigue en el historial: `git log -p`, `git show <commit>` del archivo borrado, o buscar en todos los objetos.

## Construcción del reto

MANUAL (OBLIGATORIO antes de publicar): crear un repo público (org del track): un commit agrega un archivo con la flag de este reto (ver fila Flag arriba) y un commit posterior la 'borra'. Luego escribir la URL real del repo en pista.txt (hoy va en blanco). IMPORTANTE: la flag NO debe aparecer en pista.txt ni en archivos entregados; solo en el historial del repo.

**Archivos de entrega:** `entrega/pista.txt`

