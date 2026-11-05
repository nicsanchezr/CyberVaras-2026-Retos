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
| `<categoria>/<slug>/` | **30 retos con fuente**: enunciado, writeup, receta de build, archivos de entrega y, en Web, el código y el `Dockerfile`. |
| `ctfd-final/retos_finales.csv` | Los **48 retos tal como se jugaron** en CTFd: categoría, puntaje, flag, descripción y archivos adjuntos. |
| `ctfd-final/archivos/` | Archivos adjuntos que recibieron los equipos (42). |
| `import/`, `tools/` | Índice y scripts usados para construir e importar los retos a CTFd. |

> **Ojo:** el campeonato final tuvo 48 retos. Los 30 con carpeta de fuente son los
> que se prepararon primero; los otros 18 se agregaron después y aquí solo
> están sus datos finales y adjuntos (`ctfd-final/`), sin carpeta de fuente.
> En `retos_finales.csv`, la columna `fuente_en_repo` indica cuáles tienen carpeta.

---

## Convenciones

| | |
|---|---|
| **Formato de flag** | `CITT{texto_en_snake_case}` (una flag por reto) |
| **Scoring** | Dinámico de CTFd: `initial` = puntaje base, `decay` = 25, `minimum` ≈ mitad |
| **Estado inicial** | `hidden` — se publican al abrir el campeonato |
| **Despliegue** | `static` (archivo de entrega) · `whale` (contenedor por equipo, solo Web) |

---

## Panorama de los 30 retos con fuente

| Categoría | Retos | Fácil | Medio | Difícil | Despliegue |
|---|---|---|---|---|---|
| Warmup | 3 | 3 | – | – | static |
| Web | 6 | 2 | 2 | 2 | whale |
| Crypto | 5 | 2 | 3 | – | static |
| Forense | 6 | 2 | 4 | – | static |
| Redes | 4 | 2 | 2 | – | static |
| OSINT | 3 | 1 | 2 | – | static |
| Reversing | 3 | – | 2 | 1 | static |
| **Total** | **30** | **12** | **15** | **3** | 6 whale |

El índice completo con slugs, puntajes y flags está en `import/indice_retos.csv`.

---

## Estructura

```
cybervaras-2026-retos/
├─ README.md                      <- este archivo
├─ <categoria>/<slug>/
│   ├─ challenge.yml              <- metadata ctfcli (tipo, puntaje, flag, archivos)
│   ├─ flag.txt                   <- la flag (fuente única)
│   ├─ README.md                  <- enunciado + writeup + receta de build
│   ├─ entrega/                   <- archivos que recibe el jugador (+ build.py/.sh)
│   └─ app/ · src/                <- (web: código vulnerable) · (rev: fuentes C/py)
├─ web/docker-compose.yml         <- prueba local de los 6 retos web
├─ import/
│   ├─ retos_estaticos.csv        <- import CSV de CTFd (24 estáticos)
│   ├─ indice_retos.csv           <- panorama completo
│   └─ README_import.md           <- cómo cargar en CTFd + montaje whale
└─ tools/
    ├─ build_scaffold.py          <- regenera challenge.yml / flag.txt / README
    ├─ build_all.sh               <- regenera TODAS las entregas
    └─ make_import.py             <- regenera los CSV
```

---

## Construir las entregas

Los archivos de entrega se generan de forma reproducible (no se versiona el binario,
se versiona el generador):

```bash
bash tools/build_all.sh
```

Requisitos: `python3`, `pillow`, `numpy`, `scapy`, `piexif`, `gcc`, `zip`
(`pip install pillow numpy scapy piexif`). Cada generador imprime `[ok]` y varios
verifican la flag por round-trip.

---

## Cargar en CTFd

Ver `import/README_import.md`. Resumen:
- **Estáticos (24):** `ctfcli` (recomendado) o el CSV.
- **Web (6):** construir las imágenes y configurarlas como retos **whale**
  (contenedor aislado por equipo). Las apps leen la flag de la variable `FLAG`,
  así que admiten **flag dinámica por equipo** (anti-compartir).

---

## Pistas

Solo 5 retos las llevan (configurables en CTFd), tal como se definió:
`token_quebrado`, `incluyeme`, `rsa_fragil`, `sonido_sospechoso`, `usb_perdido`,
`dns_curioso`, `xor_en_binario`. El texto de cada pista está en el `README.md` del reto.

---

## Pendiente manual (OSINT)

Tres retos OSINT requieren montaje manual porque dependen de perfiles/repos reales
sembrados por la organización (no se pueden autogenerar):
- `donde_estoy` — elegir foto de un lugar reconocible **sin EXIF de GPS**.
- `rastro_social` — crear un perfil ficticio con alias único en 2–3 plataformas.
- `el_repo_olvidado` — repo público con la flag en un commit "borrado" del historial.

Cada uno trae en su `README.md` la receta y el formato de flag a fijar.

---

## Ética

Entorno **controlado, autorizado y con fines formativos**. Todo el material ofensivo
(apps vulnerables, binarios, capturas) existe solo dentro de la infraestructura del
CTF. Las bases del campeonato (punto 7) prohíben usar estas técnicas fuera de él.

```
> 30 retos cargados. insert_coin_to_continue_
```
