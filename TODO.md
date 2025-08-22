# TODO

## Current session
- Repo scaffolded (README, .gitignore, LICENSE, CONTRIBUTING.md)
- Linked GitHub Desktop + VS Code
- Created and committed `.venv`
- Installed minimal packages (pandas, openpyxl, jupyter)
- Added requirements.txt

## Next session
- Reactivate venv (`source .venv/bin/activate`)
- Start first Jupyter notebook inside VS Code
- Test reading a sample Excel file into pandas
- Begin thinking about chunking strategy for big files

## (19 Aug 2025)
- Notebook set to repo-root CWD.
- Loaded ~400 rows from Journey_Event_Sample via usecols="B:BC".
- Parsed date cols with to_datetime(dayfirst=True); basic re-audit done.

## Next session
- Re-run notebook to checkpoint cell.
- Update sheet_map: Journey_Event_Sample starts at Row 16, Column B (header auto-detected).
- Define minimal keep-columns list (IDs, timestamps, lat/long, speeds).
- Start data_dictionary.md with those columns (meaning, type).

## (21 Aug 2025)
- Minimal keep set defined; interim parquet written at data/interim/journey_event_sample_keep.parquet
- Next: validate assumptions (units for speed/limit, const-ness of IDs), and promote load logic to src/ingest.py

## (22 Aug 2025)
- Added reusable loader `src/ingest.py` with header autodetect, usecols, and date parsing.
- Created schema validator `src/validate.py` and ran P‑T‑R checks on df_keep.
- Defined minimal keep set and saved interim Parquet at `data/interim/journey_event_sample_keep.parquet`.

## for next session
- Add per-dataset validators (e.g., `validate_connection`, `validate_installation`) as needed.
- Extend data_dictionary.md with remaining Journey_Event columns (10–15 at a time).
- Optional: add a config dict so `load_journey_event()` can also select keep_cols and return `df_keep` directly.
- Optional: branch practice — create `feature/ingest-pipeline` and open a small PR to merge back to main.
- [ ] Add config dict wrapper for Journey Event loader (next session)
- [ ] Re-run validator through wrapper to confirm same results