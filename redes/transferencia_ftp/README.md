# Redes · Transferencia FTP

| | |
|---|---|
| **Categoría** | Redes |
| **Dificultad** | medio |
| **Puntaje** | 225 (fijo: minimum == initial) |
| **Despliegue** | estático (archivo de entrega) |
| **Flag** | `CITT{ftp_export_objects}` |

## Enunciado (para el jugador)

En esta captura alguien transfirió un archivo por FTP. Recupéralo: dentro está la flag.

## Solución (writeup — NO publicar)

Identificar el canal de datos FTP (puerto negociado por PASV). En Wireshark: Follow TCP Stream del canal de datos → guardar bytes como archivo. O `tshark` export. El archivo contiene la flag.

## Construcción del reto

Generador (scapy) simula control FTP + canal de datos transfiriendo un .txt con la flag. Ver build/build.py.

**Archivos de entrega:** `entrega/ftp.pcap`

