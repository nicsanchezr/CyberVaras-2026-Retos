# Redes · DNS Curioso

| | |
|---|---|
| **Categoría** | Redes |
| **Dificultad** | medio |
| **Puntaje** | 300 (fijo: minimum == initial) |
| **Despliegue** | estático (archivo de entrega) |
| **Flag** | `CITT{exfiltracion_por_dns}` |

## Enunciado (para el jugador)

Un host hace un montón de consultas DNS a un dominio sospechoso, con subdominios larguísimos. Están exfiltrando datos. Recupéralos.

## Pista (configurable en CTFd)

> Mira los subdominios consultados. ¿Por qué son tan largos y raros? Pruébalos como base32/hex.

## Solución (writeup — NO publicar)

Extraer los qname de las consultas (`tshark -r dns.pcap -Y dns -T fields -e dns.qry.name`). Los subdominios son trozos hex/base32 que, concatenados y decodificados, dan la flag.

## Construcción del reto

Generador (scapy) crea consultas DNS cuyos subdominios son la flag troceada en hex. Ver build/build.py.

**Archivos de entrega:** `entrega/dns.pcap`

