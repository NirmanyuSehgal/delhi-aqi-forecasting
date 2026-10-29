
"""Authenticated, shadow-only live AQI forecast route.

Uses the official Delhi AQI feed as an AQI-only input scenario. Pollutant fields
remain missing and are handled by the fitted imputers inside the frozen models.
This route never changes production readiness or the release gate.
"""

import os
import sys
import json
import math
import secrets
import logging
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd
from fastapi import APIRouter, HTTPException, Request, Response

SERVICE_SRC_DIR = Path(__file__).resolve().parent
API_DIR = SERVICE_SRC_DIR.parent
PACKAGE_DIR = Path(
    os.environ.get(
        "FROZEN_PACKAGE_DIR",
        str(API_DIR.parent / "phase16_33_frozen_model_package")
    )
)

if str(SERVICE_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SERVICE_SRC_DIR))

from canonical_aqi_features import (
    RAW_FEATURES,
    BASE_COLUMNS,
    build_canonical_features,
)
import frozen_aqi_inference_missing_aware_candidate as inference_candidate

logger = logging.getLogger("delhi-aqi-shadow")
router = APIRouter()

OFFICIAL_ENDPOINT = (
    "https://aqi.delhi.gov.in/api/v1/aqi-analytics/public/live-aqi-at"
)

with open(PACKAGE_DIR / "config" / "feature_contract.json", "r", encoding="utf-8") as f:
    FEATURE_ORDER = json.load(f)["feature_order"]

STATION_ORDER = [
    "DL002", "DL004", "DL007", "DL010", "DL013",
    "DL019", "DL021", "DL028", "DL031", "DL034",
]

# Explicit aliases for mapping official portal station labels to frozen model IDs.
STATIONS = {
    "DL002": {
        "project_name": "Anand Vihar",
        "aliases": ["anandvihar"],
    },
    "DL004": {
        "project_name": "Aya Nagar",
        "aliases": ["ayanagar"],
    },
    "DL007": {
        "project_name": "CRRI Mathura Road",
        "aliases": ["crrimathuraroad"],
    },
    "DL010": {
        "project_name": "Dwarka-Sector 8",
        "aliases": ["dwarkasector8"],
    },
    "DL013": {
        "project_name": "IHBAS",
        "aliases": ["ihbas"],
    },
    "DL019": {
        "project_name": "Mandir Marg",
        "aliases": ["mandirmarg"],
    },
    "DL021": {
        "project_name": "NSIT Dwarka",
        "aliases": [
            "nsitdwarka",
            "nsutdwarka",
            "netajisubhasuniversityoftechnology",
        ],
    },
    "DL028": {
        "project_name": "Punjabi Bagh",
        "aliases": ["punjabibagh"],
    },
    "DL031": {
        "project_name": "R K Puram",
        "aliases": ["rkpuram"],
    },
    "DL034": {
        "project_name": "Sirifort",
        "aliases": ["sirifort"],
    },
}

if len(FEATURE_ORDER) != 73 or len(set(FEATURE_ORDER)) != 73:
    raise RuntimeError("Frozen feature contract must contain 73 unique columns.")

def _normalise_name(value):
    import re
    return re.sub(r"[^a-z0-9]", "", str(value).lower())

def _map_station_name(source_name):
    normalized = _normalise_name(source_name)
    matches = [
        sid for sid, spec in STATIONS.items()
        if any(alias in normalized for alias in spec["aliases"])
    ]
    if len(matches) > 1:
        raise ValueError(
            f"Ambiguous source station mapping for {source_name!r}: {matches}"
        )
    return matches[0] if matches else None

