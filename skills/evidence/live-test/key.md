# S&box live retest key

`responses/R01.md` to `R24.md` are the files the blind scorer saw. They are the analyzer's
extracts in shuffled order, each with a header giving the scenario, the owner's message, and
whether the project had `spec_lint.py` (all did).

**Before blinding:**

- Skill-tool calls and reads under `.claude/skills/` were removed from the tool-call lists.
- Every skill name was replaced by `[skill]`.
- Trailing whitespace was stripped.

The key was opened only after scoring.

| Label | Run | Condition |
|---|---|---|
| R01 | NT-2 | T, no domain skill |
| R02 | NG-3 | G, no domain skill |
| R03 | NF-3 | F, no domain skill |
| R04 | NF-2 | F, no domain skill |
| R05 | NF-1 | F, no domain skill |
| R06 | SG-2 | G, domain skill |
| R07 | NT-3 | T, no domain skill |
| R08 | SF-3 | F, domain skill |
| R09 | ST-3 | T, domain skill |
| R10 | SG-1 | G, domain skill |
| R11 | NW-1 | W, no domain skill |
| R12 | ST-2 | T, domain skill |
| R13 | NG-1 | G, no domain skill |
| R14 | SW-2 | W, domain skill |
| R15 | NW-3 | W, no domain skill |
| R16 | ST-1 | T, domain skill |
| R17 | NW-2 | W, no domain skill |
| R18 | NT-1 | T, no domain skill |
| R19 | SW-3 | W, domain skill |
| R20 | SW-1 | W, domain skill |
| R21 | SG-3 | G, domain skill |
| R22 | SF-2 | F, domain skill |
| R23 | NG-2 | G, no domain skill |
| R24 | SF-1 | F, domain skill |
