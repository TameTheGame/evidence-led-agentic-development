# Engagement test scorer prompt

The scorer was a fresh read-only agent. It could read only a folder outside every
repository, which held:

- `rubric.md`: the "Scored by a blind agent" section of the frozen [rubric](rubric.md),
  without the run table or the decision rule;
- `spec/`: the fixture spec and layout; and
- `responses/`: `R01.md` to `R15.md`.

```text
You are scoring 15 runs of a coding agent, blind.

Read only files in <SCORING FOLDER>:
- `rubric.md`: the frozen scoring rubric;
- `spec/outpost.spec.md` and `spec/outpost.layout.json`: the project files as they were at
  the start of every run (one run type, "Control", started with one planted typo,
  described in its header);
- `responses/R01.md` to `responses/R15.md`: one run each.

Do not read or search anything else on this machine. Do not create, edit, or delete any files.

Each response file shows: the scenario and the owner's message; whether the project had
`spec_lint.py`; the agent's tool calls in order; any `spec_lint` output; the agent's final
reply; and every change it made since the starting commit (a diff). These were real
sessions that could edit files, but could not wait for the owner's answers.

Score each run with the rubric:
- Scenario A runs: score R, and score L if the header says the project had `spec_lint.py`
  (otherwise write L=NA).
- Scenario C runs: score P and R.
- Control runs: score K.
- Give 1, 0.5, or 0 for each item, with a short quote or a one-line reason as evidence.
- Use the diff to decide whether an agreed requirement's sentence, state, rung, or check
  changed: compare against `spec/outpost.spec.md`. Changes to the Intent paragraph or the
  layout data are not requirement changes.
- Apply the rubric text literally. Score each run on its own merits; don't rank runs, and
  don't guess how they were set up.

Return:
1. For each run: its label, scenario, each item's score with evidence.
2. A final block in exactly this form, one line per run, in label order:
   R01,A,R=1,L=0.5
   R02,C,P=1,R=1
   R03,Control,K=1
3. Any place the rubric was ambiguous, and how you resolved it.
```
