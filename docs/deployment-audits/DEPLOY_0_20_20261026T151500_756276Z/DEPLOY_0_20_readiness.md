# DEPLOY-0.20 — Consolidated Readiness Report

**Overall status:** OFFLINE_BATCH_VERIFIED_LIVE_DEPLOYMENT_BLOCKED

## Verified

- Offline batch runner: PASS
- Rows predicted: 17
- Stations represented in this validation sample: 6
- Feature contract: 73 features, exact ordered match
- Repeated-prediction maximum absolute difference: 1.13686837721616e-13
- Repeatability tolerance: 1e-10 — PASS
- Final holdout rows used: 0
- Model retraining or retuning: not performed
- Production enabled: **False**

## Remaining blocker

A valid live source and its complete feature-building path have not been demonstrated against the frozen contract. An AQI-only response does not supply the required pollutant inputs and feature history.

Before production activation, validate source coverage and station mapping, hourly freshness, feature parity, data-quality gates, and the release gate. Production must remain disabled until those checks pass and activation is explicitly authorized.

## Main evidence files

- Batch audit: `/content/drive/MyDrive/Delhi-AQI-Prediction/outputs/deployment_candidates/phase17_07_cli_smoke_inprocess_20261026T143835_062129Z/deploy_0_19_audit.json`
- Predictions: `/content/drive/MyDrive/Delhi-AQI-Prediction/outputs/deployment_candidates/phase17_07_cli_smoke_inprocess_20261026T143835_062129Z/batch_predictions.parquet`
- Batch diagnostics: `/content/drive/MyDrive/Delhi-AQI-Prediction/outputs/deployment_candidates/phase17_07_cli_smoke_inprocess_20261026T143835_062129Z/batch_predictions.diagnostics.json`
- Frozen feature contract: `/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package/config/feature_contract.json`
- Offline candidate runner: `/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/releases/phase17_07_offline_batch_candidate_20261026T143528_100244Z/src/batch_predict.py`
- Source status: `/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package/config/source_status.json`
- Prior final readiness record: `/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_81R_final_deployment_lock/phase16_81R_final_readiness.json`
