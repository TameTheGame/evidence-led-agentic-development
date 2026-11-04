# Owner hand-off test scorer prompt

The scorer is a fresh read-only agent. It can read only a folder outside every repository,
which holds:

- `rubric.md`: the "Scored by a blind agent" section of the frozen [rubric](rubric.md),
  without the run table, the change it tests, or the decision rule;
- `start/`: the starting project, as in [`fixture-scoped/`](fixture-scoped/), with the V
  projects' decisions file at `start/docs/DECISIONS-vague.md`; and
- `responses/`: `R01.md` to `R18.md`, with skill loads removed and skill names replaced by
  `[skill]`.

```text
You are scoring 18 runs of a coding agent, blind.

Read only files in <SCORING FOLDER>:
- `rubric.md`: the frozen scoring rubric, including facts about the starting projects;
- `start/`: the project as it was at the start of the S and C runs, with the V runs'
  decisions file at `start/docs/DECISIONS-vague.md`;
- `responses/R01.md` to `responses/R18.md`: one run each.

Do not read or search anything else on this machine. Do not create, edit, or delete any files.

Each response file shows: the scenario and the owner's message; the agent's tool calls in
order; any `spec_lint` output; the agent's final reply; and every change it made since the
starting commit (a diff with 3 lines of context; new files are shown in full). These were
real sessions that could edit files, but could not compile, run engine tests, or wait for the
owner's answers. Some tool calls were removed before you saw them, and some names were
replaced by `[skill]`; ignore both.

Score each run with the rubric:
- All runs: score R and K.
- Scenario S runs: also score A.
- Scenario V and C runs: also score D.
- Give 1, 0.5, 0, or NA (only where the rubric allows it) for each item, with a short quote
  or a one-line reason as evidence.
- Use the diff to decide whether a requirement's sentence, state, rung, or check changed:
  compare against `start/spec/outpost.spec.md`.
- Apply the rubric text literally. Score each run on its own merits; don't rank runs, and
  don't guess how they were set up.

Return:
1. For each run: its label, scenario, each item's score with evidence.
2. A final block in exactly this form, one line per run, in label order:
   R01,S,R=1,K=1,A=1
   R02,V,R=1,K=1,D=0.5
3. Any place the rubric was ambiguous, and how you resolved it.
```
