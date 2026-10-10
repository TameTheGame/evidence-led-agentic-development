# S&box domain-skill test rubric (fixed before results)

This rubric tests the example domain skill
[`sbox-engine-reference`](../../../examples/sbox/skills/sbox-engine-reference/SKILL.md),
which had never been tested. It asks two questions:

- **Triggering.** Does the skill load on its own during S&box coding work?
- **Behavior.** Do agents follow what it teaches, compared with agents without it?

## Runs

There are 18 headless Claude Code sessions. Each starts in its own fresh project, which is a
git repository whose first commit is the synthetic game project in [`fixture/`](fixture/).

| Scenario | Owner's message | Runs with the domain skill (S) | Runs without it (N) |
|---|---|---|---|
| F | "A tester says players fall through the floor near the gate." | 3 | 3 |
| W | "The generated walls have no collision in game. Players walk straight through them." | 3 | 3 |
| T | "Write the engine test for OUT-SPAWN-01." | 3 | 3 |

**What every project has:**

- the fixture: the outpost spec, a layout file with a ground box, wall, apron and tower
  blocks, the generator `Code/OutpostGenerator.cs`, and `UnitTests/` with the engine
  start-up and one smoke test;
- `CLAUDE.md` containing `@AGENTS.md`, and an `AGENTS.md` saying how to run the spec lint,
  that only the owner can run the engine tests, and that neither the S&box install nor
  the engine source is available;
- the three ELAD skills in `.claude/skills/`, as released in v0.7; and
- `tools/spec_lint.py`.

S projects also have `sbox-engine-reference` in `.claude/skills/`. Nothing else differs.
The AGENTS.md snippet isn't used, as in the v0.7 release configuration.

**Planted problems.** The fixture has two, matching what the skill teaches:

- **The generator enables each `MeshComponent` before assigning its mesh.** In a game scene
  that builds no model, so the walls, the gate apron, and the tower have no collision. The
  ground is a box collider and works, so players fall through only on the apron outside
  the gate.
- **Test setup loads no `default` physics surface.** Headless, building a mesh then fails
  inside the component, and the error goes only to the engine's log.

Commands that need approval are denied, except running the spec lint. No session can
compile, run engine tests, or wait for the owner, so each run ends at its first reply.

## Recorded from the transcripts (not scored)

- whether `sbox-engine-reference` loaded, through the Skill tool or a direct `SKILL.md`
  read, and when;
- which ELAD skills loaded;
- `spec_lint` runs, and its owner gate run on each final state against the starting commit;
  and
- every file changed since the first commit.

## Scored by a blind agent

Score 1, 0.5, or 0, or NA where an item says so, and quote the evidence. The scorer sees
each run's scenario, its tool calls (with skill loads removed), its `spec_lint` output, its
final reply, and its changes since the first commit. It also sees the starting project. It
does not see the condition.

### Facts about the starting project

These are true of the fixture. Use them to judge the code; agents weren't told them.

1. **Enable order.** `AddMeshBlock` creates its `MeshComponent` enabled, then sets
   `Collision` and `Mesh`. In a game (non-editor) scene a `MeshComponent` builds its model
   only when it is enabled, so every block builds nothing in game: no collision and no
   render. In an editor scene they build.
   - **The fix:** create the component disabled, as in
     `Components.Create<MeshComponent>( false )`, set `Collision` and `Mesh`, then set
     `Enabled = true`. Any change that enables the component after `Mesh` is set, such as
     disabling and re-enabling it, also works.
   - Calling `RebuildMesh()` doesn't help: it returns early outside an editor scene.
2. **The ground works.** It is a box collider. The gate apron outside the south gate is a
   mesh block, which is why players fall through there.
3. **Default surface.** `UnitTests/TestInit.cs` loads no `default` physics surface.
   - Headless, building any `PolygonMesh` then throws inside the component. The engine
     catches the error and logs it to `logs\testhost.log` in the S&box install folder, not
     to the test output. The test sees only a null `Model`.
   - Engine tests that build generated geometry need test setup that provides a `default`
     surface. On the tested build no public API does this, so the working route is
     test-only scaffolding.
4. **Hollow mesh collision.** A body wholly inside a mesh block touches no face, so
   `StartedSolid` and overlap queries report nothing.
   - A stuck check needs an enclosure probe: a ray outward from the body's centre to the
     first face, then a ray back. A hit on the way back means the centre is inside a closed
     solid.
   - Any other method that doesn't rely only on `StartedSolid` or overlap queries also
     counts.
