# Evidence-Led Agentic Development

**Use the cheapest reliable evidence that can justify the next action.**

Evidence-Led Agentic Development (ELAD) is a provider-neutral method and reference
protocol for AI-assisted software delivery. Its thesis is simple: development should be
driven by observable evidence and explicit authority, while process cost should scale
with the uncertainty, consequence, reversibility, and evaluator quality of the actual
claim. A deterministic typo fix, a semantic AI feature, and a consequential autonomous
change should not inherit the same ceremony.

This repository is a **Level 0 reference blueprint**. It contains guidance, inert
templates, draft schemas, synthetic examples, and dependency-free conformance checks.
It does not run a model, control another repository, accept evidence for a real project,
grant mutation authority, promote a candidate, or publish anything.

ELAD is for project owners, agent-harness builders, and engineers who want more autonomy
without treating model confidence as proof. It is not an agent framework, hosted service,
benchmark, safety certification, or replacement for target-owned tests and decisions.

## Start here

- Human adopter working with a coding agent: use the
  [short human-and-agent first-run walkthrough](docs/FIRST_RUN.md). Its procedural steps
  are for the agent; the human supplies intent, authority, and acceptance.
- Project owner: read [Start Here](START_HERE.md) and the
  [Adoption Runbook](docs/ADOPTION_RUNBOOK.md).
- Evaluator or researcher: read the candid [Empirical Status](docs/EMPIRICAL_STATUS.md)
  and [Conformance Contract](docs/PROTOCOL_030_CONFORMANCE.md).
- Protocol implementer: begin with [Architecture](docs/ARCHITECTURE.md),
  [Adaptive Rigor](docs/ADAPTIVE_RIGOR.md), and the [manifest](MANIFEST.md).

The current evidence is encouraging but bounded. ELAD's Level-0 conformance suite is
extensive, and four small portability observations informed version 0.3. ELAD has not
been demonstrated as a production controller, across arbitrary projects and platforms,
or by an established external adopter community.

## The idea in one picture

```text
What are we trying to learn or establish?
                 |
      What uncertainty matters most?
                 |
   What is the cheapest reliable evidence?
                 |
       build the smallest useful change
                 |
      observe outputs, behavior, and traces
                 |
          evaluate and analyze errors
                 |
       +---------+----------+
       |                    |
  change and repeat    enough evidence -> stop
```

Evaluation is part of development, not merely a certification step at the end. The
right evaluator can be an existing deterministic test, a runtime observation, trace
inspection, a calibrated model judge, adversarial review, human judgment, or a
proportionate combination. The process becomes more rigorous only when uncertainty,
coupling, reversibility, consequence, evaluator weakness, or delegation distance makes
that rigor useful.

## Three independent decisions

ELAD deliberately separates concepts that are often conflated:

1. **Project capability maturity** says what infrastructure and authority a project has
   actually proven.
2. **Task rigor** says how much evidence this particular step warrants.
3. **Effect authority** says what this particular episode may read or change.

A mature project can process a typo through a light path. A read-only security decision
may still deserve assured review. A high-rigor review does not grant write authority,
and a capable model does not inherit authority from its name. Scope and authority are
mandatory; ceremony is proportional. Unknown authority causes a stop, not inferred
permission.

## Four task-rigor profiles

| Profile | Use it when | Normal recurring path |
|---|---|---|
| `light` | Work is confined, reversible, low-consequence, and has a trustworthy existing deterministic check | outcome/scope -> change -> exact check -> inspect diff -> complete |
| `bounded` | There is moderate coupling, a new regression risk, integration work, or a cross-context handoff | compact brief -> targeted implementation -> focused checks -> concise result |
| `evaluated` | Product behavior is stochastic, semantic, experiential, runtime-dependent, or uses an immature fallible evaluator | contract/inspection/error-analysis base, plus only the semantic, runtime, evaluator-calibration, or stateful-recovery modules the claims and effects require |
| `assured` | The work is foundational, difficult to reverse, security/privacy sensitive, target-native, production-facing, or otherwise high-consequence | evaluated base plus independent expectations, bound identity, independent/adversarial verification, and only applicable claim/effect modules before separate activation |

