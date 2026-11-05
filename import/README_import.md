# Carga de retos en CTFd

Dos caminos. **Recomendado:** `ctfcli` (usa los `challenge.yml` de cada reto, soporta
scoring dinámico y archivos adjuntos). **Alternativa rápida:** importador CSV de CTFd
para los retos estáticos.

---

## Opción A — ctfcli (recomendada)

```bash
pip install ctfcli
cd cybervaras-2026-retos
ctf init                       # apunta a https://TU-CTFD  + token admin

# instalar un reto:
ctf challenge install crypto/rsa_fragil

# o todos los estáticos de una categoría:
for d in warmup/*/ crypto/*/ forense/*/ redes/*/ osint/*/ reversing/*/ ; do
  ctf challenge install "$d"
done
```

Antes de instalar, genera las entregas: `bash tools/build_all.sh`.
Cada `challenge.yml` ya trae `type: dynamic`, `extra.initial/decay/minimum`, la flag
y los archivos de `entrega/`. Quedan en estado `hidden`: se publican el viernes 23 al
abrir el campeonato.

---

## Opción B — CSV (solo retos estáticos)

`import/retos_estaticos.csv` trae los **24 retos no-web** con columnas compatibles con
el importador de CTFd (**Admin → Config → Backup/CSV → Import challenges**).
Un flag y un tag por reto. **Ojo:** el CSV NO sube los archivos de `entrega/`; esos se
adjuntan a mano en cada reto, o se usa ctfcli.

`import/indice_retos.csv` es el panorama completo (incluye los 6 web) como referencia.

---

## Retos web (whale) — los 6 de `web/`

Los retos web necesitan una instancia Docker **aislada por equipo**. Se usa el plugin
**CTFd-whale** (https://github.com/glzjin/CTFd-Whale), igual que en el artículo de
referencia.

### Montaje (resumen)
1. En el VPS: CTFd + Docker + el plugin CTFd-whale + **frps/frpd** (proxy que publica
   las instancias). Whale crea un contenedor por equipo y le asigna subdominio/puerto.
2. Construir e identificar cada imagen:
   ```bash
   cd web
   for r in login_injectado robots_traviesos cambia_el_id galleta_falsa token_quebrado incluyeme; do
     docker build -t cybervaras/$r:latest ./$r
   done
   ```
3. En CTFd, crear cada reto como tipo **dynamic_docker** (lo añade whale) y configurar:
   - **Image:** `cybervaras/<slug>:latest`
   - **Redirect type:** `http` (los 6 son web)
   - **Flag:** la de `web/<slug>/flag.txt` — o dejar que whale inyecte una flag
     dinámica por equipo con la variable de entorno `FLAG` (las apps ya la leen de
     `os.environ["FLAG"]`).
   - Límites sugeridos por instancia: **CPU 0.5**, **RAM 128–256 MB**, **TTL 1–2 h**
     renovable. Con ~15 equipos y 6 retos, dimensiona el droplet en consecuencia.

### Flag dinámica por equipo (anti-compartir)
Las 6 apps toman la flag de la variable `FLAG`. Si activas flags dinámicas en whale,
cada equipo recibe su propia flag y compartirla no sirve. `incluyeme` la escribe en
`/flag.txt` desde el `ARG FLAG` del Dockerfile (ajústalo si usas inyección por entorno).

### Prueba local sin whale
```bash
cd web && docker compose up --build
# login_injectado:5001  robots:5002  idor:5003  cookie:5004  jwt:5005  lfi:5006
```

---

## Checklist de carga
- [ ] `bash tools/build_all.sh` ejecutado (entregas generadas)
- [ ] 24 estáticos cargados (ctfcli o CSV + adjuntos)
- [ ] 6 imágenes web construidas y retos whale configurados
- [ ] Flags probadas una a una (ver writeups en cada `README.md`)
- [ ] Pistas cargadas en los 5 retos que las llevan
- [ ] Todo en `hidden` hasta el viernes 23 · 18:00
