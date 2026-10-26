# Delhi AQI — Offline Batch Inference Candidate

This is an offline inference tool, not a live AQI service. It accepts a
Parquet file containing exactly the 73 frozen features in exact order.
It does not fetch live data or construct features from raw observations.

The runner verifies the two model SHA-256 hashes before loading them, rejects
unknown stations, missing/non-finite values, feature mismatches, and final
holdout metadata, and does not impute missing inputs.

Example:

    python src/batch_predict.py --input features.parquet --output new_predictions.parquet --metadata metadata.parquet

Metadata may contain only StationId and optional Datetime, StationName, Split
columns. Metadata must align with the feature rows. Existing output files are
not overwritten unless --overwrite is supplied.

The candidate does not verify source freshness or prove a live source is valid.
Production remains disabled.
