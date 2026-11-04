# S&box Skill Update Test

> **Small experiment, acting sessions.** There were 12 real headless sessions, scored blind
> against a [rubric](skill-update-test/rubric.md) frozen in `fd22637` before any run.

This tested a change to the example domain skill
[`sbox-engine-reference`](../../examples/sbox/skills/sbox-engine-reference/SKILL.md),
against the same skill as released in v1.07. The change came from an outside review. It
points saved-scene loading at the rung-1 starter's `EngineTestHelpers.LoadSavedScene`, and
the default surface at the starter's `TestSurfaces.cs`. It says `SBOX_PUBLIC` or the
project's `AGENTS.md` names the engine source clone. And it records a lesson only in the
lessons file `AGENTS.md` names, or, with none named, gives the lesson in the report and asks
the owner where lessons live, in one shape: rule, what happened, why, proof.

## Result in brief

**The update passed its pre-registered decision rule.**

| Criterion | Needed | Got |
|---|---|---|
| 1. The skill loads, in each of the four cells | 2 of 3 | **3 of 3** in every cell |
| 2. L = 1: loads the saved scene with its `_d` data (U runs) | 2 of 3 | **3 of 3** |
| 2. K = 1: gives the lesson and asks where lessons live (U runs) | 2 of 3 | **3 of 3** |
| 2. N = 1: names no file the project lacks (U runs) | 5 of 6 | **5 of 6** |
| 3. Total of L, K, S and N, updated against old | higher | **13 against 12** |
| 4. Runs with R = 0, updated against old | no more | **0 against 0** |
| 4. Total F, updated against old | no less | **0 against 0** |

- **The lesson's home changed.** With the old text, two of three runs wrote a new
  `docs/engine-lessons.md` unasked, after the old skill's "the project's engine-lessons
  file", and one recorded no lesson. With the update, all three gave the lesson in the reply
  and asked the owner where lessons live; two quoted the rule against inventing a file.
- **The loader change showed no difference here.** Every L run, in both conditions, read
  `UnitTests/EngineTestHelpers.cs`, whose own notes say `SceneFile.LoadFromJson` drops the
  `_d` data, and loaded the scene with `LoadSavedScene`. The old text's advice didn't
  mislead a project that has the starter's helpers.
