# S&box Live Retest

> **Small experiment, acting sessions, real engine.** There were 24 real headless sessions in
> compiled S&box projects, scored blind against a [rubric](live-test/rubric.md) frozen in
> `6399091` before any run, and checked on the engine afterwards.

This is step 3 of the [S&box next steps](../../ROADMAP.md#sbox-next-steps). It reran the
[domain-skill test](SBOX_SKILL_TEST.md)'s scenarios in a real S&box project that has the
[rung-1 starter](../../examples/sbox/rung1-starter/README.md), with agents allowed to run its
engine tests. It added ELAD scenario 5, the shared generator refactor.

## Result in brief

**The retest failed its pre-registered decision rule, on one criterion: the refactor
scenario.** No run with the domain skill refactored anything. All three stopped to ask the
owner which refactor they meant, because the project has only one area. The other four
criteria passed.

| Criterion (S runs) | Needed | Got |
|---|---|---|
| 1. D = 1: tests build geometry with a default surface (F, W, T) | 7 of 9 | **9 of 9** |
| 2. P = 1: a test fails before the fix and passes after (F, W) | 4 of 6 | **5 of 6** |
| 3. The planted bug is fixed, by the reference probes (F, W) | 5 of 6 | **6 of 6** |
| 4. G: shared checks rerun after the refactor, and probes pass | 2 of 3 | **0 of 3** |
| 5. R = 0, K = 0, and A = 0, with the skill against without | no more | **0, 0, 2 against 0, 0, 2** |

- **The starter closed the default-surface gap.** Every F, W, and T run's geometry tests
  ran with a default surface (18 of 18), against none in the domain-skill test (D = 1 in 0
  of 18).
- **Agents watched tests fail before fixing.** In 11 of 12 fall-through and wall runs, a
  test failed on the engine before the generator changed and passed after. The twelfth
  fixed first, then reverted its fix to show the test failing. In the domain-skill test, two
  of three fall-through runs with the skill fixed before testing.
- **Without the domain skill, agents now fixed the bug too.** By the reference probes, all
  12 fall-through and wall runs fixed the planted bug, 6 with the skill and 6 without. In
  the domain-skill test, none of the 6 runs without it did. All 9 F, W, and T runs without
  the skill found the cause by comparing the generator with the starter's
  `StarterGeometry.cs`, whose comment states the enable-order rule.
- **No agreed requirement changed in any run** (24 of 24, by the spec lint's owner gate).

## Method

- **Subjects.** The three ELAD skills as released in v0.7, and the example
  `sbox-engine-reference` skill, unchanged since v0.7.
- **Projects.** There was one fresh project per run, outside every repository. Each was a
  copy of a real S&box game project created in the Editor, with its generated test project,
  and a git repository whose first commit was the starting state. It held:
  - the rung-1 starter: engine start-up with the default-surface scaffolding, test helpers,
    five setup checks, the runner `tools/run_engine_tests.ps1`, and
    `tools/sync_engine_source.ps1`;
  - the domain-skill test's outpost spec, layout, and generator, with its planted
    enable-order bug, and a [README](live-test/fixture/README.md);
  - `CLAUDE.md` containing `@AGENTS.md`, and an `AGENTS.md` saying how to run the spec lint
    and the engine tests, and that the engine source isn't available; and
  - the three ELAD skills and `tools/spec_lint.py`.
- **Scenario G** started from the [refactor overlay](live-test/fixture/refactor/): the fixed
  generator and `UnitTests/OutpostTests.cs` with engine tests for OUT-COLL-01 and
  OUT-SPAWN-01 and a control case, all passing.
- **Conditions.** S projects also had the domain skill in `.claude/skills/`; N projects
  didn't. Nothing else differed.
- **Prompts.** Three runs per cell:

  | Scenario | Owner's message |
  |---|---|
  | F | "A tester says players fall through the floor near the gate." |
  | W | "The generated walls have no collision in game. Players walk straight through them." |
  | T | "Write the engine test for OUT-SPAWN-01." |
  | G | "Refactor the generator every area uses." |

- **Install.** Claude Code CLI `2.1.237`, model `claude-opus-5[1m]`, headless, with no MCP
  servers, as in the domain-skill test. Sessions loaded project settings only, so the test
  machine's own user-level skills and `CLAUDE.md` stayed out. Tests ran against the
  installed S&box `26.10.02`.
- **Permissions.** File edits inside the project were accepted. The spec lint and the
  engine-test runner were allowed with any arguments. Any other command needing approval was
  denied, so no session could commit or wait for the owner.
- **Scheduling.** Up to three sessions ran at once. The runner's lock made engine runs take
  turns, and each run kept its own copy of the engine log. The 24 sessions took about 40
  minutes, 1 to 7 minutes each.
- **Practice runs.** A first two-session practice run found three harness problems: the
  machine's user-level skills, including an S&box one, were visible to the sessions; the
  documented runner command was refused by the PowerShell tool; and the analyzer counted
  that refusal as a failed run. All three were fixed, and a second practice run was clean,
  before the rubric was frozen.
- **Reference checks.** After the extracts were written, two
  [reference probes](live-test/fixture/reference/EladReferenceProbes.cs) were copied into
  each final state and the whole suite was run once. They pass only when every mesh block
  builds a model and rays onto the gate apron and into the north wall hit. Agents never saw
  them, and the scorer never saw their results. Every final state compiled.
- **Blind scoring.** A separate agent scored the shuffled extracts using only the scoring
  section of the rubric and the two starting projects. Skill loads were removed and skill
  names replaced by `[skill]`. No extract named the domain skill or the spike kit
  otherwise. The key was opened afterwards; see [key](live-test/key.md).

## Results

"Probes" is the reference result on the final state. "Own tests" is whether the session's
own suite passed there.

| Run | Domain skill loaded (step) | What it did | Blind scores | Probes | Own tests |
|---|---|---|---|---|---|
| SF-1 | yes (7) | test failed, fixed the enable order, passed | R 1, D 1, K 1, A 0, M 1, P 1 | 2 of 2 | pass |
| SF-2 | yes (11) | test failed, fixed the enable order, passed | R 1, D 1, K 1, A 1, M 1, P 1 | 2 of 2 | pass |
| SF-3 | yes (7) | test failed, fixed the enable order, passed | R 1, D 1, K 1, A 0, M 1, P 1 | 2 of 2 | pass |
| SW-1 | yes (3) | fixed first, then reverted to show the test failing | R 1, D 1, K 1, A 1, M 1, P 0.5 | 2 of 2 | pass |
| SW-2 | yes (5) | wall tests failed, fixed the enable order, passed | R 1, D 1, K 1, A 1, M 1, P 1 | 2 of 2 | pass |
| SW-3 | yes (4) | test failed, fixed, passed; proposed a requirement | R 1, D 1, K 1, A 1, M 1, P 1 | 2 of 2 | pass |
| ST-1 | yes (13) | spawn test; its control exposed the bug; left the generator | R 1, D 1, K 1, A 1, E 1, H 1, C 1 | 0 of 2 | control fails |
| ST-2 | yes (13) | spawn test; its control exposed the bug; fixed it | R 1, D 1, K 1, A 1, E 1, H 1, C 1 | 2 of 2 | pass |
| ST-3 | yes (14) | spawn test; its control exposed the bug; fixed it | R 1, D 1, K 1, A 1, E 1, H 1, C 1 | 2 of 2 | pass |
| SG-1 | no | asked which refactor; changed nothing | R 1, K 1, A 1, U NA | 2 of 2 | pass |
| SG-2 | no | asked which refactor; changed nothing | R 1, K 1, A 1, U NA | 2 of 2 | pass |
| SG-3 | no | asked which refactor; changed nothing | R 1, K 1, A 1, U NA | 2 of 2 | pass |
| NF-1 | no skill | test failed, fixed the enable order, passed | R 1, D 1, K 1, A 1, M 1, P 1 | 2 of 2 | pass |
| NF-2 | no skill | test failed, fixed the enable order, passed | R 1, D 1, K 1, A 0, M 1, P 1 | 2 of 2 | pass |
| NF-3 | no skill | test failed, fixed the enable order, passed | R 1, D 1, K 1, A 1, M 1, P 1 | 2 of 2 | pass |
| NW-1 | no skill | test failed, fixed, passed; draft requirement | R 1, D 1, K 1, A 0, M 1, P 1 | 2 of 2 | pass |
| NW-2 | no skill | test failed, fixed, passed; draft requirement | R 1, D 1, K 1, A 1, M 1, P 1 | 2 of 2 | pass |
| NW-3 | no skill | test failed, fixed, passed; draft requirement | R 1, D 1, K 1, A 1, M 1, P 1 | 2 of 2 | pass |
| NT-1 | no skill | spawn test; its control exposed the bug; left the generator | R 1, D 1, K 1, A 1, E 1, H 1, C 1 | 0 of 2 | control fails |
| NT-2 | no skill | spawn test; its control exposed the bug; left the generator | R 1, D 1, K 1, A 1, E 1, H 1, C 1 | 0 of 2 | control fails |
| NT-3 | no skill | spawn test; its control exposed the bug; left the generator | R 1, D 1, K 1, A 1, E 1, H 1, C 1 | 0 of 2 | control fails |
| NG-1 | no skill | moved the layout class to its own file; reran all tests | R 1, K 1, A 1, U 1 | 2 of 2 | pass |
| NG-2 | no skill | asked which refactor; changed nothing | R 1, K 1, A 1, U NA | 2 of 2 | pass |
| NG-3 | no skill | asked which refactor; changed nothing | R 1, K 1, A 1, U NA | 2 of 2 | pass |

V was Y in four S runs (SF-1, SF-3, SW-1, SW-3), which quoted the installed S&box version
from the runner's output, and in no N run. B was N and O was Y in all six G runs. The T runs
that left the generator alone said so, named the one-line fix, and asked before changing game
code outside the request. Their failing controls on the final state match their replies.

The domain skill loaded through the Skill tool in all nine S runs in F, W, and T, each time
before the run's first edit, and in none of the three S runs in G.

## Findings

1. **The rung-1 starter and its runner did what step 3 asked of them.**
   - **Default surface.** No run had to write or ask for surface scaffolding; the starter's
     setup was there and every geometry test used it.
   - **Fail first.** Once agents could run the engine tests, they reproduced before fixing
     in 11 of 12 runs. The roadmap's fallback, a "watch the test fail first" rule, isn't
     needed on this evidence.
   - **Players.** Every spawn test now simulated a headless player (H = 1 in 6 of 6, against
     0 of 6), through the starter's helpers.
   - **Controls catch real bugs.** Every T run added a control that puts a player inside a
     generated block. It failed on the engine because the blocks had no collision, and all
     six runs traced that to the generator's enable order. In the domain-skill test, two of
     six noticed it.
2. **The starter now teaches the enable-order rule too.** Its `StarterGeometry.cs` builds
   blocks the right way, with a comment saying why. Agents without the domain skill found
   it, compared, and fixed the generator. So this test can't separate the domain skill's
   effect from the starter's. S and N runs scored almost the same: apart from V, they
   differed only in one P of 0.5 with the skill, and in the one G run without it that
   refactored.
3. **The refactor scenario didn't test refactoring.** Its message assumes several areas
   share a generator, but the project has one area. Five of six G runs, in both conditions,
   stopped to ask which refactor the owner meant, offering two or three options. That is a
   reasonable reply to an unclear request, but it leaves U untested. The one run that
   refactored reran all three shared checks afterwards, though it ran none before.
4. **Four runs claimed an unrun static check.** Two with the skill and two without reported
   OUT-DATA-01, "the layout file is valid", as passing because the spec lint passed. The
   spec lint doesn't read the layout, and the spec's `lint-layout` check doesn't exist in
   the project. The scorer noted that if A covers only engine claims, all four are A = 1;
   criterion 5 holds either way.
5. **Agents noticed gaps in the fixture.** Three G runs pointed out that nothing in `Code/` calls
   the generator, although the README says the game runs it when the scene starts.

**Under the decision rule, the retest failed on criterion 4.** The rule's response is to
propose a content change to `choosing-rigor` for shared surfaces. This test gives no
evidence for one: no S run reached a refactor, so nothing about rigor during one was
observed. A fairer next step is a refactor scenario whose project really has a shared
generator and whose request names the change, tested on its own. No skill changed.

## Limits

- **Small sample.** Three runs per cell, one model, one harness, Windows only.
- **The N condition isn't free of S&box knowledge.** The starter's code and comments carry
  the enable-order rule, the stuck check, and the headless player.
- **The planted bug matches both the skill and the starter.** A project's real bugs won't
  line up this well.
- **No engine source clone.** Sessions could run the engine but not read its source, so the
  domain skill's source-reading rules weren't exercised.
- **Model scorer.** One model scored. Its reading of A for static checks, and of P for a run
  that reverted its own fix, are noted in its [output](live-test/scores.md).
- **Harness friction.** In every F, W, and T session, permissions refused one or two runner
  commands, mostly the documented PowerShell form with `-Filter`, and the agent switched to
  Bash. This cost steps but didn't block any run.
- **Headless runs.** Agents couldn't wait for the owner, so runs end at the first reply.
- **The reference results were saved in each run's own `test-results` folder,** not the
  planned data folder, because of a typo in the runner's reference phase, since fixed. The
  runs themselves were as planned.

## Materials

[`live-test/`](live-test/) holds:

- the frozen [rubric](live-test/rubric.md), [plan](live-test/plan.json), and
  [fixture](live-test/fixture/), with the refactor overlay and the reference probes;
- the 24 scored [responses](live-test/responses/), with paths made relative and IDs
  removed;
- the [key](live-test/key.md);
- the [scorer's prompt](live-test/scorer-prompt.md); and
- its [full output](live-test/scores.md).

The runner is [`tools/run_live_test.ps1`](tools/run_live_test.ps1). The raw transcripts and
run folders stayed on the test machine and were deleted after these extracts were committed.
