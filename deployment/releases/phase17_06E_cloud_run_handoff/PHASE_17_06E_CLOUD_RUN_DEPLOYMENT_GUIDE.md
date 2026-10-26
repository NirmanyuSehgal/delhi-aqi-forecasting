# Phase 17.06E — Cloud Run Staging Handoff

## Current status

- Local API smoke: passed.
- API-to-frozen-model integration: passed.
- Frozen model hashes: verified.
- Production: blocked with `NO_VALIDATED_LIVE_AQI_SOURCE`.
- This deployment is private and readiness-blocked; it is not an approved live predictor.

## Files needed

- Existing base release ZIP: `/content/gdrive/MyDrive/Delhi-AQI-Prediction/deployment/releases/phase17_03L_offline_release/Delhi-AQI-Prediction_phase17_03L_offline_release.zip`
- Small overlay ZIP: `/content/gdrive/MyDrive/Delhi-AQI-Prediction/deployment/releases/phase17_06E_cloud_run_handoff/phase17_06E_cloud_run_overlay.zip`

The base archive contains the frozen model package. The overlay supplies the current
API files and Cloud Run build/deploy configuration.

## Build and deploy using Google Cloud Shell

1. Download the base release ZIP from Google Drive to your computer.
2. Upload the base ZIP and the overlay ZIP into a new Cloud Shell working folder.
3. From that folder, run the following commands, substituting the uploaded filenames:

```bash
mkdir -p ~/delhi-aqi-cloudrun/work
cd ~/delhi-aqi-cloudrun/work
unzip -q /path/to/Delhi-AQI-Prediction_phase17_03L_offline_release.zip \
  'Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package/*' -d .
unzip -oq /path/to/phase17_06E_cloud_run_overlay.zip -d .
cd Delhi-AQI-Prediction/deployment
export GCP_PROJECT_ID='YOUR_GOOGLE_CLOUD_PROJECT_ID'
export GCP_REGION='asia-south1'
bash phase17_06_inference_api/deploy_to_cloud_run_staging.sh
```

4. The script enables the required Google Cloud APIs and asks Cloud Build to build
   the Docker image remotely. Local Docker is not required.

## Verify the private service

After deployment, use an identity with Cloud Run Invoker permission. Retrieve the
service URL with:

```bash
gcloud run services describe delhi-aqi-inference \
  --region asia-south1 --format='value(status.url)'
```

Request the health endpoint with a Google identity token:

```bash
SERVICE_URL=$(gcloud run services describe delhi-aqi-inference \
  --region asia-south1 --format='value(status.url)')
TOKEN=$(gcloud auth print-identity-token)
curl -i -H "Authorization: Bearer $TOKEN" "$SERVICE_URL/healthz"
curl -i -H "Authorization: Bearer $TOKEN" "$SERVICE_URL/readyz"
```

Expected: `/healthz` returns HTTP 200. `/readyz` returns HTTP 503 with
`NO_VALIDATED_LIVE_AQI_SOURCE`. This is the intended staging state.

## Important

- Cloud Run builds and running instances may incur charges.
- Use private access; do not configure unauthenticated access for this staging service.
- Do not set `LIVE_SOURCE_VALIDATED=true` or `PRODUCTION_ENABLED=true`.
- The model still requires real station-aligned values plus historical buffers for AQI
  lag/rolling features before production predictions can be enabled.
- No final holdout data is needed for this deployment handoff.