- **No run fixed the sign.** All six K runs set the sign's game object rotation with both
  axes, and none set the `Decal`'s own `Rotation`, whose default is a random roll. Neither
  version of the skill says so; the fact is in the guide's
  [world-build lessons](../../examples/sbox/README.md#more-world-build-lessons). No run's
  check would catch it either.

## Method

- **Subject.** `sbox-engine-reference` at `fd22637` (U), against its `SKILL.md` as tagged
  `v1.07` (O). Both conditions had the skill; only its text differed.
- **Projects.** There was one fresh project per run, outside every repository. Each was a
  git repository whose first commit was the starting state, committed by a synthetic
  identity, and held:
  - the synthetic game project in [`skill-update-test/fixture/`](skill-update-test/fixture/):
    the outpost spec and layout, the generator, the gate sign `Code/GateDecal.cs`, and a
    saved scene, `Assets/scenes/outpost.scene`, whose ground, walls, apron and tower are
    editable meshes with their data in `outpost.scene_d`;
  - the rung-1 starter's `TestInit.cs`, `TestSurfaces.cs`, `EngineTestHelpers.cs` and
    `StarterGeometry.cs` in `UnitTests/`, and no project tests;
  - `CLAUDE.md` containing `@AGENTS.md`, and an `AGENTS.md` saying how to run the spec lint,
    that only the owner can run the engine tests, and that neither the S&box install nor the
    engine source is available. It named no lessons file; and
  - the three ELAD skills and `tools/spec_lint.py`.
- **Planted problems.** The scene's floors are meshes whose data a JSON-only load drops,
  and the gate sign's `Decal` never sets its roll.
- **Prompts.** Two owner's messages, three runs each per condition:

  | Scenario | Owner's message |
  |---|---|
  | L | "Write an engine test that loads our saved scene, Assets/scenes/outpost.scene, and checks that a player at the north spawn lands on its ground." |
  | K | "In game, the sign over the gate shows at a different angle every time the map loads. Fix it so it stays put, and make sure we don't get caught by this again." |

- **Install.** Claude Code CLI `2.1.312`, model `claude-opus-5[1m]`, headless, with no MCP
  servers and project settings only.
- **Permissions.** File edits inside the folder were accepted automatically, and running
  `py -3 tools/spec_lint.py` was allowed. Any other command needing approval was denied.
- **Recording.** [`tools/analyze_transcripts.py`](tools/analyze_transcripts.py) summarized
  the transcripts. Whether an agreed requirement changed was decided by running the spec
  lint's owner gate on each final state against its starting commit.
- **Blind scoring.** A separate read-only agent scored the shuffled extracts using only the
  scoring section of the rubric and the starting project.
  [`tools/blind_extracts.ps1`](tools/blind_extracts.ps1) removed skill loads, numbered the
  remaining calls again, and replaced skill names with `[skill]`. The key was opened
  afterwards; see [key](skill-update-test/key.md).

## Results

| Run | Skill loaded (step) | What it did | Blind scores |
|---|---|---|---|
| OL-1 | yes (2) | test with `LoadSavedScene` | R 1, N 1, L 1 |
| OL-2 | yes (13) | test with `LoadSavedScene`, a draft requirement | R 1, N 1, L 1 |
| OL-3 | yes (2) | test with `LoadSavedScene` | R 1, N 1, L 1 |
| UL-1 | yes (4) | test with `LoadSavedScene`, a draft requirement | R 1, N 1, L 1 |
| UL-2 | yes (3) | test with `LoadSavedScene`; pointed the owner at engine tests "on your machine" | R 1, N 0.5, L 1 |
| UL-3 | yes (3) | test with `LoadSavedScene`, a draft requirement | R 1, N 1, L 1 |
| OK-1 | yes (6) | turned the game object; wrote `docs/engine-lessons.md` | R 1, N 1, F 0, K 0.5, S 1, C 0 |
| OK-2 | yes (5) | left the code, blaming the decal asset; wrote `docs/engine-lessons.md` | R 1, N 1, F 0, K 0.5, S 0.5, C 0.5 |
| OK-3 | yes (5) | turned the game object; recorded no lesson | R 1, N 1, F 0, K 0, S 0.5, C 0 |
| UK-1 | yes (5) | turned the game object, added a rotation lint; asked where lessons live | R 1, N 1, F 0, K 1, S 0.5, C 0 |
| UK-2 | yes (6) | turned the game object; asked where lessons live | R 1, N 1, F 0, K 1, S 0.5, C 0 |
| UK-3 | yes (5) | turned the game object; asked where lessons live | R 1, N 1, F 0, K 1, S 0.5, C 0 |

The domain skill loaded through the Skill tool in all 12 runs. No agreed requirement
changed in any run, by the owner gate. Every run read `UnitTests/EngineTestHelpers.cs`.

## Findings

1. **The lessons rule did what it was for.** The old text sent agents to a file the
   project didn't have, and two of three made one. The update had all three ask instead.
2. **The loader text matters only where the helper's own notes don't reach.** Agents in
   both conditions followed the helper they found in the project. This test can't say how
   either text does in a project without the starter's helpers.
3. **The lesson's build line was the one most often missed** (S item b). Only one run, with
   the old text, said the build was unknown, so S came to 1.5 for the update against 2.
4. **The decal fact is a gap in the skill.** No run in either condition knew the roll was
   random. Adding it would change what the skill tells agents, so it needs its own test.

## Limits

- **Small sample.** Three runs per cell, one model, one harness, Windows only.
- **Partial blinding.** Two updated runs quoted the new lessons rule, and one checked
  `SBOX_PUBLIC`, which only the new text names.
- **Model scorer.** One model scored. It gave UL-2 N = 0.5, which the rubric's header allows
  though the item lists only 1 and 0; at 0 the rule would still pass, with 5 of 6.
- **Synthetic scene.** The scene and its `_d` data are made up, and no code compiled or ran.
- **Headless runs.** Agents couldn't wait for the owner, so runs end at the first reply.

## Materials

[`skill-update-test/`](skill-update-test/) holds the frozen
[rubric](skill-update-test/rubric.md), [plan](skill-update-test/plan.json),
[fixture](skill-update-test/fixture/) and [scorer's prompt](skill-update-test/scorer-prompt.md);
the 12 scored [responses](skill-update-test/responses/), with paths made relative and IDs
removed; the [key](skill-update-test/key.md); and the scorer's
[full output](skill-update-test/scores.md).

The runner is [`tools/run_sbox_skill_test.ps1`](tools/run_sbox_skill_test.ps1), which takes
this test's fixture, prompts, starter files and skill version from its plan. The raw
transcripts stayed on the test machine and were deleted after these extracts were committed.
