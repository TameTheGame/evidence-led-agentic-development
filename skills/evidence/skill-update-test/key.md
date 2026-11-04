# S&box skill update test key

`responses/R01.md` to `R12.md` are the files the blind scorer saw. They are the analyzer's
extracts in shuffled order, each with a header giving the scenario, the owner's message, and
whether the project had `spec_lint.py` (all did).

**Before blinding:**

- Skill-tool calls and reads under `.claude/skills/` were removed from the tool-call lists,
  and the calls left were numbered again, so the gaps don't show the condition.
- Every skill name was replaced by `[skill]`.
- Trailing whitespace was stripped.

The key was opened only after scoring.

| Label | Run | Condition |
|---|---|---|
| R01 | UK-2 | K, updated skill |
| R02 | OL-3 | L, old skill (v1.07) |
| R03 | OK-2 | K, old skill (v1.07) |
| R04 | OK-3 | K, old skill (v1.07) |
| R05 | UL-1 | L, updated skill |
| R06 | UL-3 | L, updated skill |
| R07 | UL-2 | L, updated skill |
| R08 | OL-2 | L, old skill (v1.07) |
| R09 | UK-3 | K, updated skill |
| R10 | OL-1 | L, old skill (v1.07) |
| R11 | OK-1 | K, old skill (v1.07) |
| R12 | UK-1 | K, updated skill |
