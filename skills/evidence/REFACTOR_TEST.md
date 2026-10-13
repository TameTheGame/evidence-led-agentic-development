# S&box Refactor Rerun

> **Small experiment, acting sessions, real engine.** There were 6 real headless sessions in
> compiled S&box projects, scored blind against a [rubric](refactor-test/rubric.md) frozen in
> `7bc1afd` before any run, and checked on the engine afterwards.

This is step 4 of the [S&box next steps](../../ROADMAP.md#sbox-next-steps). It reran ELAD
scenario 5, the shared generator refactor, on its own. In the [live retest](LIVE_TEST.md)
the project had one area, so five of six runs asked which refactor was meant. Here two areas
really share the generator, and the owner's message names the change.

## Result in brief

**The rerun failed its pre-registered decision rule, on one criterion: no run ran the shared
checks before changing the generator.** Every run made the change and then ran every shared
check, which passed. The other two criteria passed.

| Criterion (S runs) | Needed | Got |
|---|---|---|
| 1. U = 1: shared checks rerun and pass after the change, and probes pass | 2 of 3 | **3 of 3** |
| 2. B = 1: shared checks run before the first change | 2 of 3 | **0 of 3** |
| 3. R = 0, K = 0, and A = 0, with the skill against without | no more | **0, 0, 0 against 0, 0, 0** |

- **Every run refactored, and the build stayed correct.** All 6 moved `AddMeshBlock` and
  `BoxMesh` into a new `Code/MeshBlock.cs`, then ran the whole engine suite once: 11 of 11
  passed. The reference probes passed 2 of 2 on every final state. In the live retest, 1 of
  6 refactor runs changed anything.
- **No run checked the starting state first.** All 6 edited first and tested after.
- **Agents called it light.** Five runs loaded `choosing-rigor` and named the level
  **light**: a move with an ordinary revert, covered by the existing engine tests. At light,
  the skill says to change it, run the check, read the diff, and stop, which is what every
  run did. Scenario 5 expects rigor to rise for a shared surface; none raised it.
- **The domain skill made no difference.** S and N runs scored the same on every item. The
  domain skill loaded in 1 of 3 S runs, before its first edit.

## Method

- **Subjects.** The three ELAD skills as released in v0.7, and the example
  `sbox-engine-reference` skill, unchanged since v0.7.
- **Projects.** One fresh project per run, built by
  [`run_live_test.ps1`](tools/run_live_test.ps1) as the live retest's G projects were, with
  the [two-area fixture](refactor-test/fixture/) in place of the outpost's generator, tests,
  and README:
  - `Code/AreaGenerator.cs`, the live retest's fixed generator under a new name, building
    both areas;
  - a quarry spec and layout beside the outpost's, with a loading dock made of mesh blocks
    and a spawn standing on it; and
  - `UnitTests/OutpostTests.cs` and `UnitTests/QuarryTests.cs`, each with a floor-collision
    test, a spawn test, and a control case. These six are the shared checks.
- **Conditions.** S projects also had the domain skill in `.claude/skills/`; N projects
  didn't. Nothing else differed.
- **Prompt.** "Refactor the generator every area uses: move the mesh-block code into its own
  class." It is scenario 5's message plus the named change. Three runs per condition.
- **Install, permissions, and scheduling** were the live retest's: Claude Code CLI
  `2.1.237`, model `claude-opus-5[1m]`, headless, project settings only, no MCP servers,
  S&box `26.10.02`, and up to three sessions at once. The 6 sessions took 82 to 116 seconds
  each.
- **Checked before freezing.** On a starting project all 11 engine tests passed. With the
  enable-order bug planted in the shared generator, 5 of the 6 shared checks failed and the
  probes scored 0 of 2. Two neutral sessions saw only the project's skills and the CLI's
  bundled ones, none of the test machine's own.
- **Reference checks.** After the extracts were written, two
  [reference probes](refactor-test/fixture/reference/EladReferenceProbes.cs) were copied into
  each final state and the whole suite was run once. They pass only when every mesh block in
  both areas builds a model, and rays onto the outpost's apron and wall and the quarry's dock
  and cliff hit. Agents never saw them, and the scorer never saw their results.
- **Blind scoring.** A separate agent scored the shuffled extracts using only the scoring
  section of the rubric and the starting project. Skill loads were removed and skill names
  replaced by `[skill]`. The key was opened afterwards; see [key](refactor-test/key.md).

## Results

Each run made one engine run, unfiltered, after its last change to generator code, and it
passed 11 of 11. "Probes" is the reference result on the final state.

| Run | Domain skill loaded (step) | Rigor named | Blind scores | Probes | Own tests | Time |
|---|---|---|---|---|---|---|
| SR-1 | no | light | R 1, K 1, A 1, U 1, B 0 | 2 of 2 | pass | 116 s |
| SR-2 | no | light | R 1, K 1, A 1, U 1, B 0 | 2 of 2 | pass | 82 s |
| SR-3 | yes (9) | light | R 1, K 1, A 1, U 1, B 0 | 2 of 2 | pass | 87 s |
| NR-1 | no skill | light | R 1, K 1, A 1, U 1, B 0 | 2 of 2 | pass | 97 s |
| NR-2 | no skill | light | R 1, K 1, A 1, U 1, B 0 | 2 of 2 | pass | 89 s |
| NR-3 | no skill | none | R 1, K 1, A 1, U 1, B 0 | 2 of 2 | pass | 105 s |

V was N and O was Y in all six runs. No run changed a spec or a test: the spec lint's owner
gate found no agreed requirement changed in 6 of 6, and no file under `UnitTests/` changed.
Five runs also updated the README, and five ran the spec lint. Four runs, three of them S,
copied the starter's comment on the enable order into the moved code. Every run noticed that
the starter's `StarterGeometry.cs` has its own copy of the mesh-block code, and left it
alone.

`choosing-rigor` loaded in five runs, each time before the first edit. NR-3 loaded no skill.

## Findings

1. **Naming the change fixed the scenario.** With two areas and a named change, all six
   runs refactored instead of asking. Scenario 5 now tests what it was meant to.
2. **Agents reran every shared check after the change, without being told which.** Every
   run ran the whole suite, so both areas' checks ran, not only one area's. This is the
   "reruns every machine check whose `touches` includes the generator" part of scenario 5,
   and it held in 6 of 6.
3. **No run took a baseline, and the skill doesn't ask for one at light.** Agents judged a
   pure move with existing exact tests to be light, and followed the light level as written.
   Scenario 5 expects rigor to rise for the shared surface, and the roadmap expected checks
   before and after. Neither happened.
4. **A baseline would have changed nothing here.** Every run's checks passed after the
   change. A baseline matters when a check fails afterwards: it shows whether the change
   broke it or it was failing already. This test never reached that case, so it gives no
   evidence that the missing baseline costs anything.

**Under the decision rule, the rerun failed on criterion 2.** The rule's response is to
propose a rule for `choosing-rigor` or `matching-evidence-to-claims`: before changing code
that other checks depend on, run those checks, so a later failure can be told apart from one
that was already there. Finding 4 is evidence that the rule would add a run to every such
change without changing the outcome here. A narrower rule, to check the starting state only
when a shared check fails after a change, would cost nothing when checks pass. Either needs
its own pressure test before any skill changes. No skill changed.

## Limits

- **Small sample.** Three runs per condition, one model, one harness, Windows only.
- **No failure case.** The refactor was simple and every run kept it correct, so no run met
  a failing shared check. That is the case where a baseline would matter.
- **A clear request.** The owner's message named the change. Real requests may be vaguer, as
  the live retest's was.
- **Imperfect blinding.** Removed skill loads leave gaps in the step numbers, and SR-3's extra
  gap hints at its extra skill. With identical scores in both conditions, this can't have
  changed the comparison.
- **Model scorer.** One model scored. It read A as covering only what a reply claims, and V
  as N for runs that rely on engine results without naming the version; see its
  [output](refactor-test/scores.md).
- **One session ran its engine tests in the background** and read the output later. The
  analyzer first missed that output; it was fixed to include it before blinding.
- **Headless runs.** Agents couldn't wait for the owner, so runs end at the first reply.

## Materials

[`refactor-test/`](refactor-test/) holds:

- the frozen [rubric](refactor-test/rubric.md), [plan](refactor-test/plan.json), and
  [fixture](refactor-test/fixture/), with the reference probes;
- the 6 scored [responses](refactor-test/responses/), with paths made relative and IDs
  removed;
- the [key](refactor-test/key.md);
- the [scorer's prompt](refactor-test/scorer-prompt.md); and
- its [full output](refactor-test/scores.md).

The runner is [`tools/run_live_test.ps1`](tools/run_live_test.ps1), scenario `G2`. The raw
transcripts and run folders stayed on the test machine and were deleted after these extracts
were committed.
