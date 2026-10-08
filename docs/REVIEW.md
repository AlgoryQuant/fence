# Review of `samples/cards.diff`

Verdict: do not merge.

The diff replaces the implement card's forbid line with an empty one. The next run would hit `card has no May not write line` only if someone noticed. If the empty line were instead deleted by a later edit that left no line at all, the checker already fails closed. This diff does not get that far: it writes `cards/implement.md`, which the card itself forbids.

The agent that produced it was allowed to change `src/` and `tests/` only. Touching the card is the change that cannot be undone by reading the model's summary, because the summary would be judged by the weakened card.

The only output of review is this record. The card stays as it was.
