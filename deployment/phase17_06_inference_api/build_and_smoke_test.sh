#!/usr/bin/env bash
set -euo pipefail

DEPLOY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SERVICE_DIR="$DEPLOY_DIR/phase17_06_inference_api"
IMAGE_TAG="${1:-delhi-aqi-inference:17.06D}"
CONTAINER_NAME="delhi-aqi-smoke-$$"
HOST_PORT="${HOST_PORT:-18765}"

command -v docker >/dev/null 2>&1 || { echo "ERROR: Docker CLI not found."; exit 10; }
docker info >/dev/null 2>&1 || { echo "ERROR: Docker daemon unavailable."; exit 11; }

echo "[1/4] Building image: $IMAGE_TAG"
docker build -f "$SERVICE_DIR/Dockerfile" -t "$IMAGE_TAG" "$DEPLOY_DIR"

cleanup() { docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true; }
trap cleanup EXIT

echo "[2/4] Starting container with production disabled"
docker run -d --name "$CONTAINER_NAME" \
  -e LIVE_SOURCE_VALIDATED=false \
  -e PRODUCTION_ENABLED=false \
  -p "127.0.0.1:${HOST_PORT}:8080" \
  "$IMAGE_TAG" >/dev/null

echo "[3/4] Checking health and readiness endpoints"
python - "$HOST_PORT" <<'PYCODE'
import json, sys, time, urllib.request, urllib.error
port = int(sys.argv[1])
base = f"http://127.0.0.1:{port}"
health = None
last_error = None
for _ in range(45):
    try:
        with urllib.request.urlopen(base + "/healthz", timeout=2) as response:
            health = (response.status, json.loads(response.read().decode()))
        break
    except Exception as exc:
        last_error = exc
        time.sleep(1)
if health is None:
    raise SystemExit(f"FAIL: /healthz unavailable: {last_error}")
assert health[0] == 200 and health[1].get("status") == "alive", health
try:
    urllib.request.urlopen(base + "/readyz", timeout=5)
    raise SystemExit("FAIL: /readyz unexpectedly returned HTTP 200")
except urllib.error.HTTPError as exc:
    body = json.loads(exc.read().decode())
    assert exc.code == 503, (exc.code, body)
    assert body.get("status") == "NO_VALIDATED_LIVE_AQI_SOURCE", body
print("PASS: /healthz HTTP 200")
print("PASS: /readyz HTTP 503; production correctly blocked")
PYCODE

echo "[4/4] Container build and blocked-readiness smoke test passed"
echo "Image: $IMAGE_TAG"
echo "Production has NOT been enabled."
