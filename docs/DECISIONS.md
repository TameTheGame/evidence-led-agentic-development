# Decisions

## ADR-0019 — Versioned release closure and two-component numbering

**Status:** accepted by the maintainer on 2026-09-05 for v0.5 and future blueprint updates

Completed Direct/Conserve and repository-consolidation changes were pushed without a new
release. The maintainer requested v0.5, two-component numbers, and release closure as
the default. [Releasing](RELEASING.md) is the canonical policy: accepted user-facing
updates include a coherent version bump, notes, validation, tag, and verified GitHub
Release unless explicitly scoped to draft/local-only work. This is standing permission
for this public blueprint only, not a generic publication capability or adopter authority.

The alternative of renaming old releases would break existing pins and provenance.
Instead, old three-component tags and non-normative 0.3 drafts remain immutable. Active
protocol identities advance together to exact `0.5`; mixed-version chains fail closed.
Adoption requires an explicit owner-local repin and affected checks. Rollback means
using the prior exact release, not rewriting its tag or combining protocol versions.

The existing hosted workflow gains one narrowly scoped release job after the full
conformance matrix; pull requests and ordinary branch pushes retain read-only access.
Validation rejects malformed versions, mismatched tags, missing notes, and stale release
metadata. Failed publication is unfinished delivery, not a reason to move a published tag.

## ADR-0018 — Delivery mode is separate from rigor

**Status:** accepted for Level 0 guidance on 2026-09-05; released in v0.5

[Operating Modes](OPERATING_MODES.md) is the canonical delivery-mode policy. Direct
supports capable primary-agent completion inside existing scope, including light and
bounded source tasks. Conserve explicitly routes bounded work to an eligible cheaper
or local subject. Logical roles do not require a separate agent per role, and
constrained-worker packaging applies to selected delegates.

This supersedes blanket local-first routing in current guidance while retaining review
budgets, claim-scoped revalidation, qualification for repeated autonomy, and actual effect
boundaries. Historical release claims and runtime evidence remain historical. No selector
engine, target repin, or runtime activation follows. ADR-0019 releases this guidance and
updates the protocol identities without adding target operational capability.
The dated research note supplies design motivation, not comparative efficacy evidence.

## ADR-0001 — Evidence-led mission

**Status:** accepted for Level 0

Optimize for evidence-backed independent closure per unit of human attention, context,
compute, latency, cost, and risk. Activity and autonomy duration are not primary goals.

## ADR-0002 — Default-deny, owner-local authority

**Status:** accepted for Level 0

The blueprint cannot grant target authority. Effective authority is the intersection of
owner workflow, project profile, active authority, risk/data policy, tool effect,
capability certificate, and fenced lease. Unknown means deny.

## ADR-0003 — Protocol versus target boundary

**Status:** accepted for Level 0

The reusable core owns protocol and conformance. Each target repository owns its product,
facade, artifacts, gates, evidence, candidate state, promotion, and publication. No
mutating operation spans owner repositories.

## ADR-0004 — Exact model+harness capability

**Status:** accepted for Level 0

Capability is measured for an exact model/runtime/harness/adapter/template/tool/budget
subject. Provider/model names do not grant authority, and proof does not transfer between
harnesses.

## ADR-0005 — Promotion excluded from worker contracts

**Status:** accepted for Level 0

Worker packets and receipts stop at candidate-only finalization. Promotion requires a
future separate design, fresh authority, separate writer and fence, malicious fixtures,
independent review, and owner activation. Publication remains distinct.

## ADR-0006 — Immutable manifest envelopes

**Status:** accepted for Level 0 contract design

Retrieval and evidence manifests are separate first-class contracts. Material bindings
use canonical ID, portable repository path, SHA-256, and schema version. Each manifest
binds its referenced entries as raw bytes; the enclosing packet or receipt binds the
complete manifest using the canonical structured-JSON framing, avoiding a self-hash.
These inert contracts grant no retrieval, evidence acceptance, or operational authority
at Level 0.

## ADR-0007 — One portable repository-path grammar

**Status:** accepted for Level 0 conformance

Every applicable schema and semantic validator must implement the normative grammar in
`docs/PATH_IDENTITY.md` and consume the same verdicts in `tests/path-vectors.json`.
Platform-specific permissiveness cannot widen the protocol. Operational filesystem
containment and reparse/symlink controls remain additional later-level proofs.

## ADR-0008 — Repository-owned authority and evidence policy

**Status:** accepted for Level 0 contract design in 0.2.0

Each repository owns a distinct active-authority record and evidence policy, both bound
to its canonical repository ID. Product-wide risk/data policy may be shared only as a
narrowing input. Machine evidence closes a claim only when owner authority enables
`evidenceAcceptance` and the repository's active evidence policy matches the exact claim
class, evidence class, evaluator, acceptance owner, and eligible writer.

## ADR-0009 — Typed claims and exact subject resolution

**Status:** accepted for Level 0 contract design in 0.2.0

Intent and packet claims bind a stable `claimClass` and pre-run subject selector.
Evidence, worker receipts, review bundles, and human receipts must resolve that selector
to the same exact repository, subject/candidate, base head, and SHA-256. A subject may not
be relabeled after evaluation to fit available evidence.

## ADR-0010 — Closed-world receipt lifecycle

**Status:** accepted for Level 0 conformance in 0.2.0; independence corrected in 0.3.0

