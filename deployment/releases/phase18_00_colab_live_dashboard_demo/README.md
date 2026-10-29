# Phase18 00 Colab Live Dashboard Demo

## Purpose

This release adds a Colab/Gradio presentation demo for the Delhi AQI
one-hour-ahead (`AQI_t_plus_1`) frozen ensemble.

## Included

- `notebooks/Delhi_AQI_Live_TPlus1_Dashboard_Demo.ipynb` — clean, two-cell notebook with a single-cell launcher.
- `deployment/phase17_06_inference_api/src/shadow_live.py` — live snapshot
  retrieval, station mapping, timestamp/history checks, and shadow flow.
- `deployment/phase17_06_inference_api/src/canonical_aqi_features.py` —
  canonical feature construction.
- `deployment/phase17_06_inference_api/src/frozen_aqi_inference_missing_aware_candidate.py`
  — frozen model loading, feature validation, and weighted ensemble inference.

## Running the demo

Open `notebooks/Delhi_AQI_Live_TPlus1_Dashboard_Demo.ipynb` in Google Colab and run its launcher cell. The user's
Google Drive must contain the original `Delhi-AQI-Prediction` project folder
with the approved frozen model artifacts and configuration files.

On each Predict click, the application attempts to retrieve fresh source
history, builds the frozen 73-feature input, and shows the two component
predictions and final weighted ensemble forecast.

## Status

**DEMO / SHADOW ONLY — NOT PRODUCTION**

The official station feed observed during the demo checks exposed AQI readings
and observation timestamps but did not expose the pollutant concentration
inputs required by the complete model feature contract. On the audited frame
from 2026-10-29, 560 of 730 feature cells (76.71%) were missing and were
handled by the frozen pipelines' fitted imputers.

This is a presentation/demo result, not evidence of production readiness.
The production release gate is unchanged and remains disabled.

## Excluded

The original model binaries, raw and processed datasets, generated forecasts,
credentials, and runtime state are not included in this release.

The share URL produced by Gradio is temporary and depends on the Colab runtime.
