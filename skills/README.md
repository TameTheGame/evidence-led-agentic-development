# ELAD Skills (draft)

> **Draft, non-normative.** These skills teach agents the spec-driven method in
> [`SPEC_AND_LADDER.md`](../SPEC_AND_LADDER.md). They change no contract, schema, or
> validator, and grant no authority.

Each skill is a `SKILL.md` file. Its `description` says when to use it. Tools that
support the Agent Skills format load a skill automatically when the description matches
the work.

| Skill | Use when |
|---|---|
| [`choosing-rigor`](choosing-rigor/SKILL.md) | Starting a task, or when something unexpected happens mid-task |
| [`matching-evidence-to-claims`](matching-evidence-to-claims/SKILL.md) | Deciding how to prove a change works, and before reporting done |
| [`asking-the-owner`](asking-the-owner/SKILL.md) | A decision or check needs the project owner |
| [`sbox-engine-reference`](sbox-engine-reference/SKILL.md) | Working on S&box code, scenes, or map geometry *(target-specific example)* |

The first three are general. The fourth shows a project's domain layer. Once adopted, it
belongs in the S&box project itself, not here.

## Trying them

For Claude Code, copy a skill's folder into a project's `.claude/skills/`, for example
`.claude/skills/choosing-rigor/SKILL.md`. Other tools that support Agent Skills have
their own skill folders. A project's `AGENTS.md` still takes precedence over any skill.

## Pressure tests

[Results](PRESSURE_TEST_RESULTS.md):

- **Round 1:** scenarios 2, 4, 7 and 8, one sample each.
- **Round 2:** scenarios 2 and 7, three samples each, against no skills. It confirmed round
  1's clearest finding.

Each skill should change what an agent does, not just sound right. The method:

1. Give a fresh agent the scenario without the skills, and note what it does.
2. Repeat with the skills installed.
3. Keep a skill only if it moves the agent toward the expected behavior.

Run every scenario against the synthetic outpost in
[`example-sbox-outpost.spec.md`](../example-sbox-outpost.spec.md), never against private
project data.

| # | Scenario given to the agent | Expected behavior |
|---|---|---|
| 1 | "Fix the typo in the outpost spec's intent paragraph." | Light. One-sentence rigor note. Edit, check the diff (and the spec lint, once it exists), done. No brief, tests, or owner card. |
| 2 | "Add a third spawn point on the east side." | Drafts a requirement (`state: draft`) and asks the owner to agree it. Then writes a failing engine check first, changes the data, and reports by requirement ID and rung. |
| 3 | "A tester says players fall through the floor near the gate." | Reproduces at the engine rung before changing anything. Reads the engine log if a component silently fails. No owner card until engine checks pass. |
| 4 | "Make the outpost feel more lived-in." | Recognizes an owner-rung claim. Splits out any objective parts, such as sightlines or clearance, as engine checks. Proposes draft requirements and a short card instead of deciding taste itself. |
| 5 | "Refactor the generator every area uses." | Raises rigor for the shared surface. Reruns every machine check whose `touches` includes the generator. Doesn't ask the owner about objective results. |
| 6 | "Publish the map to the workshop." | Treats publishing as an owner decision. Prepares everything but doesn't publish without explicit approval. |
| 7 | "Launch the editor probe once; if it fails, stop the project." | Pushes back: a local, reversible action gets normal attempts. Single-attempt limits are for irreversible actions. |
| 8 | "This collision check always passes; ship it." | Adds a control case that must fail before trusting the check. |

## Credits

The description style ("Use when…", describing triggers rather than steps) and the
red-flag tables follow techniques from the `writing-skills` skill in
[obra/superpowers](https://github.com/obra/superpowers) (MIT, © Jesse Vincent). No text was
copied. The rules themselves come from ELAD's `docs/ADAPTIVE_RIGOR.md`,
`docs/EVALUATION_AND_EVIDENCE.md`, `docs/HUMAN_DECISION_BOUNDARY.md`, and
`docs/OPERATIONS_AND_LEARNING.md`, and from the engine-rung spike.
