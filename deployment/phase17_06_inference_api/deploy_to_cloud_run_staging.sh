#!/usr/bin/env bash
set -euo pipefail

# Run this script from the deployment directory.
# It deploys a private, readiness-blocked Cloud Run service.

: "${GCP_PROJECT_ID:?Set GCP_PROJECT_ID to your Google Cloud project ID first}"
GCP_REGION="${GCP_REGION:-asia-south1}"
SERVICE_NAME="${SERVICE_NAME:-delhi-aqi-inference}"

test -d "phase16_33_frozen_model_package" || {
  echo "ERROR: Run this script from the deployment directory."
  exit 2
}
test -f "Dockerfile" || {
  echo "ERROR: Root Dockerfile missing."
  exit 3
}
test -f "phase17_06_inference_api/release_gate.json" || {
  echo "ERROR: Release gate missing."
  exit 4
}

python - <<'PYCODE'
import json
with open("phase17_06_inference_api/release_gate.json", "r", encoding="utf-8") as f:
    gate = json.load(f)
assert gate.get("production_enabled") is False, "Production gate must remain disabled"
assert gate.get("live_source_validated") is False, "Live source must remain unvalidated"
print("PASS: deployment gate is closed.")
PYCODE

gcloud config set project "$GCP_PROJECT_ID"

gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  --project "$GCP_PROJECT_ID"

# Cloud Build builds remotely from this directory; local Docker is not needed.
# No unauthenticated access; production readiness remains disabled.
gcloud run deploy "$SERVICE_NAME" \
  --source . \
  --project "$GCP_PROJECT_ID" \
  --region "$GCP_REGION" \
  --no-allow-unauthenticated \
  --port 8080 \
  --cpu 2 \
  --memory 4Gi \
  --timeout 300 \
  --min 0 \
  --max 1 \
  --set-env-vars="LIVE_SOURCE_VALIDATED=false,PRODUCTION_ENABLED=false"

echo
echo "Deployment command completed."
echo "Verify /healthz and /readyz using an authenticated Cloud Run request."
echo "Expected /healthz: HTTP 200."
echo "Expected /readyz: HTTP 503 NO_VALIDATED_LIVE_AQI_SOURCE."
echo "Production predictions must remain disabled."
