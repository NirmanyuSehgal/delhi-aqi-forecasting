
import os
import sys
import json
import secrets
import logging
import importlib
from pathlib import Path

import numpy as np
import pandas as pd
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("delhi-aqi-api")

SERVICE_DIR = Path(__file__).resolve().parent
PACKAGE_DIR = Path(
    os.environ.get(
        "FROZEN_PACKAGE_DIR",
        str(SERVICE_DIR.parent / "phase16_33_frozen_model_package")
    )
)
GATE_FILE = Path(
    os.environ.get("RELEASE_GATE_FILE", str(SERVICE_DIR / "release_gate.json"))
)
CONTRACT_FILE = PACKAGE_DIR / "config" / "feature_contract.json"

with open(CONTRACT_FILE, "r", encoding="utf-8") as f:
    FEATURE_ORDER = json.load(f)["feature_order"]

if len(FEATURE_ORDER) != 73 or len(set(FEATURE_ORDER)) != 73:
    raise RuntimeError("Frozen feature contract must contain 73 unique columns.")

ALLOWED_STATIONS = {
    "DL031", "DL002", "DL021", "DL028", "DL019",
    "DL010", "DL034", "DL007", "DL013", "DL004",
}
PREDICTION_COLUMNS = [
    "AQI_pred_extra_trees",
    "AQI_pred_random_forest",
    "AQI_t_plus_1_pred",
]
MAX_ROWS_PER_REQUEST = 500

# Crucially: the frozen model module is NOT imported at application startup.
_INFERENCE_MODULE = None

app = FastAPI(
    title="Delhi AQI t+1 Inference API",
    version="17.06B-R1",
    description="Frozen 73-feature ensemble with a fail-closed production gate.",
)

def get_readiness():
    reasons = []

    try:
        with open(GATE_FILE, "r", encoding="utf-8") as f:
            gate = json.load(f)
    except Exception:
        gate = {}
        reasons.append("release_gate_unavailable")

    if gate.get("live_source_validated") is not True:
        reasons.append("live_source_not_validated_in_release_gate")
    if gate.get("production_enabled") is not True:
        reasons.append("production_disabled_in_release_gate")

    if os.environ.get("LIVE_SOURCE_VALIDATED", "false").lower() != "true":
        reasons.append("LIVE_SOURCE_VALIDATED_environment_flag_not_true")
    if os.environ.get("PRODUCTION_ENABLED", "false").lower() != "true":
        reasons.append("PRODUCTION_ENABLED_environment_flag_not_true")
    if not os.environ.get("API_BEARER_TOKEN", "").strip():
        reasons.append("API_BEARER_TOKEN_not_configured")

    return len(reasons) == 0, reasons

def load_frozen_inference():
    global _INFERENCE_MODULE
    if _INFERENCE_MODULE is None:
        source_dir = str(PACKAGE_DIR / "src")
        if source_dir not in sys.path:
            sys.path.insert(0, source_dir)
        _INFERENCE_MODULE = importlib.import_module("frozen_aqi_inference")
    return _INFERENCE_MODULE

@app.get("/")
def root():
    return {
        "service": "Delhi AQI t+1 Inference API",
        "version": "17.06B-R1",
        "production_enabled": False,
        "message": "Use /healthz for liveness and /readyz for readiness.",
    }

@app.get("/healthz")
def healthz():
    return {
        "status": "alive",
        "model_loading": "lazy",
        "production_enabled": False,
    }

@app.get("/readyz")
def readyz():
    ready, reasons = get_readiness()
    return JSONResponse(
        status_code=200 if ready else 503,
        content={
            "ready": ready,
            "status": "READY" if ready else "NO_VALIDATED_LIVE_AQI_SOURCE",
            "reasons": reasons,
            "feature_count": len(FEATURE_ORDER),
            "production_enabled": ready,
        },
    )

@app.post("/predict")
async def predict(request: Request):
    # Block before loading models, validating data, or doing any inference.
    ready, reasons = get_readiness()
    if not ready:
        raise HTTPException(
            status_code=503,
            detail={
                "error": "production_predictions_blocked",
                "status": "NO_VALIDATED_LIVE_AQI_SOURCE",
                "reasons": reasons,
            },
        )

    token = os.environ.get("API_BEARER_TOKEN", "").strip()
    auth = request.headers.get("authorization", "")
    supplied = auth[7:].strip() if auth.lower().startswith("bearer ") else ""

    if not token or not supplied or not secrets.compare_digest(supplied, token):
        raise HTTPException(status_code=401, detail="Valid bearer token required.")

    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Body must be valid JSON.")

    records = payload.get("records") if isinstance(payload, dict) else None
    if not isinstance(records, list) or not records:
        raise HTTPException(
            status_code=422,
            detail="Provide a non-empty JSON array at key 'records'.",
        )
    if len(records) > MAX_ROWS_PER_REQUEST:
        raise HTTPException(
            status_code=413,
            detail=f"Maximum {MAX_ROWS_PER_REQUEST} rows per request.",
        )
    if not all(isinstance(row, dict) for row in records):
        raise HTTPException(status_code=422, detail="Each record must be a JSON object.")

    X = pd.DataFrame.from_records(records)
    missing = [col for col in FEATURE_ORDER if col not in X.columns]
    extra = [col for col in X.columns if col not in FEATURE_ORDER]

    if missing or extra:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "feature_contract_mismatch",
                "missing_features": missing,
                "extra_features": extra,
                "expected_feature_count": 73,
            },
        )

    X = X.loc[:, FEATURE_ORDER].copy()
    X["StationId"] = X["StationId"].astype(str)

    invalid_stations = sorted(set(X["StationId"].dropna()) - ALLOWED_STATIONS)
    if X["StationId"].isna().any() or invalid_stations:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "invalid_station_id",
                "invalid_station_ids": invalid_stations,
            },
        )

    numeric_features = [c for c in FEATURE_ORDER if c != "StationId"]
    for col in numeric_features:
        try:
            X[col] = pd.to_numeric(X[col], errors="raise")
        except Exception:
            raise HTTPException(
                status_code=422,
                detail={"error": "non_numeric_feature", "feature": col},
            )

    if X[numeric_features].isna().any().any():
        raise HTTPException(status_code=422, detail="Missing numeric feature values.")
    if not np.isfinite(X[numeric_features].to_numpy(dtype=float)).all():
        raise HTTPException(status_code=422, detail="Non-finite numeric feature values.")

    try:
        inference = load_frozen_inference()
        checked = inference.validate_feature_frame(X)
        if isinstance(checked, pd.DataFrame):
            X = checked

        pred = inference.predict_aqi(X)
        missing_outputs = [c for c in PREDICTION_COLUMNS if c not in pred.columns]
        if missing_outputs:
            raise RuntimeError("Frozen inference output schema mismatch.")

        output = []
        for _, row in pred[PREDICTION_COLUMNS].iterrows():
            output.append({c: float(row[c]) for c in PREDICTION_COLUMNS})

        return {
            "status": "success",
            "target": "AQI_t_plus_1",
            "horizon": "1 hour ahead",
            "n_predictions": len(output),
            "predictions": output,
        }

    except HTTPException:
        raise
    except ValueError as exc:
        logger.warning("Feature validation failed (%s)", type(exc).__name__)
        raise HTTPException(status_code=422, detail="Feature validation failed.")
    except Exception as exc:
        logger.error("Inference failed (%s)", type(exc).__name__)
        raise HTTPException(status_code=500, detail="Inference failed.")
