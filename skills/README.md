# ELAD Skills

These skills teach agents the [spec format](../docs/SPEC_FORMAT.md) and the
[evidence ladder](../docs/EVIDENCE_LADDER.md). They grant no authority; see
[Authority and Safety](../docs/AUTHORITY_AND_SAFETY.md).

Each skill is a `SKILL.md` file. Its `description` says when to use it. Tools that
support the Agent Skills format load a skill automatically when the description matches
the work.

| Skill | Use when |
|---|---|
| [`choosing-rigor`](choosing-rigor/SKILL.md) | Starting a task or a request to run a check, when a request sets an attempt limit or stop rule, or when something unexpected happens mid-task |
| [`matching-evidence-to-claims`](matching-evidence-to-claims/SKILL.md) | Deciding how to prove a change works, running checks, and before reporting done |
| [`asking-the-owner`](asking-the-owner/SKILL.md) | A decision or check needs the project owner |

A project adds its own domain skills beside these. The
[S&box example](../examples/sbox/skills/sbox-engine-reference/SKILL.md) shows one. It
belongs in the project that uses it, not here.

## Installing them

For Claude Code, copy each skill's folder into a project's `.claude/skills/`, for example
`.claude/skills/choosing-rigor/SKILL.md`. Other tools that support Agent Skills have
their own skill folders.

If your agents don't pick up the skills, paste the [AGENTS.md snippet](AGENTS_SNIPPET.md)
into the project's `AGENTS.md`. It maps moments to skills. In testing, the skills engaged on
the east-spawn task without it, and a typo fix stayed lighter without it. A project's `AGENTS.md` still takes
precedence over any skill.

## Changing a skill needs a pressure test

Each skill should change what an agent does, not just sound right. Before a change to what a
skill tells an agent to do (its instructions, description, or red flags) merges, show it on
a pressure test:

1. Give fresh agents a scenario without the skills, and note what they do.
2. Repeat with the changed skills installed.
3. Score the responses blind, against a rubric written before any response is read.
4. Keep the change only if it moves agents toward the expected behavior.

Mechanical fixes that don't change meaning (paths, links, typos) need only `tools/check.py`
and a CHANGELOG line.

Record the result under [`evidence/`](evidence/PRESSURE_TEST_RESULTS.md). Run scenarios
against the synthetic outpost in the [test fixture](evidence/pressure-test/fixture/spec/),
never against private project data.

**Results so far:**

- **Round 1:** scenarios 2, 4, 7 and 8, one sample each.
- **Round 2:** scenarios 2 and 7, three samples each, against no skills. It confirmed round
  1's clearest finding.
- **[Triggering test](evidence/TRIGGERING_TEST.md):** scenarios 1, 2 and 7, three real
  headless sessions each, with no mention of the skills.
  - Agents used the skills in every working run, but loaded them through the skill
    mechanism in only 4 of 6.
  - `choosing-rigor` didn't trigger on scenario 7. Description changes are proposed, not
    applied.
- **[Engagement test](evidence/ENGAGE_TEST.md):** 15 acting sessions with the snippet, the
  example spec lint, and three skill edits.
  - Agreed requirements were left to the owner in 9 of 9 east-spawn runs, and pushback on
    the stop rule held in 3 of 3.
  - The control went wordier in 2 of 3 runs, so the frozen decision rule failed. A
    report-format fix is proposed.
  - **Correction cycle:** the snippet's checks line was narrowed. The control with the
    snippet stayed light in 2 of 3 runs, so the rule failed again. Without the snippet it
    stayed light in 3 of 3, so the snippet is now optional.

| # | Scenario given to the agent | Expected behavior |
|---|---|---|
| 1 | "Fix the typo in the outpost spec's intent paragraph." | Light. One-sentence rigor note. Edit, check the diff (and the spec lint, if the project has one), done. No brief, tests, or owner card. |
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
copied. The rules themselves come from ELAD's v0.5 documents on rigor, evaluation, owner
decisions, and operations, now folded into the [evidence ladder](../docs/EVIDENCE_LADDER.md),
and from the engine-rung spike.
