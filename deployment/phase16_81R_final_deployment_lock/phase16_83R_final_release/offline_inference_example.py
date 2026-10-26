# ==============================================================================
# OFFLINE INFERENCE EXAMPLE — PHASE 16.83R
# ==============================================================================

from pathlib import Path
import json
import numpy as np
import pandas as pd
import joblib

PROJECT_ROOT = Path("/content/drive/MyDrive/Delhi-AQI-Prediction")
PACKAGE = Path("/content/drive/MyDrive/Delhi-AQI-Prediction/deployment/phase16_33_frozen_model_package")

with open(
    PACKAGE / "config" / "feature_contract.json",
    "r"
) as f:
    contract = json.load(f)

FEATURES = contract["feature_order"]

ET = joblib.load(
    PACKAGE / "models" /
    "phase15_10_final_tuned_extra_trees_trainval.joblib"
)

RF = joblib.load(
    PACKAGE / "models" /
    "phase15_10_final_tuned_random_forest_trainval.joblib"
)

def predict_frozen_ensemble(
    X: pd.DataFrame
) -> np.ndarray:

    if list(X.columns) != FEATURES:
        raise ValueError(
            "Input does not exactly match the frozen 73-feature contract."
        )

    if X.isna().any().any():
        raise ValueError(
            "Input contains missing values. "
            "Use a fully prepared frozen-contract feature frame."
        )

    et_pred = np.asarray(
        ET.predict(X),
        dtype=float
    )

    rf_pred = np.asarray(
        RF.predict(X),
        dtype=float
    )

    return (
        0.594466 * et_pred
        + 0.405534 * rf_pred
    )

# Production is intentionally disabled.
# prediction = predict_frozen_ensemble(X)
# print(prediction)
