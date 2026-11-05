# Redes · Telnet Indiscreto

| | |
|---|---|
| **Categoría** | Redes |
| **Dificultad** | fácil |
| **Puntaje base** | 150 (dinámico) |
| **Despliegue** | estático (archivo de entrega) |
| **Flag** | `CITT{telnet_es_inseguro}` |

## Enunciado (para el jugador)

Telnet no cifra nada. Reconstruye la sesión de este pcap y lee lo que el usuario escribió.

## Solución (writeup — NO publicar)

Seguir el TCP stream del puerto 23. El usuario escribe un comando (p. ej. `echo CITT{...}`) visible carácter a carácter en el stream.

## Construcción del reto

Generador (scapy) simula sesión Telnet con la flag tecleada. Ver entrega/build.py.

**Archivos de entrega:** `entrega/telnet.pcap`

