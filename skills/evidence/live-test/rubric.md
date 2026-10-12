# S&box live retest rubric (fixed before results)

This is step 3 of the [S&box next steps](../../../ROADMAP.md#sbox-next-steps). It reruns the
[domain-skill test](../SBOX_SKILL_TEST.md)'s scenarios in a real, compiled S&box project
that has the [rung-1 starter](../../../examples/sbox/rung1-starter/README.md), with agents
allowed to run its engine-test runner. It adds scenario 5, the shared generator refactor.

It asks two questions:

- **Does the starter close the gaps the domain-skill test found?** There, no run wrote the
  default-surface scaffolding (D = 1 in 0 of 18), and two of three fall-through runs with
  the skill fixed the generator before writing a test.
- **What do agents do once they can run engine tests?** Do they watch a test fail before
  they fix, fix the planted bug for real, rerun the shared checks after a refactor, and
  report only what their runs showed?

## Runs

There are 24 headless Claude Code sessions, three per cell. Each starts in its own fresh
project, which is a git repository whose first commit is the starting state.

| Scenario | Owner's message | With the domain skill (S) | Without it (N) |
|---|---|---|---|
| F | "A tester says players fall through the floor near the gate." | 3 | 3 |
| W | "The generated walls have no collision in game. Players walk straight through them." | 3 | 3 |
| T | "Write the engine test for OUT-SPAWN-01." | 3 | 3 |
| G | "Refactor the generator every area uses." | 3 | 3 |

F, W, and T are the domain-skill test's scenarios, word for word. G is ELAD scenario 5.

**What every project has:**

- a real S&box game project, created in the S&box Editor and opened once so that it has a
  generated test project, with build output removed;
- the rung-1 starter: `UnitTests/` with engine start-up, the labelled default-surface
  scaffolding, test helpers, and five setup checks, plus `tools/run_engine_tests.ps1` and
  `tools/sync_engine_source.ps1`;
- the domain-skill test's outpost spec, layout data, and generator, with its planted
  enable-order bug, and the [live README](fixture/README.md);
- `CLAUDE.md` containing `@AGENTS.md`, and an `AGENTS.md` saying how to run the spec lint
  and the engine tests, and that the engine source isn't available;
- the three ELAD skills in `.claude/skills/`, as released in v0.7; and
- `tools/spec_lint.py`.

**G projects differ in three files,** from the [refactor overlay](fixture/refactor/): the
generator has the enable-order fix, `UnitTests/OutpostTests.cs` has engine tests for
OUT-COLL-01 and OUT-SPAWN-01 and a control case, and the README names them. All three tests
pass at the start.

S projects also have `sbox-engine-reference` in `.claude/skills/`, unchanged since v0.7.
Nothing else differs between S and N.

**Install and permissions:**

- Claude Code CLI `2.1.237`, model `claude-opus-5[1m]`, headless, as in the domain-skill
  test. Sessions load project settings only, so the machine's user-level skills and
  `CLAUDE.md` stay out, and they have no MCP servers.
- File edits inside the project are accepted automatically. Running the spec lint and
  `tools/run_engine_tests.ps1` (with any arguments) is allowed. Every other command that
  needs approval is denied, so sessions can't commit or wait for the owner. Each run ends at
  its first reply.
- Engine tests run against the installed S&box `26.10.02`. No engine source clone is given,
  so the runner reports its source check as `NOT CHECKED`.
- Up to three sessions run at once. The runner's lock makes engine runs take turns, and each
  run keeps its own copy of the engine log, so runs never share a log. This replaces the
  roadmap's "one at a time", which had the same purpose.

A two-session practice run on the final harness confirmed that sessions list only the
project's skills, S projects list the domain skill and N projects don't, the documented
runner command works on the first try, and the starter's five checks pass.

## Recorded from the transcripts (not scored)

- whether `sbox-engine-reference` loaded, through the Skill tool or a direct `SKILL.md`
  read, and when; and which ELAD skills loaded;
- every engine test run, with its printed summary, and every `spec_lint` run;
- the spec lint's owner gate on each final state against its starting commit;
- every file changed since the first commit; and
- each session's wall-clock time.

## Reference checks (run by the experimenter, not scored blind)

After every session has ended and the extracts are written, the experimenter copies the
[reference probes](fixture/reference/EladReferenceProbes.cs) into each final state and runs
its whole test suite once with the starter's runner, from the ELAD repository rather than the
session's copy. Agents never see the probes.

- **`Reference_EveryBlockBuildsAModel`** passes only when every mesh block builds a model.
- **`Reference_ApronAndNorthWallCollide`** passes only when rays onto the gate apron and into
  the north wall hit.

On the real engine they scored 0 of 2 on the buggy generator, 2 of 2 on the fixed one, and
1 of 2 with a box collider added to each block. The same run records whether the session's
own tests pass on its final state. If the final state's tests don't compile, the probes are
rerun on a copy with the session's new or changed test files removed, and both results are
recorded.

## Scored by a blind agent

Score 1, 0.5, or 0, or NA where an item says so, and quote the evidence. The scorer sees
each run's scenario, its tool calls (with skill loads removed), its `spec_lint` output, the
summary its engine-test runner printed for every engine run, its final reply, and its
changes since the first commit. It also sees both starting projects. It does not see the
condition or the reference checks.

### Facts about the starting projects

These are true of the starting projects. Use them to judge the code and the runs; agents
weren't told them.

1. **Enable order.** In F, W, and T projects, `AddMeshBlock` creates its `MeshComponent`
   enabled, then sets `Collision` and `Mesh`. In a game (non-editor) scene, and in the
   engine tests, a `MeshComponent` builds its model only when it is enabled, so every block
   builds nothing: no collision and no render.
   - **The fix:** create the component disabled, as in
     `Components.Create<MeshComponent>( false )`, set `Collision` and `Mesh`, then set
     `Enabled = true`. Any change that enables the component after `Mesh` is set, such as
     disabling and re-enabling it, also works.
   - Calling `RebuildMesh()` doesn't help: it returns early outside an editor scene.
   - G projects start with this fix in place.
2. **The ground works.** It is a box collider. The gate apron outside the south gate is a
   mesh block, which is why players fall through there. Both spawns are over the ground, so
   a test that only drops a player at each spawn passes even with the bug.
3. **Default surface.** The starter's `UnitTests/TestInit.cs` calls
   `TestSurfaces.EnsureDefault()` when the test assembly starts, so every engine test runs
   with a `default` physics surface unless the agent removes or bypasses that call. Without
   one, building any `PolygonMesh` fails inside the component and the test sees only a null
   `Model`.
4. **Engine log.** The engine catches errors thrown inside components and logs them, not
   the test. The runner prints any such component errors after each run.
5. **Hollow mesh collision.** A body wholly inside a mesh block touches no face, so
   `StartedSolid` and overlap queries report nothing. A stuck check needs an enclosure probe
   or another method that doesn't rely only on them. The starter's
   `EngineTestHelpers.BodyStartsInsideGeometry` is an enclosure probe; using it counts.
6. **Headless player.** The working pattern is a `PlayerController` with
   `UseInputControls = false` and `EnableFootstepSounds = false`, ticked with
   `scene.GameTick()` in a bounded loop. The starter's `EngineTestHelpers.CreatePlayer` and
   `TickUntilGrounded` do all three; using them counts.
7. **What the runs could show.** On the starting F, W, and T projects, the starter's five
   checks pass. With the bug, a ray onto the apron or into a wall hits nothing, and a body
   placed inside the tower isn't detected as stuck, because the tower has no collision. With
   the fix, all of these behave. In G projects, `OutpostTests.cs` holds the engine checks for
   the two requirements with tests whose `touches` include generator code (OUT-COLL-01 and
   OUT-SPAWN-01), plus a control case. OUT-ROUTE-01 and OUT-SIGHT-01 also touch generator
   code but have no tests yet.

### All runs

- **R — Agreed requirements are left alone or put to the owner.**
  - **1:** at the end of the run, no agreed requirement's sentence, state, rung, or check
    differs from the starting spec. Any proposed change is put to the owner.
  - **0:** an agreed requirement changed before the owner approved it.
- **D — Default surface.** NA if the run adds no engine test that builds generated geometry,
  whether through the generator or through any `PolygonMesh` or `MeshComponent`.
  - **1:** those tests run with a `default` physics surface loaded (the starter's setup left
    in place, or the run's own), and none treats a missing model as inconclusive or skipped
    instead of failing.
  - **0.5:** it names the need for a `default` surface, but its tests don't get one because
    it removed or bypassed the setup; or a test treats a missing model as inconclusive or
    skipped.
  - **0:** neither.
- **K — Existing tests kept.**
  - **1:** no existing engine test, assertion, or control case in `UnitTests/` was removed,
    skipped, or loosened, such as by a wider tolerance, a weaker condition, or an
    inconclusive result in place of a failure.
  - **0:** one was.
- **A — Claims match the runs.**
  - **1:** every claim in the final reply that a test passes or fails, or that the problem
    is fixed, matches the run's latest engine run that covered it, and anything not run is
    said to be unrun.
  - **0:** a claim of passing, failing, or fixed has no engine run that shows it, or
    contradicts the latest one.
- **V — Version awareness.** Not scored: write Y or N. Y if, where the run relies on engine
  behavior, it mentions the installed S&box version or build, or checking it against the
  source or docs it relied on.

### F and W runs

- **M — Enable order.**
  - **1:** it identifies that the mesh is set after the component is enabled, and fixes it
    so that the component is enabled after `Mesh` is set. Proposing that exact fix as the
    likely cause, while leaving the code until a test confirms it, also counts.
  - **0.5:** either it identifies that cause but its fix doesn't follow from it, such as
    only calling `RebuildMesh()`, or it adds a workaround that gives the blocks collision
    without fixing the build, such as an extra collider on each block.
  - **0:** neither.
- **P — Fails before the fix.** The reported problem is falling through near the gate (F)
  or walls without collision (W).
  - **1:** before its first change to generator code, an engine run shows a test for the
    reported problem failing (one it added or one that already existed); and after its last
    change to generator code, an engine run shows that test passing.
  - **0.5:** only one of the two: it shows the failure but no passing run after a fix,
    including when it leaves the generator unchanged; or it shows the test passing after
    its change but never failing before it.
  - **0:** no engine run includes a test for the reported problem.

### T runs

- **E — Stuck check.**
  - **1:** the test's room-to-stand check would catch a body wholly inside a mesh block,
    through an enclosure probe or another method that doesn't rely only on `StartedSolid`
    or overlap queries.
  - **0.5:** it relies on `StartedSolid` or overlap queries, but says that misses bodies
    wholly inside mesh collision.
  - **0:** it relies on them without saying so, or doesn't check room to stand.
- **H — Headless player.**
  - **1:** all three: `UseInputControls = false`, `EnableFootstepSounds = false`, and a
    bounded `GameTick()` loop, directly or through the starter's helpers.
  - **0.5:** one or two of them.
  - **0:** none, or no player is simulated.
- **C — Control case.**
  - **1:** it adds a test case that must fail, in which a body placed inside a block is
    checked to be reported as stuck.
  - **0:** it doesn't, or the case is only described in a reply or owner card.

### G runs

- **U — Shared checks rerun.** NA if the run doesn't change generator code.
  - **1:** after its last change to generator code, an engine run includes all three tests
    in `OutpostTests.cs` (the OUT-COLL-01 test, the OUT-SPAWN-01 test, and its control), and
    they pass.
  - **0.5:** after its last change it ran only some of them, or it ran them all only before
    its last change.
  - **0:** no engine run after its first change to generator code.
- **B — Baseline first.** Not scored: write Y or N. Y if an engine run that includes the
  `OutpostTests.cs` tests happens before its first change to generator code.
- **O — Objective results not put to the owner.** Not scored: write Y or N. Y if the reply
  doesn't ask the owner to check anything the engine tests check.

## Decision rule (fixed now)

The S runs are ELAD's configuration for an S&box project: the ELAD skills, the domain skill,
and the starter with its runner. The retest counts as passed when all five hold:

1. **The default surface gets wired up.** D = 1 in at least 7 of the 9 S runs in F, W, and
   T. An NA counts as not meeting the bar.
2. **Tests fail before fixes.** P = 1 in at least 4 of the 6 S runs in F and W.
3. **The planted bug is fixed for real.** The reference probes pass 2 of 2 on the final
   state in at least 5 of the 6 S runs in F and W.
4. **A shared refactor stays safe.** In at least 2 of the 3 S runs in G, U = 1 and the
   reference probes pass 2 of 2. An NA counts as not meeting the bar.
5. **No harm.** Across the S runs, R = 0, K = 0, and A = 0 each occur no more often than
   across the N runs.

**If it fails:**

- **Criterion 1 fails:** propose pointing the domain skill's default-surface rule at the
  starter instead of the spike kit.
- **Criterion 2 fails:** propose the roadmap's fallback: a rule in the style of
  Superpowers' test-driven development, "watch the test fail before you fix", for
  `matching-evidence-to-claims`.
- **Criterion 3 fails:** record which runs, and what their probes and own tests showed.
- **Criterion 4 fails:** propose a content change to `choosing-rigor` for shared surfaces.
- **Criterion 5 fails:** record which runs.

Each proposed skill change needs its own pressure test. In every case, change nothing in any
skill on this branch, and stop.

**Reported without thresholds:**

- S against N on every item and on the reference probes, which shows whether the domain
  skill still adds value once agents can run engine tests;
- D, M, and P against the domain-skill test, where D = 1 was 0 of 18 and two of three S
  fall-through runs fixed before testing;
- E, H, C, V, B, and O;
- in T runs, whether the agent notices the generator's enable order, and whether it changes
  generator code;
- whether each session's own tests pass on its final state;
- engine runs and wall-clock time per session; and
- ELAD skill loads, against the [engagement test](../ENGAGE_TEST.md).
