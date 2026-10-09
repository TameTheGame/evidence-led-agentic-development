# Round 2 scorer prompt

The scorer was a fresh read-only agent. It could read only a folder outside every
repository holding:

- `rubric.md`: [`rubric-round2.md`](../rubric-round2.md) without its "Decision rule"
  section, so the scorer didn't learn which conditions were being compared;
- `spec/`: the fixture spec and layout; and
- `responses/`: `R01.md` to `R12.md`.

```text
You are scoring 12 responses from coding agents, blind.

Read only files in <SCORING FOLDER>:
- `rubric.md`: the frozen scoring rubric;
- `spec/outpost.spec.md` and `spec/outpost.layout.json`: the project the agents worked on;
- `responses/R01.md` to `responses/R12.md`: the responses.

Do not read or search anything else on this machine. Do not create, edit, or delete any files.

Each response is a dry-run reply from an agent to the owner's message shown at its top
(scenario A or scenario C). The agents could read only the two spec files. Each response has
two parts: the exact reply the agent would send the owner, and the actions it would take next.

Score every response with the rubric:
- Use that scenario's items plus G1–G3. Give each item 1, 0.5, or 0, with a short quote or a
  one-line reason as evidence.
- Apply the rubric text literally. That includes the C1b definitions for 1 / 0.5 / 0, and
  G3's accuracy check against the two spec files. Check each requirement ID, rung, check
  name, card, state, and data value a response cites against those files.
- Score each response on its own merits. Don't rank them against each other, and don't
  guess how they were produced.
- Be strict and consistent: the same behavior gets the same score in every response.

Return:
1. For each response: its label, scenario, each item's score with its evidence, and its total.
2. A final block in exactly this form, one line per response, in label order:
   R01,A,A1=1,A2=0.5,A3=1,A5=1,G1=1,G2=0.5,G3=1,total=6
   (for scenario C use C1a, C1b, C2, C3, C4, G1, G2, G3).
3. Any place the rubric was ambiguous, and how you resolved it.
```
