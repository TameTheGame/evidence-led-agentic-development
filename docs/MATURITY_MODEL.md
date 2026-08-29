# Maturity Model

Maturity describes the highest operational capability a project has actually proven. It
is not a checklist, a score, or a reason to give every task more process.

A mature project can still use a `light` path for a confined edit. A young project can
use `assured` review for a high-consequence read-only decision without gaining any write
authority. Advance only when the next capability is useful and its required proof exists.

## Level 0 — Use the method

The project uses ELAD's evidence loop, adaptive rigor, and owner-defined authority with
ordinary documentation and tests. It may also use inert templates and synthetic examples.

This is a valid stopping point. Formal machine contracts are optional.

This ELAD reference repository is Level 0: its validator proves internal schemas,
templates, synthetic fixtures, path rules, lifecycle behavior, and default-deny state. It
does not run a model or prove a real target, runtime, reviewer, or platform integration.

## Level 1 — Contract read-only work

The project can create identity-bound manifests, read-only packets and receipts, gate
calculations, and compact continuation records without changing the target.

Use this level when read-only work needs auditable cross-context identity, replay refusal,
budget checks, or calibrated evaluators. It does not replace the light path.

## Level 2 — Isolate candidate changes

The project can write and verify an isolated candidate without mutating the target or
promoting the result.

Proof covers base and worktree identity, path confinement, preservation of unrelated
work, candidate identity, relevant evaluation, compact handoff, and candidate-only
finalization. A formal receipt is needed only when the task's rigor requires one.

## Level 3 — Route repeated autonomous work

Exact model-and-harness profiles can receive the task classes and effects they have
empirically demonstrated.

Proof uses representative successes, proportionate failure and held-out cases, measured
usable context and tool horizon, evaluator calibration, known limits, resource
observations, and expiry or drift rules. Store this qualification and reuse it until an
invalidation trigger fires.

## Level 4 — Execute fenced target operations

The project can run narrow target-owned mutation or runtime plans on proven surfaces.

Proof covers exact target identity, ownership where overlap matters, stale and replayed
completion, crash or disconnect recovery, cleanup, and target-specific serializer or
runtime evidence. Do not add leases to read-only or isolated work that has no scarce
surface.

## Level 5 — Deliver an operational path

The project has proven an owner-local, production-shaped path from intent through
candidate delivery and separately authorized promotion.

Proof includes compact continuation, appropriate independent verification, target-owner
activation, focused owner acceptance where needed, rollback, and separation between
candidate completion, promotion, and publication.

## Level 6 — Maintain several projects through drift

Several projects share a versioned neutral protocol while retaining their own authority,
routing, evaluators, adapters, and qualification records.

Proof includes compatibility releases, focused requalification after drift, evaluator
maintenance, efficacy and cost observations, supply-chain provenance, and evidence that
the process is being simplified or improved rather than merely growing.

## Advancing a level

A capability transition is foundational work and normally uses `assured` rigor:

1. freeze the capability and its acceptance cases;
2. implement only the next bounded surface;
3. test realistic success, failure, recovery, and adversarial cases;
4. independently verify the exact implementation and evidence;
5. retain owner-controlled decisions;
6. activate through an owner-local record; and
7. preserve rollback and invalidation triggers.

Create maturity gates for reusable capabilities or consequential transitions, not for
ordinary features. The exact machine requirements live in the [protocol conformance
reference](PROTOCOL_040_CONFORMANCE.md).
