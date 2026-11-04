# S&box skill update test rubric (fixed before results)

This rubric tests a change to the example domain skill
[`sbox-engine-reference`](../../../examples/sbox/skills/sbox-engine-reference/SKILL.md). The
change does four things:

- it points saved-scene loading at the rung-1 starter's `EngineTestHelpers.LoadSavedScene`,
  where the old text said `SceneFile.LoadFromJson` and `Scene.Load` work;
- it points the default surface at the starter's `UnitTests/TestSurfaces.cs`, where the old
  text pointed at the spike kit, which a project doesn't have;
- it says `SBOX_PUBLIC` or the project's `AGENTS.md` names the engine source clone; and
- it records a lesson only in the lessons file `AGENTS.md` names, and when none is named,
  gives the lesson in the report and asks the owner where lessons live, in one shape: rule,
  what happened, why, proof.

It asks one question: do agents with the updated skill do better on these points than
agents with the skill as released in v1.07, and no worse elsewhere?

## Runs

There are 12 headless Claude Code sessions. Each starts in its own fresh project, which is a
git repository whose first commit is the synthetic game project in [`fixture/`](fixture/).

| Scenario | Owner's message | Old skill (O) | Updated skill (U) |
|---|---|---|---|
| L | "Write an engine test that loads our saved scene, Assets/scenes/outpost.scene, and checks that a player at the north spawn lands on its ground." | 3 | 3 |
| K | "In game, the sign over the gate shows at a different angle every time the map loads. Fix it so it stays put, and make sure we don't get caught by this again." | 3 | 3 |

**What every project has:**

- the fixture: the outpost spec and layout, the generator `Code/OutpostGenerator.cs`, the
  gate sign `Code/GateDecal.cs`, and the saved scene `Assets/scenes/outpost.scene` with its
  mesh data in `outpost.scene_d`;
- `UnitTests/` with the rung-1 starter's `TestInit.cs`, `TestSurfaces.cs`,
  `EngineTestHelpers.cs` and `StarterGeometry.cs`, as a project that copied the starter in
  has, and no project tests;
- `CLAUDE.md` containing `@AGENTS.md`, and an `AGENTS.md` saying how to run the spec lint,
  that only the owner can run the engine tests, and that neither the S&box install nor the
  engine source is available. It names no lessons file;
- the three ELAD skills in `.claude/skills/`, from this branch; and
- `tools/spec_lint.py`.

Every project has `sbox-engine-reference` in `.claude/skills/`. O projects have its
`SKILL.md` as tagged `v1.07`; U projects have it from this branch. Nothing else differs.

Commands that need approval are denied, except running the spec lint. No session can
compile, run engine tests, or wait for the owner, so each run ends at its first reply.

## Recorded from the transcripts (not scored)

- whether `sbox-engine-reference` loaded, through the Skill tool or a direct `SKILL.md`
  read, and when;
- which ELAD skills loaded;
- whether the run read `UnitTests/EngineTestHelpers.cs`;
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

1. **The saved scene's floors are editable meshes.** In `Assets/scenes/outpost.scene` the
   ground, walls, gate apron and tower are `MeshComponent`s whose `Mesh` is a `$blob`
   reference into `outpost.scene_d`.
   - `SceneFile.LoadFromJson` reads only the scene's JSON and drops the `_d` data, so those
     meshes load empty, and a player falls through the ground.
   - `Scene.LoadFromFile` fails in a headless test.
   - `Scene.Load` with its default loading screen never finishes loading headlessly, so a
     player in the scene never moves.
   - `EngineTestHelpers.LoadSavedScene( scene, "Assets/scenes/outpost.scene" )` reads the
     `_d` file and loads without a loading screen. That is the working route.
2. **Test start-up is in place.** `UnitTests/TestInit.cs` starts the engine and registers a
   `default` physics surface through `UnitTests/TestSurfaces.cs`, so meshes build in tests.
3. **The sign's roll is random.** A `Decal`'s `Rotation` is its roll about its forward axis,
   and defaults to the range `new ParticleFloat( 0, 360 )`, drawn again each time the
   component is enabled. `GateDecal` never sets it, so the sign lands at a new angle each
   time the scene loads.
   - **The fix:** set the decal's `Rotation` to a constant, such as `decal.Rotation = 0f`,
     or the angle the sign needs.
   - Setting only the game object's `WorldRotation` doesn't fix the roll.
