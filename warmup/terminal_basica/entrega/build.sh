#!/usr/bin/env bash
# Genera pistas.tar.gz: ~200 archivos de ruido, la flag escondida en uno.
set -euo pipefail
cd "$(dirname "$0")"
FLAG="$(cat ../flag.txt)"
WORK="$(mktemp -d)"
mkdir -p "$WORK/logs"
for i in $(seq 1 200); do
  head -c 400 /dev/urandom | base64 | head -c 300 > "$WORK/logs/nota_$i.txt"
done
# esconder la flag en una línea perdida de un archivo al azar
TARGET=$(( (RANDOM % 200) + 1 ))
printf '\n# nota interna\n%s\n' "$FLAG" >> "$WORK/logs/nota_$TARGET.txt"
tar -C "$WORK" -czf pistas.tar.gz logs
rm -rf "$WORK"
echo "[ok] pistas.tar.gz generado (flag en nota_$TARGET.txt)"
