# Web · Cambia el ID

| | |
|---|---|
| **Categoría** | Web |
| **Dificultad** | medio |
| **Puntaje base** | 200 (dinámico) |
| **Despliegue** | whale (contenedor por equipo) |
| **Flag** | `CITT{idor_acceso_horizontal}` |

## Enunciado (para el jugador)

Inicia sesión con la cuenta de prueba que te damos y revisa tu perfil. La URL tiene un número... ¿qué pasa si lo cambias? Encuentra el perfil del administrador.

## Solución (writeup — NO publicar)

IDOR: tras login, el perfil está en `/profile?id=1002`. Cambiando a `/profile?id=1` (o iterando) se accede al perfil admin sin control de autorización. La flag está en el perfil admin.

## Construcción del reto

App Flask, usuarios en SQLite, endpoint /profile?id= sin verificar propiedad. Credenciales de prueba fijas. Ver app/.

