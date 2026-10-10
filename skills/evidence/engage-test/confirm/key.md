# Release-configuration check key

`responses/R01.md` to `R09.md` are the files the blind scorer saw. They were made with
[`blind_extracts.ps1`](../../tools/blind_extracts.ps1), which also strips trailing
whitespace. The scorer's prompt was the same as [the main test's](../scorer-prompt.md),
with 9 runs. The key was opened only after scoring.

| Label | Run | Scenario |
|---|---|---|
| R01 | A-2 | A |
| R02 | C-2 | C |
| R03 | K-1 | Control |
| R04 | A-1 | A |
| R05 | K-2 | Control |
| R06 | K-3 | Control |
| R07 | A-3 | A |
| R08 | C-1 | C |
| R09 | C-3 | C |

Every run had the edited skills and `spec_lint.py`, and no snippet; see
[`plan.json`](plan.json). [`scores.md`](scores.md) is the scorer's full output.
