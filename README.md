# CyberVaras 2026 · Retos del Sexto Campeonato

```
root@cybervaras:~/2026$ cat README.md
// LVL 6 · Sexto Campeonato · 23–24 oct 2026 · Jeopardy online 24 h
// 48 retos · 7 categorías · flags CITT{...}
```

Archivo público de los retos del **Sexto Campeonato CyberVaras 2026** (Track de
Ciberseguridad · CITT Antonio Varas · Duoc UC). Todo el material es para
**formación en ciberseguridad, en entornos controlados y con fines educativos**.
El campeonato ya terminó: las flags y los writeups son públicos para que puedas
practicar y aprender. Sitio del evento: https://2026.cybervaras.xyz

## Qué hay en este repositorio

| Ruta | Contenido |
|---|---|
| `ctfd-final/retos_finales.csv` | Los **48 retos tal como se jugaron** en CTFd: categoría, puntaje, flag, descripción y archivos adjuntos. |
| `ctfd-final/archivos/` | Archivos adjuntos que recibieron los equipos (42 archivos). |
| `<categoria>/<slug>/` | **34 retos con fuente**: enunciado, writeup, generador, archivos de entrega y, en Web, el código y el `Dockerfile`. |
| `web/` | Código de los 10 retos web, `compose.prod.yml` y `Caddyfile` (proxy inverso con HTTPS). |
| `import/`, `tools/` | Índice y scripts para construir e importar los retos a CTFd. |

> **Ojo:** los otros 14 retos del campeonato (warmups, criptografía, forense y OSINT
> sencillos, más «Bienvenida») se crearon directamente en CTFd: aquí están sus datos
> finales y adjuntos en `ctfd-final/`, pero no tienen carpeta de fuente. La columna
> `fuente_en_repo` del CSV y las tablas de abajo indican cuáles la tienen.

---

## Convenciones

| | |
|---|---|
| **Formato de flag** | `CITT{texto_en_snake_case}` (una flag por reto) |
| **Scoring** | Puntaje fijo en todos los retos (`minimum == initial`) |
| **Despliegue** | Estáticos: archivo de entrega. Web: 10 instancias fijas con Caddy en un droplet aparte (HTTPS por subdominio) |
| **Pistas** | 8 pistas en 8 retos, con costo en puntos (ver `hints` de CTFd) |

---

## Panorama de los 48 retos

| Categoría | Retos | Con fuente en el repo | Despliegue |
|---|---|---|---|
| Warmup | 7 | 3 | static |
| Web | 10 | 10 | instancia fija (Caddy) |
| Crypto | 9 | 5 | static |
| Forense | 10 | 6 | static |
| Redes | 5 | 4 | static |
| OSINT | 4 | 3 | static |
| Reversing | 3 | 3 | static |
| **Total** | **48** | **34** | |

La categoría Warmup incluye el reto «Bienvenida» (10 puntos, para practicar el envío de una flag) y Crypto agrupa las categorías «Crypto» y «Criptografía» de CTFd.

### Warmup (7)

| # | Reto | Puntos | Fuente |
|---|---|---|---|
| 1 | Primer contacto | 50 | solo adjuntos (`ctfd-final/`) |
| 2 | Doble vuelta | 100 | solo adjuntos (`ctfd-final/`) |
| 3 | Al revés | 75 | solo adjuntos (`ctfd-final/`) |
| 14 | Bienvenida | 10 | solo adjuntos (`ctfd-final/`) |
| 15 | Capas | 100 | [`warmup/capas`](warmup/capas) |
| 16 | insert_coin | 50 | [`warmup/insert_coin`](warmup/insert_coin) |
| 17 | Terminal Básica | 75 | [`warmup/terminal_basica`](warmup/terminal_basica) |

### Web (10)

| # | Reto | Puntos | Fuente |
|---|---|---|---|
| 18 | Cambia el ID | 200 | [`web/cambia_el_id`](web/cambia_el_id) |
| 19 | Galleta Falsa | 250 | [`web/galleta_falsa`](web/galleta_falsa) |
| 20 | Inclúyeme | 400 | [`web/incluyeme`](web/incluyeme) |
| 21 | Login Injectado | 100 | [`web/login_injectado`](web/login_injectado) |
| 22 | Robots Traviesos | 125 | [`web/robots_traviesos`](web/robots_traviesos) |
| 23 | Token Quebrado | 350 | [`web/token_quebrado`](web/token_quebrado) |
| 43 | Cazador de Agentes | 125 | [`web/cazador_agentes`](web/cazador_agentes) |
| 44 | Métodos HTTP | 150 | [`web/metodos_http`](web/metodos_http) |
| 45 | SSRF Interno | 350 | [`web/ssrf_interno`](web/ssrf_interno) |
| 46 | XXE Clásico | 350 | [`web/xxe_clasico`](web/xxe_clasico) |

### Crypto (9)

