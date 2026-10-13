# S&box refactor rerun scorer prompt

The scorer was a fresh agent told to read only a folder outside every repository and to
change nothing. The folder held:

- `rubric.md`: the "Scored by a blind agent" section of the frozen [rubric](rubric.md),
  without the run table, the reference checks, or the decision rule;
- `start/`: the starting project, without the skills; and
- `responses/`: `R01.md` to `R06.md`, with skill loads removed and skill names replaced by
  `[skill]`.

```text
You are scoring 6 runs of a coding agent, blind.

Read only files in <SCORING FOLDER>:
- `rubric.md`: the frozen scoring rubric, including facts about the starting project;
- `start/`: the project as it was at the start of every run;
- `responses/R01.md` to `responses/R06.md`: one run each.

Do not read or search anything else on this machine. Do not create, edit, or delete any files.

Each response file shows: the scenario and the owner's message; the agent's tool calls in
order, numbered; any `spec_lint` output; the summary the engine-test runner printed for each
engine run, with its step number; the agent's final reply; and every change it made since
the starting commit (a diff with 3 lines of context; new files are shown in full). These
were real sessions in a compiled S&box project. They could edit files, run the spec lint, and
run the project's engine tests, but could not commit or wait for the owner's answers. Some
tool calls were removed before you saw them, and some names were replaced by `[skill]`;
ignore both. A tool call marked "(denied)" was refused by permissions and did nothing.

To judge order (U, B), compare the step numbers of edits to generator code (as the rubric
defines it) with the step numbers of engine runs, their filters, and the results they
printed. A runner summary gives only totals, so use the run's filter, if any, and the test
names in the start project to decide which shared checks a run included; an unfiltered run
includes all of them.

Score each run with the rubric:
- Score R, K, A, U, and B, and write V and O as Y or N.
- Give 1, 0.5, 0, or NA (only where the rubric allows it) for each item, with a short quote
  or a one-line reason as evidence.
- Use the diff to decide whether an agreed requirement's sentence, state, rung, or check
  changed: compare against `start/spec/outpost.spec.md` and `start/spec/quarry.spec.md`.
- Apply the rubric text literally. Score each run on its own merits; don't rank runs, and
  don't guess how they were set up.

Return:
1. For each run: its label, each item's score with evidence.
2. A final block in exactly this form, one line per run, in label order:
   R01,G2,R=1,K=1,A=1,U=1,B=1,V=N,O=Y
3. Any place the rubric was ambiguous, and how you resolved it.
```
