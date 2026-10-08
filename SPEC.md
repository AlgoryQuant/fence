# Spec

A coding agent is allowed to start only after a card exists. The card is written by a person. The agent does not get to widen it.

## Card

Every card has the same seven lines:

1. Role. One job.
2. Name. So two agents cannot share a pen.
3. May read. The only inputs.
4. May not write. The eval uses this line.
5. Order. The steps, in order.
6. Stop. When to halt, including the case where the result is empty.
7. Output. The only artifact that counts as done.

`cards/implement.md` may change `src/` and `tests/`. It may not change the card, the README, or `AGENTS.md`. `cards/review.md` may write only `incidents/`. `cards/parent.md` writes the task and does not implement it.

## What the checker proves

`src/fence.py` reads `May not write` and the paths in a unified diff. It exits 0 when every path stays outside that list. It exits 1 and prints the first forbidden path otherwise.

Paths are normalized before the comparison. `src/../README.md` is `README.md`. A path that climbs out of the tree with `..`, or an absolute path, is forbidden even when the card forgot to name it.

## What a pass is

Both sample diffs behave as specified, and `pytest` is green in CI on a clean machine. A pass is not a claim that a model obeyed. A pass is a diff that stayed inside the card.

## Out of scope

This repo does not deploy an agent, call a model, or store a customer engagement. The method is the card, the rejected diffs under `samples/`, and the tests that lock the expected result.
