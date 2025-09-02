from pathlib import Path
from typing import Iterable, Optional, Union
import pandas as pd

def guess_header_row(xlsx_path: Union[str, Path], sheet_name: str, look_rows: int = 40) -> int:
    """
    Try to guess which row contains column headers by scanning the first `look_rows` rows.
    Returns a 0-based row index suitable for pandas' `header=`.
    """
    # Read first few rows without treating any row as header
    tmp = pd.read_excel(xlsx_path, sheet_name=sheet_name, header=None, nrows=look_rows)

    scores = []
    for i in range(len(tmp)):
        row = tmp.iloc[i]
        nonnull = row.notna().sum()                  # how many non-empty cells
        texty = sum(isinstance(v, str) for v in row) # how many look like text
        uniq = row.nunique(dropna=True)              # how many unique values
        scores.append((i, int(nonnull), int(texty), int(uniq)))

    # Pick row with most filled + most text-like cells (heuristic)
    scores.sort(key=lambda t: (t[1], t[2], t[3]), reverse=True)
    return scores[0][0]


def load_journey_event(
    xlsx_path: Union[str, Path],
    sheet_name: str = "Journey_Event_Sample",
    header: Union[int, str] = "auto",           # "auto" = guess, or give row index (0-based)
    usecols: Optional[str] = None,              # Excel range string, e.g., "B:BC" to skip first blank column
    nrows: Optional[int] = None,                # Limit rows (fast testing)
    date_cols: Optional[Iterable[str]] = None,  # Which columns to parse as datetime
    dayfirst: bool = True,                      # Parse day-first dates (UK style)
    drop_unnamed: bool = True                   # Drop columns named "Unnamed: ..."
) -> pd.DataFrame:
    """
    Load a Journey Event sheet cleanly:
      1. Auto-detect header row if needed.
      2. Restrict to subset of rows/cols if specified.
      3. Drop any 'Unnamed: ...' columns (common in Excel).
      4. Parse given date columns as datetime, coercing errors to NaT.
    Returns a tidy DataFrame.
    """
    xlsx_path = Path(xlsx_path)

    # --- Step 1: decide which row has headers ---
    if header == "auto":
        header_idx = guess_header_row(xlsx_path, sheet_name)
    else:
        header_idx = int(header)

    # --- Step 2: load the Excel sheet ---
    df = pd.read_excel(
        xlsx_path,
        sheet_name=sheet_name,
        header=header_idx,
        nrows=nrows,
        usecols=usecols
    )

    # --- Step 3: drop 'Unnamed' columns that are artifacts from Excel ---
    if drop_unnamed:
        drop_these = [c for c in df.columns if str(c).startswith("Unnamed")]
        if drop_these:
            df = df.drop(columns=drop_these)

    # --- Step 4: convert date columns to datetime (with error handling) ---
    if date_cols:
        present = [c for c in date_cols if c in df.columns]
        for c in present:
            df[c] = pd.to_datetime(df[c], dayfirst=dayfirst, errors="coerce")

    return df

from typing import Dict, Any, Optional
from pathlib import Path

# (keep your existing imports and functions above)

def load_journey_event_with_config(
    xlsx_path: Path,
    cfg: Dict[str, Any],
    *,
    write_interim: Optional[Path] = None
):
    """
    Convenience wrapper:
      - Uses your existing load_journey_event()
      - Selects keep_cols (if provided)
      - Runs validation (if validate=True)
      - Optionally writes an interim file (parquet or csv based on extension)
      - Returns the final DataFrame (usually the keep set)

    Expected cfg keys (all optional except sheet_name):
      sheet_name: str                     # e.g., "Journey_Event_Sample"
      header: int or "auto"               # autodetect or explicit 0-based row
      usecols: str or None                # e.g., "B:BC"
      nrows: int or None                  # sample size during exploration
      date_cols: list[str] or None        # columns to parse as datetime
      dayfirst: bool                      # default True (UK style)
      drop_unnamed: bool                  # default True
      keep_cols: list[str] or None        # if provided, select these columns
      validate: bool                      # if True, run validate_journey_event()
    """
    # --- 1) Load using the base loader
    df = load_journey_event(
        xlsx_path=xlsx_path,
        sheet_name=cfg.get("sheet_name", "Journey_Event_Sample"),
        header=cfg.get("header", "auto"),
        usecols=cfg.get("usecols"),
        nrows=cfg.get("nrows"),
        date_cols=cfg.get("date_cols"),
        dayfirst=cfg.get("dayfirst", True),
        drop_unnamed=cfg.get("drop_unnamed", True),
    )

    # --- 2) Select keep columns if provided
    keep_cols = cfg.get("keep_cols")
    if keep_cols:
        present = [c for c in keep_cols if c in df.columns]
        df = df[present].copy()

    # --- 3) Validate if requested
    if cfg.get("validate", False):
        try:
            # lazy import to avoid circulars if validate isn’t installed yet
            from src.validate import validate_journey_event
            validate_journey_event(df)
        except ImportError:
            raise RuntimeError("Validation requested but src.validate not available")

    # --- 4) Optional: write an interim file if path given
    if write_interim:
        out = Path(write_interim)
        out.parent.mkdir(parents=True, exist_ok=True)
        if out.suffix.lower() == ".parquet":
            df.to_parquet(out, index=False)
        elif out.suffix.lower() in {".csv", ".txt"}:
            df.to_csv(out, index=False)
        else:
            raise ValueError(f"Unsupported interim extension: {out.suffix}")

    return df