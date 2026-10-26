# Delhi AQI t+1 Forecasting — Phase 16.83R Final Offline Release

## Release status

**OFFLINE FROZEN RELEASE — NOT LIVE PRODUCTION**

Release:
`phase16_83R_offline_frozen_release`

Created:
`2026-10-07T17:14:30.325333`

## Objective

Predict `AQI_t_plus_1` one hour ahead using information available through time t.

## Frozen model

Final weighted ensemble:

- Tuned Extra Trees: `0.594466`
- Tuned Random Forest: `0.405534`

Components were refit on TRAIN+VALIDATION.

FINAL_HOLDOUT remains untouched.

## Frozen feature contract

Contract:
`delhi_aqi_73_features_v1`

Feature count:
**73**

Critical ordering:

- Position 41: `NO2_lag_12h`
- Position 42: `NOx_lag_12h`

Authoritative contract:

`/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package/config/feature_contract.json`

## Frozen split

Split artifact:

`/content/drive/MyDrive/Delhi-AQI-Prediction/outputs/reports/phase15_1_time_split_assignments.parquet`

Counts:

- TRAIN: **166,845**
- VALIDATION: **69,097**
- FINAL_HOLDOUT: **68,352**
- UNUSED_GAP: **19**

## Offline validation

Phase 16.82R passed:

- exact 73-feature order
- frozen model loading
- Extra Trees inference
- Random Forest inference
- exact weighted ensemble arithmetic
- valid schema acceptance
- missing-feature rejection
- unexpected-feature rejection
- FINAL_HOLDOUT isolation

Smoke test:
**32 VALIDATION rows**

FINAL_HOLDOUT rows used:
**0**

## Frozen final holdout reference metrics

Rows:
**68,352**

MAE:
**3.216121**

RMSE:
**7.658390**

R²:
**0.996634**

±5 AQI:
**85.249883%**

±10 AQI:
**94.605864%**

±20 AQI:
**98.090765%**

These are frozen reference results and were not recomputed or used in Phase 16.83R.

## Model integrity

Extra Trees SHA256:
`f0b3d43a56a7d5e4f08554f37ff234e1b5e012b5d5d69f18c750844b36cbe72d`

Random Forest SHA256:
`538b5ff34152d19221518e831528093b7bcc57e2b05f82669718f540b514abd8`

The model files are referenced in place from the frozen deployment package and
are not duplicated into the release directory.

## Production status

Validated live production sources:
**0**

Production status:
**NO_VALIDATED_LIVE_AQI_SOURCE**

Production deployment:
**BLOCKED**

Forbidden substitutions:

- Open-Meteo
- AQICN / WAQI
- AQI surrogate
- AQI reconstruction
- silent feature substitution

## Deployment boundary

The frozen models are valid for offline inference with the exact 73-feature
contract.

Live production requires a separately validated source capable of supplying
the complete required input vector without modifying the model or feature
contract.

## Important paths

Frozen deployment package:

`/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package`

Final deployment lock:

`/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_81R_final_deployment_lock`

Phase 16.82R smoke-test artifacts:

`/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_81R_final_deployment_lock/phase16_82R_offline_smoke_test`

Phase 16.83R release directory:

`/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_81R_final_deployment_lock/phase16_83R_final_release`

Release manifest:

`/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_81R_final_deployment_lock/phase16_83R_final_release/phase16_83R_release_manifest.json`

Production guard:

`/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_81R_final_deployment_lock/production_source_guard.py`

## Safety state

Model touched: **False**

Model retrained: **False**

Model retuned: **False**

Feature contract changed: **False**

Production source changed: **False**

Final holdout touched: **False**

Holdout rows used: **0**
