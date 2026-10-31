# Robbor CP — Fly.io fix

## Symptoms
- `fly deploy --image ...` reported success
- Machines ended in **stopped** state
- `https://robbor-cp-uttvga.fly.dev/` did not respond

## Root causes
1. **CMD was `fastapi run`** with no host/port — in containers this often binds to `127.0.0.1` only, so Fly Proxy cannot reach the app.
2. **`auto_stop_machines = stop` + `min_machines_running = 0`** — machines stop when idle; combined with a bad bind, the service never becomes reachable.
3. Deploy used **`--image`** so a broken image was re-pushed without rebuilding the Dockerfile.

## Fixes in this package
- `CMD` uses `uvicorn main:app --host 0.0.0.0 --port 8000`
- Health check on `/health`
- `auto_stop_machines = "off"` and `min_machines_running = 1` for always-on demo/production
- `DEPLOY.sh` forces a **Dockerfile rebuild** (no `--image`)

## Deploy
```bash
unzip robbor-cp-fly-fix.zip
cd robbor-cp-fly-fix
./DEPLOY.sh
# or:
fly deploy -a robbor-cp-uttvga --config fly.toml --wait-timeout 10m
```

Verify:
```bash
curl -s https://robbor-cp-uttvga.fly.dev/health
curl -s https://robbor-cp-uttvga.fly.dev/api/v1/summary
open https://robbor-cp-uttvga.fly.dev/
```

## Local / other clouds
```bash
docker compose up --build -d
curl http://127.0.0.1:8000/health
```
