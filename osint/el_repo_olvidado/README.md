# OSINT · El Repo Olvidado

| | |
|---|---|
| **Categoría** | OSINT |
| **Dificultad** | medio |
| **Puntaje base** | 225 (dinámico) |
| **Despliegue** | estático (archivo de entrega) |
| **Flag** | `CITT{git_log_recuerda_todo}` |

## Enunciado (para el jugador)

Un desarrollador 'borró' una credencial de su repositorio público. Pero git nunca olvida. Encuentra la flag en el historial.

## Solución (writeup — NO publicar)

Clonar el repo sembrado. La flag se 'eliminó' en un commit posterior pero sigue en el historial: `git log -p`, `git show <commit>` del archivo borrado, o buscar en todos los objetos.

## Construcción del reto

MANUAL: crear un repo público (org del track) donde un commit añade la flag y otro la 'borra'. pista.txt da la URL. Ver README.

**Archivos de entrega:** `entrega/pista.txt`

