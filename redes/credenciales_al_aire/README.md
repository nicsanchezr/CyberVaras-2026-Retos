# Redes · Credenciales al Aire

| | |
|---|---|
| **Categoría** | Redes |
| **Dificultad** | fácil |
| **Puntaje base** | 150 (dinámico) |
| **Despliegue** | estático (archivo de entrega) |
| **Flag** | `CITT{http_en_texto_claro}` |

## Enunciado (para el jugador)

Capturamos tráfico de una red. Alguien inició sesión por HTTP (sin HTTPS). Sus credenciales viajaron en claro... y una de ellas es la flag.

## Solución (writeup — NO publicar)

Abrir en Wireshark, seguir el stream HTTP del POST de login, o `tshark -r captura.pcap -Y http.request.method==POST`. La contraseña enviada es la flag.

## Construcción del reto

Generador (scapy) arma un pcap con un POST HTTP cuyo campo password es la flag. Ver entrega/build.py.

**Archivos de entrega:** `entrega/captura.pcap`

