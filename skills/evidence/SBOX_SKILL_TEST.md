# S&box Domain-Skill Test

> **Small experiment, acting sessions.** There were 18 real headless sessions, scored blind
> against a [rubric](sbox-skill-test/rubric.md) frozen in `7bdd0c6` before any run.

This was the first test of the example domain skill
[`sbox-engine-reference`](../../examples/sbox/skills/sbox-engine-reference/SKILL.md). It
asked whether the skill loads on its own during S&box coding work, and whether agents
follow what it teaches, compared with agents without it.

## Result in brief

**The skill passed its pre-registered decision rule.**

| Criterion | Needed | Got |
|---|---|---|
| 1. The skill loads, in each scenario | 2 of 3 | **3 of 3** in every scenario |
| 2. M = 1: fixes the enable order (F and W runs) | 4 of 6 | **6 of 6** |
| 2. D ≥ 0.5: handles the missing default surface | 6 of 9 | **8 of 9** |
| 2. G = 1: names `testhost.log` for engine errors | 6 of 9 | **8 of 9** |
| 2. E = 1: stuck check catches a body inside a mesh (T runs) | 2 of 3 | **3 of 3** |
| 3. Total of M, D, G, E and H, with the skill against without | higher | **21 against 2** |
| 4. Runs with R = 0, with the skill against without | no more | **0 against 0** |

- **Without the skill, no run found the planted cause** (0 of 6 F and W runs).
  - All three fall-through runs guessed that setting `Collision` before `Mesh` was the
    problem. One also lengthened the gate apron in the layout data and added a layout lint.
  - All three wall runs added a `BoxCollider` to every block. That gives collision, but in
    game the blocks would still build no model, so they would stay invisible.
- **With the skill, all six fixed the enable order.** Each created the component disabled,
  assigned the mesh, then enabled it.
