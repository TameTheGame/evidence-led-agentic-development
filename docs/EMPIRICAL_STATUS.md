# Empirical Status

ELAD v0.10 rests on five kinds of evidence:

- two blind pressure-test rounds of its skills, in dry runs;
- a triggering test and an engagement test of the skills in real headless sessions;
- three S&box tests in real headless sessions: one of the example's domain skill, then a
  live retest and a refactor rerun in compiled S&box projects;
- one engine-rung spike in a real game engine; and
- four earlier development experiments against v0.3.0.

Together they support core parts of the method in bounded settings. ELAD has not yet been
used on a real project, or demonstrated as a production automation system. This document
separates those claims.

## Skills in real headless sessions (v0.7)

Headless Claude Code sessions (CLI `2.1.237`, `claude-opus-5`) each started in a fresh
synthetic project with the skills installed. Nothing told the agent about the skills.

- **[Triggering test](../skills/evidence/TRIGGERING_TEST.md).** With the v0.6 skills, they
  were used in every working run, but loaded through the skill mechanism in only 4 of 6.
  `choosing-rigor` never loaded on the one-shot probe. All three east-spawn runs edited an
  agreed requirement before asking the owner.
- **[Engagement test](../skills/evidence/ENGAGE_TEST.md).** This tested the v0.7
  configuration: two description edits, one red flag, an optional snippet, and an example
  spec lint. All runs were acting sessions, scored blind against frozen rules.
  - **The original rule and its one correction cycle failed,** on a typo control that got
    wordier with the snippet.
  - **The release configuration then passed its own pre-registered check:** the edited
    skills with the lint, and no snippet.
    - The east spawn left agreed requirements to the owner in 3 of 3 runs.
    - The probe pushed back in 2 of 3.
    - The control stayed light in 3 of 3.
  - **Across every engagement run, no agreed requirement was changed without the owner.**

**Limits:**

- three runs per cell;
- one model and one harness, on Windows only;
- a synthetic fixture;
- a model scorer with partial blinding;
- runs end at the first reply; and
- the lint's owner gate was never triggered in a live session.

## The S&box domain skill (v0.8)

The [domain-skill test](../skills/evidence/SBOX_SKILL_TEST.md) gave headless sessions a
synthetic S&box game project with two planted engine problems. Half the runs had the
example `sbox-engine-reference` skill. It passed its pre-registered, blind-scored rule.

- It loaded on its own in 9 of 9 runs.
- With it, agents fixed the planted enable-order bug in 6 of 6 runs. Without it, none did:
  they guessed another cause or added a collider workaround.
- With it, 8 of 9 runs named the missing default physics surface, but none could write the
  test scaffolding for it.

**Limits:**

- three runs per cell;
- one model, on Windows only;
- the planted problems match the skill's content;
- no engine source or install was available, and no code was compiled; and
- partial blinding.

## The S&box live retest (v0.8)

The [live retest](../skills/evidence/LIVE_TEST.md) reran those scenarios in 24 sessions in
compiled S&box projects with the
[rung-1 starter](../examples/sbox/rung1-starter/README.md). Agents could run the engine
tests, and reference probes checked each final state on the engine.

- Every geometry test ran with a default surface (18 of 18, against 0 of 18 before).
- In 11 of 12 fall-through and wall runs, a test failed on the engine before the fix and
  passed after.
- The planted bug was fixed in 12 of 12 of those runs, with or without the domain skill.
  The starter's own code shows the enable-order rule, and agents without the skill found it
  there.
- It failed its pre-registered rule on one criterion: in the refactor scenario, agents
  asked which refactor was meant, because the project had only one area.

**Limits:**

- three runs per cell, one model, Windows only;
- the condition without the domain skill still had the starter's S&box knowledge;
- no engine source clone was available; and
- a model scorer.

## The S&box refactor rerun (v0.8)

The [refactor rerun](../skills/evidence/REFACTOR_TEST.md) tested the refactor scenario alone,
in 6 sessions. The project's two areas share the generator, and the request named the
change.

- All 6 runs moved the code, then ran every shared check, which passed. Reference probes
  confirmed the build in 6 of 6.
- No run ran the shared checks before the change, so it failed its pre-registered rule.
  Agents rated the move light, and at light `choosing-rigor` doesn't ask for a baseline.
- With and without the domain skill, runs scored the same.

**Limits:** three runs per condition, one model, Windows only, a model scorer, and no run
met a failing check, which is when a baseline would matter.

## Pressure tests of the skills (v0.6)

Fresh agents received owner requests about a synthetic map project. They worked with the
three skills, with no skills, and in round 1 with an unmodified Superpowers library.
Responses were dry runs. They were scored blind by a separate model, against a rubric
frozen before any response was read.

- **Round 1** had one sample per cell across four scenarios. With the skills, agents
  recommended changing a risky "one try, then stop forever" rule. The other conditions
  didn't.
- **Round 2** had three samples per cell, on two scenarios.
  - **The stop rule:** with the skills, agents recommended a better rule in 2 of 3 runs,
    against 0 of 3 without them, and ran cheaper checks first in 3 of 3 runs, against 0
    of 3.
  - **The east spawn:** the skills scored 7.0 against 5.8 out of 7.

