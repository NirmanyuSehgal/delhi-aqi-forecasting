
from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd

# This candidate lives in deployment/phase17_06_inference_api/src/.
PACKAGE_ROOT = (
    Path(__file__).resolve().parents[2]
    / "phase16_33_frozen_model_package"
)
MODEL_ROOT = PACKAGE_ROOT / "models"
CONFIG_ROOT = PACKAGE_ROOT / "config"

with open(CONFIG_ROOT / "feature_contract.json", "r", encoding="utf-8") as f:
    FEATURE_CONTRACT = json.load(f)

with open(CONFIG_ROOT / "ensemble_config.json", "r", encoding="utf-8") as f:
    ENSEMBLE_CONFIG = json.load(f)

FEATURE_ORDER = list(FEATURE_CONTRACT["feature_order"])

SUPPORTED_STATIONS = {
    "DL002", "DL004", "DL007", "DL010", "DL013",
    "DL019", "DL021", "DL028", "DL031", "DL034",
}

# Load the large frozen artifacts only when a real prediction is requested.
_EXTRA_TREES = None
_RANDOM_FOREST = None

def validate_feature_frame(X):
    """Validate the frozen 73-column contract while preserving valid NaNs."""

    if not isinstance(X, pd.DataFrame):
        raise TypeError("Inference input must be a pandas DataFrame.")

    if X.empty:
        raise ValueError("Inference input contains zero rows.")

    expected = list(FEATURE_ORDER)
    actual = list(X.columns)

    missing = [c for c in expected if c not in actual]
    unexpected = [c for c in actual if c not in expected]

    if missing:
        raise ValueError("Missing frozen features: " + ", ".join(missing))

    if unexpected:
        raise ValueError("Unexpected inference features: " + ", ".join(unexpected))

    X = X.loc[:, expected].copy()

    if X.shape[1] != 73:
        raise ValueError(f"Expected 73 features, got {X.shape[1]}.")

    if "StationId" not in X.columns:
        raise ValueError("StationId is required.")

    if X["StationId"].isna().any():
        raise ValueError("StationId must not be missing.")

    X["StationId"] = X["StationId"].astype(str).str.strip()

    unsupported = sorted(set(X["StationId"]) - SUPPORTED_STATIONS)
    if unsupported:
        raise ValueError("Unsupported station IDs: " + ", ".join(unsupported))

    numeric_features = [c for c in expected if c != "StationId"]

    for col in numeric_features:
        original = X[col]
        numeric = pd.to_numeric(original, errors="coerce")

        # Reject malformed non-null values; do not silently treat text as missing.
        malformed = original.notna() & numeric.isna()
        if malformed.any():
            examples = original.loc[malformed].astype(str).head(3).tolist()
            raise ValueError(
                f"Non-numeric values in feature {col!r}; examples: {examples}"
            )

        values = numeric.to_numpy(dtype=np.float64)
        if np.isinf(values).any():
            raise ValueError(f"Infinite values are not permitted in feature {col!r}.")

        # NaN is intentionally retained: the fitted frozen pipeline's
        # SimpleImputer is expected to handle missing numeric input.
        X[col] = numeric.astype(np.float64)

    return X


def predict_with_models(X, extra_trees, random_forest):
    """Apply frozen weights to supplied compatible estimators; useful for tests."""

    X = validate_feature_frame(X)

    pred_et = np.asarray(extra_trees.predict(X), dtype=float).reshape(-1)
    pred_rf = np.asarray(random_forest.predict(X), dtype=float).reshape(-1)

    if len(pred_et) != len(X) or len(pred_rf) != len(X):
        raise ValueError("Estimator prediction row count does not match input.")

    if not np.isfinite(pred_et).all() or not np.isfinite(pred_rf).all():
        raise ValueError("An estimator returned non-finite predictions.")

    weights = ENSEMBLE_CONFIG["weights"]
    weight_et = float(weights["tuned_extra_trees"])
    weight_rf = float(weights["tuned_random_forest"])

    pred_ensemble = weight_et * pred_et + weight_rf * pred_rf

    return pd.DataFrame({
        "AQI_pred_extra_trees": pred_et,
        "AQI_pred_random_forest": pred_rf,
        "AQI_t_plus_1_pred": pred_ensemble,
    })


def load_frozen_models():
    """Deserialize the original frozen models only when explicitly called."""

    global _EXTRA_TREES, _RANDOM_FOREST

    if _EXTRA_TREES is None:
        _EXTRA_TREES = joblib.load(
            MODEL_ROOT / "phase15_10_final_tuned_extra_trees_trainval.joblib"
        )

    if _RANDOM_FOREST is None:
        _RANDOM_FOREST = joblib.load(
            MODEL_ROOT / "phase15_10_final_tuned_random_forest_trainval.joblib"
        )

    return _EXTRA_TREES, _RANDOM_FOREST


def predict_aqi(X):
    """Predict with the frozen weighted ensemble; does not retrain models."""

    extra_trees, random_forest = load_frozen_models()
    return predict_with_models(X, extra_trees, random_forest)
