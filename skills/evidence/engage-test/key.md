# Engagement test key

`responses/R01.md` to `R15.md` are the files the blind scorer saw. They are the analyzer's
extracts in shuffled order, each with a header giving:

- the scenario;
- the owner's message;
- whether the project had `spec_lint.py`; and
- for the control, the planted typo.

All three A conditions are labelled "Scenario A". The key was opened only after scoring.

| Label | Run | Condition |
|---|---|---|
| R01 | K-3 | Control |
| R02 | K-2 | Control |
| R03 | A-2 | A, with snippet and lint |
| R04 | A-1 | A, with snippet and lint |
| R05 | A-3 | A, with snippet and lint |
| R06 | C-2 | C, with snippet and lint |
| R07 | C-3 | C, with snippet and lint |
| R08 | K-1 | Control |
| R09 | N-2 | A, no snippet |
| R10 | N-3 | A, no snippet |
| R11 | L-3 | A, no lint |
| R12 | L-1 | A, no lint |
| R13 | N-1 | A, no snippet |
| R14 | C-1 | C, with snippet and lint |
| R15 | L-2 | A, no lint |

**One edit after scoring.** In `R02.md`, one blank line held a space from the agent's
reply, which this repository's whitespace check rejects. It was removed; nothing else
changed.

[`scores.md`](scores.md) is the scorer's full output. [`scorer-prompt.md`](scorer-prompt.md)
is what the scorer was told.
