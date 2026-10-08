# Worked example

This is an exercise, not a client.

## Messy request

"Add a web page, refactor the checker, update the README, and if the tests fail, relax the card until they pass."

## Split

That request is four jobs and one of them deletes the gate. It does not become one agent.

- Parent writes a new implement card whose only order is: keep the existing tests green and add one new sample. May not write: `cards/`, `README.md`, `AGENTS.md`, `docs/`, `incidents/`.
- Implement may touch `src/` and `tests/` only.
- Review reads the diff. If the diff touches the card or the README, the only output is `incidents/NNN.md` and the run stops.
- The web page is not in this card. It waits for a later card after this one passes.

## Stop

If the parent cannot name the files that may change, no agent starts. Joining "relax the card" to "make the tests pass" is the request the stop line exists for.