def _fetch_official_snapshot(requested_ist):
    """Fetch one requested hourly snapshot. Uses urllib to avoid an extra dependency."""
    query = urllib.parse.urlencode({"at": requested_ist.isoformat()})
    request = urllib.request.Request(
        f"{OFFICIAL_ENDPOINT}?{query}",
        headers={
            "Accept": "application/json",
            "User-Agent": "Delhi-AQI-Shadow-Inference/17.06",
        },
        method="GET",
    )
    with urllib.request.urlopen(request, timeout=12) as response:
        if response.status != 200:
            raise RuntimeError(f"Official AQI API returned HTTP {response.status}.")
        payload = json.loads(response.read().decode("utf-8"))

    if not isinstance(payload, dict) or payload.get("success") is not True:
        raise RuntimeError("Official AQI API did not confirm a successful response.")
    return payload

def build_live_feature_frame(snapshot_fetcher=None, now_ist=None):
    """Build and validate a 10-row frozen-feature frame from the last 13 AQI snapshots.

    snapshot_fetcher and now_ist are injectable for offline unit tests. In the live
    route, the official HTTPS fetcher and current India time are used.
    """
    if now_ist is None:
        now = pd.Timestamp.now(tz="Asia/Kolkata")
    else:
        now = pd.Timestamp(now_ist)
        if now.tzinfo is None:
            now = now.tz_localize("Asia/Kolkata")
        else:
            now = now.tz_convert("Asia/Kolkata")

    last_requested = now.floor("h")
    requested_times = [
        last_requested - pd.Timedelta(hours=offset)
        for offset in range(12, -1, -1)
    ]

    fetcher = snapshot_fetcher or _fetch_official_snapshot

    # Concurrent calls reduce endpoint latency while keeping concurrency bounded.
    with ThreadPoolExecutor(max_workers=7) as pool:
        futures = {
            timestamp: pool.submit(fetcher, timestamp)
            for timestamp in requested_times
        }

        payloads = {}
        for timestamp in requested_times:
            try:
                payloads[timestamp] = futures[timestamp].result(timeout=20)
            except Exception as exc:
                raise RuntimeError(
                    f"Official snapshot retrieval failed for {timestamp.isoformat()}."
                ) from exc

    history_rows = []
    source_uuids = {}
    source_names = {}

    for requested_ist in requested_times:
        payload = payloads[requested_ist]

        if not isinstance(payload, dict) or payload.get("success") is not True:
            raise RuntimeError("An official AQI snapshot was unsuccessful.")

        records = payload.get("data", {}).get("stations", [])
        if not isinstance(records, list) or not records:
            raise RuntimeError("Official AQI response has no station records.")

        matched = {}
        for record in records:
            if not isinstance(record, dict):
                continue
            sid = _map_station_name(record.get("station_name", ""))
            if sid is None:
                continue
            if sid in matched:
                raise RuntimeError(
                    f"Multiple official records map to project station {sid}."
                )
            matched[sid] = record

        missing_stations = [sid for sid in STATION_ORDER if sid not in matched]
        if missing_stations:
            raise RuntimeError(
                "Official snapshot is missing required stations: "
                + ", ".join(missing_stations)
            )

        requested_naive = requested_ist.tz_localize(None)

        for sid in STATION_ORDER:
            record = matched[sid]

            if record.get("is_reporting") is not True:
                raise RuntimeError(
                    f"Official station {sid} is not marked as reporting."
                )

            try:
                aqi = float(record["aqi_value"])
            except (KeyError, TypeError, ValueError) as exc:
                raise RuntimeError(
                    f"Official AQI value is absent or invalid for {sid}."
                ) from exc

            if not math.isfinite(aqi) or aqi < 0:
                raise RuntimeError(f"Official AQI value is not finite/non-negative for {sid}.")

            observed_utc = pd.to_datetime(
                record.get("last_reading_time"),
                errors="coerce",
                utc=True,
            )
            if pd.isna(observed_utc):
                raise RuntimeError(f"Official observation timestamp is invalid for {sid}.")

            observed_ist = observed_utc.tz_convert("Asia/Kolkata")
            observed_naive = observed_ist.tz_localize(None)
            time_delta = abs((observed_naive - requested_naive).total_seconds())

            if time_delta > 45 * 60:
                raise RuntimeError(
                    f"Timestamp for {sid} differs from requested snapshot "
                    f"by {time_delta / 60:.1f} minutes."
                )

            feed_uuid = str(record.get("station_id", "")).strip()
            if sid in source_uuids and feed_uuid and source_uuids[sid] != feed_uuid:
                raise RuntimeError(f"Official source ID changed across snapshots for {sid}.")
            if feed_uuid:
                source_uuids[sid] = feed_uuid
            source_names[sid] = str(record.get("station_name", ""))

            row = {
                "StationId": sid,
                "StationName": STATIONS[sid]["project_name"],
                "Datetime": observed_naive,
            }
            for feature in RAW_FEATURES:
                row[feature] = np.nan
            row["AQI"] = aqi
            history_rows.append(row)

    history = pd.DataFrame(history_rows, columns=BASE_COLUMNS)
    history["Datetime"] = pd.to_datetime(history["Datetime"])
    history["StationId"] = history["StationId"].astype(str)
    history = history.sort_values(["StationId", "Datetime"]).reset_index(drop=True)

    if history.duplicated(["StationId", "Datetime"]).any():
        raise RuntimeError("Duplicate station-time observations found in live history.")

    timestamp_sequences = []
    for sid in STATION_ORDER:
        station_history = history.loc[history["StationId"].eq(sid)].sort_values("Datetime")
        if len(station_history) != 13:
            raise RuntimeError(
                f"Expected 13 history rows for {sid}, found {len(station_history)}."
            )

        deltas = station_history["Datetime"].diff().dropna()
        if not deltas.eq(pd.Timedelta(hours=1)).all():
            raise RuntimeError(f"History for {sid} is not on exact hourly cadence.")

        timestamp_sequences.append(tuple(station_history["Datetime"].tolist()))

    if len(set(timestamp_sequences)) != 1:
        raise RuntimeError("The ten stations do not share the same 13 hourly timestamps.")

    forecast_origin = pd.Timestamp(history["Datetime"].max())
    now_naive = now.tz_localize(None)
    source_age_hours = (now_naive - forecast_origin).total_seconds() / 3600

    if source_age_hours < -0.1 or source_age_hours > 2.0:
        raise RuntimeError(
            f"Latest common observation is stale/out of range: "
            f"{source_age_hours:.2f} hours old."
        )

    engineered = build_canonical_features(history[BASE_COLUMNS].copy())
    latest = engineered.loc[
        engineered["Datetime"].eq(forecast_origin)
    ].copy()

    if latest["StationId"].duplicated().any():
        raise RuntimeError("Canonical builder returned duplicate station rows.")
    if set(latest["StationId"].astype(str)) != set(STATION_ORDER):
        raise RuntimeError("Canonical output does not contain exactly the ten frozen stations.")

    latest["StationId"] = latest["StationId"].astype(str)
    latest = (
        latest.set_index("StationId")
        .loc[STATION_ORDER]
        .reset_index()
    )

    missing_contract = [c for c in FEATURE_ORDER if c not in latest.columns]
    if missing_contract:
        raise RuntimeError(
            "Canonical builder omitted frozen features: "
            + ", ".join(missing_contract)
        )

    X = latest.loc[:, FEATURE_ORDER].copy()
    X = inference_candidate.validate_feature_frame(X)

    if X.shape != (10, 73):
        raise RuntimeError(f"Expected 10 x 73 features, received {X.shape}.")
    if int(X.isna().sum().sum()) != 560:
        raise RuntimeError(
            "Unexpected missingness for AQI-only input: "
            f"{int(X.isna().sum().sum())} missing feature cells, expected 560."
        )

    metadata = {
        "forecast_origin_ist": forecast_origin.isoformat(),
        "forecast_target_ist": (forecast_origin + pd.Timedelta(hours=1)).isoformat(),
        "source_age_hours": round(float(source_age_hours), 4),
        "snapshot_count": len(requested_times),
        "history_rows": len(history),
        "feature_count": len(FEATURE_ORDER),
        "missing_feature_cells": int(X.isna().sum().sum()),
        "total_feature_cells": int(X.size),
        "source_station_mapping": [
            {
                "StationId": sid,
                "project_station_name": STATIONS[sid]["project_name"],
                "official_station_name": source_names.get(sid),
                "official_station_uuid": source_uuids.get(sid),
            }
            for sid in STATION_ORDER
        ],
    }
    return X, metadata

