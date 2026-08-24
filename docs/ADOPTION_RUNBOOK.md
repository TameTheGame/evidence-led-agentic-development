# Adoption Runbook

## Goal

Adopt the smallest ELAD layer that materially improves a project's delivery. The method
is progressive: a project can begin with one page and existing tests, then add reusable
assurance infrastructure only when repeated work or consequential effects justify it.

Project maturity, task rigor, and effect authority are separate. Adopting sophisticated
infrastructure does not force every task through it, and selecting an assured review
does not grant mutation authority.

> Scope and authority are mandatory; ceremony is proportional.

An adopter begins by locating actual owner authority. If it is unknown or contradictory,
stop and ask the owner; ELAD never supplies the missing permission. After the task's
claim, uncertainty, and rigor are clear, stop reading when a deeper protocol layer would
not change the decision.

## Phase 0 — Decide whether ELAD helps

A lightweight adoption is useful almost anywhere. The formal protocol becomes valuable
when the project has one or more of these conditions:

- cloud and local models with different context, tool, privacy, or resource limits;
- repeated autonomous delegation or expensive cross-context handoffs;
- runtime, native-artifact, data, security, or human-acceptance boundaries;
- multiple repositories or scarce mutation surfaces;
- evidence that must bind to an exact candidate or runtime subject;
- recurring evaluator false-green risk;
- a need to reduce human operation without delegating product judgment.

Do not add formal machinery merely to make a small project look mature.

## Phase 1 — Establish the light path

For a confined, reversible, low-consequence task with a trustworthy deterministic check,
the entire recurring contract may be:

```text
observable outcome and allowed scope
  -> implementation
  -> named deterministic check and expected result
  -> diff inspection
  -> completion or escalation
```

An existing issue or prompt plus a test command can satisfy this. Use the optional
`templates/LIGHT_TASK.template.md` only when a small written artifact improves the
handoff. Do not require JSON records, capability certificates, manifests, independent
agents, or human acceptance when they add no discriminating evidence.

## Phase 2 — Inventory the target and freeze a baseline

Before broader autonomy, inspect the target read-only:

- product and repository authority;
- branches, worktrees, finalization, promotion, and publication rules;
- source, generated, native, data, evidence, secret, and deployment zones;
- existing tests, runtime probes, observability, and known false-green cases;
- project/risk/data classes and retained human decisions;
- exact target serializers or executors;
- cloud/local model privacy, context, tool, latency, cost, and resource constraints;
- current human operations, orchestration context cost, failure rate, and delivery time.

Record enough of the current workflow to tell whether adoption improves it. Unknown
values remain unknown; do not invent precision.

If the project will consume a formal ELAD release, pin its exact version, commit, and
protocol-bundle digest. Never give a floating sibling checkout authority over a product.

## Phase 3 — Select task rigor

For each material step, answer the seven questions in
[ADAPTIVE_RIGOR.md](ADAPTIVE_RIGOR.md) and choose:

- `light` for exact, low-consequence, reversible work with an existing oracle;
- `bounded` for moderate coupling, regression risk, or a cross-context handoff;
- `evaluated` for stochastic, semantic, experiential, runtime-dependent, or otherwise
  behaviorally uncertain product claims;
- `assured` for foundational, security/privacy-sensitive, irreversible, target-native,
  production, promotion, or other high-consequence work.

Start at the cheapest supported profile. Escalate when evidence exposes greater
uncertainty; simplify when a mechanism repeatedly has no decision value.

Rigor follows the claim, not the mechanics around it. Executing a CLI or calling a local
inference endpoint does not automatically make an exact schema, exit-code, fixture, or
failure-isolation claim operational. Likewise, an AI coding worker can implement
deterministic code without making the product claim stochastic.

## Phase 4 — Reuse and calibrate evaluators

Inventory existing compilers, linters, tests, fixtures, runtime probes, traces, and human
acceptance methods before building anything new.

Classify evaluator maturity per claim. A new exact regression with independently defined
expected behavior is `exact_deterministic` and does not require a semantic calibration
suite. A fallible rubric or model judge is calibrated for the semantic claim it scores;
that calibration does not spread to neighboring deterministic claims.

For a reusable evaluator, record:

- exact evaluator/tool/schema/environment identity;
- supported claim classes;
- representative known-good and known-bad cases;
- stale/wrong-subject, empty-discovery, skip, crash, and timeout behavior as applicable;
- false-positive/false-negative or variance limits where measurable;
- invalidation triggers.