5. **Headless player.** The working pattern is a `PlayerController` with
   `UseInputControls = false` and `EnableFootstepSounds = false`, ticked with
   `scene.GameTick()` in a bounded loop.
6. **No compiling.** Agents couldn't compile or run anything except the spec lint. Score
   what the code and the reply would do, not whether they compiled.

### All runs

- **R — Agreed requirements are left alone or put to the owner.**
  - **1:** at the end of the run, no agreed requirement's sentence, state, rung, or check
    differs from the starting spec. Any proposed change is put to the owner.
  - **0:** an agreed requirement changed before the owner approved it.
- **D — Default surface.** NA if the run neither adds nor proposes engine tests that build
  generated geometry, whether through the generator or through any `PolygonMesh` or
  `MeshComponent`.
  - **1:** it adds test setup code meant to provide a `default` physics surface before
    those tests run.
  - **0.5:** it tells the owner those tests need a `default` surface, or that meshes won't
    build headlessly without one, but adds no setup code for it. A TODO or placeholder
    counts as 0.5.
  - **0:** neither.
- **G — Engine log.** NA if the run doesn't ask the owner to run engine tests.
  - **1:** it names `testhost.log`, in the S&box install folder's `logs`, as where engine or
    component errors from the test run appear.
  - **0.5:** it says component errors may be caught or logged by the engine, and to check
    an engine log, without naming `testhost.log`.
  - **0:** neither.
- **V — Version awareness.** Not scored: write Y or N. Y if, where the run relies on engine
  behavior, it mentions checking the installed S&box version or build (such as the
  `.version` file) against the source or docs it relied on.

### F and W runs

- **M — Enable order.**
  - **1:** it identifies that the mesh is set after the component is enabled, and fixes
    it so that the component is enabled after `Mesh` is set. Proposing that exact fix as
    the likely cause, while leaving the code until a test confirms it, also counts.
  - **0.5:** either it identifies that cause but its fix doesn't follow from it, such as
    only calling `RebuildMesh()`, or it adds a workaround that gives the blocks collision
    without fixing the build, such as an extra collider on each block.
  - **0:** neither.

### F runs

- **X — Reproduce first.** Not part of the decision rule.
  - **1:** it adds an engine test that reproduces the report before changing generator
    code, or leaves generator code unchanged and asks the owner to run the test first.
  - **0.5:** it adds the test after changing generator code.
  - **0:** it adds no engine test.

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
    bounded `GameTick()` loop.
  - **0.5:** one or two of them.
  - **0:** none, or no player is simulated.
- **C — Control case.** Not part of the decision rule.
  - **1:** it adds a case that must fail, in which a body placed inside a block is reported
    as stuck.
  - **0:** it doesn't.

## Decision rule (fixed now)

The domain skill counts as supported when all four hold:

1. **It triggers.** `sbox-engine-reference` loads in at least 2 of 3 S runs in each
   scenario.
2. **Its teaching shows up.** In the S runs:
   - M = 1 in at least 4 of the 6 F and W runs;
   - D ≥ 0.5 in at least 6 of 9 runs;
   - G = 1 in at least 6 of 9 runs; and
   - E = 1 in at least 2 of 3 T runs.

   An NA counts as not meeting the bar.
3. **It beats no skill.** The S runs' total of M, D, G, E, and H exceeds the N runs' total,
   with NA as 0.
4. **It does no harm.** The S runs have no more R = 0 than the N runs.

**If it fails:**

- **Criterion 1 fails:** propose a description change.
- **Criterion 2 or 3 fails in runs where the skill loaded:** propose content changes.
- **Criterion 4 fails:** record which runs.

In every case, change nothing in the skill on this branch, and stop.

**Reported without thresholds:**

- D = 1 against D = 0.5, which shows whether agents can write the default-surface
  scaffolding without the spike kit's code. That is the case for the rung-1 starter in the
  [S&box next steps](../../../ROADMAP.md#sbox-next-steps);
- X in the F runs, which is ELAD scenario 3 ("A tester says players fall through the floor
  near the gate"), not yet tested before this;
- C, H, and V;
- in T runs, whether the agent notices the generator's enable order; and
- ELAD skill loads, against the [engagement test](../ENGAGE_TEST.md).
