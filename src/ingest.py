from pathlib import Path
from typing import Iterable, Optional, Union, List
import pandas as pd

def guess_header_row(xlsx_path: Union[str, Path], sheet_name: str, look_rows: int = 40) -> int:
    """
    Heuristically guess which row contains real column names by scanning the top `look_rows`.
    Returns 0-based row index suitable for pandas' `header=`.
    """
    tmp = pd.read_excel(xlsx_path, sheet_name=sheet_name, header=None, nrows=look_rows)
    scores = []
    for i in range(len(tmp)):
        row = tmp.iloc[i]
        nonnull = row.notna().sum()
        texty = sum(isinstance(v, str) for v in row)
        uniq = row.nunique(dropna=True)
        scores.append((i, int(nonnull), int(texty), int(uniq)))
    # Choose the row that looks most header-like
    scores.sort(key=lambda t: (t[1], t[2], t[3]), reverse=True)
    return scores[0][0]

def load_journey_event(
    xlsx_path: Union[str, Path],
    sheet_name: str = "Journey_Event_Sample",
    header: Union[int, str] = "auto",           # "auto" or explicit 0-based row
    usecols: Optional[str] = None,              # e.g., "B:BC" to skip blank col A
    nrows: Optional[int] = None,                # e.g., 400 during exploration
    date_cols: Optional[Iterable[str]] = None,  # e.g., ["RTC Date Time","GPS Date Time","Event Time Stamp"]
    dayfirst: bool = True,
    drop_unnamed: bool = True
) -> pd.DataFrame:
    """
    Load a Journey Event-like sheet robustly.

    - Auto-detect header row if header="auto".
    - Optionally restrict columns via Excel range notation (e.g., "B:BC").
    - Optionally limit rows for fast iteration (nrows).
    - Convert date columns with day-first parsing and coerce bad values to NaT.
    - Optionally drop 'Unnamed: ...' columns.
    """
    xlsx_path = Path(xlsx_path)

    # 1) Decide header row
    if header == "auto":
        header_idx = guess_header_row(xlsx_path, sheet_name)
    else:
        header_idx = int(header)

    # 2) Load
    df = pd.read_excel(
        xlsx_path,
        sheet_name=sheet_name,
        header=header_idx,
        nrows=nrows,
        usecols=usecols
    )

    # 3) Tidy columns: drop Unnamed
    if drop_unnamed:
        drop_these = [c for c in df.columns if str(c).startswith("Unnamed")]
        if drop_these:
            df = df.drop(columns=drop_these)

    # 4) Dates
    if date_cols:
        present = [c for c in date_cols if c in df.columns]
        for c in present:
            df[c] = pd.to_datetime(df[c], dayfirst=dayfirst, errors="coerce")

    return df