This file is not code. It is the task. The program stays in `src/fence.py` until a separate run implements this.

Role: write the task before any agent runs.

Name: Parent.

May read: the request only.

May not write: src/, tests/, cards/implement.md, cards/review.md.

May write: cards/parent.md until the run starts. After the run starts this card is frozen.

Order: one diff changes both src/fence.py and README.md. fence prints README.md and exits 1. Add that diff as samples/mixed.diff and add one test. Leave the existing six cases green.

Stop: the new test passes and the report prints cases 7, passed 7, failed 0. Do not add a second feature. Do not edit cards, README, AGENTS, or incidents in the implement run.

Output: one card. Do not implement it.
