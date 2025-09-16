

# src/utils.py
import pandas as pd

def guess_header_row(xlsx_path, sheet_name, look_rows=60):
    tmp = pd.read_excel(xlsx_path, sheet_name=sheet_name, header=None, nrows=look_rows)
    scores = []
    for i in range(len(tmp)):
        row = tmp.iloc[i]
        nonnull = row.notna().sum()
        texty = sum(isinstance(v, str) for v in row)
        uniq = row.nunique(dropna=True)
        scores.append((i, int(nonnull), int(texty), int(uniq)))
    scores.sort(key=lambda t: (t[1], t[2], t[3]), reverse=True)
    return scores[0][0]