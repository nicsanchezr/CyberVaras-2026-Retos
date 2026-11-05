# Crypto · Hash Expuesto

| | |
|---|---|
| **Categoría** | Crypto |
| **Dificultad** | medio |
| **Puntaje base** | 200 (dinámico) |
| **Despliegue** | estático (archivo de entrega) |
| **Flag** | `CITT{rockyou_lo_tenia}` |

## Enunciado (para el jugador)

Filtramos una tabla de hashes. Varios son contraseñas comunes. Crackéalas: la flag se arma con las contraseñas recuperadas.

## Solución (writeup — NO publicar)

Identificar tipo (MD5/SHA1) con hashid. Crackear con `john`/`hashcat` + rockyou. Las palabras recuperadas, concatenadas con `_`, forman el contenido de la flag.

## Construcción del reto

Generador toma palabras débiles (de rockyou), las hashea, y define la flag como su unión. Ver entrega/build.py.

**Archivos de entrega:** `entrega/hashes.txt`