def _authorise_shadow_request(request):
    """Use the existing bearer token; do not permit unauthenticated model access."""
    token = os.environ.get("API_BEARER_TOKEN", "").strip()

    if not token:
        raise HTTPException(
            status_code=503,
            detail={
                "error": "shadow_auth_not_configured",
                "message": "The shadow route requires API_BEARER_TOKEN.",
            },
        )

    auth = request.headers.get("authorization", "")
    supplied = auth[7:].strip() if auth.lower().startswith("bearer ") else ""

    if not supplied or not secrets.compare_digest(supplied, token):
        raise HTTPException(
            status_code=401,
            detail="Valid bearer token required for the shadow route.",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.get("/shadow/forecast/live", tags=["shadow"])
def shadow_live_forecast(request: Request, response: Response):
    """Return a protected, shadow-only forecast for the ten frozen Delhi stations."""
    _authorise_shadow_request(request)

    response.headers["Cache-Control"] = "no-store, max-age=0"
    response.headers["Pragma"] = "no-cache"

    try:
        X, metadata = build_live_feature_frame()
        predictions = inference_candidate.predict_aqi(X)

        if len(predictions) != 10:
            raise RuntimeError("Frozen inference did not return ten predictions.")

        output_rows = []
        for i, sid in enumerate(STATION_ORDER):
            output_rows.append({
                "StationId": sid,
                "station_name": STATIONS[sid]["project_name"],
                "current_AQI_t": float(X.iloc[i]["AQI"]),
                "AQI_pred_extra_trees": float(predictions.iloc[i]["AQI_pred_extra_trees"]),
                "AQI_pred_random_forest": float(predictions.iloc[i]["AQI_pred_random_forest"]),
                "AQI_t_plus_1_pred": float(predictions.iloc[i]["AQI_t_plus_1_pred"]),
                "missing_features_per_row": int(X.iloc[i].isna().sum()),
                "forecast_status": "SHADOW_ONLY_NOT_PRODUCTION",
            })

        # No actual t+1 AQI is available when generating the forecast.
        return {
            "status": "SHADOW_ONLY_NOT_PRODUCTION",
            "target": "AQI_t_plus_1",
            "horizon": "1 hour ahead",
            "model_version": "phase15_frozen_final",
            "input_mode": "official_station_AQI_only",
            "forecast_origin_ist": metadata["forecast_origin_ist"],
            "forecast_target_ist": metadata["forecast_target_ist"],
            "source": {
                "name": "Official Delhi AQI portal",
                "endpoint": OFFICIAL_ENDPOINT,
                "snapshots_used": metadata["snapshot_count"],
                "source_age_hours": metadata["source_age_hours"],
            },
            "feature_audit": {
                "feature_count": metadata["feature_count"],
                "missing_feature_cells": metadata["missing_feature_cells"],
                "total_feature_cells": metadata["total_feature_cells"],
                "missing_features_per_station": 56,
            },
            "warnings": [
                "SHADOW_ONLY_NOT_PRODUCTION",
                "Only AQI values are directly observed in this input mode.",
                "Unavailable raw pollutant measurements remain missing and are passed "
                "to the fitted imputers in the frozen pipelines.",
                "Historical AQI-only holdout results do not by themselves validate "
                "a production data source.",
            ],
            "predictions": output_rows,
        }

    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Shadow live forecast failed (%s)", type(exc).__name__)
        raise HTTPException(
            status_code=502,
            detail={
                "error": "shadow_live_forecast_failed",
                "reason_type": type(exc).__name__,
                "message": "Forecast construction or inference failed. Check service logs.",
            },
        ) from exc