Receipt admission is determined by an external seven-dimensional oracle with exactly 33
allowed sealed tuples among 44,100 combinations. Version 0.2 correctly failed closed
against the table but overstated evaluator independence because operational admission
also used table membership. Version 0.3 adds a separately expressed rules-derived
predicate and focused aggregate/shape/mutation vectors, then compares rule and table over
the full domain. It must not copy the allowlist into code. Every unlisted tuple is denied.

## ADR-0011 — Explicit digest framing and external continuation trust

**Status:** accepted for Level 0 conformance in 0.2.0

Structured protocol JSON is hashed from sorted-key compact UTF-8 JSON plus one terminal
line-feed byte. Source, evidence, review, and other payloads are hashed as raw bytes. A
fresh continuation begins at an independently trusted continuation-anchor digest and
walks the immutable chain; a receipt cannot be its own trust root. External human
receipts bind one eligible reviewer to one sealed exact-byte review bundle.

## ADR-0012 — End-to-end budget containment

**Status:** accepted for Level 0 contract design in 0.2.0

Every budget dimension obeys configured writer >= measured-safe certificate >= requested
packet >= observed receipt. Sequential tool calls are bounded separately and cannot
exceed total calls. One exact resource-envelope identity spans the chain; run-specific
observations cannot broaden certified capability.

## ADR-0013 — 0.2.0 breaking pre-release hardening

**Status:** accepted

The 0.1.0 root is retained as a failed adversarial-review baseline, not an adoption
candidate. Version 0.2.0 makes incompatible corrections to ownership, evidence closure,
claims/subjects, receipts, budget containment, digest framing, continuation trust, human
review, and malicious path coverage while preserving Level 0/default-deny status.

## ADR-0014 — Adaptive task rigor is orthogonal to maturity and authority

**Status:** accepted for Level 0 design in 0.3.0

Every task selects `light`, `bounded`, `evaluated`, or `assured` evidence effort
from uncertainty, complexity, reversibility, consequence, per-claim evaluator maturity, and
delegation distance. Project maturity describes proven capability; effect authority
describes allowed consequences. Neither forces nor grants the other. A light task may
use only its existing contract and deterministic check. The full packet/receipt chain is
conditional assured infrastructure.

Profile evidence is a claim-neutral base plus closed modules derived from claim classes,
their evaluator maturity, and task effect. Runtime evidence is conditional on runtime or
operational claims; rollback proof is conditional on stateful reversible effects. The
applicability record is descriptive and authority-free, and orchestration must bind it to
the accepted task contract rather than allowing a worker to waive modules by assertion.

## ADR-0015 — Reusable calibration and explicit normative inventory

**Status:** accepted for Level 0 design in 0.3.0

Evaluator negatives, capability qualification, path/lifecycle corpora, and adoption
proof are amortized infrastructure with named invalidation triggers. Routine tasks reuse
current calibration and run task-specific evidence. New durable gates are reserved for
reusable capabilities or consequential transitions, not ordinary features.

`blueprint.json` explicitly classifies normative schemas, registries, conformance
vectors, and preserved non-normative drafts. The authenticated bundle is derived from
that closed inventory rather than a filename glob, so an unfinished artifact cannot
silently become normative by location.

## ADR-0016 — Portability corrections follow claims, not development mechanics

**Status:** accepted for Level-0 release-candidate design after four bounded portability
observations; see `docs/EMPIRICAL_STATUS.md`

Four observations—deterministic single-agent work, cold external adoption,
deterministic heterogeneous delegation, and semantic product evaluation—showed that
rigor must follow the material claim and stakes. Evaluator maturity is therefore bound
per claim class. A newly authored exact regression is not an unproven fallible evaluator,
executing a program does not by itself create an operational claim, and an AI coding
worker does not by itself create stochastic product behavior.

Adoption uses progressive disclosure while keeping scope and authority non-skippable.
An ordinary finite worker handoff receives a compact Markdown packet; the assured JSON
chain remains conditional. Exact execution subjects distinguish coding and product
inference harnesses. Small semantic evaluation may use proportional generator samples,
a calibrated judge, one-factor causal iteration, and a stopping rule that neither ignores
a failed designed discriminator nor chases perfect scores indefinitely. Model-judge
evidence never becomes external-human acceptance.

## ADR-0017 — Proportional assurance is a 0.4 compatibility boundary

**Status:** accepted for Level-0 release in 0.4.0

The lifecycle-cost invariant, hard non-resetting review budgets, causal claim-scoped
revalidation, Git-native tracked-artifact identity, and qualified local-first routing
materially change how ELAD selects and repeats assurance work. They therefore ship as
Protocol 0.4 rather than remaining indefinitely under `Unreleased` while the normative
artifacts still identify themselves as 0.3.

The change is deliberately a compact policy correction, not a reusable-control registry,
selection engine, vector framework, receipt expansion, or generic control platform. The
existing schemas remain structurally the same, but every active protocol, schema,
registry, vector, template, example, bundle, and validator identity is rebound to exact
0.4.0 so mixed-version chains fail closed.

A target pinned to 0.3.0 remains valid only against that exact release. Adopting 0.4.0
requires an explicit repin and target-owned, claim-scoped revalidation of the affected
review and learning flow; it grants no new target authority. The preserved integrated
episode drafts remain non-normative 0.3 artifacts. Rollback is continued pinning to
`v0.3.0`, not a mixed 0.3/0.4 chain.
