# Delhi AQI Forecasting — One-Hour-Ahead Prediction

## Project goal

Forecast next-hour Delhi Air Quality Index (AQI) from information available
at the current hour, using a frozen 73-feature contract and a selected set of
10 Delhi monitoring stations.

## Frozen model

The selected ensemble combines:
- Tuned Extra Trees: weight 0.594466
- Tuned Random Forest: weight 0.405534

Previously recorded final holdout metrics:
- MAE: 3.216121
- RMSE: 7.658390
- R²: 0.996634

The final holdout was kept separate from model selection. These historical
metrics are not evidence of current live-source performance.

## Deployment status

**Live production is blocked.** Offline inference and the local blocked-state
API checks passed, but a live source has not yet been validated to provide
the required pollutant history and leakage-free 73-feature vectors for all
frozen stations. The release gate must remain closed until source mapping,
freshness, feature parity, data-quality checks, and explicit release approval
are complete.

## Repository contents

This curated repository contains source code, notebooks with saved outputs
removed, the frozen feature/configuration files, deployment scaffold, offline
batch runner, selected handoff documents, and deployment audit records.

Large model artifacts, raw/processed datasets, checkpoints, archives, and
generated prediction files are intentionally excluded from Git. The model
artifacts must be obtained from a trusted storage location and verified against
the project's approved SHA256 manifest before use.

## Security and reproducibility

- Do not commit API tokens, credentials, private keys, or `.env` files.
- Keep the real release gate disabled until all required evidence is approved.
- Do not use the test-only release gate for production.
- Re-run the documented source, feature-contract, and deployment checks before
  any production release.

## Data and licensing

This repository does not redistribute the raw air-quality dataset. Verify the
data source's license and citation requirements before publishing data,
derived datasets, or this project publicly. Add an appropriate project license
only after confirming rights for all included material.
## Live T+1 Dashboard Demo (Colab)

The repository includes a Gradio dashboard notebook for demonstrating the
live next-hour forecasting workflow:

`notebooks/Delhi_AQI_Live_TPlus1_Dashboard_Demo.ipynb`

### Run the presentation demo

1. Open the notebook in Google Colab.
2. Ensure Google Drive contains the original `Delhi-AQI-Prediction` project
   directory, including the frozen model artifacts and deployment configuration.
3. Run the single launcher cell.
4. Select one of the ten supported Delhi stations and click
   **Predict Next-Hour AQI**.
5. The dashboard requests fresh hourly AQI snapshots, validates the live
   history, builds the frozen 73-feature input, and displays the Extra Trees,
   Random Forest, and final weighted ensemble predictions.

The launcher uses the original frozen models. It does not retrain them.

### Demo status and live-data limitation

**The dashboard is a live shadow demonstration, not a production deployment.**

The verified public station feed supplied AQI readings and observation
timestamps but did not supply the pollutant concentration measurements
required by the complete frozen model input. In the audited live feature frame
on 2026-10-29, 560 of 730 feature cells were missing (76.71%). The frozen
pipelines impute unavailable inputs, so the displayed forecast must not be
presented as a fully observed-input or production-validated forecast.

The production release gate remains disabled. The successful Colab demo does
not change the production status, and historical holdout metrics are not a
substitute for live end-to-end validation.

### Runtime and artifacts

The Gradio sharing URL is temporary and works only while the Colab runtime
remains active. Each Predict click requests new source history. The launcher
requires the original project and frozen model files in Google Drive.

Large model binaries, datasets, checkpoints, and prediction outputs are
intentionally excluded from GitHub. The demo notebook in this repository
contains no saved execution outputs.
