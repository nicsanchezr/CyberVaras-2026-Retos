# Carga de retos en CTFd — CyberVaras 2026 (Plan B)

Dos caminos para los estáticos. **Recomendado:** `ctfcli` (usa los `challenge.yml`,
soporta archivos adjuntos y scoring). **Alternativa rápida:** importador CSV de CTFd.
Los 10 web NO usan CTFd-whale: van como **instancias fijas** en el droplet de retos
(ver más abajo) y en CTFd se crean como retos normales que apuntan a una URL.

> **Scoring (Plan B): puntaje FIJO para los 30.** Cada `challenge.yml` trae
> `minimum == initial` (decay queda inerte). Si editas puntajes a mano, vuelve a
> correr `python3 tools/fijar_puntaje_fijo.py` para re-normalizar.

---

## Infraestructura (2 droplets DigitalOcean)

- **CTFd — droplet principal (2 vCPU / 2 GB), `ctf.cybervaras.xyz`.** Corre solo
  CTFd + DB + Redis + proxy (WORKERS=4). Liviano; **no se le tocan dependencias**.
- **Retos web — droplet (2 vCPU / 4 GB), `retos.cybervaras.xyz`.**
  Wildcard `*.retos.cybervaras.xyz` ya resuelve a esa IP. Acá corren las 6 apps +
  Caddy (HTTPS automático por subdominio).

---

## Opción A — ctfcli (estáticos, recomendada)

```bash
pip install ctfcli
cd cybervaras-2026-retos
ctf init                       # apunta a https://ctf.cybervaras.xyz + token admin

# instalar un reto:
ctf challenge install crypto/rsa_fragil

# o todos los estáticos (24 = todo menos web/):
for d in warmup/*/ crypto/*/ forense/*/ redes/*/ osint/*/ reversing/*/ ; do
  ctf challenge install "$d"
done
```

Antes de instalar, genera las entregas: `bash tools/build_all.sh`.
Cada `challenge.yml` ya trae `type: dynamic`, `extra.initial/decay/minimum`
(con minimum == initial → **fijo**), la flag y los archivos de `entrega/`.
Quedan en estado `hidden`: se publican el viernes 23 al abrir.

## Opción B — CSV (estáticos)

`import/retos_estaticos.csv` trae los **24 retos no-web** con columnas compatibles con
el importador de CTFd (**Admin → Config → Backup/CSV → Import challenges**).
Un flag y un tag por reto. **Ojo:** el CSV NO sube los archivos de `entrega/`; esos se
adjuntan a mano, o se usa ctfcli.

`import/indice_retos.csv` es el panorama completo (incluye los 10 web) para control interno.

---

## Retos web (10) — instancias fijas con Caddy (droplet de retos)

**Por qué NO whale:** el plugin CTFd-whale no corre limpio en CTFd 3.8.8 (exige
downgradear requests/urllib3/charset-normalizer dentro del contenedor de CTFd; hack
frágil y sin mantención). Para no arriesgar el CTFd de producción a días del evento,
los 10 web van como instancias fijas.

### Despliegue (en el droplet `retos.cybervaras.xyz`)

En `web/` hay dos archivos de producción:
- `compose.prod.yml` — las 6 apps (flag por entorno; `incluyeme` por build arg) + Caddy.
- `Caddyfile` — ruteo subdominio → contenedor, con HTTPS Let's Encrypt automático.

```bash
cd web
docker compose -f compose.prod.yml up -d --build
# firewall: ufw allow 22,80,443/tcp   (nada más)
```

Supuesto: las apps escuchan en el puerto **5000** interno (así vienen). Si cambia,
ajustar el `Caddyfile`.

### Mapa subdominio → reto → flag → puntaje (fijo)

| Reto | URL | Pts | Flag |
|---|---|---|---|
| Login Injectado | https://login.retos.cybervaras.xyz | 100 | `CITT{sql_injection_101}` |
| Robots Traviesos | https://robots.retos.cybervaras.xyz | 125 | `CITT{nunca_confies_en_robots_txt}` |
| Cambia el ID | https://idor.retos.cybervaras.xyz | 200 | `CITT{idor_acceso_horizontal}` |
| Galleta Falsa | https://cookie.retos.cybervaras.xyz | 250 | `CITT{cookies_no_son_para_confiar}` |
| Token Quebrado | https://jwt.retos.cybervaras.xyz | 350 | `CITT{jwt_alg_none_es_peligroso}` |
| Inclúyeme | https://lfi.retos.cybervaras.xyz | 400 | `CITT{lfi_hasta_la_raiz}` |
| Cazador de Agentes | https://ua.retos.cybervaras.xyz | 125 | `CITT{el_user_agent_te_delata}` |
| Métodos HTTP | https://methods.retos.cybervaras.xyz | 150 | `CITT{metodo_http_olvidado}` |
| SSRF Interno | https://ssrf.retos.cybervaras.xyz | 350 | `CITT{ssrf_al_metadata_interno}` |
| XXE Clásico | https://xxe.retos.cybervaras.xyz | 350 | `CITT{xxe_entidades_externas}` |

### En CTFd

Crear los 6 como retos **dynamic normales (NO dynamic_docker)**, estado `hidden`, con
la flag de la tabla y el link en la Description (`Objetivo en: https://…`, ya incluido
en cada `challenge.yml`). Puntaje **fijo** (minimum == initial, decay 25).

### Trade-off asumido

Instancia compartida y flag compartida (sin aislamiento por equipo). Los 6 son
**stateless** (SQLi / robots / IDOR / cookie / JWT / LFI), así que compartir instancia
no rompe nada; único riesgo: que un equipo pase la flag a otro → **vigilar el scoreboard**.

### Seguridad

Apps vulnerables-a-propósito y públicas → **arriba solo durante el evento**. `ufw` con
22/80/443. Al terminar: `docker compose -f compose.prod.yml down` y apagar/destruir el
droplet de retos.

### Prueba local (sin Caddy, puertos fijos)

```bash
cd web && docker compose up --build
# login:5001  robots:5002  idor:5003  cookie:5004  jwt:5005  lfi:5006
```

---

## Checklist de carga
- [ ] `bash tools/build_all.sh` ejecutado (entregas + scoring fijo)
- [ ] 24 estáticos cargados (ctfcli o CSV + adjuntos)
- [ ] Droplet de retos: `compose.prod.yml up -d --build`, 6 subdominios con HTTPS OK
- [ ] 10 web creados en CTFd como `dynamic` con su URL en la Description
- [ ] Flags probadas una a una (ver writeups en cada `README.md`)
- [ ] Pistas cargadas en los retos que las llevan
- [ ] Todo en `hidden` hasta el viernes 23 · 18:00
- [ ] 3 OSINT: solo tras armado manual (no publicar antes)
