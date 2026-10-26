# DEPLOY-0.21 — Static Serving API and Release-Gate Audit

**Created (UTC):** 2026-10-26T15:35:45.964511+00:00

- Audit mode: read-only static inspection
- Models loaded: No
- Service started: No
- Production activation attempted: No
- Files inspected: 32
- Python syntax failures: 0

## Inspected source and configuration findings

### `deployment/phase16_81R_final_deployment_lock/phase16_81R_final_readiness.json`
- Static Python syntax: not_applicable
- SHA256: `b3ae978f3340ac889377ce86e6c1f94635e0134e209ceab726fd88aa1bffc948`
- Matching lines: 16
  - L25: `    "production_status": "NO_VALIDATED_LIVE_AQI_SOURCE",`
  - L29: `        "production_ready": false,`
  - L34: `        "production_ready": false,`
  - L35: `        "reason": "Official API access was blocked from Colab at the network layer; production capability was not validated."`
  - L39: `        "production_ready": false,`
  - L40: `        "reason": "Current CPCB production data route was not confirmed from the deployment environment."`
  - L44: `        "production_ready": false,`
  - L49: `        "production_ready": false,`
  - L54: `        "production_ready": false,`
  - L59: `        "production_ready": false,`
  - L64: `        "production_ready": false,`
  - L69: `  "production_lock": {`
  - L70: `    "production_enabled": false,`
  - L72: `    "reason": "No validated live source currently supplies the complete frozen 73-feature vector with compatible station/AQI provenance.",`
  - L87: `    "production_source_changed": false,`
  - L88: `    "feature_contract_changed": false,`

### `deployment/phase16_81R_final_deployment_lock/phase16_82R_offline_smoke_test/phase16_82R_offline_inference_smoke_test.json`
- Static Python syntax: not_applicable
- SHA256: `5018e0e1e1306be0bbd3237487d48307b36c8869cdd0259481ee1ee2c5894d1c`
- Matching lines: 7
  - L12: `  "feature_path": "/content/drive/MyDrive/Delhi-AQI-Prediction/data/processed/delhi_10_station_feature_engineered.parquet",`
  - L13: `  "split_path": "/content/drive/MyDrive/Delhi-AQI-Prediction/outputs/reports/phase15_1_time_split_assignments.parquet",`
  - L30: `    "missing_feature_rejected": true,`
  - L33: `  "production_status": "NO_VALIDATED_LIVE_AQI_SOURCE",`
  - L34: `  "production_enabled": false,`
  - L38: `  "feature_contract_changed": false,`
  - L39: `  "production_source_changed": false,`

### `deployment/phase16_81R_final_deployment_lock/phase16_83R_final_release/FINAL_OFFLINE_HANDOFF.md`
- Static Python syntax: not_applicable
- SHA256: `4167c48a798567ac82f321f8a31aadd90ee9bf27a7f99203b5532115b7081c3d`
- Matching lines: 20
  - L5: `**OFFLINE FROZEN RELEASE — NOT LIVE PRODUCTION**`
  - L15: `Predict `AQI_t_plus_1` one hour ahead using information available through time t.`
  - L28: `## Frozen feature contract`
  - L43: ``/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package/config/feature_contract.json``
  - L49: ``/content/drive/MyDrive/Delhi-AQI-Prediction/outputs/reports/phase15_1_time_split_assignments.parquet``
  - L68: `- missing-feature rejection`
  - L114: `## Production status`
  - L116: `Validated live production sources:`
  - L119: `Production status:`
  - L122: `Production deployment:`
  - L138: `Live production requires a separately validated source capable of supplying`
  - L146: ``/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package``
  - L150: ``/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_81R_final_deployment_lock``
  - L154: ``/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_81R_final_deployment_lock/phase16_82R_offline_smoke_test``
  - L158: ``/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_81R_final_deployment_lock/phase16_83R_final_release``
  - L162: ``/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_81R_final_deployment_lock/phase16_83R_final_release/phase16_83R_release_manifest.json``
  - L164: `Production guard:`
  - L166: ``/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_81R_final_deployment_lock/production_source_guard.py``
  - L176: `Feature contract changed: **False**`
  - L178: `Production source changed: **False**`

### `deployment/phase16_81R_final_deployment_lock/phase16_83R_final_release/PROJECT_STATUS_PHASE16_83R_FINAL.json`
- Static Python syntax: not_applicable
- SHA256: `741b49347a3f6438281f4267d292e6c0b8c5e6e106763f4d3bd550d24ffad792`
- Matching lines: 10
  - L6: `  "live_production_ready": false,`
  - L7: `  "production_status": "NO_VALIDATED_LIVE_AQI_SOURCE",`
  - L8: `  "validated_live_sources": 0,`
  - L9: `  "feature_contract_verified": true,`
  - L22: `  "feature_contract_changed": false,`
  - L23: `  "production_source_changed": false,`
  - L25: `  "release_manifest": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_81R_final_deployment_lock/phase16_83R_final_release/phase16_83R_release_manifest.json",`
  - L26: `  "handoff_document": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_81R_final_deployment_lock/phase16_83R_final_release/FINAL_OFFLINE_HANDOFF.md",`
  - L27: `  "offline_example": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_81R_final_deployment_lock/phase16_83R_final_release/offline_inference_example.py",`
  - L28: `  "next_state": "Offline frozen release complete. Live production remains blocked."`

### `deployment/phase16_81R_final_deployment_lock/phase16_83R_final_release/offline_inference_example.py`
- Static Python syntax: PASS
- SHA256: `5067bcb847ab4da6119596b3513518ddde653d5864f4ecc02982e1b9424a5065`
- Matching lines: 10
  - L11: `PROJECT_ROOT = Path("/content/drive/MyDrive/Delhi-AQI-Prediction")`
  - L12: `PACKAGE = Path("/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package")`
  - L15: `    PACKAGE / "config" / "feature_contract.json",`
  - L32: `def predict_frozen_ensemble(`
  - L38: `            "Input does not exactly match the frozen 73-feature contract."`
  - L48: `        ET.predict(X),`
  - L53: `        RF.predict(X),`
  - L62: `# Production is intentionally disabled.`
  - L63: `# prediction = predict_frozen_ensemble(X)`
  - L64: `# print(prediction)`

