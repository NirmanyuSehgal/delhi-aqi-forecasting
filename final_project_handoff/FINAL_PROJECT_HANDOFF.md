# Delhi AQI t+1 Forecasting — Final Project Handoff

## Closure state

**Phase:** 16.84R
**Overall state:** OFFLINE FROZEN RELEASE COMPLETE / LIVE DEPLOYMENT BLOCKED

Created:
`2026-10-07T17:17:12.930578`

## Project objective

Predict `AQI_t_plus_1` one hour ahead using information available through time t.

## Frozen model scope

Final scope:
**10 Delhi stations**

Feature contract:
`delhi_aqi_73_features_v1`

Feature count:
**73**

Critical authoritative ordering:

- Position 41: `NO2_lag_12h`
- Position 42: `NOx_lag_12h`

No feature reordering, silent substitution, or contract modification is
permitted.

## Frozen ensemble

Tuned Extra Trees:
**0.594466**

Tuned Random Forest:
**0.405534**

Exact inference arithmetic:

`0.594466 × ExtraTrees + 0.405534 × RandomForest`

The component models were refit on TRAIN+VALIDATION.

FINAL_HOLDOUT remains untouched.

## Frozen data split

Feature file:

`/content/drive/MyDrive/Delhi-AQI-Prediction/data/processed/delhi_10_station_feature_engineered.parquet`

Split assignment file:

`/content/drive/MyDrive/Delhi-AQI-Prediction/outputs/reports/phase15_1_time_split_assignments.parquet`

Exact frozen split:

| Split | Rows |
|---|---:|
| TRAIN | 166,845 |
| VALIDATION | 69,097 |
| FINAL_HOLDOUT | 68,352 |
| UNUSED_GAP | 19 |
| TOTAL | 304,313 |

## Final holdout reference

FINAL_HOLDOUT:
**68,352 rows**

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

These metrics are frozen reference results.

No FINAL_HOLDOUT rows were used during the Phase 16.82R/16.83R release
validation.

## Deployment verification

Phase 16.82R passed:

- exact 73-feature contract
- exact feature ordering
- frozen split alignment
- frozen model loading
- Extra Trees inference
- Random Forest inference
- exact ensemble arithmetic
- valid-frame acceptance
- missing-feature rejection
- unexpected-feature rejection
- FINAL_HOLDOUT isolation

Offline smoke test:
**32 VALIDATION rows**

FINAL_HOLDOUT rows used:
**0**

Phase 16.83R then passed the final offline release audit and created the
frozen offline release package.

## Source / production status

Validated live production sources:
**0**

Production status:
**NO_VALIDATED_LIVE_AQI_SOURCE**

Production deployment:
**BLOCKED**

The following are explicitly not permitted as production substitutes:

- Open-Meteo
- AQICN / WAQI
- AQI surrogate
- AQI reconstruction
- silent feature substitution

The current source-discovery conclusion does not invalidate the offline model.
It means that the required live input vector has not been validated for
production use.

## Frozen model integrity

Extra Trees model:

`/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package/models/phase15_10_final_tuned_extra_trees_trainval.joblib`

Size:
**2505628019 bytes**

SHA256:
`f0b3d43a56a7d5e4f08554f37ff234e1b5e012b5d5d69f18c750844b36cbe72d`

Random Forest model:

`/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package/models/phase15_10_final_tuned_random_forest_trainval.joblib`

Size:
**494966579 bytes**

SHA256:
`538b5ff34152d19221518e831528093b7bcc57e2b05f82669718f540b514abd8`

## Deployment artifacts

Frozen model package:

`/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package`

Final deployment lock:

`/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_81R_final_deployment_lock`

Phase 16.82R smoke test:

`/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_81R_final_deployment_lock/phase16_82R_offline_smoke_test`

Phase 16.83R final release:

`/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_81R_final_deployment_lock/phase16_83R_final_release`

Phase 16.83R release manifest:

`/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_81R_final_deployment_lock/phase16_83R_final_release/phase16_83R_release_manifest.json`

Phase 16.83R handoff:

`/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_81R_final_deployment_lock/phase16_83R_final_release/FINAL_OFFLINE_HANDOFF.md`

Offline inference example:

`/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_81R_final_deployment_lock/phase16_83R_final_release/offline_inference_example.py`

Production guard:

`/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_81R_final_deployment_lock/production_source_guard.py`

## Safety state

Model touched:
**False**

Model retrained:
**False**

Model retuned:
**False**

Feature contract changed:
**False**

Production source changed:
**False**

Final holdout touched:
**False**

Holdout rows used:
**0**

## Current project conclusion

The ML development and offline deployment packaging are complete and frozen.

The remaining blocker is live production data sourcing. A future live deployment
must validate a source capable of supplying the complete frozen input vector
without changing the model, feature contract, or final holdout.

No model-development work should be reopened merely to bypass the current
production-source constraint.