4. **What the project lacks.** It has no lessons file, and its `AGENTS.md` names none. It
   has no ELAD spike kit, no engine source clone, and no S&box install.
5. **No compiling.** Agents couldn't compile or run anything except the spec lint. Score
   what the code and the reply would do, not whether they compiled.

### All runs

- **R — Agreed requirements are left alone or put to the owner.**
  - **1:** at the end of the run, no agreed requirement's sentence, state, rung, or check
    differs from the starting spec. Any proposed change is put to the owner.
  - **0:** an agreed requirement changed before the owner approved it.
- **N — No files that aren't there.**
  - **1:** the reply and the changes refer to no file or folder the project lacks as if it
    were there, such as an ELAD spike kit, a `TestSurfaces.cs` other than the one in
    `UnitTests/`, an engine-lessons file, or an engine source clone. A file the run itself
    creates is there. Saying that something isn't available is fine.
  - **0:** at least one such reference, such as telling the owner to copy the spike kit's
    `TestSurfaces.cs`, or saying a lesson went into a lessons file the project doesn't have.

### L runs

- **L — Loading the saved scene.**
  - **1:** the test loads `Assets/scenes/outpost.scene` with
    `EngineTestHelpers.LoadSavedScene`, or another route that reads `outpost.scene_d` and
    loads without a loading screen.
  - **0.5:** it uses a route that drops the `_d` data or uses a loading screen, but tells
    the owner that route may load the meshes empty or never finish loading.
  - **0:** otherwise, such as `SceneFile.LoadFromJson` with `Scene.Load`, or
    `Scene.LoadFromFile`, with no such warning, or building the area from the generator
    instead of loading the saved scene.

### K runs

- **F — The fix.**
  - **1:** it sets the decal's `Rotation` to a constant.
  - **0.5:** it makes the roll repeatable another way, such as a fixed seed, or names the
    constant-`Rotation` fix without making it.
  - **0:** neither, including changing only the game object's rotation.
- **K — Where the lesson goes.**
  - **1:** it gives the lesson in the reply and asks the owner where lessons should be
    recorded, or proposes a place and asks before writing there.
  - **0.5:** it records the lesson in a file of its own choosing, new or existing, without
    asking, and says where in the reply.
  - **0:** it records no lesson, or says a lesson was recorded somewhere it wasn't.
- **S — What the lesson says.** Wherever the lesson is, in the reply or in a file, count
  which of these it gives: (a) what to do; (b) what went wrong, and the S&box build or
  version, or that the build is unknown; (c) why, with an engine source path, or that no
  source was checked; and (d) the check that now catches it, or "nothing yet".
  - **1:** all four.
  - **0.5:** three.
  - **0:** two or fewer, or no lesson.
- **C — A check.** Not part of the decision rule.
  - **1:** it adds a test or static check that fails when the sign's roll isn't a constant.
  - **0.5:** it proposes such a check without adding it.
  - **0:** neither.

## Decision rule (fixed now)

The update counts as supported when all four hold:

1. **It triggers.** `sbox-engine-reference` loads in at least 2 of 3 runs in each of the
   four cells.
2. **Its changes show up.** In the U runs:
   - L = 1 in at least 2 of the 3 L runs;
   - K = 1 in at least 2 of the 3 K runs; and
   - N = 1 in at least 5 of the 6 runs.
3. **It beats the old text.** The U runs' total of L, K, S and N exceeds the O runs' total.
4. **It does no harm.** The U runs have no more R = 0 than the O runs, and their total F is
   at least the O runs' total.

An NA counts as not meeting a bar, and as 0 in a total.

**If it fails:**

- **Criterion 1 fails:** record which cells, and stop; both conditions share the skill's
  description, so this points at the environment.
- **Criterion 2 or 3 fails in runs where the skill loaded:** propose content changes.
- **Criterion 4 fails:** record which runs.

In every case, change nothing more in the skill on this branch, and stop.

**Reported without thresholds:**

- S and C in each condition;
- in L runs, whether the run read `UnitTests/EngineTestHelpers.cs`, and which loader runs
  that didn't chose;
- in K runs, whether a run created a lessons file, and its name; and
- ELAD skill loads.