Results, rubrics, responses, and keys are in
[`skills/evidence/`](../skills/evidence/PRESSURE_TEST_RESULTS.md).

**Limits:**

- small samples;
- plans rather than actions;
- one model for the agents and the scorer;
- partial blinding; and
- skills loaded by instruction. Automatic triggering was tested later, in the headless
  sessions above.

## Engine-rung spike (v0.6)

A runnable kit checked whether a project's own tests can run rung-1 checks headlessly in
S&box (Facepunch, Source 2). Seven runs on build `26.10.02` proved collision, traces,
spawn landing, and stuck detection against generated geometry, plus loading a simple saved
scene. Two caveats come with that result:

- the default physics surface needed test-only scaffolding; and
- stuck detection needed a probe for concave mesh collision.

See the [S&box example](../examples/sbox/README.md).

**Limits:**

- one engine build, on Windows only;
- synthetic geometry; and
- saved scenes that reference prefabs or collision models are untested.

## Protocol conformance through v0.5 (archived)

Through v0.5, a dependency-free Level-0 suite checked the repository's protocol
artifacts. Those artifacts and the suite are archived at the `v0.5` tag
([Archive](../ARCHIVE.md)). At the 0.3.0 release boundary it included:

- structural and semantic checks over 29 schema/template pairs;
- a portable path corpus with malicious and reserved-name cases;
- context, authority, subject, evidence, resource, adoption, and task-rigor vectors;
- a closed-world receipt lifecycle over all 44,100 tuples, with 33 admitted rows;
- differential comparison between an external admission table and a separately expressed
  predicate;
- an independently anchored exact-byte synthetic continuation chain; and
- an explicit authenticated normative-artifact inventory.

A green run establishes conformance of those inert artifacts and synthetic cases. It does
not establish a live model, target adapter, runtime, operating-system matrix, human
decision, project outcome, or safety property outside the checked contracts.

Version 0.4 rebinds the active normative inventory and validators to exact 0.4 identities
and adds focused integrity checks for the proportional-review policy. It adds no new
reference-project experiment and does not upgrade the empirical claims below; those
observations remain historical results against their frozen 0.3.0 baseline.

Version 0.5 releases the Direct/Conserve guidance, advances active identities to `0.5`,
and validates release metadata and version-tag matching. It adds no new model comparison
or reference-project experiment; neither the mode guidance nor release automation expands
the empirical or operational claims below.

## Empirical reference-project results

A separate Python repository-inventory CLI was used for four bounded experiments
against a frozen ELAD 0.3.0 baseline:

| Experiment | Result | What it supported |
|---|---|---|
| Deterministic single-agent development | A confined CLI slice completed with 34 deterministic tests | The lightweight path could guide ordinary software work without requiring the full assured packet chain |
| Cold adoption | A fresh adopter found the light path but encountered onboarding ambiguity | Progressive disclosure needed improvement while authority remained non-skippable |
| Deterministic heterogeneous delegation | A bounded worker implemented a parser slice; the integrated suite reached 59 deterministic tests | A compact worker packet and frozen orchestrator-owned checks were sufficient for that low-risk delegation |
| Semantic product evaluation | The suite reached 72 deterministic tests; an eight-case semantic set found a conflicting-signal defect at 7/8, and one causal prompt correction reached 8/8 | Evaluated rigor produced information that deterministic tests could not, while neighboring exact claims stayed deterministic |

Those experiments motivated the per-claim evaluator-maturity correction, the compact
bounded-worker packet, clearer execution-subject identity, and the separation of coding
agents from stochastic product behavior.

## Important limits on the reference-project evidence

- All four experiments came from one small CLI product family over a short period.
- The work was not a randomized study and did not compare ELAD with a controlled
  alternative methodology.
- The experiment corpus and raw harness records are not distributed in this public source
  tree, so the portability results are not independently reproducible from this repository.
- The semantic result used a small designed case set. Reaching 8/8 does not establish
  broad summary quality, production reliability, or model generality.
- No external maintainer, user community, or independent organization has reported
  sustained adoption.
- No runtime component, live authority service, or target adapter exists here. None is
  planned for the core.
- No production workload, consequential autonomous mutation, target-runtime
  cross-platform matrix, or long-term efficacy study has passed.

These are evidence gaps, not failed claims. They must remain unclaimed until corresponding
evidence exists.

## Claims ELAD does not currently make

ELAD does not claim to be:

- a proven production controller;
- a general safety certification for coding agents;
- validated across arbitrary providers, models, harnesses, languages, or platforms;
- more efficient than other methods in aggregate;
- adopted by an established ecosystem; or
- sufficient by itself to authorize effects in another repository.

`1.0` has two conditions in [Releasing](RELEASING.md):

- **Automatic skill triggering tested in a real install.** This has now been tested in real
  headless installs, within the limits above.
- **Use on one real project,** recorded with synthetic lessons. This is still open, and it
  is the next meaningful empirical step.

More documents or machinery would not count.
