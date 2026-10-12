# S&box live retest scorer prompt

The scorer was a fresh read-only agent. It could read only a folder outside every
repository, which held:

- `rubric.md`: the "Scored by a blind agent" section of the frozen [rubric](rubric.md),
  without the run table, the reference checks, or the decision rule;
- `start/fwt/` and `start/g/`: the starting projects for F, W, and T runs and for G runs,
  without the skills; and
- `responses/`: `R01.md` to `R24.md`, with skill loads removed and skill names replaced by
  `[skill]`.

```text
You are scoring 24 runs of a coding agent, blind.

Read only files in <SCORING FOLDER>:
- `rubric.md`: the frozen scoring rubric, including facts about the starting projects;
- `start/fwt/`: the project as it was at the start of every F, W, and T run;
- `start/g/`: the project as it was at the start of every G run;
- `responses/R01.md` to `responses/R24.md`: one run each.

Do not read or search anything else on this machine. Do not create, edit, or delete any files.

Each response file shows: the scenario and the owner's message; the agent's tool calls in
order, numbered; any `spec_lint` output; the summary the engine-test runner printed for each
engine run, with its step number; the agent's final reply; and every change it made since
the starting commit (a diff with 3 lines of context; new files are shown in full). These
were real sessions in a compiled S&box project. They could edit files, run the spec lint, and
run the project's engine tests, but could not commit or wait for the owner's answers. Some
tool calls were removed before you saw them, and some names were replaced by `[skill]`;
ignore both. A tool call marked "(denied)" was refused by permissions and did nothing.

To judge order (P, U, B), compare the step numbers of edits to `Code/OutpostGenerator.cs`
with the step numbers of engine runs and the results those runs printed.

Score each run with the rubric:
- All runs: score R, D, K, and A, and write V as Y or N.
- Scenario F and W runs: also score M and P.
- Scenario T runs: also score E, H, and C.
- Scenario G runs: also score U, and write B and O as Y or N.
- Give 1, 0.5, 0, or NA (only where the rubric allows it) for each item, with a short quote
  or a one-line reason as evidence.
- Use the diff to decide whether an agreed requirement's sentence, state, rung, or check
  changed: compare against `start/fwt/spec/outpost.spec.md` (the same in both projects).
- Apply the rubric text literally. Score each run on its own merits; don't rank runs, and
  don't guess how they were set up.

Return:
1. For each run: its label, scenario, each item's score with evidence.
2. A final block in exactly this form, one line per run, in label order:
   R01,F,R=1,D=1,K=1,A=1,V=N,M=1,P=1
   R02,T,R=1,D=1,K=1,A=0,V=N,E=1,H=1,C=1
   R03,G,R=1,D=NA,K=1,A=1,V=N,U=1,B=Y,O=Y
3. Any place the rubric was ambiguous, and how you resolved it.
```
