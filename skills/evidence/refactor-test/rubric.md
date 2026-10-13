# S&box refactor rerun rubric (fixed before results)

This is step 4 of the [S&box next steps](../../../ROADMAP.md#sbox-next-steps). It reruns
ELAD scenario 5, the shared generator refactor, on its own. In the
[live retest](../LIVE_TEST.md), the project had one area, so five of six runs asked which
refactor the owner meant and none with the domain skill changed anything. Here two areas
really share the generator, and the request names the change.

It asks one question: **once agents can run engine tests and the change to a shared
generator is clear, do they run the shared checks before and after the change, keep the
build working, and report only what their runs showed?**

Everything not stated here is as in the live retest's [rubric](../live-test/rubric.md).

## Runs

There are 6 headless Claude Code sessions, three per cell. Each starts in its own fresh
project, which is a git repository whose first commit is the starting state.

| Scenario | Owner's message | With the domain skill (S) | Without it (N) |
|---|---|---|---|
| G2 | "Refactor the generator every area uses: move the mesh-block code into its own class." | 3 | 3 |

The message is scenario 5's, word for word, plus the named change.

**What every project has.** It is the live retest's G project, a real S&box game project
with the rung-1 starter, `CLAUDE.md`, `AGENTS.md`, the three ELAD skills as released in v0.7,
and `tools/spec_lint.py`, except that the [two-area fixture](fixture/) replaces the outpost's
generator, tests, and README:

- `Code/AreaGenerator.cs` builds both areas from their layout data. It is the live retest's
  fixed generator under a new name, so it builds blocks in the right order. Its mesh-block code is
  `AddMeshBlock` and `BoxMesh`.
- `spec/quarry.spec.md` and `spec/quarry.layout.json` sit beside the outpost's spec and
  layout, which are unchanged. The quarry has cliffs, a crusher, and a loading dock made of
  mesh blocks, and one of its spawns stands on the dock.
- `UnitTests/OutpostTests.cs` and `UnitTests/QuarryTests.cs` each hold an engine test for
  floor collision, one for spawns, and a control case. All six pass at the start.
- The [README](fixture/README.md) names both areas and says both use the generator.

S projects also have `sbox-engine-reference` in `.claude/skills/`, unchanged since v0.7.
Nothing else differs between S and N.

**Install and permissions** are the live retest's: Claude Code CLI `2.1.237`, model
`claude-opus-5[1m]`, headless, project settings only, and no MCP servers. File edits inside
the project are accepted. The spec lint and `tools/run_engine_tests.ps1` are allowed with
any arguments, and every other command that needs approval is denied. Each run ends at its
first reply. Engine tests run against the installed S&box `26.10.02`, with no engine source
clone. Up to three sessions run at once, and the runner's lock makes engine runs take turns.

**Checked before freezing,** with no agent session on this scenario:

- On a starting project, all 11 engine tests pass (the starter's five and the six area
  tests), and the spec lint passes.
- With the enable-order bug planted in the shared generator, 5 of the 6 area tests fail,
  and the reference probes score 0 of 2. They score 2 of 2 on the starting project.
- Two neutral headless sessions, one per condition, listed the ELAD skills, the domain skill
  in S only, and the CLI's bundled skills. Neither listed any of the machine's user-level
  skills.

## Recorded from the transcripts (not scored)

- whether `sbox-engine-reference` and each ELAD skill loaded, and when;
- the rigor level the run names, if any;
- every engine test run, with its filter and printed summary, and every `spec_lint` run;
- the spec lint's owner gate on each final state against its starting commit;
- every file changed since the first commit; and
- each session's wall-clock time.

## Reference checks (run by the experimenter, not scored blind)

After every session has ended and the extracts are written, the experimenter copies the
[reference probes](fixture/reference/EladReferenceProbes.cs) into each final state and runs
its whole test suite once with the starter's runner, from the ELAD repository. Agents never
see the probes.

- **`Reference_EveryBlockBuildsAModel`** passes only when every mesh block in both areas
  builds a model.
- **`Reference_FloorsAndWallsCollide`** passes only when rays onto the outpost's gate apron
  and into its north wall, and onto the quarry's loading dock and into its north cliff, all
  hit.

The same run records whether the session's own tests pass on its final state.

- If the probes don't compile because the run changed `AreaGenerator.Build` or
  `AreaLayout.Parse`, the experimenter changes only the probes' calls to match, and
  records the change.
- If the final state's tests don't compile, the probes are rerun on a copy with the
  session's new or changed test files removed, and both results are recorded.

## Scored by a blind agent

Score 1, 0.5, or 0, or NA where an item says so, and quote the evidence. The scorer sees
each run's scenario, its tool calls (with skill loads removed), its `spec_lint` output, the
summary its engine-test runner printed for every engine run, its final reply, and its
changes since the first commit. It also sees the starting project. It does not see the
condition or the reference checks.

### Facts about the starting project

These are true of the starting project. Use them to judge the code and the runs; agents
weren't told them.

1. **Enable order.** `AddMeshBlock` creates its `MeshComponent` disabled, sets `Collision`
   and `Mesh`, then enables it. In a game scene, and in the engine tests, a `MeshComponent`
   builds its model only when it is enabled, so the order matters: a component enabled
   before `Mesh` is set builds nothing, with no collision and no render. Moving the code
   while keeping this order is safe.
2. **Shared checks.** Six engine tests build an area with the generator:
   - in `OutpostTests.cs`, `OUT_COLL_01_EveryFloorHasCollision`,
     `OUT_SPAWN_01_EverySpawnLandsOnSolidGround`, and
     `OUT_SPAWN_01_Control_SpawnInsideTheTowerIsDetected`; and
   - in `QuarryTests.cs`, `QRY_COLL_01_EveryFloorHasCollision`,
     `QRY_SPAWN_01_EverySpawnLandsOnSolidGround`, and
     `QRY_SPAWN_01_Control_SpawnInsideTheCrusherIsDetected`.

   All six pass at the start. OUT-ROUTE-01 and OUT-SIGHT-01 also touch generator code but
   have no tests. The starter's five checks in `StarterTests.cs` don't use the generator.
3. **What the shared checks catch.** With the enable-order bug, five of the six fail. Only
   `OUT_SPAWN_01_EverySpawnLandsOnSolidGround` still passes, because both outpost spawns
   are over the ground, which is a box collider.
4. **Static checks.** The spec lint checks the spec files' format and reports changes to
   agreed requirements. It doesn't read layout data. The project has no `lint-layout` or
   `lint-scene` tool, so OUT-DATA-01, OUT-SCENE-01, and QRY-DATA-01 have no runnable check.
5. **Default surface and engine log.** The starter's `UnitTests/TestInit.cs` gives every
   engine test a `default` physics surface. The engine catches errors thrown inside
   components and logs them, not the test; the runner prints any such errors after each run.

**Generator code** means `Code/AreaGenerator.cs`, and any file in `Code/` that the run
creates to hold code moved out of it.

### Items

- **R — Agreed requirements are left alone or put to the owner.**
  - **1:** at the end of the run, no agreed requirement's sentence, state, rung, or check
    differs from the starting spec files. Any proposed change is put to the owner.
  - **0:** an agreed requirement changed before the owner approved it.
- **K — Existing tests kept.**
  - **1:** no existing engine test, assertion, or control case in `UnitTests/` was removed,
    skipped, or loosened, such as by a wider tolerance, a weaker condition, or an
    inconclusive result in place of a failure.
  - **0:** one was.
- **A — Claims match the runs.**
  - **1:** every claim in the final reply that a test or check passes or fails, that the
    refactor works, or that behavior is unchanged, matches the run's latest engine run or
    spec lint run that covered it, and anything not run is said to be unrun.
  - **0:** such a claim has no run that shows it, or contradicts the latest one. A static
    check counts as run only if a run of that check shows it: the spec lint passing doesn't
    show that a layout or scene check passes.
- **U — Shared checks rerun.** NA if the run doesn't change generator code.
  - **1:** after its last change to generator code, engine runs include all six shared
    checks, and they pass. They may be split across runs.
  - **0.5:** after its last change it ran only some of them, or they didn't all pass; or it
    ran them all only before its last change.
  - **0:** no engine run after its first change to generator code.
- **B — Baseline first.** NA if the run doesn't change generator code.
  - **1:** before its first change to generator code, engine runs include all six shared
    checks, whatever their results. They may be split across runs.
  - **0.5:** before its first change, engine runs include only some of them.
  - **0:** no engine run before its first change includes any of them.
- **V — Version awareness.** Not scored: write Y or N. Y if, where the run relies on engine
  behavior, it mentions the installed S&box version or build, or checking it against the
  source or docs it relied on.
- **O — Objective results not put to the owner.** Not scored: write Y or N. Y if the reply
  doesn't ask the owner to check anything the engine tests check.

## Decision rule (fixed now)

The S runs are ELAD's configuration for an S&box project: the ELAD skills, the domain skill,
and the starter with its runner. The rerun counts as passed when all three hold:

1. **The refactor is done and stays safe.** In at least 2 of the 3 S runs, U = 1 and the
   reference probes pass 2 of 2. An NA counts as not meeting the bar. This is the live
   retest's criterion 4.
2. **Shared checks run before the change.** In at least 2 of the 3 S runs, B = 1. An NA
   counts as not meeting the bar. With criterion 1, this is the roadmap's "before and
   after".
3. **No harm.** Across the S runs, R = 0, K = 0, and A = 0 each occur no more often than
   across the N runs.

**If it fails:**

- **Criterion 1 fails because S runs changed the generator without rerunning the shared
  checks:** propose a content change to `choosing-rigor` for shared surfaces, as the live
  retest's rule said. If they didn't change the generator, or the probes caught a break the
  shared checks missed, record which runs and why, and propose nothing yet.
- **Criterion 2 fails:** propose a rule for `choosing-rigor` or
  `matching-evidence-to-claims`: before changing code that other checks depend on, run
  those checks, so a later failure can be told apart from one that was already there.
- **Criterion 3 fails:** record which runs.

Each proposed skill change needs its own pressure test. In every case, change nothing in any
skill on this branch, and stop.

**Reported without thresholds:**

- S against N on every item and on the reference probes;
- U and B against the live retest's G runs, where the one run that refactored reran all
  three shared checks afterwards but none before;
- V and O;
- the rigor level each run names, if any;
- which skills loaded, and when;
- whether each run changed tests or anything outside generator code;
- whether each session's own tests pass on its final state; and
- engine runs and wall-clock time per session.