### `deployment/phase16_81R_final_deployment_lock/phase16_83R_final_release/phase16_83R_release_manifest.json`
- Static Python syntax: not_applicable
- SHA256: `4fe63bbaa3caebfa8501415942284f8c93898d7a5deac0e6d17d31c6d4a06459`
- Matching lines: 18
  - L5: `  "objective": "Predict AQI_t_plus_1 one hour ahead using information available through time t.",`
  - L8: `  "feature_contract": {`
  - L13: `    "path": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package/config/feature_contract.json"`
  - L24: `      "path": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package/models/phase15_10_final_tuned_extra_trees_trainval.joblib",`
  - L29: `      "path": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package/models/phase15_10_final_tuned_random_forest_trainval.joblib",`
  - L35: `    "feature_file": "/content/drive/MyDrive/Delhi-AQI-Prediction/data/processed/delhi_10_station_feature_engineered.parquet",`
  - L36: `    "split_file": "/content/drive/MyDrive/Delhi-AQI-Prediction/outputs/reports/phase15_1_time_split_assignments.parquet",`
  - L50: `    "validator_missing_feature_rejection": true,`
  - L64: `  "production": {`
  - L66: `    "enabled": false,`
  - L67: `    "validated_live_sources": 0,`
  - L79: `    "feature_contract_changed": false,`
  - L80: `    "production_source_changed": false,`
  - L85: `    "inference_module": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package/src/frozen_aqi_inference.py",`
  - L86: `    "production_guard": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_81R_final_deployment_lock/production_source_guard.py",`
  - L87: `    "phase16_82r_smoke_predictions": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_81R_final_deployment_lock/phase16_82R_offline_smoke_test/phase16_82R_validation_smoke_predictions.parquet",`
  - L88: `    "phase16_82r_diagnostics": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_81R_final_deployment_lock/phase16_82R_offline_smoke_test/phase16_82R_offline_inference_smoke_test.json"`
  - L90: `  "release_note": "Offline frozen-model release only. Live production remains blocked because no validated live source currently supplies the complete frozen input vector."`

### `deployment/phase16_81R_final_deployment_lock/production_source_guard.py`
- Static Python syntax: PASS
- SHA256: `06e80b9287cb4850d4d6e121b92689dc118efc320d750da8744933e74d5795f7`
- Matching lines: 9
  - L2: `Frozen Delhi AQI production-source guard.`
  - L4: `Live production inference remains blocked until a validated`
  - L8: `PRODUCTION_SOURCE_STATUS = "NO_VALIDATED_LIVE_AQI_SOURCE"`
  - L12: `class ProductionSourceBlocked(RuntimeError):`
  - L16: `def assert_production_source_ready():`
  - L18: `        PRODUCTION_SOURCE_STATUS`
  - L19: `        != "VALIDATED_LIVE_SOURCE_AVAILABLE"`
  - L21: `        raise ProductionSourceBlocked(`
  - L31: `    assert_production_source_ready()`

