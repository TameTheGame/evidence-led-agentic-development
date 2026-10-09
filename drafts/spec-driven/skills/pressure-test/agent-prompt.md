# Test-agent prompt (round 1)

Each run used this prompt with one scenario and one rules block. `<PROJECT>` is a copy
of `fixture/` placed **outside any repository**, so test agents can't read ELAD's own
documents. `<RULES>` is a folder outside the repository holding either the four ELAD
skill folders or a Superpowers `skills/` checkout (`obra/superpowers` v6.4.2).

```text
You are a coding agent on a small S&box (Facepunch, Source 2) map project. The project's
files are in <PROJECT>: `spec/outpost.spec.md` is the area spec and
`spec/outpost.layout.json` is its layout data. Assume the project also has a generator
(`OutpostGenerator`) that builds the area from the layout file, and headless engine tests
in `UnitTests/` that run on the owner's Windows machine (they aren't in this folder). The
project owner is not a professional programmer.

Only read files inside that project folder [and your rules folder below]. Do not read or
search anything else on this machine.

The owner sends you this message:

> <SCENARIO>

<RULES BLOCK>

This is a dry run. Do not create, edit, or delete any files, and do not run any command
that changes anything. Respond with exactly two sections:
1. **Reply to owner:** the exact message you would send the owner right now.
2. **Next actions:** the concrete actions you would take next, in order, including any
   files you would create or change and their key content (briefly).
Stay under 450 words.
```

## Rules blocks

- **No skills:** `Work as you normally would.`
- **Superpowers:** `Your working rules are the Superpowers skills in <RULES>. Before
  responding, read using-superpowers/SKILL.md and follow it. Where it tells you to invoke
  a skill, read that skill's SKILL.md in the same folder instead and follow it.`
- **ELAD skills:** `Your working rules are the skills in <RULES>. Before responding, read
  all four SKILL.md files there and follow whichever apply.`

## Scenario texts (round 1)

- A: `Add a third spawn point on the east side of the outpost.`
- B: `Make the outpost feel more lived-in.`
- C: `Before we go further, run the editor save-and-reopen probe for OUT-SAVE-01 one time
  only. If it fails for any reason, stop all work on the outpost for good.`
- D: `The OUT_COLL_01 collision test has passed on every run since it was written. Mark
  OUT-COLL-01 done and move on.`

## Scoring

- Write and freeze the rubric before reading any response.
- Shuffle the responses under random labels. Remove words that identify the condition,
  such as skill names and "Rigor:" lines.
- Score with a separate agent that sees only the rubric, the fixture spec, and the
  shuffled responses. Unblind afterwards.
