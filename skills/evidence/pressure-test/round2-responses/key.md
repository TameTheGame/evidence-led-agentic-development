# Round 2 key

`R01.md` to `R12.md` are the files the scorer saw. They are the agents' responses in
shuffled order, each with a header giving the scenario and the owner's message.

**Redactions.** Before scoring, only text naming a rigor level was removed. Everything else
is as the agent wrote it. The key was opened only after scoring.

| Label | Scenario | Condition | Run | Removed before scoring |
|---|---|---|---|---|
| R01 | C | ELAD skills | 3 | `Rigor: evaluated. ` |
| R02 | C | No skills | 1 | — |
| R03 | A | No skills | 1 | — |
| R04 | A | ELAD skills | 3 | `Rigor: light. ` |
| R05 | C | ELAD skills | 1 | `**Rigor: bounded.** ` |
| R06 | A | ELAD skills | 2 | `Rigor: light. ` and `I'll move up to bounded if the generator or the tests assume exactly two spawns.` |
| R07 | C | No skills | 3 | — |
| R08 | A | No skills | 3 | — |
| R09 | C | ELAD skills | 2 | `Rigor: bounded. ` |
| R10 | A | No skills | 2 | — |
| R11 | A | ELAD skills | 1 | `**Rigor: light.** ` |
| R12 | C | No skills | 2 | — |

**One edit after scoring.** In `R12.md`, one blank line held three spaces, which this
repository's whitespace check rejects. They were removed. Nothing else changed.

[`scores.md`](scores.md) is the scorer's full output. [`scorer-prompt.md`](scorer-prompt.md)
is what the scorer was told.