- **No run in either condition wrote the default-surface scaffolding** (D = 1 in 0 of 18).
  With the skill, 8 of 9 runs named the gap, and 7 pointed to the spike kit's
  `TestSurfaces.cs`, which a project doesn't have. That supports the
  [rung-1 starter](../../ROADMAP.md#sbox-next-steps).
- **No agreed requirement changed in any run** (18 of 18, by the spec lint's owner gate).
  Eight runs added a new requirement, all as `draft`, and put it to the owner.

## Method

- **Subject.** `examples/sbox/skills/sbox-engine-reference` as released in v0.7, unchanged.
- **Projects.** There was one fresh project per run, outside every repository. Each project
  was a git repository whose first commit was the starting state, committed by a synthetic
  identity, and held:
  - the synthetic game project in [`sbox-skill-test/fixture/`](sbox-skill-test/fixture/):
    the outpost spec, a layout with a ground box and wall, apron and tower blocks, the
    generator `Code/OutpostGenerator.cs`, and `UnitTests/` with engine start-up and one
    smoke test;
  - `CLAUDE.md` containing `@AGENTS.md`, and an `AGENTS.md` saying how to run the spec lint,
    that only the owner can run the engine tests, and that neither the S&box install nor the
    engine source is available; and
  - the three ELAD skills as released in v0.7, and `tools/spec_lint.py`. The AGENTS.md
    snippet wasn't used.
- **Planted problems.** Both match what the skill teaches:
  - **The generator enables each `MeshComponent` before assigning its mesh.** In a game
    scene that builds no model, so the walls, the gate apron, and the tower have no
    collision. The ground is a box collider and works.
  - **Test setup loads no `default` physics surface,** so meshes can't build headlessly, and
    the error goes only to the engine's log.
- **Conditions.** S projects also had the domain skill in `.claude/skills/`; N projects
  didn't. Nothing else differed.
- **Prompts.** These were three owner's messages, three runs each per condition:

  | Scenario | Owner's message |
  |---|---|
  | F | "A tester says players fall through the floor near the gate." |
  | W | "The generated walls have no collision in game. Players walk straight through them." |
  | T | "Write the engine test for OUT-SPAWN-01." |

- **Install.** Claude Code CLI `2.1.237`, model `claude-opus-5[1m]`, headless, with no MCP
  servers. A smoke test in throwaway projects confirmed that S projects listed the domain
  skill, N projects didn't, and the lint was allowed.
- **Permissions.**
  - File edits inside the folder were accepted automatically.
  - Running `py -3 tools/spec_lint.py` was allowed.
  - Any other command needing approval was denied, so no session could compile, run tests,
    or commit.
- **Recording.**
  - The transcripts were summarized with
    [`tools/analyze_transcripts.py`](tools/analyze_transcripts.py). For this test it gained
    `--context` and `--new-files`, so the scorer saw new test files in full, and local paths
    are scrubbed from diffs.
  - Whether an agreed requirement changed was decided objectively, by running the spec
    lint's owner gate on each final state against its starting commit.
- **Blind scoring.**
  - A separate agent scored the shuffled extracts using only the scoring section of the
    rubric and the starting project.
  - [`tools/blind_extracts.ps1`](tools/blind_extracts.ps1) removed skill loads from the tool
    calls and replaced skill names with `[skill]`.
  - The key was opened afterwards; see [key](sbox-skill-test/key.md).

## Results

| Run | Domain skill loaded (step) | Diagnosis and change | Blind scores |
|---|---|---|---|
| SF-1 | yes (8) | enable order; fixed the generator, then wrote a test | R 1, D 0.5, G 1, M 1, X 0.5 |
| SF-2 | yes (2) | enable order; fixed the generator, then wrote a test | R 1, D 0.5, G 1, M 1, X 0.5 |
| SF-3 | yes (9) | enable order; wrote a test, then fixed the generator | R 1, D 0.5, G 1, M 1, X 1 |
| SW-1 | yes (1) | enable order; fixed it, added a test and a draft requirement | R 1, D 0.5, G 1, M 1 |
| SW-2 | yes (5) | enable order; fixed it, added a test and a draft requirement | R 1, D 0.5, G NA, M 1 |
| SW-3 | yes (7) | enable order; fixed it, added a test and a draft requirement | R 1, D 0.5, G 1, M 1 |
| ST-1 | yes (10) | wrote the spawn test; flagged the enable order and left it | R 1, D 0.5, G 1, E 1, H 0, C 1 |
| ST-2 | yes (9) | wrote the spawn test | R 1, D 0, G 1, E 1, H 0, C 1 |
| ST-3 | yes (11) | wrote the spawn test; flagged the enable order and left it | R 1, D 0.5, G 1, E 1, H 0, C 1 |
| NF-1 | no skill | guessed `Collision` before `Mesh`; wrote a test, left the code | R 1, D 0, G 0, M 0, X 1 |
| NF-2 | no skill | same guess; lengthened the apron, added a layout lint (and a line about it in `AGENTS.md`) and a draft requirement | R 1, D 0, G NA, M 0, X 0 |
| NF-3 | no skill | same guess; wrote a test and a draft requirement, left the code | R 1, D 0, G 0, M 0, X 1 |
| NW-1 | no skill | added a `BoxCollider` to every block, a test, and a draft requirement | R 1, D 0, G 0, M 0.5 |
| NW-2 | no skill | added a `BoxCollider` to every block, a test, and a draft requirement | R 1, D 0, G 0, M 0.5 |
| NW-3 | no skill | added a `BoxCollider` to every block, a test, and a draft requirement | R 1, D 0, G 0, M 0.5 |
| NT-1 | no skill | wrote the spawn test | R 1, D 0, G 0, E 0.5, H 0, C 1 |
| NT-2 | no skill | wrote the spawn test | R 1, D 0, G 0, E 0, H 0, C 1 |
| NT-3 | no skill | wrote the spawn test | R 1, D 0, G 0, E 0, H 0, C 0 |

The domain skill loaded through the Skill tool in all nine S runs, every time before the
run's first edit. No run read its `SKILL.md` directly.

**ELAD skill loads through the Skill tool:**

| Skill | S runs | N runs |
|---|---|---|
| `choosing-rigor` | 9 | 9 |
| `matching-evidence-to-claims` | 9 | 8, plus 1 direct read |
| `asking-the-owner` | 9 | 6, plus 2 direct reads |

## Findings

1. **The skill's facts transferred, and they mattered.**
   - **Enable order.** The rule turned a wrong guess or a workaround into the correct fix
     in every F and W run.
   - **Engine log.** `testhost.log` appeared in 8 of 9 runs, in the owner's instructions or
     in the tests' failure messages. It appeared in none without the skill.
   - **Stuck check.** All three spawn tests could catch a body inside a mesh block, against
     none without the skill. Two used the enclosure probe, and one swept down from above.
2. **The default surface is the gap.** Agents knew they needed one, but couldn't write it:
   the skill describes the problem and points to a file in the ELAD spike kit, not in the
   project. Several runs asked the owner for the file, or made their tests report
   "inconclusive" when the mesh didn't build. A copyable rung-1 starter would close this.
   The next step in the [roadmap](../../ROADMAP.md#sbox-next-steps) is to build it and rerun
   these scenarios.
3. **No spawn test simulated a player.** All six T runs checked spawns with traces instead
   of a `PlayerController`, so the skill's player guidance (H) was never used. Traces are a
   cheaper check of "lands on solid ground with room to stand", but they don't prove a
   player actually lands.
4. **Confidence changed the order of work.** ELAD scenario 3 expects reproducing at the
   engine rung before changing anything (X).
   - With the skill, two of three F runs fixed the generator before writing the test. Their
     cards still asked the owner to run the test on the old code first.
   - Without it, two of three left the code alone, but their diagnosis was wrong.
5. **The version check went unused.** No run compared the installed build with the source
   (V = N in all 18). This environment had neither, so this test can't say whether the rule
   works.
6. **Spawn-test runs with the skill noticed the planted bug.** Two of three flagged the
   generator's enable order as a likely cause of missing collision, and left it to the
   owner as outside the request. No run without the skill noticed it.

**No change to the skill is needed under the decision rule.** Two candidates for later, not
applied:

- point the default-surface rule at the rung-1 starter once it exists; and
- if spawn checks should prove landing, say when to simulate a player rather than trace.

Either would change what the skill tells agents, so each needs its own pressure test.

## Limits

- **Small sample.** Three runs per cell, one model, one harness, Windows only.
- **Planted problems match the skill.** This tests whether the skill's facts transfer to
  agents, not whether its facts are complete. A project's real bugs won't line up this well.
- **No engine source or install.** In a real project the skill sends agents to a local
  engine clone, and agents without the skill could read it too. The baseline here is weaker
  than in a real project.
- **No code compiled or ran.** The scorer judged the code by reading it. Whether the tests
  pass on a real machine is untested.
- **Partial blinding.**
  - Several replies named the spike kit or `TestSurfaces.cs`, which reveals the skill.
  - One run's lint output listed four skill folders.
- **Model scorer.** One model scored. It counted control cases written only in an owner card
  (C), which doesn't affect the decision rule.
- **Headless runs.** Agents couldn't wait for the owner, so runs end at the first reply.

## Materials

[`sbox-skill-test/`](sbox-skill-test/) holds:

- the frozen [rubric](sbox-skill-test/rubric.md), [plan](sbox-skill-test/plan.json), and
  [fixture](sbox-skill-test/fixture/);
- the 18 scored [responses](sbox-skill-test/responses/), with paths made relative and IDs
  removed;
- the [key](sbox-skill-test/key.md);
- the [scorer's prompt](sbox-skill-test/scorer-prompt.md); and
- its [full output](sbox-skill-test/scores.md).

The runner is [`tools/run_sbox_skill_test.ps1`](tools/run_sbox_skill_test.ps1). The raw
transcripts stayed on the test machine and were deleted after these extracts were committed.
