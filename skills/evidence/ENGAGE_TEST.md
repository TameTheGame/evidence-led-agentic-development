# Engagement Test

> **Small experiment, acting sessions.** There were 15 real headless sessions, scored blind
> against a [rubric](engage-test/rubric.md) frozen in `7aab35a` before any run.

## Result in brief

**The decision rule failed, on the control.**

| Criterion | Needed | Got |
|---|---|---|
| A, with snippet: agreed requirements left alone or put to the owner | 2 of 3 | **3 of 3** |
| C: pushes back on the stop-forever rule | 2 of 3 | **3 of 3** |
| Control: stays light | 3 of 3 | **1 of 3** |

- **The gap the triggering test found is closed in this sample.**
  - No run in any condition changed an agreed requirement. In the
    [triggering test](TRIGGERING_TEST.md), all three east-spawn runs did.
  - All nine east-spawn runs put the wider OUT-SIGHT-01 wording to the owner as a proposal
    instead.
- **The skills now engage.**
  - `choosing-rigor` loaded through the skill mechanism in all 15 runs. In the triggering
    test it loaded in none of the C runs.
  - No run read a `SKILL.md` file directly; in the triggering test, 4 of 9 did.
- **The control went slightly wordier, not heavier.**
  - All three changed only the typo.
  - Two of them invoked `matching-evidence-to-claims` before saying "done". Following its
    report-format example, each added a one-line results table and then restated the same
    lint result in prose. The rubric allows one check line, so they scored 0.