### `deployment/phase17_06_inference_api/CLOUD_RUN_DEPLOYMENT_HANDOFF.md`
- Static Python syntax: not_applicable
- SHA256: `89ed286d65e12c47a646254922d96946d3ec617d26363d1d8951d4862edefc7c`
- Matching lines: 14
  - L8: `- Production: blocked with `NO_VALIDATED_LIVE_AQI_SOURCE`.`
  - L9: `- This deployment is private and readiness-blocked; it is not an approved live predictor.`
  - L13: `- Existing base release ZIP: `/content/gdrive/MyDrive/Delhi-AQI-Prediction/deployment/releases/phase17_03L_offline_release/Delhi-AQI-Prediction_phase17_03L_offline_release.zip``
  - L14: `- Small overlay ZIP: `/content/gdrive/MyDrive/Delhi-AQI-Prediction/deployment/releases/phase17_06E_cloud_run_handoff/phase17_06E_cloud_run_overlay.zip``
  - L28: `unzip -q /path/to/Delhi-AQI-Prediction_phase17_03L_offline_release.zip \`
  - L29: `  'Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package/*' -d .`
  - L31: `cd Delhi-AQI-Prediction/deployment`
  - L50: `Request the health endpoint with a Google identity token:`
  - L55: `TOKEN=$(gcloud auth print-identity-token)`
  - L56: `curl -i -H "Authorization: Bearer $TOKEN" "$SERVICE_URL/healthz"`
  - L57: `curl -i -H "Authorization: Bearer $TOKEN" "$SERVICE_URL/readyz"`
  - L60: `Expected: `/healthz` returns HTTP 200. `/readyz` returns HTTP 503 with`
  - L67: `- Do not set `LIVE_SOURCE_VALIDATED=true` or `PRODUCTION_ENABLED=true`.`
  - L69: `  lag/rolling features before production predictions can be enabled.`

### `deployment/phase17_06_inference_api/Dockerfile`
- Static Python syntax: not_applicable
- SHA256: `26070904646394b791f575dfa2c9dcc62ee0fdff6db0c18d516e6b55c4786b18`
- Matching lines: 1
  - L6: `    RELEASE_GATE_FILE=/app/phase17_06_inference_api/release_gate.json`

### `deployment/phase17_06_inference_api/README.md`
- Static Python syntax: not_applicable
- SHA256: `8176ae7d4f0a500be85c6ad410fa6972534e59a61423f54ed5b3e2ebc7b66ea1`
- Matching lines: 14
  - L5: ``NO_VALIDATED_LIVE_AQI_SOURCE` — production predictions are blocked.`
  - L11: `- `GET /healthz`: process liveness.`
  - L12: `- `GET /readyz`: production readiness; returns HTTP 503 while blocked.`
  - L13: `- `POST /predict`: accepts a JSON object containing a `records` list, each with`
  - L14: `  the exact frozen 73 features. Returns 503 until all release gates pass.`
  - L15: `- Prediction requests require `Authorization: Bearer <API_BEARER_TOKEN>``
  - L16: `  after readiness is approved.`
  - L33: `Then query `/healthz` and `/readyz`. Expected: health returns HTTP 200;`
  - L34: `readiness returns HTTP 503 and `NO_VALIDATED_LIVE_AQI_SOURCE`.`
  - L38: `- `LIVE_SOURCE_VALIDATED=true``
  - L39: `- `PRODUCTION_ENABLED=true``
  - L40: `- `API_BEARER_TOKEN` set as a platform secret`
  - L42: `Both the environment flags and `release_gate.json` must be approved; setting`
  - L49: `construct lag/rolling features. It is not a completed live production system.`

### `deployment/phase17_06_inference_api/app.py`
- Static Python syntax: PASS
- SHA256: `94cdee5df4edb8d0fee5cf35c38a5cbb822a69f0cbccd09b7516abb72b15f194`
- Matching lines: 48
  - Route decorator L89: `@app.get("/")`
  - Route decorator L98: `@app.get("/healthz")`
  - Route decorator L106: `@app.get("/readyz")`
  - Route decorator L120: `@app.post("/predict")`
  - L26: `    os.environ.get("RELEASE_GATE_FILE", str(SERVICE_DIR / "release_gate.json"))`
  - L28: `CONTRACT_FILE = PACKAGE_DIR / "config" / "feature_contract.json"`
  - L34: `    raise RuntimeError("Frozen feature contract must contain 73 unique columns.")`
  - L40: `PREDICTION_COLUMNS = [`
  - L53: `    description="Frozen 73-feature ensemble with a fail-closed production gate.",`
  - L56: `def get_readiness():`
  - L64: `        reasons.append("release_gate_unavailable")`
  - L66: `    if gate.get("live_source_validated") is not True:`
  - L67: `        reasons.append("live_source_not_validated_in_release_gate")`
  - L68: `    if gate.get("production_enabled") is not True:`
  - L69: `        reasons.append("production_disabled_in_release_gate")`
  - L71: `    if os.environ.get("LIVE_SOURCE_VALIDATED", "false").lower() != "true":`
  - L72: `        reasons.append("LIVE_SOURCE_VALIDATED_environment_flag_not_true")`
  - L73: `    if os.environ.get("PRODUCTION_ENABLED", "false").lower() != "true":`
  - L74: `        reasons.append("PRODUCTION_ENABLED_environment_flag_not_true")`
  - L75: `    if not os.environ.get("API_BEARER_TOKEN", "").strip():`
  - L76: `        reasons.append("API_BEARER_TOKEN_not_configured")`
  - L94: `        "production_enabled": False,`
  - L95: `        "message": "Use /healthz for liveness and /readyz for readiness.",`
  - L98: `@app.get("/healthz")`
  - L99: `def healthz():`
  - L103: `        "production_enabled": False,`
  - L106: `@app.get("/readyz")`
  - L107: `def readyz():`
  - L108: `    ready, reasons = get_readiness()`
  - L116: `            "production_enabled": ready,`
  - L120: `@app.post("/predict")`
  - L121: `async def predict(request: Request):`
  - L123: `    ready, reasons = get_readiness()`
  - L128: `                "error": "production_predictions_blocked",`
  - L134: `    token = os.environ.get("API_BEARER_TOKEN", "").strip()`
  - L136: `    supplied = auth[7:].strip() if auth.lower().startswith("bearer ") else ""`
  - L138: `    if not token or not supplied or not secrets.compare_digest(supplied, token):`
  - L139: `        raise HTTPException(status_code=401, detail="Valid bearer token required.")`
  - L168: `                "error": "feature_contract_mismatch",`
  - L169: `                "missing_features": missing,`
  - L176: `    X["StationId"] = X["StationId"].astype(str)`
  - L178: `    invalid_stations = sorted(set(X["StationId"].dropna()) - ALLOWED_STATIONS)`
  - L179: `    if X["StationId"].isna().any() or invalid_stations:`
  - L183: `                "error": "invalid_station_id",`
  - L184: `                "invalid_station_ids": invalid_stations,`
  - L188: `    numeric_features = [c for c in FEATURE_ORDER if c != "StationId"]`
  - L209: `        pred = inference.predict_aqi(X)`
  - L210: `        missing_outputs = [c for c in PREDICTION_COLUMNS if c not in pred.columns]`
  - L215: `        for _, row in pred[PREDICTION_COLUMNS].iterrows():`

### `deployment/phase17_06_inference_api/phase17_06A_scaffold_manifest.json`
- Static Python syntax: not_applicable
- SHA256: `be37ee14760bb9995cfddc826bb611268b23b8b0ed98fd9bc5a27b6640b805fb`
- Matching lines: 7
  - L4: `  "decision": "SERVING_SCAFFOLD_CREATED_PRODUCTION_BLOCKED",`
  - L5: `  "project_root": "/content/gdrive/MyDrive/Delhi-AQI-Prediction",`
  - L18: `  "frozen_feature_contract_sha256": "cab75c26df1290defff2d5093ffab1b1f43c3c653340317c4d109d99930a8e0d",`
  - L40: `    "deployment/phase17_06_inference_api/release_gate.json": {`
  - L46: `  "live_source_validated": false,`
  - L47: `  "production_enabled": false,`
  - L48: `  "production_status": "NO_VALIDATED_LIVE_AQI_SOURCE",`

### `deployment/phase17_06_inference_api/release_gate.json`
- Static Python syntax: not_applicable
- SHA256: `33b7ab29ca6fda438baa2bb0c2cb142e8307090fe3260b56aa718026e6c116f9`
- Matching lines: 5
  - L3: `  "feature_contract_count": 73,`
  - L4: `  "frozen_feature_contract_sha256": "cab75c26df1290defff2d5093ffab1b1f43c3c653340317c4d109d99930a8e0d",`
  - L9: `  "live_source_validated": false,`
  - L10: `  "production_enabled": false,`
  - L14: `    "Verified mapping from each of the ten frozen stations to source station IDs",`

### `deployment/releases/phase17_03L_offline_release/phase17_03L_release_bundle_verification.json`
- Static Python syntax: not_applicable
- SHA256: `4629b013e23add67388e3bb571acb2169d84ced37d542fccb6fa91c5e9e04d91`
- Matching lines: 4
  - L4: `  "archive": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/releases/phase17_03L_offline_release/Delhi-AQI-Prediction_phase17_03L_offline_release.zip",`
  - L12: `  "full_validation_prediction_max_abs_differences": {`
  - L20: `  "production_enabled": false,`
  - L21: `  "production_status": "NO_VALIDATED_LIVE_AQI_SOURCE",`

### `deployment/releases/phase17_03L_offline_release/phase17_03M_safe_release_cleanup_report.json`
- Static Python syntax: not_applicable
- SHA256: `f1a6d5c322a63e715c98814768688f7da283c12c153ad38156d81feeefcba2fa`
- Matching lines: 3
  - L4: `  "release_archive": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/releases/phase17_03L_offline_release/Delhi-AQI-Prediction_phase17_03L_offline_release.zip",`
  - L13: `  "production_enabled": false,`
  - L14: `  "production_status": "NO_VALIDATED_LIVE_AQI_SOURCE"`

### `deployment/releases/phase17_03L_offline_release/phase17_03N_final_release_handoff/PHASE_17_03N_FINAL_RELEASE_HANDOFF.md`
- Static Python syntax: not_applicable
- SHA256: `88cbe0257efaf1cb112fad750a39c7d113c43b3bc96aac6a94dcd337e7846213`
- Matching lines: 6
  - L7: `- Release ZIP: `/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/releases/phase17_03L_offline_release/Delhi-AQI-Prediction_phase17_03L_offline_release.zip``
  - L13: `- Production enabled: **False**`
  - L14: `- Production status: `NO_VALIDATED_LIVE_AQI_SOURCE``
  - L17: `Passed: Phase 17.03I/L/M explicitly report NO_VALIDATED_LIVE_AQI_SOURCE with production_enabled=false, and the source config contains no explicit positive readiness signal. The config is not required to repeat the exact runtime status string.`
  - L21: `Audit JSON: `/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/releases/phase17_03L_offline_release/phase17_03N_final_release_handoff/phase17_03N_final_release_audit.json``
  - L22: `Repair evidence: `/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/releases/phase17_03L_offline_release/phase17_03N_final_release_handoff/phase17_03N_R1_source_gate_audit_repair.json``

### `deployment/releases/phase17_03L_offline_release/phase17_03N_final_release_handoff/phase17_03N_R1_source_gate_audit_repair.json`
- Static Python syntax: not_applicable
- SHA256: `98d798d47e2d43a8618365a45da0f73ee4f089446f61339180ab7cbbeeb6c0f5`
- Matching lines: 12
  - L8: `      "production_status": "NO_VALIDATED_LIVE_AQI_SOURCE",`
  - L9: `      "production_enabled": false`
  - L12: `      "production_status": "NO_VALIDATED_LIVE_AQI_SOURCE",`
  - L13: `      "production_enabled": false`
  - L16: `      "production_status": "NO_VALIDATED_LIVE_AQI_SOURCE",`
  - L17: `      "production_enabled": false`
  - L20: `      "production_status": "NO_VALIDATED_LIVE_AQI_SOURCE",`
  - L21: `      "production_enabled": false`
  - L25: `  "source_config_true_production_flags": [],`
  - L26: `  "details": "Passed: Phase 17.03I/L/M explicitly report NO_VALIDATED_LIVE_AQI_SOURCE with production_enabled=false, and the source config contains no explicit positive readiness signal. The config is not required to repeat the exact runtime status string.",`
  - L27: `  "production_enabled": false,`
  - L28: `  "production_status": "NO_VALIDATED_LIVE_AQI_SOURCE"`

### `deployment/releases/phase17_03L_offline_release/phase17_03N_final_release_handoff/phase17_03N_final_release_audit.json`
- Static Python syntax: not_applicable
- SHA256: `b7c84f4b12f51d6368858a11ca8b4d87eea3541c3ec504cdc4968ee31d91f187`
- Matching lines: 44
  - L9: `      "detail": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/releases/phase17_03L_offline_release/Delhi-AQI-Prediction_phase17_03L_offline_release.zip"`
  - L13: `      "detail": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/releases/phase17_03L_offline_release/phase17_03L_release_bundle_verification.json"`
  - L17: `      "detail": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/releases/phase17_03L_offline_release/phase17_03M_safe_release_cleanup_report.json"`
  - L21: `      "detail": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package/config/source_status.json"`
  - L23: `    "artifact_feature_contract": {`
  - L25: `      "detail": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package/config/feature_contract.json"`
  - L29: `      "detail": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/tests/phase17_03H_runner_parity/phase17_03H_parity_report.json"`
  - L33: `      "detail": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/tests/phase17_03I_full_validation_runner_parity/phase17_03I_full_validation_parity_report.json"`
  - L37: `      "detail": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/tests/phase17_03J_negative_input_tests/phase17_03J_negative_input_report.json"`
  - L41: `      "detail": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/tests/phase17_03K_offline_release_evidence/phase17_03K_offline_release_evidence_audit.json"`
  - L45: `      "detail": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package/models/phase15_10_final_tuned_extra_trees_trainval.joblib"`
  - L49: `      "detail": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package/models/phase15_10_final_tuned_random_forest_trainval.joblib"`
  - L79: `    "StationId_is_feature_73": {`
  - L81: `      "detail": "Final feature=StationId"`
  - L101: `      "detail": "23,103 validation rows; all three prediction outputs within tolerance."`
  - L107: `    "live_source_gate_remains_blocked": {`
  - L109: `      "detail": "Passed: Phase 17.03I/L/M explicitly report NO_VALIDATED_LIVE_AQI_SOURCE with production_enabled=false, and the source config contains no explicit positive readiness signal. The config is not required to repeat the exact runtime status string."`
  - L111: `    "production_not_enabled_in_source_config": {`
  - L113: `      "detail": "No production_enabled=true flag found."`
  - L115: `    "phase_I_production_disabled": {`
  - L117: `      "detail": "production_enabled=False"`
  - L119: `    "phase_J_production_disabled": {`
  - L121: `      "detail": "production_enabled=False"`
  - L123: `    "phase_K_production_disabled": {`
  - L125: `      "detail": "production_enabled=False"`
  - L127: `    "phase_L_production_disabled": {`
  - L129: `      "detail": "production_enabled=False"`
  - L131: `    "phase_M_production_disabled": {`
  - L133: `      "detail": "production_enabled=False"`
  - L141: `      "detail": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/releases/phase17_03L_offline_release/bundle"`
  - L145: `      "detail": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/releases/phase17_03L_offline_release/verification_extract"`
  - L148: `  "release_zip": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/releases/phase17_03L_offline_release/Delhi-AQI-Prediction_phase17_03L_offline_release.zip",`
  - L159: `  "production_enabled": false,`
  - L160: `  "production_status": "NO_VALIDATED_LIVE_AQI_SOURCE",`
  - L161: `  "source_gate_repair_note": "The original check required the exact runtime status string to appear as a value in source_status.json. The corrected check uses the persisted Phase 17.03I/L/M runtime statuses and rejects explicit positive readiness signals in source configuration. No configuration or model file was changed.",`
  - L162: `  "source_status_file_checked": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package/config/source_status.json",`
  - L165: `      "production_status": "NO_VALIDATED_LIVE_AQI_SOURCE",`
  - L166: `      "production_enabled": false`
  - L169: `      "production_status": "NO_VALIDATED_LIVE_AQI_SOURCE",`
  - L170: `      "production_enabled": false`
  - L173: `      "production_status": "NO_VALIDATED_LIVE_AQI_SOURCE",`
  - L174: `      "production_enabled": false`
  - L177: `      "production_status": "NO_VALIDATED_LIVE_AQI_SOURCE",`
  - L178: `      "production_enabled": false`

### `deployment/releases/phase17_06E_cloud_run_handoff/PHASE_17_06E_CLOUD_RUN_DEPLOYMENT_GUIDE.md`
- Static Python syntax: not_applicable
- SHA256: `89ed286d65e12c47a646254922d96946d3ec617d26363d1d8951d4862edefc7c`
- Matching lines: 14
  - L8: `- Production: blocked with `NO_VALIDATED_LIVE_AQI_SOURCE`.`
  - L9: `- This deployment is private and readiness-blocked; it is not an approved live predictor.`
  - L13: `- Existing base release ZIP: `/content/gdrive/MyDrive/Delhi-AQI-Prediction/deployment/releases/phase17_03L_offline_release/Delhi-AQI-Prediction_phase17_03L_offline_release.zip``
  - L14: `- Small overlay ZIP: `/content/gdrive/MyDrive/Delhi-AQI-Prediction/deployment/releases/phase17_06E_cloud_run_handoff/phase17_06E_cloud_run_overlay.zip``
  - L28: `unzip -q /path/to/Delhi-AQI-Prediction_phase17_03L_offline_release.zip \`
  - L29: `  'Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package/*' -d .`
  - L31: `cd Delhi-AQI-Prediction/deployment`
  - L50: `Request the health endpoint with a Google identity token:`
  - L55: `TOKEN=$(gcloud auth print-identity-token)`
  - L56: `curl -i -H "Authorization: Bearer $TOKEN" "$SERVICE_URL/healthz"`
  - L57: `curl -i -H "Authorization: Bearer $TOKEN" "$SERVICE_URL/readyz"`
  - L60: `Expected: `/healthz` returns HTTP 200. `/readyz` returns HTTP 503 with`
  - L67: `- Do not set `LIVE_SOURCE_VALIDATED=true` or `PRODUCTION_ENABLED=true`.`
  - L69: `  lag/rolling features before production predictions can be enabled.`

### `deployment/releases/phase17_06E_cloud_run_handoff/phase17_06E_cloud_run_handoff_report.json`
- Static Python syntax: not_applicable
- SHA256: `fa6883740b9a7af8a7fa640907a13b4985f868393960941d48261af9287dd8ec`
- Matching lines: 8
  - L5: `  "project_root": "/content/gdrive/MyDrive/Delhi-AQI-Prediction",`
  - L6: `  "base_release_zip": "/content/gdrive/MyDrive/Delhi-AQI-Prediction/deployment/releases/phase17_03L_offline_release/Delhi-AQI-Prediction_phase17_03L_offline_release.zip",`
  - L8: `  "overlay_zip": "/content/gdrive/MyDrive/Delhi-AQI-Prediction/deployment/releases/phase17_06E_cloud_run_handoff/phase17_06E_cloud_run_overlay.zip",`
  - L15: `  "cloud_run_deploy_script": "/content/gdrive/MyDrive/Delhi-AQI-Prediction/deployment/phase17_06_inference_api/deploy_to_cloud_run_staging.sh",`
  - L16: `  "deployment_guide": "/content/gdrive/MyDrive/Delhi-AQI-Prediction/deployment/releases/phase17_06E_cloud_run_handoff/PHASE_17_06E_CLOUD_RUN_DEPLOYMENT_GUIDE.md",`
  - L19: `  "live_source_validated": false,`
  - L20: `  "production_enabled": false,`
  - L21: `  "production_status": "NO_VALIDATED_LIVE_AQI_SOURCE",`

### `deployment/releases/phase17_07_offline_batch_candidate_20261026T143528_100244Z/README.md`
- Static Python syntax: not_applicable
- SHA256: `5920abb7b3a0229c87dc4ee07f757cef13797b84ca01dec0c83f831330396beb`
- Matching lines: 4
  - L13: `    python src/batch_predict.py --input features.parquet --output new_predictions.parquet --metadata metadata.parquet`
  - L15: `Metadata may contain only StationId and optional Datetime, StationName, Split`
  - L19: `The candidate does not verify source freshness or prove a live source is valid.`
  - L20: `Production remains disabled.`

### `deployment/releases/phase17_07_offline_batch_candidate_20261026T143528_100244Z/candidate_manifest.json`
- Static Python syntax: not_applicable
- SHA256: `5eb444c66f2989219c56209ed1038bc6ff9e5982966dd148132601b96db8c3f9`
- Matching lines: 4
  - L4: `  "status": "OFFLINE_ONLY_CANDIDATE_NOT_LIVE_PRODUCTION",`
  - L17: `  "live_source_validated": false,`
  - L18: `  "production_enabled": false,`
  - L29: `    "src/batch_predict.py": "66f9aaaff04059214706ab806e8f598ce8a5423b4a4f7ea7c046992dd01309ac",`

### `deployment/releases/phase17_07_offline_batch_candidate_20261026T143528_100244Z/src/batch_predict.py`
- Static Python syntax: PASS
- SHA256: `66f9aaaff04059214706ab806e8f598ce8a5423b4a4f7ea7c046992dd01309ac`
- Matching lines: 37
  - L22: `ALLOWED_METADATA = {"StationId", "Datetime", "StationName", "Split"}`
  - L95: `    contract = read_json(package / "config" / "feature_contract.json")`
  - L106: `        raise ValueError("Invalid frozen feature contract.")`
  - L141: `    if X["StationId"].isna().any():`
  - L142: `        raise ValueError("StationId contains missing values.")`
  - L143: `    X["StationId"] = X["StationId"].astype(str)`
  - L145: `    invalid_stations = sorted(set(X["StationId"]) - ALLOWED_STATIONS)`
  - L147: `        raise ValueError(f"Unknown station IDs: {invalid_stations}")`
  - L149: `    numeric = [c for c in features if c != "StationId"]`
  - L163: `        if "StationId" not in metadata:`
  - L164: `            raise ValueError("Metadata must contain StationId.")`
  - L165: `        if not metadata["StationId"].astype(str).reset_index(drop=True).equals(`
  - L166: `            X["StationId"].reset_index(drop=True)`
  - L168: `            raise ValueError("Metadata station IDs/order do not align with inputs.")`
  - L184: `    predictions = inference.predict_aqi(checked)`
  - L185: `    missing_outputs = [c for c in OUTPUT_COLUMNS if c not in predictions.columns]`
  - L187: `        raise RuntimeError(f"Prediction outputs missing: {missing_outputs}")`
  - L189: `    pred_values = predictions[OUTPUT_COLUMNS].to_numpy(dtype=float)`
  - L191: `        raise RuntimeError("Non-finite predictions returned.")`
  - L194: `        w_et * predictions["AQI_pred_extra_trees"].to_numpy(dtype=float)`
  - L195: `        + w_rf * predictions["AQI_pred_random_forest"].to_numpy(dtype=float)`
  - L198: `        expected_ensemble - predictions["AQI_t_plus_1_pred"].to_numpy(dtype=float)`
  - L206: `        "StationId": X["StationId"].to_numpy(),`
  - L207: `        "AQI_pred_extra_trees": predictions["AQI_pred_extra_trees"].to_numpy(),`
  - L208: `        "AQI_pred_random_forest": predictions["AQI_pred_random_forest"].to_numpy(),`
  - L209: `        "AQI_t_plus_1_pred": predictions["AQI_t_plus_1_pred"].to_numpy(),`
  - L210: `        "PredictionHorizonHours": 1,`
  - L213: `        "FeatureContractVersion": contract.get("contract_version", "unknown"),`
  - L217: `        "ProductionStatus": "DISABLED",`
  - L218: `        "PredictionGeneratedAtUTC": created,`
  - L223: `            output["PredictionTime"] = metadata["Datetime"].to_numpy()`
  - L244: `        "station_count": int(X["StationId"].nunique()),`
  - L250: `        "live_source_validated": False,`
  - L251: `        "production_enabled": False,`
  - L261: `    print(f"Rows: {len(output)}; stations: {X['StationId'].nunique()}")`
  - L262: `    print(f"Predictions: {output_path}")`
  - L264: `    print("Production remains disabled.")`

### `deployment/tests/phase16_28_aqi_surrogate_feasibility/phase16_28R_diagnostic.json`
- Static Python syntax: not_applicable
- SHA256: `614091e8fd1d91a09d0cefd5bf5f098c80860116eb6b285216ae8f15b820c3e7`
- Matching lines: 1
  - L35: `  "production_source_changed": false`

### `deployment/tests/phase16_29_temporal_aqi_surrogate/phase16_29_diagnostic.json`
- Static Python syntax: not_applicable
- SHA256: `9408faffc17f6669eb4432c2d382755265b01df756cb5032731710a0cebfcedb`
- Matching lines: 1
  - L33: `  "production_source_changed": false,`

### `deployment/tests/phase17_02B_offline_interface/phase17_02B_offline_interface_readiness.json`
- Static Python syntax: not_applicable
- SHA256: `33c396a967d6919301ac2e29369857d35793ad80fc13b2c4c2904ba72db6af9e`
- Matching lines: 26
  - L5: `  "production_status": "NO_VALIDATED_LIVE_AQI_SOURCE",`
  - L6: `  "production_enabled": false,`
  - L7: `  "live_source_download_attempted": false,`
  - L8: `  "frozen_model_or_feature_contract_changed": false,`
  - L11: `    "feature_contract",`
  - L16: `    "feature_contract",`
  - L20: `    "feature_contract": {`
  - L21: `      "path": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package/feature_contract.json",`
  - L26: `      "path": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package/ensemble_config.json",`
  - L31: `      "path": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package/source_status.json",`
  - L36: `      "path": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package/deployment_manifest.json",`
  - L41: `      "path": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package/src/frozen_aqi_inference.py",`
  - L46: `      "path": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package/models/phase15_10_final_tuned_extra_trees_trainval.joblib",`
  - L51: `      "path": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package/models/phase15_10_final_tuned_random_forest_trainval.joblib",`
  - L55: `    "production_source_guard": {`
  - L56: `      "path": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_81R_final_deployment_lock/production_source_guard.py",`
  - L61: `      "path": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_81R_final_deployment_lock/phase16_83R_final_release/offline_inference_example.py",`
  - L66: `      "path": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_81R_final_deployment_lock/phase16_83R_final_release/FINAL_OFFLINE_HANDOFF.md",`
  - L72: `    "feature_contract": {`
  - L90: `        "feature_contract",`
  - L97: `        "production_source_changed"`
  - L106: `        "predict_aqi"`
  - L114: `        "predict_frozen_ensemble"`
  - L119: `    "production_source_guard": {`
  - L122: `        "assert_production_source_ready",`
  - L126: `        "ProductionSourceBlocked"`

### `deployment/tests/phase17_03K_offline_release_evidence/PHASE_17_03K_OFFLINE_RELEASE_EVIDENCE.md`
- Static Python syntax: not_applicable
- SHA256: `98a2c094b46d1fa3054a71b511becece471e5108cb5776fe90159a1ef76b20cb`
- Matching lines: 7
  - L8: `- Phase 17.03I: 23,103 complete-case validation rows passed prediction parity.`
  - L10: `- Frozen feature contract: 73 features.`
  - L16: `- Production enabled: **False**`
  - L17: `- Production status: `NO_VALIDATED_LIVE_AQI_SOURCE``
  - L19: `The evidence supports the tested offline inference workflow only. It does not validate a live data feed, and it does not authorize production use.`
  - L23: `- JSON audit: `/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/tests/phase17_03K_offline_release_evidence/phase17_03K_offline_release_evidence_audit.json``
  - L24: `- SHA-256 artifact manifest: `/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/tests/phase17_03K_offline_release_evidence/phase17_03K_artifact_sha256_manifest.json``

### `deployment/tests/phase17_03K_offline_release_evidence/phase17_03K_artifact_sha256_manifest.json`
- Static Python syntax: not_applicable
- SHA256: `66d6e607b805fa650d793f4e74608019bbd4e5edfee833541d8014196ebc78a0`
- Matching lines: 16
  - L6: `      "path": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/tests/phase17_03H_runner_parity/phase17_03H_parity_report.json",`
  - L11: `      "path": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/tests/phase17_03I_full_validation_runner_parity/phase17_03I_full_validation_parity_report.json",`
  - L16: `      "path": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/tests/phase17_03J_negative_input_tests/phase17_03J_negative_input_report.json",`
  - L20: `    "feature_contract": {`
  - L21: `      "path": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package/config/feature_contract.json",`
  - L26: `      "path": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package/config/ensemble_config.json",`
  - L31: `      "path": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package/config/source_status.json",`
  - L36: `      "path": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package/models/phase15_10_final_tuned_extra_trees_trainval.joblib",`
  - L41: `      "path": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package/models/phase15_10_final_tuned_random_forest_trainval.joblib",`
  - L46: `      "path": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package/src/frozen_aqi_inference.py",`
  - L51: `      "path": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/tests/phase17_03B_offline_runner/offline_inference_runner.py",`
  - L56: `      "path": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/tests/phase17_03B_offline_runner/offline_input_template_73_features.csv",`
  - L61: `      "path": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/tests/phase17_03B_offline_runner/README_OFFLINE_INFERENCE.md",`
  - L66: `      "path": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/tests/phase17_03H_runner_parity/phase17_03H_prediction_parity.csv",`
  - L71: `      "path": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/tests/phase17_03I_full_validation_runner_parity/phase17_03I_prediction_parity.csv",`
  - L76: `      "path": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/tests/phase17_03J_negative_input_tests/phase17_03J_negative_input_report.json",`

### `deployment/tests/phase17_03K_offline_release_evidence/phase17_03K_offline_release_evidence_audit.json`
- Static Python syntax: not_applicable
- SHA256: `122ff000de65976cde7fd2f112dfd86f7d26bbb71699c05db802d50785a51825`
- Matching lines: 28
  - L9: `      "details": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/tests/phase17_03H_runner_parity/phase17_03H_parity_report.json"`
  - L13: `      "details": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/tests/phase17_03I_full_validation_runner_parity/phase17_03I_full_validation_parity_report.json"`
  - L17: `      "details": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/tests/phase17_03J_negative_input_tests/phase17_03J_negative_input_report.json"`
  - L19: `    "artifact_exists_feature_contract": {`
  - L21: `      "details": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package/config/feature_contract.json"`
  - L25: `      "details": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package/config/ensemble_config.json"`
  - L29: `      "details": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package/config/source_status.json"`
  - L33: `      "details": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package/models/phase15_10_final_tuned_extra_trees_trainval.joblib"`
  - L37: `      "details": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package/models/phase15_10_final_tuned_random_forest_trainval.joblib"`
  - L41: `      "details": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package/src/frozen_aqi_inference.py"`
  - L45: `      "details": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/tests/phase17_03B_offline_runner/offline_inference_runner.py"`
  - L49: `      "details": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/tests/phase17_03B_offline_runner/offline_input_template_73_features.csv"`
  - L53: `      "details": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/tests/phase17_03B_offline_runner/README_OFFLINE_INFERENCE.md"`
  - L71: `    "three_prediction_columns_in_parity_tolerance": {`
  - L83: `    "phase_I_production_disabled": {`
  - L85: `      "details": "production_enabled=False"`
  - L95: `    "phase_J_production_disabled": {`
  - L97: `      "details": "production_enabled=False"`
  - L99: `    "frozen_feature_contract": {`
  - L103: `    "station_id_in_feature_contract": {`
  - L105: `      "details": "StationId position=73"`
  - L113: `    "phase_17_03H": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/tests/phase17_03H_runner_parity/phase17_03H_parity_report.json",`
  - L114: `    "phase_17_03I": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/tests/phase17_03I_full_validation_runner_parity/phase17_03I_full_validation_parity_report.json",`
  - L115: `    "phase_17_03J": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/tests/phase17_03J_negative_input_tests/phase17_03J_negative_input_report.json"`
  - L124: `  "artifact_sha256_manifest": "/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/tests/phase17_03K_offline_release_evidence/phase17_03K_artifact_sha256_manifest.json",`
  - L126: `  "production_enabled": false,`
  - L127: `  "production_status": "NO_VALIDATED_LIVE_AQI_SOURCE",`
  - L128: `  "qualification": "This audit validates offline inference artifacts and test evidence only. It does not authorize live production deployment."`

### `deployment/tests/phase17_06C_api_inference_integration/test_only_release_gate.json`
- Static Python syntax: not_applicable
- SHA256: `e5473897a5d52f6ca56797f35161a735bae2e55e7c96d8d03f43fd52a928ec6f`
- Matching lines: 4
  - L4: `  "reason": "Local integration test only; not production authorization.",`
  - L5: `  "live_source_validated": true,`
  - L6: `  "production_enabled": true,`
  - L7: `  "test_only_warning": "This file must never replace the real release_gate.json. It exists only to exercise the protected inference route locally."`

### `deployment/tests/phase17_06D_deployment_build_readiness/phase17_06D_deployment_build_readiness.json`
- Static Python syntax: not_applicable
- SHA256: `644bda2b7ee6727cdb51c75ac42961899374e4a87b23024033b90029fe623bee`
- Matching lines: 7
  - L5: `  "project_root": "/content/gdrive/MyDrive/Delhi-AQI-Prediction",`
  - L6: `  "service_directory": "/content/gdrive/MyDrive/Delhi-AQI-Prediction/deployment/phase17_06_inference_api",`
  - L7: `  "build_script": "/content/gdrive/MyDrive/Delhi-AQI-Prediction/deployment/phase17_06_inference_api/build_and_smoke_test.sh",`
  - L20: `  "actual_release_gate_unchanged": true,`
  - L21: `  "production_enabled": false,`
  - L22: `  "production_status": "NO_VALIDATED_LIVE_AQI_SOURCE",`
  - L24: `  "next_step": "Run build_and_smoke_test.sh on a Docker-capable host. Keep production disabled until live source and feature-history validation pass."`

### `deployment/tests/phase17_07B_metrics_registry_protocol/phase17_07B_research_readiness_summary.json`
- Static Python syntax: not_applicable
- SHA256: `63505021cdde21a9646142aab0da2bdad1e472f10cbec511024b80e74d8117b9`
- Matching lines: 186
  - L5: `  "project_root": "/content/gdrive/MyDrive/Delhi-AQI-Prediction",`
  - L19: `    "prediction_schema_candidates": 23`
  - L21: `  "prediction_schema_candidates": [`
  - L23: `      "relative_path": "outputs/phase6_test_predictions.parquet",`
  - L27: `        "StationId",`
  - L32: `        "Persistence_Prediction",`
  - L33: `        "LinearRegression_Prediction",`
  - L34: `        "DecisionTree_Prediction",`
  - L35: `        "RandomForest_Prediction",`
  - L36: `        "XGBoost_Prediction"`
  - L40: `      "relative_path": "outputs/reports/phase15_8_top_two_validation_predictions.parquet",`
  - L45: `        "StationId",`
  - L47: `        "Tuned_Extra_Trees_Prediction",`
  - L48: `        "Tuned_Random_Forest_Prediction"`
  - L52: `      "relative_path": "outputs/reports/phase15_9_optimized_ensemble_validation_predictions.parquet",`
  - L57: `        "StationId",`
  - L59: `        "Tuned_Extra_Trees_Prediction",`
  - L60: `        "Tuned_Random_Forest_Prediction",`
  - L61: `        "Optimized_Ensemble_Prediction",`
  - L66: `      "relative_path": "outputs/FINAL_RESULTS/02_MODEL_RESULTS/EXTRA_TREES/prediction_error_diagnostics.parquet",`
  - L71: `        "StationId",`
  - L73: `        "Prediction",`
  - L77: `        "Predicted_Category",`
  - L82: `      "relative_path": "outputs/FINAL_RESULTS/02_MODEL_RESULTS/RANDOM_FOREST/prediction_error_diagnostics.parquet",`
  - L87: `        "StationId",`
  - L89: `        "Prediction",`
  - L93: `        "Predicted_Category",`
  - L98: `      "relative_path": "outputs/FINAL_RESULTS/02_MODEL_RESULTS/ENSEMBLE/prediction_error_diagnostics.parquet",`
  - L103: `        "StationId",`
  - L105: `        "Prediction",`
  - L109: `        "Predicted_Category",`
  - L114: `      "relative_path": "outputs/reports/phase15_12_final_holdout/phase15_12_final_holdout_predictions.parquet",`
  - L119: `        "StationId",`
  - L121: `        "Tuned_Extra_Trees_Prediction",`
  - L122: `        "Tuned_Random_Forest_Prediction",`
  - L123: `        "Final_Ensemble_Prediction",`
  - L124: `        "Persistence_Prediction",`
  - L130: `      "relative_path": "outputs/checkpoints/session_runtime/prediction_df.parquet",`
  - L135: `        "StationId",`
  - L137: `        "Tuned_Extra_Trees_Prediction",`
  - L138: `        "Tuned_Random_Forest_Prediction",`
  - L139: `        "Final_Ensemble_Prediction",`
  - L140: `        "Persistence_Prediction",`
  - L151: `        "StationId",`
  - L153: `        "Tuned_Extra_Trees_Prediction",`

## Interpretation

This report records static source evidence only. It does not certify live-source compatibility, readiness-gate success, or production readiness. The existing deployment lock remains in force unless separately and explicitly validated and authorized.

Machine-readable report: `/content/drive/MyDrive/Delhi-AQI-Prediction/outputs/deployment_readiness/DEPLOY_0_21_20261026T153545_964511Z/DEPLOY_0_21_static_api_gate_audit.json`