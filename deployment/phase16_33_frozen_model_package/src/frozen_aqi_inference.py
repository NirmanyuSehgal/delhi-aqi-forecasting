from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
MODEL_ROOT = PACKAGE_ROOT / "models"
CONFIG_ROOT = PACKAGE_ROOT / "config"


with open(
    CONFIG_ROOT / "feature_contract.json",
    "r"
) as f:
    FEATURE_CONTRACT = json.load(f)


with open(
    CONFIG_ROOT / "ensemble_config.json",
    "r"
) as f:
    ENSEMBLE_CONFIG = json.load(f)


FEATURE_ORDER = FEATURE_CONTRACT["feature_order"]


EXTRA_TREES = joblib.load(
    MODEL_ROOT
    / "phase15_10_final_tuned_extra_trees_trainval.joblib"
)

RANDOM_FOREST = joblib.load(
    MODEL_ROOT
    / "phase15_10_final_tuned_random_forest_trainval.joblib"
)


def validate_feature_frame(X):
    """
    Enforce the exact frozen 73-feature inference contract.
    """

    if not isinstance(X, pd.DataFrame):
        raise TypeError(
            "Inference input must be a pandas DataFrame."
        )

    if len(X) == 0:
        raise ValueError(
            "Inference input contains zero rows."
        )

    expected = list(FEATURE_ORDER)
    actual = list(X.columns)

    missing = [
        f for f in expected
        if f not in actual
    ]

    unexpected = [
        f for f in actual
        if f not in expected
    ]

    if missing:
        raise ValueError(
            "Missing frozen features: "
            + ", ".join(missing)
        )

    if unexpected:
        raise ValueError(
            "Unexpected inference features: "
            + ", ".join(unexpected)
        )

    # Enforce exact frozen column order.
    X = X.loc[:, expected].copy()

    if X.shape[1] != 73:
        raise ValueError(
            f"Expected 73 features, got {X.shape[1]}."
        )

    if X.isna().any().any():

        missing_counts = (
            X.isna()
            .sum()
            .loc[lambda s: s > 0]
            .to_dict()
        )

        raise ValueError(
            "Missing values detected: "
            + repr(missing_counts)
        )

    return X


def predict_aqi(X):
    """
    Frozen weighted ensemble prediction.

    Returns:
        AQI_pred_extra_trees
        AQI_pred_random_forest
        AQI_t_plus_1_pred
    """

    X = validate_feature_frame(X)

    pred_et = np.asarray(
        EXTRA_TREES.predict(X),
        dtype=float
    )

    pred_rf = np.asarray(
        RANDOM_FOREST.predict(X),
        dtype=float
    )

    weight_et = float(
        ENSEMBLE_CONFIG[
            "weights"
        ][
            "tuned_extra_trees"
        ]
    )

    weight_rf = float(
        ENSEMBLE_CONFIG[
            "weights"
        ][
            "tuned_random_forest"
        ]
    )

    pred_ensemble = (
        weight_et * pred_et
        + weight_rf * pred_rf
    )

    return pd.DataFrame({
        "AQI_pred_extra_trees":
            pred_et,

        "AQI_pred_random_forest":
            pred_rf,

        "AQI_t_plus_1_pred":
            pred_ensemble,
    })