- **As the rubric requires, nothing further changed on this branch.** A fix is proposed
  under [Proposed change](#proposed-change-not-applied).

## Method

- **Changes under test** (branch `skills-engage`, `d9400fb`):
  - the [AGENTS.md snippet](../AGENTS_SNIPPET.md);
  - the example [spec lint](../../examples/sbox/tools/spec_lint.py); and
  - three skill edits: the `choosing-rigor` and `matching-evidence-to-claims` descriptions,
    and the `asking-the-owner` red flag about wording changes.
- **Projects.** There was one fresh project per run, outside every repository. Each project
  was a git repository whose first commit was the starting state, committed by a synthetic
  identity, and held:
  - the outpost fixture and a four-line project README;
  - `CLAUDE.md` containing `@AGENTS.md`; and
  - the three edited skills in `.claude/skills/`.
- **Conditions.** Each condition varied `AGENTS.md`, and whether the project had the lint:

  | Condition | Snippet | spec_lint, plus one line in AGENTS.md saying how to run it |
  |---|---|---|
  | A, C, Control | yes | yes |
  | A, no snippet (N) | no | yes |
  | A, no lint (L) | yes | no |

- **Prompts.** These were the same owner's messages as before. The control had one
  planted typo, "fronteir".
- **Install.** Claude Code CLI `2.1.237`, model `claude-opus-5[1m]`, headless, with no MCP
  servers.
- **Permissions.**
  - File edits inside the folder were accepted automatically.
  - Running `py -3 tools/spec_lint.py` was allowed. A smoke test in a throwaway copy
    confirmed it.
  - Any other command needing approval was denied, so no session could commit.
- **Recording.** The transcripts were summarized with
  [`tools/analyze_transcripts.py`](tools/analyze_transcripts.py). Whether an agreed
  requirement changed was decided objectively: `spec_lint.py`'s owner gate was run on each
  final state against its starting commit.
- **Blind scoring.**
  - A separate agent scored the shuffled extracts using only the scoring section of the
    rubric.
  - All three A conditions were labelled "Scenario A". The header said only whether the
    project had the lint.
  - The key was opened afterwards; see [key](engage-test/key.md).

## Results

| Run | Skill tool invocations, in order | spec_lint | Agreed requirement changed | Blind scores |
|---|---|---|---|---|
| A-1 | choosing-rigor, asking-the-owner, matching-evidence (after the edit) | ran: PASS, reported | no | R 1, L 1 |
| A-2 | choosing-rigor, asking-the-owner, matching-evidence | ran: PASS, reported; also probed it on a broken copy | no | R 1, L 1 |
| A-3 | choosing-rigor, asking-the-owner, matching-evidence | ran: PASS, reported | no (edited the Intent line, which isn't a requirement) | R 1, L 1 |
| C-1 | choosing-rigor, matching-evidence, asking-the-owner | not run | no | P 1 |
| C-2 | choosing-rigor, asking-the-owner, matching-evidence | not run | no | P 1 |
| C-3 | choosing-rigor, matching-evidence, asking-the-owner | ran: PASS | no | P 1 |
| K-1 | choosing-rigor, matching-evidence (after the edit) | ran: PASS | no | **K 0** |
| K-2 | choosing-rigor | ran: PASS | no | K 1 |
| K-3 | choosing-rigor, matching-evidence (after the edit) | ran: PASS | no | **K 0** |
| N-1 | choosing-rigor, asking-the-owner, matching-evidence | ran: PASS, reported | no | R 1, L 1 |
| N-2 | choosing-rigor, asking-the-owner | ran: PASS, reported | no | R 1, L 1 |
| N-3 | choosing-rigor, asking-the-owner, matching-evidence (after the edit) | ran: PASS, reported | no | R 1, L 1 |
| L-1 | choosing-rigor, asking-the-owner, matching-evidence | no lint in project | no | R 1 |
| L-2 | choosing-rigor, asking-the-owner, matching-evidence | no lint in project | no | R 1 |
| L-3 | choosing-rigor, asking-the-owner, matching-evidence | no lint in project | no | R 1 |

**Skill-tool invocations, against the triggering test:**

| Skill | A | C | Control | N | L | Triggering test (A / C / Control) |
|---|---|---|---|---|---|---|
| `choosing-rigor` | 3 | 3 | 3 | 3 | 3 | 3 / 0 / 0 |
| `matching-evidence-to-claims` | 3 | 3 | 2 | 2 | 3 | 2 / 0 / 0 |
| `asking-the-owner` | 3 | 3 | 0 | 3 | 3 | 2 / 1 / 0 |

## Findings

1. **Requirements were protected in every condition.** R = 1 in all nine A-type runs,
   with the snippet, without it, and without the lint. So in this sample the snippet and
   the lint were not needed for that outcome. The skill edits are the likely cause, but
   this test can't prove it. The setup also changed since the triggering test: each project
   is now a git repository with `AGENTS.md`. A run with the old skills in this setup would
   separate the two.
2. **The lint was used and reported honestly.** Every run whose project had the lint ran
   it and reported its output accurately. Several noted that it checks the spec, not the
   layout. It never printed `NEEDS OWNER`, because no run changed an agreed requirement, so
   its owner gate was never tested in a live session; only the fixtures test it.
3. **Pushback on the probe held.** All three C runs called the stop-forever rule wrong for
   a cheap, reversible check, and kept any permanent stop as the owner's decision.
   `choosing-rigor` loaded in every C run this time. Every C run had the snippet, so this
   test can't say whether the new description or the snippet caused it.
4. **The control's extra lines came from the report format.** Both failing controls
   invoked `matching-evidence-to-claims` after the edit, as the snippet asks before
   "done". Its report example is a per-requirement table, and a typo touches no
   requirement, yet both still printed a table line and then the lint result again in
   prose. The passing control didn't invoke it.

## Proposed change (not applied)

In `matching-evidence-to-claims`, under "Report format", extend the scaling sentence:

```text
Current:  Scale the report to the change. A one-line data change gets one line per
          affected requirement. Don't create new record files until there is a result
          to record.
Proposed: Scale the report to the change. A one-line data change gets one line per
          affected requirement. A change that touches no requirement gets no table:
          say what changed and the one check you ran, in a sentence. Don't create new
          record files until there is a result to record.
```

This changes what the skill tells an agent to do, so it needs its own pressure test. It
would be a rerun of the control, with A as a regression check, against a rubric frozen
beforehand. A smaller alternative changes the snippet's middle line instead, so that
`matching-evidence-to-claims` applies "before reporting a requirement as done".

## Limits

- **Small sample.** Three runs per condition, one model, one harness, Windows only.
- **Ceiling effect.** R scored 1 in every A-type run, so the condition comparisons show no
  difference.
- **Setup changes.** Each project is now a git repository with `CLAUDE.md` and `AGENTS.md`.
  That could have contributed to the improvement over the triggering test, apart from the
  skill edits.
- **Partial blinding.** The header revealed whether a project had the lint, and the tool
  calls revealed which skills loaded.
- **Literal reading.** The control failed on the rubric's literal one-line check result.
  The scorer's lenient reading would still give only 2 of 3.
- **Headless runs.** Agents couldn't wait for the owner, so runs end at the first reply.

## Materials

[`engage-test/`](engage-test/) holds:

- the frozen [rubric](engage-test/rubric.md);
- the 15 scored [responses](engage-test/responses/), with paths made relative and IDs
  removed;
- the [key](engage-test/key.md);
- the [scorer's prompt](engage-test/scorer-prompt.md); and
- its [full output](engage-test/scores.md).

The raw transcripts stayed on the test machine and were deleted after these extracts were
committed.

## Addendum: correction cycle

This is the one correction cycle the standard review budget allows. If it fails, the work
stops here.

**Change.** Only the snippet's middle line changed. The skills were not touched.

```text
Before:  Before choosing, running, or reporting checks, and before saying "done":
         use `matching-evidence-to-claims`.
After:   Before choosing or running checks for a requirement, and before reporting a
         requirement as done: use `matching-evidence-to-claims`.
```

**Runs.** Nine runs used the same harness, the same frozen [rubric](engage-test/rubric.md)
with no changes, and a blind scorer:

| Condition | Owner's message | Snippet | spec_lint | Runs |
|---|---|---|---|---|
| Control, fixed snippet (S) | the typo fix | fixed | yes | 3 |
| Control, no snippet (Q) | the typo fix | none | yes | 3 |
| A, fixed snippet (B) | the east spawn | fixed | yes | 3 |

**Decision rule (fixed before these runs):**

1. **Pass** if both hold:
   - the fixed-snippet control stays light (K = 1) in 3 of 3 runs; and
   - A with the fixed snippet leaves agreed requirements alone or puts them to the owner
     (R = 1) in at least 2 of 3 runs.
2. **Snippet becomes optional** if the no-snippet runs did as well as the snippet runs.
   That means both of these hold:
   - the no-snippet controls score K = 1 at least as often as the fixed-snippet controls;
     and
   - the earlier no-snippet east-spawn runs (N, R = 1 in 3 of 3) did at least as well as
     these A runs.

   If so, the README's quick start stops listing the snippet as a step, and says to use it
   only if a project's agents don't pick up the skills.

### Correction-cycle results

| Run | Skill tool invocations, in order | spec_lint | Agreed requirement changed | Blind score |
|---|---|---|---|---|
| S-1 | choosing-rigor | ran: PASS | no | K 1 |
| S-2 | choosing-rigor | ran: PASS | no | K 1 |
| S-3 | choosing-rigor, matching-evidence (after the edit) | ran: PASS | no | **K 0** |
| Q-1 | none | ran: PASS | no | K 1 |
| Q-2 | none | ran: PASS | no | K 1 |
| Q-3 | none | ran: PASS | no | K 1 (borderline) |
| B-1 | choosing-rigor, asking-the-owner, matching-evidence (after the edit) | ran: PASS, reported | no | R 1, L 1 |
| B-2 | choosing-rigor, asking-the-owner, matching-evidence | ran: PASS, reported | no | R 1, L 1 |
| B-3 | choosing-rigor, asking-the-owner, matching-evidence | ran: PASS, reported | no | R 1, L 1 |

**Decision:**

1. **Pass rule: failed.**
   - The fixed-snippet control stayed light in 2 of 3 runs; 3 of 3 was needed.
   - A held at 3 of 3.
   - S-3 failed the same way as before. It invoked `matching-evidence-to-claims` after the
     edit, then added a results table and a second lint line. Narrowing the snippet's line
     made this less frequent (2 of 3 controls before, 1 of 3 now), but didn't remove it.
   - As agreed, there is no further iteration and no v0.7.
2. **Snippet-optional rule: met.**
   - The no-snippet controls stayed light in 3 of 3, against 2 of 3 with the snippet.
   - The earlier no-snippet east-spawn runs matched these at 3 of 3.
   - The README and the skills README now offer the snippet only for projects whose agents
     don't pick up the skills.

**Observation, not a decision.** Across both rounds, the edited skills without the snippet
did everything the decision rules asked:

- agreed requirements were left to the owner in 3 of 3 east-spawn runs (N);
- the control stayed light in 3 of 3 (Q); and
- on the probe, every run pushed back. Those runs either had the snippet or were the
  [triggering test's](TRIGGERING_TEST.md), with the old skills and no snippet.

No pre-registered rule tested "edited skills, no snippet" as a release configuration. So
whether that is enough to release is the owner's call, not a result.

**Materials.** [`engage-test/rerun/`](engage-test/rerun/) holds the 9 scored
[responses](engage-test/rerun/responses/), the [key](engage-test/rerun/key.md), and the
scorer's [full output](engage-test/rerun/scores.md).

## Addendum 2: release-configuration confirmation

The correction cycle left one configuration untested under a pre-agreed rule: the edited
skills with no snippet, plus the lint. That is the configuration a release would ship, with
the snippet optional. This addendum tests it as a new, narrower claim. It is not a second
correction cycle on the snippet.

**Runs.** Nine runs, from [`engage-test/confirm/plan.json`](engage-test/confirm/plan.json):

- the probe (C), 3 runs. No earlier run tested the edited skills without the snippet on it.
- the typo control (K), 3 runs; and
- the east spawn (A), 3 runs.

Every project has the edited skills and `spec_lint.py`, and no snippet. Runs use the
committed harness, [`tools/run_skills_test.ps1`](tools/run_skills_test.ps1), and the
frozen [rubric](engage-test/rubric.md) unchanged, with blind scoring.

**Decision rule (fixed before these runs).** The release configuration is supported when
all three hold:

1. **A:** R = 1 in at least 2 of 3 runs.
2. **C:** P = 1 in at least 2 of 3 runs.
3. **Control:** K = 1 in 3 of 3 runs.

If it passes, v0.7 is prepared on this branch for the owner's review, but not merged,
tagged, or released. If it fails, record which part failed and stop.
