Parent writes one card before a run and does not implement it.
Implement follows cards/implement.md and may write only under src/ and tests/.
Review follows cards/review.md and may write only under incidents/.
Cards, this file, and the README stay frozen during a run.
A path is judged after `.` and `..` are collapsed. Climbing out of the tree is forbidden.
If a run touches a forbidden path, stop. Record the diff under samples/ and lock the expected result in tests/.
The checker is the gate. A model's own summary is not a pass.
