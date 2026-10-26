"""
Frozen Delhi AQI production-source guard.

Live production inference remains blocked until a validated
source supplies the exact frozen 73-feature vector.
"""

PRODUCTION_SOURCE_STATUS = "NO_VALIDATED_LIVE_AQI_SOURCE"
EXPECTED_FEATURE_COUNT = 73


class ProductionSourceBlocked(RuntimeError):
    pass


def assert_production_source_ready():
    if (
        PRODUCTION_SOURCE_STATUS
        != "VALIDATED_LIVE_SOURCE_AVAILABLE"
    ):
        raise ProductionSourceBlocked(
            "Live inference blocked: no validated source supplies "
            "the frozen 73-feature vector."
        )


def validate_feature_order(
    feature_names,
    expected_features
):
    assert_production_source_ready()

    actual = list(feature_names)
    expected = list(expected_features)

    if len(actual) != EXPECTED_FEATURE_COUNT:
        raise ValueError(
            f"Expected {EXPECTED_FEATURE_COUNT} features; "
            f"received {len(actual)}."
        )

    if actual != expected:
        raise ValueError(
            "Feature order does not match the frozen contract."
        )

    return True
