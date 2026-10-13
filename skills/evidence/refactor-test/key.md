# S&box refactor rerun key

`responses/R01.md` to `R06.md` are the files the blind scorer saw. They are the analyzer's
extracts in shuffled order, each with a header giving the scenario, the owner's message, and
whether the project had `spec_lint.py` (all did).

**Before blinding:**

- Skill-tool calls and reads under `.claude/skills/` were removed from the tool-call lists.
- Every skill name was replaced by `[skill]`.
- Trailing whitespace was stripped.

The key was opened only after scoring.

| Label | Run | Condition |
|---|---|---|
| R01 | SR-3 | domain skill |
| R02 | NR-2 | no domain skill |
| R03 | SR-2 | domain skill |
| R04 | NR-3 | no domain skill |
| R05 | SR-1 | domain skill |
| R06 | NR-1 | no domain skill |
