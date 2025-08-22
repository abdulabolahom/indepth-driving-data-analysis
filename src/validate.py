# src/validate.py
from typing import Dict, Iterable, Optional
import pandas as pd
import numpy as np

class SchemaError(AssertionError):
    """Raised when the dataframe does not meet the schema contract."""

def check_presence(df: pd.DataFrame, required_cols: Iterable[str]) -> None:
    """Fail if any required column is missing."""
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise SchemaError(f"Missing required columns: {missing}")

def check_types(df: pd.DataFrame, expected_types: Dict[str, str]) -> None:
    """
    Fail if a column's dtype doesn't match the expectation.
    expected_types values accepted: 'datetime', 'numeric', 'string'
    """
    for col, kind in expected_types.items():
        if col not in df.columns:
            continue  # presence handled earlier
        dtype = df[col].dtype

        if kind == "datetime":
            ok = str(dtype).startswith("datetime64")
        elif kind == "numeric":
            ok = pd.api.types.is_numeric_dtype(dtype)
        elif kind == "string":
            # allow object or string dtypes
            ok = pd.api.types.is_string_dtype(dtype) or dtype == "object"
        else:
            raise ValueError(f"Unknown kind {kind} for {col}")

        if not ok:
            raise SchemaError(f"Column '{col}' has dtype {dtype}, expected {kind}")

def check_ranges(df: pd.DataFrame) -> None:
    """
    Minimal sanity checks for Journey Event-like data.
    Rules are lenient (allow NaN) but catch absurd values.
    """
    # Latitude [-90, 90], Longitude [-180, 180]
    if "Latitude" in df.columns:
        bad_lat = df["Latitude"].dropna().pipe(lambda s: (s < -90) | (s > 90)).sum()
        if bad_lat:
            raise SchemaError(f"Latitude out of range count: {bad_lat}")
    if "Longitude" in df.columns:
        bad_lon = df["Longitude"].dropna().pipe(lambda s: (s < -180) | (s > 180)).sum()
        if bad_lon:
            raise SchemaError(f"Longitude out of range count: {bad_lon}")

    # Speeds should not be crazy negative (allow small negatives if noise)
    for c in ("Horizontal Speed", "Road Speed Limit"):
        if c in df.columns and pd.api.types.is_numeric_dtype(df[c]):
            bad = df[c].dropna().lt(-1e-6).sum()
            if bad:
                raise SchemaError(f"{c} has {bad} negative values")

def validate_journey_event(df: pd.DataFrame) -> None:
    """
    Run the P-T-R checks for Journey Event minimal keep set.
    Raise SchemaError on failure; silent (return None) on success.
    """
    required = [
        "Journey ID", "Event Time Stamp", "GPS Date Time",
        "Latitude", "Longitude", "Horizontal Speed", "Road Speed Limit",
    ]
    check_presence(df, required)

    expected_types = {
        "Journey ID": "string",
        "Event Time Stamp": "datetime",
        "GPS Date Time": "datetime",
        "Latitude": "numeric",
        "Longitude": "numeric",
        "Horizontal Speed": "numeric",
        "Road Speed Limit": "numeric",
    }
    check_types(df, expected_types)

    check_ranges(df)