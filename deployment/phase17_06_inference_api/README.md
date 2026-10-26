# Delhi AQI t+1 Inference API — Phase 17.06A

## Current state

`NO_VALIDATED_LIVE_AQI_SOURCE` — production predictions are blocked.
This is deliberate. The previous OGD requests failed at the connection layer;
OpenAQ did not demonstrate coverage for the complete frozen input contract.

## Endpoints

- `GET /healthz`: process liveness.
- `GET /readyz`: production readiness; returns HTTP 503 while blocked.
- `POST /predict`: accepts a JSON object containing a `records` list, each with
  the exact frozen 73 features. Returns 503 until all release gates pass.
- Prediction requests require `Authorization: Bearer <API_BEARER_TOKEN>`
  after readiness is approved.

## Build

From the `deployment` directory, after confirming `.dockerignore` contains only
the frozen model package and this service folder, run:

```bash
docker build -f phase17_06_inference_api/Dockerfile -t delhi-aqi-inference:17.06A .
```

## Local container smoke test

```bash
docker run --rm -p 8080:8080 delhi-aqi-inference:17.06A
```

Then query `/healthz` and `/readyz`. Expected: health returns HTTP 200;
readiness returns HTTP 503 and `NO_VALIDATED_LIVE_AQI_SOURCE`.

## Required environment variables for a future approved deployment

- `LIVE_SOURCE_VALIDATED=true`
- `PRODUCTION_ENABLED=true`
- `API_BEARER_TOKEN` set as a platform secret

Both the environment flags and `release_gate.json` must be approved; setting
environment variables alone does not open the gate. Do not enable them until
the live data source and all 73 features are validated end to end.

## Critical limitation

This scaffold packages the serving layer. It does not fetch live AQI data or
construct lag/rolling features. It is not a completed live production system.
