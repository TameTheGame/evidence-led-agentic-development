# Test Strategy

Version 0.5 uses dependency-free, read-only Python conformance checks. Python 3.10 or
newer is required; no third-party packages are installed.

These checks validate reusable blueprint infrastructure. They do not require every
adopting-project task to generate a formal packet or receipt.

## Proof layers

1. **Structural checks** parse schemas, inert templates, registries, synthetic examples,
   and repository documents. They verify default-deny state, exact inventories, closed
   shapes, links, and text hygiene.
2. **Independent semantic corpora** keep important expected verdicts outside production
   admission logic: portable paths, lifecycle transitions, claim aggregates, adaptive
   rigor, context/authority, protocol security, and adoption/qualification cases.
3. **Exact-byte synthetic continuation** verifies a complete inert handoff from an
   independently pinned anchor without relying on a transcript.
4. **Release-bundle validation** authenticates the explicit normative inventory and
   denies unclassified schemas, registries, or conformance vectors.

All fixtures are synthetic and non-operational.

## Adaptive-rigor selector

`tests/task-rigor-vectors.json` covers the four profiles, each task selection dimension,
compound escalation, voluntary higher rigor, profile-base plus per-claim evaluator,
claim-domain, and task-effect modules, seven-question loop state, scaffolding classification,
simplification/escalation triggers, and explicit denial of authority effects. Its
decoupling cases prove that assured read-only static work needs no runtime/rollback,
a new exact regression does not become evaluator-immature, a semantic claim can carry an
unproven fallible evaluator without smearing that maturity onto exact claims, stateful
static work does need rollback, and read-only runtime work needs runtime but not rollback.

The selector recommends a minimum evidence posture. It cannot authorize mutation,
evidence acceptance, promotion, or publication. A light task does not need to persist the
machine-readable decision; the validator exists for projects that choose automated
routing or auditable selection.

## Path corpus

`tests/path-vectors.json` is the canonical positive/negative corpus for formal
repository paths. Every applicable schema and semantic checker must agree on rooted,
drive/UNC, separator, traversal, alternate-data-stream, terminal-dot/space, control,
case-fold, and reserved-device cases.

This cheap corpus is reusable safety infrastructure. It is not per-task paperwork.

## Lifecycle transition oracle

`tests/receipt-lifecycle-vectors.json` declares seven dimensions and 33 admitted rows
within a 44,100-tuple cross-product. `tests/lifecycle-semantic-vectors.json` separately
covers claim aggregation, all 15 unique admitted shapes, and single-field denials across
all dimensions.

The validator's rules-derived admission predicate does not read `allowedRows`. It is
compared with external table membership for all 44,100 tuples. Faults in either the
table or rule implementation must be detectable independently.

The 44,100 figure is exhaustive negative space, not 44,100 realistic hand-authored test
cases. Runtime is measured in milliseconds. Retain this suite for protocol conformance,
but invoke the lifecycle only for formal assured receipts.

## Other 0.5 semantic suites

- `validate_context_authority_v05.py`: protocol/core-lock identity, maturity/effect
  containment, context delivery, and bounded continuation.
- `validate_protocol_security_v05.py`: typed references, exact subjects, evidence and
  review authenticity, and malicious substitutions.
- `validate_adoption_v05.py`: qualification, resource, adoption-efficacy, and policy
  semantics.
- `validate_task_rigor_v05.py`: advisory task-rigor selection and proportional
  evidence/scaffolding rules.
- `validate_release_bundle_v05.py`: exact authenticated Level 0 artifact inventory.

These are Level 0 in-memory conformance slices. They do not imply that a live controller
composes them yet.

Integrated episode semantics are intentionally not implemented. The preserved episode
schema, template, and vector declarations under `drafts/` are excluded from normative
conformance until a separately justified semantic composition contract exists.

## Evaluator-calibration rule

Negative, malicious, crash, skip, and stale-subject tests calibrate reusable evaluators.
Routine implementation tasks may cite current calibration and run focused cases. Rerun
affected calibration after evaluator/schema/tool/adapter/runtime drift or when a new
failure mode carries material false-green consequence.

## Cross-platform matrix

A configured read-only workflow may run the same dependency-free suite on Windows,
Ubuntu, and macOS with supported Python versions. Configuration is not evidence until
every cell passes for the exact commit.

## What Level 0 does not prove

The suite does not implement or qualify a live model, packet compiler, admission
service, candidate manager, lease backend, target adapter, runtime harness, evidence
acceptance, gate transition, promotion, publication, or real human decision. Those are
target-owned empirical capabilities with their own proportionate tests and authority.