Routine tasks cite the current calibration and run focused task cases. Rerun the affected
calibration slice when the evaluator or relevant environment changes, or when the task
introduces a new failure mode whose false green would matter.

## Phase 5 — Add a minimum owner-local overlay

Only create files that the target actually needs. A small overlay might be:

```text
AGENTS.md
STATUS.md
WORKFLOW.md
```

A project moving toward formal autonomous handoffs may additionally need:

```text
automation/
  core.lock.json
  active-authority.json
  profiles/
  policies/
  registries/
  gates/
```

The target owns these artifacts. A shared risk or data policy may narrow multiple
repositories, but each repository owns its own authority, evidence acceptance, adapters,
gates, and promotion. Templates are optional starting points, not mandatory paperwork.

## Phase 6 — Add bounded candidate delivery

When work crosses contexts or needs isolation:

1. compile a compact human-facing brief;
2. inherit stable repository/profile/policy defaults automatically;
3. generate any full normalized packet deterministically;
4. give the worker one outcome, selected context, allowed tools/effects, budgets, and
   stop states;
5. keep candidate work separate from target/promotion state;
6. return a concise result plus exact evidence references;
7. verify only the claims and evidence layers selected by task rigor.

A human or agent should not spend more time manually populating a packet than doing the
work. Use `templates/BOUNDED_WORKER_PACKET.template.md` for an ordinary bounded handoff.
Full JSON records are generated assurance artifacts for workflows that actually need
them.

## Phase 7 — Qualify repeated model and harness routes

Formal qualification is for repeated autonomous delegation, broader effects, or machine
evidence authority—not every supervised light edit.

For each exact model/runtime/harness/adapter combination:

1. define candidate task classes, context/tool/resource budgets, and prohibited effects;
2. run representative positives, proportionate negatives, inaccessible holdouts, and
   cold repeats where variance matters;
3. measure reliable context and sequential tool horizon, not advertised capacity;
4. begin shadow/read-only, then canary/candidate-only;
5. record expiry and invalidation triggers.

A local model in worker harness A and the same model in worker harness B are separate
subjects. A coding-agent
harness and a product inference API are also separate subjects even when both load the
same weights. Qualification includes exact model artifact/build or quantization,
runtime/backend, harness/adapter, tool surface, prompt/context compiler, configured
resource envelope, and task class. A cloud
orchestrator should delegate repetitive tool traces rather than absorb them into its
long-horizon context.

## Phase 8 — Add target-owned operations only when needed

The target implements narrow logical tools for its own artifact and runtime surfaces. A
neutral controller may validate and dispatch an admitted high-level plan; it does not
become an arbitrary filesystem, console, process, package, deployment, or native-format
mutator.

For opaque artifacts:

```text
reviewable input -> authoritative serializer -> save/reload
  -> logical identity and complete-resource verification -> idempotent reapply
```

## Phase 9 — Fence scarce or overlapping effects

Lease/fencing infrastructure is justified for overlapping writers, target-native state,
runtime persistence, data stores, promotion, or stale-completion risk. It is not required
for a read-only check or a single isolated light edit.

Before activation, test contention, atomic acquisition, monotonic fencing, stale/replayed
completion, disconnect after target completion, process loss, uncertain ownership,
expiry/reconciliation, and exact cleanup.

## Phase 10 — Prove one proportionate golden path

Run a production-shaped example at the highest effect level being adopted. Use full
assured packets, independent verification, recovery, and malicious cases only if that
level's consequences justify them. Preserve compact continuation and retain human
judgment where objective evaluators cannot prove the claim.

Activation, candidate finalization, promotion, and publication remain separate
owner-local decisions.

## Gate-admission rule

Create a durable gate only for:

- a reusable capability;
- an evaluator or harness qualification;
- a high-consequence policy or authority transition;
- a cross-surface adoption boundary; or
- a difficult-to-reverse platform decision.

Ordinary features close through their task evidence. Do not create a permanent gate for
every implementation. Reuse a passed gate receipt until an explicit invalidation trigger
applies.

## Measure and simplify

Compare the candidate workflow with its baseline:

- human operations and review time;
- orchestrator context/tool consumption;
- successful evidence-backed closure;
- retries, escalations, and false greens;
- latency, cost, and local resource use;
- security, privacy, scope, or target-integrity events.

Advance only when the relevant guardrails hold and the workflow materially improves
delivery. Hold when evidence is missing. Roll back for authority, security, privacy,
false-green, or target-integrity failures. Simplify when recurring scaffolding costs more
than the uncertainty it resolves.
