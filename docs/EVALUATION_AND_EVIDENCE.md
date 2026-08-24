# Evaluation and Evidence

## Evaluation drives development

Evaluation begins with a learning question, not a demand for maximum test volume:

1. What behavior or fact must this step establish?
2. Which uncertainty could change the implementation decision?
3. What is the cheapest evaluator that can reliably discriminate it?
4. What did the outputs, behavior, or traces reveal?
5. Which error class should change the next build?
6. Is the evidence sufficient to stop?

An existing deterministic test may be the complete evaluator for a light task. A
behaviorally uncertain feature may need examples, traces, a frozen eval sample, semantic
judgment, and several build/evaluate/error-analysis iterations. A foundational component
may justify independent oracles, malicious cases, recovery, and adversarial review.

## Match evidence to the claim

Projects define their own evidence layers. A common ladder is:

1. schema/static/deterministic;
2. pure unit;
3. framework/runtime unit;
4. service/headless/integration;
5. local client/rendered;
6. multi-process or same-machine network;
7. real remote;
8. clean/cache-isolated/deployment;
9. external human acceptance.

These layers are not synonyms and are not automatically cumulative. A screenshot cannot
prove authorization or collision; a headless server cannot prove UI quality; a warm
cache cannot prove clean delivery. Select the cheapest layer that actually resolves the
claim.

For `light` and many `bounded` tasks, a concise expected result is enough. Typed claim
IDs, subject selectors, evidence manifests, and lifecycle receipts become useful when
work crosses contexts, multiple evidence sources must reconcile, the subject could be
confused, or closure has material consequences.

The optional task-rigor selector separates a claim-neutral profile base from closed
per-claim/effect modules. A static/deterministic claim requires a deterministic check; a
semantic/stochastic claim requires a baseline/eval set and evaluator check; a
runtime/operational claim requires runtime or trace evidence. Stateful reversible effects
require rollback proof, while read-only work and irreversible effects do not invent one.
Evaluator maturity is classified per claim. Immaturity adds calibration evidence only
to the fallibly evaluated claim without automatically adding runtime evidence or
semantic machinery to neighboring exact checks. A new exact regression with
independently grounded expected values is not an unproven fallible evaluator merely
because it is new. The coarse applicability record does not replace exact assured claim IDs,
subjects, effects, acceptance owners, or target evidence policy.

Executing a program does not by itself make a claim runtime/operational. Exact CLI
stdout, exit status, JSON shape, fixture comparison, or mocked service-failure isolation
can remain deterministic. Reserve the runtime domain for claims whose truth materially
depends on live state, timing, traces, distributed behavior, persistence, native effects,
or another operational property exact comparison cannot establish.

For mixed work, write the split down before implementation. For example:

| Claim | Domain | Cheapest reliable evidence |
|---|---|---|
| opt-in flag, schema, bounded input, failure isolation | static/deterministic | exact unit/integration checks against independent fixtures |
| purpose, grounding, uncertainty handling, usefulness | semantic/stochastic | small frozen cases, rubric, calibrated judge, and sampled outputs |

The task may select `evaluated` because of its semantic claim while its exact tests stay
ordinary deterministic evidence.

## Preserve epistemic independence proportionally

Implementation logic should not generate both the behavior and its expected answer.
Suitable independent expectations include:

- a pre-existing specification or exact test;
- a separately authored fixture, truth table, rule predicate, or test oracle;
- a runtime observer outside the changed component;
- worker-inaccessible holdouts;
- a calibrated semantic evaluator;
- an independent agent or external human.

The same worker may run a trustworthy existing deterministic test. Require stronger role
separation when the evaluator is new, stochastic, implementation-derived, or vulnerable
to a consequential false green. Model confidence and self-review can guide diagnosis but
cannot establish correctness alone.

## Evaluate the evaluators

Evaluator calibration is reusable infrastructure. Calibrate against the failure modes
that matter for its claim class:

- representative known-green and known-bad cases;
- wrong or stale subject;
- zero test discovery and silent skip;
- missing evidence, partial output, crash, and timeout;
- adversarial cases;
- repeated cold runs for stochastic evaluators;
- worker-inaccessible holdouts where leakage is plausible;
- expected false-positive/false-negative or variance ceilings.

