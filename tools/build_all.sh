#!/usr/bin/env bash
# Regenera TODO: scaffold + artefactos de entrega de cada reto.
# Uso: bash tools/build_all.sh   (desde la raiz del repo)
set -euo pipefail
cd "$(dirname "$0")/.."
echo "== scaffold =="
python3 tools/build_scaffold.py

echo "== scoring fijo (minimum == initial) =="
python3 tools/fijar_puntaje_fijo.py

echo "== warmup =="
bash   warmup/terminal_basica/build/build.sh
python3 warmup/capas/build/build.py

echo "== crypto =="
for r in cesar_recargado xor_de_bolsillo hash_expuesto xor_reciclado rsa_fragil; do
  python3 crypto/$r/build/build.py
done

echo "== forense =="
for r in metadatos_delatores pixel_oculto zip_terco sonido_sospechoso bitacora_rota usb_perdido; do
  python3 forense/$r/build/build.py
done

echo "== redes =="
for r in credenciales_al_aire telnet_indiscreto transferencia_ftp dns_curioso; do
  python3 redes/$r/build/build.py
done

echo "== reversing =="
python3 reversing/clave_a_la_vista/src/build.py
python3 reversing/xor_en_binario/src/build.py
python3 reversing/script_enredado/src/build.py

echo "== import =="
python3 tools/make_import.py

echo "OK: artefactos regenerados. Los retos web se construyen con Docker (ver web/)."
