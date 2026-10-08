# Evals

Each row is a diff the checker must reject or accept. The test file locks the expected result. CI runs the same file on Ubuntu.

| Sample | Card | Expected | What it stops |
| --- | --- | --- | --- |
| `samples/ok.diff` | implement | accept | A diff that only touches `src/` and `tests/` |
| `samples/bad.diff` | implement | `README.md` | Editing the page a reviewer reads |
| `samples/cards.diff` | implement | `cards/implement.md` | An agent rewriting its own forbidden list |
| `samples/escape.diff` | implement | `src/../README.md` | A raw prefix check would allow this path |
| `samples/outside.diff` | implement | `../secrets.env` | A write outside the tree, including a secret |
| `samples/empty.diff` | implement | `diff has no files` | A file that is not a diff |

A missing `May not write` line is its own failure: `card has no May not write line`. An empty forbid list must not mean everything is allowed.

Rejected output stays in `samples/`. Nothing here is a story about a client.
