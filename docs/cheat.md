# Cheatsheet

Virtual environment (Mac)
	•	Create: python3 -m venv .venv
	•	Activate: source .venv/bin/activate
	•	Deactivate: deactivate
	•	Upgrade pip: python3 -m pip install --upgrade pip
	•	Install pkgs: pip install pandas openpyxl jupyter
	•	Save env: pip freeze > requirements.txt

    Tip: In .vscode/settings.json
    { "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python" }

    Git basics (solo workflow)
	•	Status: git status
	•	Stage: git add <file> or git add -A
	•	Commit: git commit -m "type: short, imperative message"
	•	Push: git push origin main
	•	Pull: git pull
	•	Undo last (soft): git reset --soft HEAD~1

Commit message “types” you can use: feat, fix, docs, chore, refactor, test, data.

Jupyter notebook habits
	•	Two cell types: Markdown (explain) and Code (do).
	•	Keep a header cell: goal, inputs, outputs.
	•	Small, linear steps; run all cells before committing.
	•	Prefer Parquet for interim data (fast, keeps dtypes).
	•	Install once: pip install pyarrow
	•	Write: df.to_parquet("data/interim/file.parquet", index=False)
	•	Read: pd.read_parquet("data/interim/file.parquet")

---

## Session start ritual (5 mins)
1. **Open repo** in VS Code.
2. **Activate venv**:  
   ```bash
   source .venv/bin/activate


## Session end ritual (5 mins)
	1.	Notebook checkpoint: add a markdown cell:
        ## ✅ Stopped here — next: <one concrete next step>
    2.	Save interim output (fast reload later):
        from pathlib import Path
        Path("data/interim").mkdir(parents=True, exist_ok=True)
        # example
    3.	Docs breadcrumb: update TODO.md (Today / Next session).
    4.	Commit & push (text/code only):
        git add notebooks/*.ipynb docs/*.md src/**/*.py
        git commit -m "checkpoint: <short what changed>"
        git push
    5.	Close Excel (to clear ~$ lock files) → optional deactivate.