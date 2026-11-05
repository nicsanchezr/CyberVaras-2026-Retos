# Web · XXE Clásico

| | |
|---|---|
| **Categoría** | Web |
| **Dificultad** | difícil |
| **Puntaje** | 350 (fijo: minimum == initial) |
| **Despliegue** | instancia web fija · https://xxe.retos.cybervaras.xyz (droplet retos, vía Caddy) |
| **Flag** | `CITT{xxe_entidades_externas}` |

## Enunciado (para el jugador)

El importador de facturas XML de DocFlow procesa el documento que envíes y registra al cliente. ¿Y si el XML pide leer un archivo del propio servidor?

Objetivo en: https://xxe.retos.cybervaras.xyz

## Pista (configurable en CTFd)

> El parser resuelve entidades externas. Declara un DOCTYPE con una ENTITY SYSTEM que apunte a file:///flag.txt y úsala dentro de <nombre>.

## Solución (writeup — NO publicar)

XXE: el parser usa resolve_entities + load_dtd. Enviar un DOCTYPE con `<!ENTITY xxe SYSTEM "file:///flag.txt">` y usar `&xxe;` dentro de <nombre> hace que el sistema refleje el contenido del archivo (la flag) como 'cliente registrado'. no_network=True evita SSRF por XXE; solo lee archivos locales del contenedor.

## Construcción del reto

App Flask + lxml. /import parsea el XML con XMLParser(resolve_entities=True, load_dtd=True, no_network=True) y refleja <nombre>. La flag vive en /flag.txt (ARG FLAG del Dockerfile). Ver app/.