| # | Reto | Puntos | Fuente |
|---|---|---|---|
| 4 | César se fue de vacaciones | 100 | solo adjuntos (`ctfd-final/`) |
| 5 | La clave está en el nombre | 200 | solo adjuntos (`ctfd-final/`) |
| 6 | O exclusivo | 125 | solo adjuntos (`ctfd-final/`) |
| 7 | RSA de juguete | 250 | solo adjuntos (`ctfd-final/`) |
| 24 | César Recargado | 100 | [`crypto/cesar_recargado`](crypto/cesar_recargado) |
| 25 | Hash Expuesto | 200 | [`crypto/hash_expuesto`](crypto/hash_expuesto) |
| 26 | RSA Frágil | 250 | [`crypto/rsa_fragil`](crypto/rsa_fragil) |
| 27 | XOR de Bolsillo | 125 | [`crypto/xor_de_bolsillo`](crypto/xor_de_bolsillo) |
| 28 | XOR Reciclado | 275 | [`crypto/xor_reciclado`](crypto/xor_reciclado) |

### Forense (10)

| # | Reto | Puntos | Fuente |
|---|---|---|---|
| 8 | Metadatos que hablan | 100 | solo adjuntos (`ctfd-final/`) |
| 9 | Cadenas ocultas | 125 | solo adjuntos (`ctfd-final/`) |
| 10 | El archivo dentro del archivo | 225 | solo adjuntos (`ctfd-final/`) |
| 11 | Registro sospechoso | 200 | solo adjuntos (`ctfd-final/`) |
| 29 | Bitácora Rota | 250 | [`forense/bitacora_rota`](forense/bitacora_rota) |
| 30 | Metadatos Delatores | 100 | [`forense/metadatos_delatores`](forense/metadatos_delatores) |
| 31 | Píxel Oculto | 150 | [`forense/pixel_oculto`](forense/pixel_oculto) |
| 32 | Sonido Sospechoso | 250 | [`forense/sonido_sospechoso`](forense/sonido_sospechoso) |
| 33 | USB Perdido | 275 | [`forense/usb_perdido`](forense/usb_perdido) |
| 34 | ZIP Terco | 225 | [`forense/zip_terco`](forense/zip_terco) |

### Redes (5)

| # | Reto | Puntos | Fuente |
|---|---|---|---|
| 12 | Conversación en claro | 150 | solo adjuntos (`ctfd-final/`) |
| 35 | Credenciales al Aire | 150 | [`redes/credenciales_al_aire`](redes/credenciales_al_aire) |
| 36 | DNS Curioso | 300 | [`redes/dns_curioso`](redes/dns_curioso) |
| 37 | Telnet Indiscreto | 150 | [`redes/telnet_indiscreto`](redes/telnet_indiscreto) |
| 38 | Transferencia FTP | 225 | [`redes/transferencia_ftp`](redes/transferencia_ftp) |

### OSINT (4)

| # | Reto | Puntos | Fuente |
|---|---|---|---|
| 13 | El perfil ficticio | 225 | solo adjuntos (`ctfd-final/`) |
| 42 | El Repo Olvidado | 225 | [`osint/el_repo_olvidado`](osint/el_repo_olvidado) |
| 47 | Rastro Social | 250 | [`osint/rastro_social`](osint/rastro_social) |
| 48 | ¿Dónde Estoy? | 150 | [`osint/donde_estoy`](osint/donde_estoy) |

### Reversing (3)

| # | Reto | Puntos | Fuente |
|---|---|---|---|
| 39 | Clave a la Vista | 200 | [`reversing/clave_a_la_vista`](reversing/clave_a_la_vista) |
| 40 | Script Enredado | 250 | [`reversing/script_enredado`](reversing/script_enredado) |
| 41 | XOR en Binario | 400 | [`reversing/xor_en_binario`](reversing/xor_en_binario) |

---

## Estructura de un reto con fuente

```
<categoria>/<slug>/
├─ challenge.yml     <- metadata ctfcli (tipo, puntaje, flag, archivos)
├─ flag.txt          <- la flag
├─ README.md         <- enunciado + writeup + receta de build
├─ entrega/          <- solo lo que recibe el jugador
├─ build/            <- generador (build.py/.sh), no se entrega
└─ app/ · src/       <- (web: código vulnerable) · (reversing: fuentes C/py)
```

## Construir las entregas

Los archivos de entrega se generan de forma reproducible:

```bash
bash tools/build_all.sh
```

Requisitos: `python3`, `pillow`, `numpy`, `scapy`, `piexif`, `gcc`, `zip`
(`pip install pillow numpy scapy piexif`). **Hazlo en Linux**: los binarios de
*reversing* (`crackme`, `xorme`) deben ser ELF de Linux; compilados en macOS
quedarían como Mach-O y no servirían para los jugadores.

## Cargar en CTFd

Ver `import/README_import.md`. Los estáticos se importan con `ctfcli` o con el CSV;
los retos web se despliegan como contenedores y las apps leen la flag de la
variable `FLAG`.

---

## Ética

Entorno **controlado, autorizado y con fines formativos**. Todo el material ofensivo
(apps vulnerables, binarios, capturas) existe solo dentro de la infraestructura del
CTF. Las bases del campeonato (punto 7) prohíben usar estas técnicas fuera de él.

```
> 48 retos jugados. nos vemos en octubre del próximo año_
```