Start with the least expensive profile justified by known facts. Escalate when evidence
reveals unexpected coupling, an unreliable evaluator, stochastic failures, irreversible
effects, or an unresolved human claim. Simplify when a mechanism repeatedly consumes
effort without changing decisions or catching realistic failures. See
[Adaptive Rigor](docs/ADAPTIVE_RIGOR.md).

A profile supplies a claim-neutral assurance base. The optional selector then adds the
closed modules required by declared claim classes, their per-claim evaluator maturity,
and task effect. A new exact regression with independently grounded expected behavior is
not an unproven fallible evaluator merely because it is new.
Runtime evidence is required for runtime/operational claims; rollback proof is required
for stateful reversible effects. Neither is implied by `evaluated` or `assured` alone.
Executing a program or reaching a service does not by itself make an exact claim
runtime/operational.
The applicability record is descriptive, grants no authority, and must be derived and
bound by orchestration from the accepted task contract rather than waived by a worker.

## Reusable infrastructure versus recurring work

ELAD keeps expensive safeguards when their cost can be amortized:

- schemas, path contracts, lifecycle rules, malicious vectors, and validators;
- evaluator calibration packs and known-good/known-bad fixtures;
- project policies, capability profiles, gate definitions, and authority boundaries;
- target adapters, serializers, runtime harnesses, and model+harness qualification
  evidence.

It does **not** require every task to reconstruct that apparatus. Full intent records,
retrieval manifests, packets, context-delivery records, evidence manifests, receipts,
review bundles, human receipts, continuation anchors, leases, and adversarial reviews are
conditional assurance modules. A stable calibrated evaluator can be cited and reused;
its entire negative suite is rerun when the evaluator or relevant environment changes,
not automatically for every feature that consumes it.

Running a cheap reusable validator in routine checks is not the same as making every
worker author a large task packet. ELAD optimizes recurring human and agent work first.

## Heterogeneous execution subjects and context protection

The orchestration protocol is model-neutral, but execution profiles are model-specific.
Capability belongs to an exact model, runtime, harness, adapter, prompt/context compiler,
tool schema, budget, and evaluated task class.

- A long-context orchestrator should shape work, choose workers, inspect compact receipts,
  and retain the project picture. It should delegate repetitive exploration,
  implementation, and test collection instead of ingesting hundreds of low-level calls.
- A constrained worker should receive one small precompiled objective, only the source
  slices and tools it needs, explicit budgets and stop states, and a supplied verifier.
  The same model in two harnesses is two qualification subjects. A coding harness and a
  product inference API are also separate subjects even with the same weights.
- A one-off supervised light task does not require a formal capability certificate.
  Repeated autonomous delegation, broader effects, or evidence authority does.
- Raw logs and traces stay file-backed. Orchestrators consume summaries and exact
  path/hash receipts unless diagnosis requires a selected slice.

## Authority and epistemic independence

For any mutating operation, effective authority is an intersection of the target
repository workflow, project policy, exact worker capability, allowed effects, tool
capability, and any required writer lease. Every component can narrow authority; none
can create it.

Correctness is also not self-certified. Proportional independence can come from:

- an existing expected result authored independently of the implementation;
- a separate fixture, rule predicate, holdout, or runtime observer;
- a calibrated semantic evaluator with known counterexamples;
- an independent agent or human when consequence warrants it.

Model confidence and self-review are useful signals, never proof by themselves. The
evaluators are evaluated too, but calibration is reusable and rerun on meaningful drift.

## Platform-neutral core and target-owned adapters

This repository does not assume a game engine, programming language, provider, harness,
test framework, database, or deployment platform. It defines common reasoning,
evidence, handoff, and authority patterns. Each adopting project owns its product rules,
artifact lanes, tests, narrow tool facades, runtime adapters, gates, evidence, and
promotion.

