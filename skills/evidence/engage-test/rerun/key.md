# Correction-cycle key

`responses/R01.md` to `R09.md` are the files the blind scorer saw. The scorer's prompt was
the same as [the main test's](../scorer-prompt.md), with 9 runs instead of 15. The key was
opened only after scoring.

| Label | Run | Condition |
|---|---|---|
| R01 | Q-1 | Control, no snippet |
| R02 | S-2 | Control, fixed snippet |
| R03 | S-1 | Control, fixed snippet |
| R04 | Q-3 | Control, no snippet |
| R05 | B-2 | A, fixed snippet |
| R06 | S-3 | Control, fixed snippet |
| R07 | Q-2 | Control, no snippet |
| R08 | B-3 | A, fixed snippet |
| R09 | B-1 | A, fixed snippet |

**One edit after scoring.** In `R06.md`, one line held trailing whitespace from the
agent's reply, which this repository's whitespace check rejects. It was removed; nothing
else changed.

[`scores.md`](scores.md) is the scorer's full output.
