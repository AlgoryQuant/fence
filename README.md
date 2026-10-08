# fence

`fence` is a gate for coding agents. A person writes a card first. The card names the only files an agent may change. The checker reads that card and a diff. It exits 0 when the diff stays inside the card. Otherwise it exits 1 and prints the first forbidden path.

The proof is the eval set, not a description of the model. `samples/` holds the accepted diff and the diffs that must be rejected, including a path that climbs out through `..` and a write of a secret outside the tree. `docs/EVALS.md` is the table. `SPEC.md` is the card format. `docs/EXAMPLE.md` turns one messy request into separate cards and is labeled as an exercise.

## Run

```powershell
cd C:\fence
py -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m pytest
```

On macOS or Linux, use `python3 -m venv .venv` and `./.venv/bin/python -m pytest`.

## Check one diff

```powershell
.\.venv\Scripts\python src\fence.py check --card cards\implement.md --diff samples\ok.diff
.\.venv\Scripts\python src\fence.py check --card cards\implement.md --diff samples\bad.diff
```

The first command exits 0. The second prints `README.md` and exits 1.

CI runs the same tests on every push.