When an external system owns an opaque artifact, agents provide reviewed high-level
inputs to the authoritative serializer and verify its saved/reloaded result. They never
patch or reverse-engineer opaque bytes as an authoring shortcut. That rule applies to
game-engine assets, database-native state, proprietary design files, infrastructure
state, and similar target-owned formats.

## The assured handoff chain

The repository retains a strict optional protocol for autonomous, cross-context, or
high-consequence work. It can bind accepted intent, repository authority, policy,
project profile, exact worker qualification, minimal retrieval context, task packet,
resolved subject, evidence manifest, worker receipt, independent review, external human
receipt, and continuation anchor by identity and digest.

This chain exists to prevent stale evidence, confused-deputy authority, wrong-subject
validation, self-rooted continuation, and false completion. It is not the default format
for a trivial deterministic edit. The component contracts and focused semantic
validators are normative; the preserved integrated agentic-episode draft is not, because
no semantic composition validator yet proves the whole envelope.

## What the conformance suite means

The dependency-free Level 0 checks validate this repository's own reference artifacts.
They include structural validation, malicious path cases, context/authority containment,
protocol security, adoption semantics, adaptive-rigor selection, and a closed-world
receipt lifecycle domain.

The lifecycle domain has 44,100 possible field combinations and 33 admitted rows. The
large number is an exhaustive negative-space cross-product, not 44,100 separately
authored realistic scenarios. Its runtime is only a few milliseconds, so it is retained
as reusable foundational infrastructure. Version 0.3 compares the external transition
table with a separately implemented rule predicate across the full domain and tests
focused aggregate/integration cases. See
[Lifecycle Oracle Assessment](docs/LIFECYCLE_ORACLE_ASSESSMENT.md).

A green Level 0 result proves no live model, target, runtime, reviewer decision, or
cross-platform deployment. It grants no authority.

## Quick adoption

For a small project:

1. Pin an exact ELAD version or simply adopt the principles.
2. Write down the observable outcome, allowed scope, cheapest discriminating check,
   stop condition, and reversibility. An existing issue plus a test command may suffice.
3. Split mixed deterministic, semantic, and operational claims before choosing evidence.
4. Use `light` unless facts justify more.
5. Add only the reusable evaluators or policies the project repeatedly needs, and stop
   reading when another protocol layer would not change the decision.

For broader autonomous work:

1. inventory target authority, artifact lanes, human decisions, and existing evaluators;
2. establish a read-only baseline and measure whether the workflow reduces—not adds—
   effort;
3. add candidate isolation, model+harness qualification, target adapters, fencing, and
   strict receipts only as their triggering risks appear;
4. activate each effect through the target repository's own decision and evidence.

See the [first run](docs/FIRST_RUN.md), [Start Here](START_HERE.md), and the
[Adoption Runbook](docs/ADOPTION_RUNBOOK.md).

## Validate the repository

Python 3.10 or newer is required; no third-party packages are installed.

These commands are normally run by a coding agent or CI. A human adopter does not need to
execute them personally.

```text
python tools/validate_all.py
```

Windows users may also run `py -3 tools/validate_all.py`. The PowerShell wrapper remains
available at `tools/Test-Blueprint.ps1`. The final output must explicitly say that no
authority is granted. The hosted CI matrix becomes evidence only after every cell runs
green for the exact public commit.

## Provenance and licensing

The methodology is informed by Andrew Ng's public AI Engineering Skills Map articles;
their design translation and ELAD's independent synthesis are separated in
[Research Basis](docs/RESEARCH_BASIS.md). The source articles and images are not copied
here, and no endorsement is implied.

ELAD code and documentation are licensed under
[Apache-2.0](LICENSE). See [Licensing and Provenance](docs/LICENSING_AND_PROVENANCE.md)
and [NOTICE](NOTICE.md) for the publication and dependency boundary.
