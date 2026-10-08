# fence

`fence` checks a diff against an agent card. It exits 0 when every changed file stays outside the card's `May not write` list. Otherwise it exits 1 and prints the first forbidden path.

The cards in `cards/` were written before the checker. `AGENTS.md` says who may write where.

## Run the tests

```powershell
cd C:\fence
py -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m pytest
```

## Check a diff

```powershell
.\.venv\Scripts\python src\fence.py check --card cards\implement.md --diff samples\ok.diff
.\.venv\Scripts\python src\fence.py check --card cards\implement.md --diff samples\bad.diff
```

The first command exits 0. The second prints `README.md` and exits 1.