Store the evaluator identity, supported claim classes, calibration receipt, and
invalidation triggers. A routine task can cite that receipt and run focused positive
cases. Rerun the affected calibration slice when evaluator code, schema, tool, adapter,
engine/runtime, model judge, policy, or relevant environment changes—or when a new
high-consequence failure mode appears.

A task-specific negative is required when the task changes the evaluator, creates a new
failure class, or would make a false green materially harmful. It is not universal
paperwork.

Generator sampling and evaluator sampling answer different questions. Use a small,
proportionate number of product-output draws to expose obvious instability; this is not a
default demand for Monte Carlo testing. Separately repeat a stochastic evaluator when
measuring judge variance. Bind both to the exact subject, including material generation
settings such as temperature, thinking mode, and output-token limit.

## Runtime, trace, model, and human evidence

- **Runtime evidence** is authoritative for behavior that static inspection cannot prove.
  Bind it to the exact executable, configuration, data root, candidate, and environment
  needed by the claim.
- **Trace inspection** helps identify the first causal error and should remain
  file-backed. Put selected causal slices—not complete logs—into orchestration context.
- **LLM-based evaluation** is appropriate for a narrow semantic class after calibration.
  It must expose uncertainty and cannot establish authority, security, privacy,
  persistence, rights, exact runtime identity, promotion, publication, or final product
  taste by confidence alone.
- **An LLM judge is model evidence, not external-human acceptance.** It cannot produce
  a human receipt or close a claim whose accepted owner is an external human.
- **Human judgment** remains appropriate for product meaning, subjective experience,
  trust, consequential tradeoffs, rights, and real-world conditions that automation
  cannot reliably observe. Ask only after objective prerequisites are green and present a
  small stable card.

When a predeclared numeric threshold passes but a designed discriminator still exposes a
classified correctness defect, prefer one cheap causal change and one focused rerun over
both immediate victory and unlimited score chasing. Then stop when the claim is supported.

## Assured claim and evidence contracts

When the `assured` profile is selected, a task packet can list each claim with:

- stable claim ID and class;
- pre-run subject selector;
- machine or external-human acceptance owner;
- evidence class and evaluator;
- required evidence roles;
- pass/fail/inconclusive states;
- any task-specific negative or reusable calibration reference.

A receipt resolves every claim to one exact repository/candidate/base/content subject.
Supporting evidence repeats that subject. A green aggregate cannot hide an open human
claim or silently validate a neighboring artifact.

Passing evaluator output and accepting it as closure remain separate acts. Machine
closure requires target-repository authority and an applicable evidence-policy rule.
Human closure requires an eligible external reviewer and the exact sealed review bundle
they inspected. A worker cannot manufacture its own external-human acceptance.

## Evidence storage and context

- Keep raw evidence outside routine model context.
- Preserve enough bytes and identity to reproduce the conclusion, not every irrelevant
  trace.
- Redact secrets and private data before broader routing.
- Use exact path/hash manifests when evidence crosses contexts, must survive
  interruption, or supports consequential closure.
- For a one-context light task, the test result and inspected diff may be enough; do not
  create manifests solely to satisfy form.

## Closed-world assured receipt outcomes

The optional assured receipt protocol cross-checks terminal status, finalization state
and ceiling, candidate state, aggregate claim state, evidence-manifest state, and next
action. The external table lists 33 admitted tuples in a 44,100-value domain; every
unlisted tuple fails closed.

Version 0.3 also implements the lifecycle decision as a separately expressed rule
predicate and compares that predicate with the external table over the complete domain.
Focused vectors exercise aggregate derivation, representative admitted shapes, and
single-field denial mutations. This makes the table an independent conformance oracle
for the implementation rather than the implementation's own lookup presented as proof.

The full lifecycle is inexpensive reusable infrastructure, but it applies only when a
task produces a formal worker receipt. A light deterministic task does not need a
seven-dimensional receipt merely because the validator exists.
