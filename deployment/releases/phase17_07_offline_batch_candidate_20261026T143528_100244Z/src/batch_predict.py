import argparse
import hashlib
import importlib.util
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HASHES = {
    "phase15_10_final_tuned_extra_trees_trainval.joblib":
        "f0b3d43a56a7d5e4f08554f37ff234e1b5e012b5d5d69f18c750844b36cbe72d",
    "phase15_10_final_tuned_random_forest_trainval.joblib":
        "538b5ff34152d19221518e831528093b7bcc57e2b05f82669718f540b514abd8",
}
ALLOWED_STATIONS = {
    "DL002", "DL004", "DL007", "DL010", "DL013",
    "DL019", "DL021", "DL028", "DL031", "DL034",
}
ALLOWED_METADATA = {"StationId", "Datetime", "StationName", "Split"}
OUTPUT_COLUMNS = [
    "AQI_pred_extra_trees",
    "AQI_pred_random_forest",
    "AQI_t_plus_1_pred",
]

def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def read_json(path):
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)

def import_inference(package):
    module_path = package / "src" / "frozen_aqi_inference.py"
    spec = importlib.util.spec_from_file_location(
        "delhi_aqi_offline_batch_inference", module_path
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot import inference module: {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main():
    parser = argparse.ArgumentParser(
        description="Offline batch inference for the frozen Delhi AQI ensemble."
    )
    parser.add_argument("--input", required=True, help="73-feature input Parquet")
    parser.add_argument("--output", required=True, help="New output Parquet path")
    parser.add_argument("--package-dir", default=None)
    parser.add_argument("--metadata", default=None)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()
    candidate_root = Path(__file__).resolve().parents[1]

    if args.package_dir:
        package = Path(args.package_dir).expanduser().resolve()
    else:
        package = candidate_root.parents[1] / "phase16_33_frozen_model_package"

    metadata_path = (
        Path(args.metadata).expanduser().resolve()
        if args.metadata else None
    )
    diagnostics_path = output_path.with_suffix(".diagnostics.json")

    if not input_path.is_file():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    if input_path.suffix.lower() != ".parquet":
        raise ValueError("Input must be Parquet.")
    if output_path.suffix.lower() != ".parquet":
        raise ValueError("Output must end in .parquet.")
    if not package.is_dir():
        raise FileNotFoundError(f"Frozen package not found: {package}")

    # Refuse output paths inside the frozen package.
    if os.path.commonpath([str(output_path), str(package)]) == str(package):
        raise ValueError("Output must be outside the frozen model package.")

    if not args.overwrite and (
        output_path.exists() or diagnostics_path.exists()
    ):
        raise FileExistsError("Output already exists; choose a new output path.")

    contract = read_json(package / "config" / "feature_contract.json")
    ensemble = read_json(package / "config" / "ensemble_config.json")
    release = read_json(package / "deployment_manifest.json")
    features = contract.get("feature_order", [])

    if (
        len(features) != 73
        or len(set(features)) != 73
        or contract.get("feature_count") != 73
        or contract.get("target") != "AQI_t_plus_1"
    ):
        raise ValueError("Invalid frozen feature contract.")

    # Verify exact model bytes before deserializing either model.
    for filename, expected in HASHES.items():
        model_path = package / "models" / filename
        if not model_path.is_file():
            raise FileNotFoundError(f"Model missing: {model_path}")
        actual = sha256_file(model_path)
        if actual != expected:
            raise RuntimeError(f"Model SHA-256 mismatch: {filename}")

    weights = ensemble["weights"]
    w_et = float(weights["tuned_extra_trees"])
    w_rf = float(weights["tuned_random_forest"])
    if not (
        np.isclose(w_et, 0.594466, atol=1e-6)
        and np.isclose(w_rf, 0.405534, atol=1e-6)
        and np.isclose(w_et + w_rf, 1.0, atol=1e-6)
    ):
        raise ValueError("Ensemble weights do not match the frozen configuration.")

    # Validate input before loading the large model files.
    X = pd.read_parquet(input_path)
    if X.empty:
        raise ValueError("Input contains zero rows.")
    if X.columns.duplicated().any():
        raise ValueError("Input has duplicate column names.")
    if list(X.columns) != features:
        missing = [c for c in features if c not in X.columns]
        extra = [c for c in X.columns if c not in features]
        raise ValueError(
            f"Exact frozen column order required. Missing={missing}; extra={extra}"
        )

    X = X.copy()
    if X["StationId"].isna().any():
        raise ValueError("StationId contains missing values.")
    X["StationId"] = X["StationId"].astype(str)

    invalid_stations = sorted(set(X["StationId"]) - ALLOWED_STATIONS)
    if invalid_stations:
        raise ValueError(f"Unknown station IDs: {invalid_stations}")

    numeric = [c for c in features if c != "StationId"]
    for col in numeric:
        X[col] = pd.to_numeric(X[col], errors="raise")
    if not np.isfinite(X[numeric].to_numpy(dtype=float)).all():
        raise ValueError("Non-finite inputs found; no imputation is performed.")

    metadata = None
    if metadata_path:
        metadata = pd.read_parquet(metadata_path)
        if len(metadata) != len(X):
            raise ValueError("Metadata row count does not match input.")
        extra = set(metadata.columns) - ALLOWED_METADATA
        if extra:
            raise ValueError(f"Metadata has forbidden columns: {sorted(extra)}")
        if "StationId" not in metadata:
            raise ValueError("Metadata must contain StationId.")
        if not metadata["StationId"].astype(str).reset_index(drop=True).equals(
            X["StationId"].reset_index(drop=True)
        ):
            raise ValueError("Metadata station IDs/order do not align with inputs.")
        if "Split" in metadata:
            splits = metadata["Split"].astype(str).str.upper()
            if splits.eq("FINAL_HOLDOUT").any():
                raise ValueError("Final-holdout metadata is not permitted.")
        if "Datetime" in metadata:
            metadata["Datetime"] = pd.to_datetime(
                metadata["Datetime"], errors="raise"
            )

    # This imports the packaged module and loads the frozen models.
    inference = import_inference(package)
    checked = inference.validate_feature_frame(X)
    if not isinstance(checked, pd.DataFrame) or list(checked.columns) != features:
        raise ValueError("Frozen inference validator did not preserve the contract.")

    predictions = inference.predict_aqi(checked)
    missing_outputs = [c for c in OUTPUT_COLUMNS if c not in predictions.columns]
    if missing_outputs:
        raise RuntimeError(f"Prediction outputs missing: {missing_outputs}")

    pred_values = predictions[OUTPUT_COLUMNS].to_numpy(dtype=float)
    if not np.isfinite(pred_values).all():
        raise RuntimeError("Non-finite predictions returned.")

    expected_ensemble = (
        w_et * predictions["AQI_pred_extra_trees"].to_numpy(dtype=float)
        + w_rf * predictions["AQI_pred_random_forest"].to_numpy(dtype=float)
    )
    max_difference = float(np.max(np.abs(
        expected_ensemble - predictions["AQI_t_plus_1_pred"].to_numpy(dtype=float)
    )))
    if max_difference > 1e-10:
        raise RuntimeError("Ensemble arithmetic check failed.")

    created = pd.Timestamp.now(tz="UTC")
    output = pd.DataFrame({
        "InputRowIndex": np.arange(len(X)),
        "StationId": X["StationId"].to_numpy(),
        "AQI_pred_extra_trees": predictions["AQI_pred_extra_trees"].to_numpy(),
        "AQI_pred_random_forest": predictions["AQI_pred_random_forest"].to_numpy(),
        "AQI_t_plus_1_pred": predictions["AQI_t_plus_1_pred"].to_numpy(),
        "PredictionHorizonHours": 1,
        "Target": "AQI_t_plus_1",
        "ModelPackageVersion": release.get("package_version", "unknown"),
        "FeatureContractVersion": contract.get("contract_version", "unknown"),
        "RunType": "OFFLINE_BATCH",
        "FeatureValidationStatus": "PASS",
        "SourceFreshnessStatus": "NOT_CHECKED",
        "ProductionStatus": "DISABLED",
        "PredictionGeneratedAtUTC": created,
    })

    if metadata is not None:
        if "Datetime" in metadata:
            output["PredictionTime"] = metadata["Datetime"].to_numpy()
            output["TargetTime"] = (
                metadata["Datetime"] + pd.Timedelta(hours=1)
            ).to_numpy()
        if "StationName" in metadata:
            output["StationName"] = metadata["StationName"].to_numpy()
        if "Split" in metadata:
            output["InputSplit"] = metadata["Split"].astype(str).to_numpy()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    if not args.overwrite and (
        output_path.exists() or diagnostics_path.exists()
    ):
        raise FileExistsError("Output appeared during the run; refusing overwrite.")

    diagnostics = {
        "status": "PASS",
        "run_type": "OFFLINE_BATCH",
        "input_path": str(input_path),
        "output_path": str(output_path),
        "rows": len(output),
        "station_count": int(X["StationId"].nunique()),
        "feature_count": len(features),
        "exact_feature_order": True,
        "all_inputs_finite": True,
        "ensemble_arithmetic_max_abs_difference": max_difference,
        "source_freshness_validated": False,
        "live_source_validated": False,
        "production_enabled": False,
        "models_retrained": False,
        "models_retuned": False,
    }

    output.to_parquet(output_path, index=False)
    with diagnostics_path.open("x", encoding="utf-8") as stream:
        json.dump(diagnostics, stream, indent=2)

    print("OFFLINE BATCH INFERENCE: PASS")
    print(f"Rows: {len(output)}; stations: {X['StationId'].nunique()}")
    print(f"Predictions: {output_path}")
    print(f"Diagnostics: {diagnostics_path}")
    print("Production remains disabled.")

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(1)
