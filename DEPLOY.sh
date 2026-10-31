#!/usr/bin/env bash
# Force rebuild from Dockerfile (do NOT pass --image)
set -euo pipefail
cd "$(dirname "$0")"

echo "==> Allocate public IPs if missing..."
fly ips allocate-v4 --shared -a robbor-cp-uttvga 2>/dev/null || true
fly ips allocate-v6 -a robbor-cp-uttvga 2>/dev/null || true

echo "==> Deploy (rebuild image from local Dockerfile)..."
fly deploy -a robbor-cp-uttvga \
  --config fly.toml \
  --wait-timeout 10m \
  --ha=false

echo "==> Status"
fly status -a robbor-cp-uttvga
echo "==> Probe"
sleep 3
curl -sS -m 15 https://robbor-cp-uttvga.fly.dev/health || true
echo
curl -sS -m 15 -o /dev/null -w "dashboard HTTP %{http_code}\n" https://robbor-cp-uttvga.fly.dev/ || true
echo "Open: https://robbor-cp-uttvga.fly.dev/"
