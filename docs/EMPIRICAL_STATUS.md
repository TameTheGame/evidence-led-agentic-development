# Empirical Status

ELAD v0.6 rests on three kinds of evidence:

- two blind pressure-test rounds of its skills;
- one engine-rung spike in a real game engine; and
- four earlier development experiments against v0.3.0.

Together they support core parts of the method in bounded settings. ELAD has not yet been
used on a real project at v0.6 or demonstrated as a production automation system. This
document separates those claims.

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
- skills loaded by instruction, so automatic triggering is untested.

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

## Separate harness-readiness companion evidence

The public
[ELAD Harness Readiness Suite](https://github.com/TameTheGame/elad-harness-readiness-suite)
is a separately maintained operational companion for applying ELAD's qualification logic
to exact local coding-model and harness subjects. Release
[`v0.1.0`](https://github.com/TameTheGame/elad-harness-readiness-suite/releases/tag/v0.1.0)
contains a dependency-free synthetic demo, 35 deterministic framework checks, and a
six-cell hosted Windows/macOS/Ubuntu matrix on Python 3.10 and 3.13.

Its design was extracted from a separate owner-local comparison of four harness subjects
on one exact local coding model. That origin case contained 24 controlled-parity runs and
140 production-realism products, with blinded semantic review and separate
handoff/long-session checks. The raw corpus and private machine evidence are not
distributed, so those origin results remain bounded and are not independently
reproducible. The public synthetic suite makes the testing logic reproducible; it does
not reproduce or certify the original winner.

Publishing the companion adds neither a live adapter nor execution authority to this
repository. It does not establish universal model/harness rank, arbitrary-project
generality, OS isolation, restricted-data safety, or production readiness.

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

The next meaningful empirical steps are the two conditions for `1.0` in
[Releasing](RELEASING.md):

- a test of automatic skill triggering in a real install; and
- use of ELAD on one real project, recorded with synthetic lessons.

More documents or machinery would not count.
