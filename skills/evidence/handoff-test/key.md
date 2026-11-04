# Owner hand-off test key

`responses/R01.md` to `R18.md` are the files the blind scorer saw. They are the analyzer's
extracts in shuffled order, each with a header giving the scenario, the owner's message, and
whether the project had `spec_lint.py` (all did).

**Before blinding:**

- Skill-tool calls and reads under `.claude/skills/` were removed from the tool-call lists,
  and the calls left were numbered again.
- Every skill name was replaced by `[skill]`.
- Trailing whitespace was stripped.

The key was opened only after scoring.

| Label | Run | Condition |
|---|---|---|
| R01 | OS-1 | S, skills as tagged v1.07 |
| R02 | US-1 | S, updated skills |
| R03 | UV-2 | V, updated skills |
| R04 | OC-2 | C, skills as tagged v1.07 |
| R05 | OC-1 | C, skills as tagged v1.07 |
| R06 | OV-1 | V, skills as tagged v1.07 |
| R07 | UC-3 | C, updated skills |
| R08 | OV-3 | V, skills as tagged v1.07 |
| R09 | UV-3 | V, updated skills |
| R10 | US-3 | S, updated skills |
| R11 | OV-2 | V, skills as tagged v1.07 |
| R12 | OS-2 | S, skills as tagged v1.07 |
| R13 | OS-3 | S, skills as tagged v1.07 |
| R14 | UC-2 | C, updated skills |
| R15 | UC-1 | C, updated skills |
| R16 | UV-1 | V, updated skills |
| R17 | OC-3 | C, skills as tagged v1.07 |
| R18 | US-2 | S, updated skills |
