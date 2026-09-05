# Repository Manifest

**Version:** 0.5

## Read first

| Path | Purpose |
|---|---|
| `README.md` | Plain-language methodology, profiles, boundaries, and adoption |
| `START_HERE.md` | Short owner/agent entrypoint |
| `docs/OPERATING_MODES.md` | Canonical Direct/Conserve delivery guidance, conditional worker controls, and adoption evidence |
| `docs/FIRST_RUN.md` | Project-owner decisions and explicitly prefixed agent instructions |
| `docs/EMPIRICAL_STATUS.md` | Demonstrated, bounded, and untested claims |
| `STATUS.md` | Current candidate state, completed surfaces, and absent authority |
| `AGENTS.md` | Repository rules and adaptive change lifecycle |
| `docs/ADAPTIVE_RIGOR.md` | Practical guide to choosing the lightest defensible rigor |
| `blueprint.json` | Machine-readable identity, default-deny state, registries, and explicit release inventory |

## Root governance and provenance

| Path | Purpose |
|---|---|
| `VERSION` | Canonical version marker |
| `protocol-bundle.json` | Generated authenticated inventory; never self-includes |
| `GOVERNANCE.md` | Shared-protocol versus target ownership |
| `SECURITY.md` | Threat and reporting boundary |
| `CONTRIBUTING.md` | Contract-change procedure |
| `CHANGELOG.md` | Version history |
| `docs/RELEASING.md` | Canonical two-component versioning and default release-completion policy |
| `releases/v0.5.md` | Checked-in v0.5 GitHub Release notes |
| `ROADMAP.md` | Future maturity capabilities |
| `LICENSE`, `NOTICE.md` | Apache-2.0 license and attribution notice |

## Design documents

| Path | Purpose |
|---|---|
| `docs/PRINCIPLES.md` | Engineering-efficacy and evidence-led principles |
| `docs/ARCHITECTURE.md` | Orthogonal maturity/rigor/authority and adaptive execution shapes |
| `docs/ADOPTION_RUNBOOK.md` | Progressive adoption from a true lightweight path |
| `docs/EVALUATION_AND_EVIDENCE.md` | Adaptive evaluator selection, independence, calibration, and assured claims |
| `docs/LIFECYCLE_ORACLE_ASSESSMENT.md` | Cost/value/independence disposition of the 44,100-domain oracle |
| `docs/MATURITY_MODEL.md` | Proven capability levels, independent of per-task rigor |
| `docs/MODEL_QUALIFICATION.md` | Exact cloud/local model+harness qualification and routing |
| `docs/MODEL_HARNESS_READINESS_EVALUATION.md` | Separate operational companion for fair model/harness readiness comparison |
| `docs/OPERATIONS_AND_LEARNING.md` | Observability, error analysis, efficacy, drift, and simplification |
| `docs/HUMAN_DECISION_BOUNDARY.md` | Decisions retained by the project owner and concise review cards |
| `docs/PATH_IDENTITY.md` | One portable repository-path grammar |
| `docs/THREAT_MODEL.md` | Trust boundaries and failure modes |
| `docs/RESEARCH_BASIS.md` | Research attribution, methodology translation, and dated non-normative Astra adoption note |
| `docs/PROTOCOL_05_CONFORMANCE.md` | Exact Level 0 conformance claims and limits |
| `docs/DECISIONS.md` | Durable protocol decisions |
| `docs/LICENSING_AND_PROVENANCE.md` | Publication prerequisites |

## Adaptive-rigor executable core

| Path | Purpose |
|---|---|
| `spec/registries/task-rigor-profiles.json` | Four profiles, selection floors, and closed claim/effect/evaluator evidence modules |
| `spec/schemas/task-rigor-decision.schema.json` | Optional fail-closed advisory decision; grants no authority |
| `templates/task-rigor-decision.template.json` | Inert machine-readable selector template |
| `templates/LIGHT_TASK.template.md` | Optional small task card; existing issue/prompt may substitute |
| `templates/BOUNDED_WORKER_PACKET.template.md` | Compact finite worker handoff; distinct from the assured JSON packet |
| `tests/task-rigor-vectors.json` | Eleven positive and 37 malicious/contradictory cases, including per-claim evaluator and claim/effect decoupling |
| `tools/validate_task_rigor_v05.py` | Dependency-free selector conformance |

## Draft schema contracts

There are 29 one-to-one normative schema/template pairs. They are structural reference contracts,
not operational services.

### Target-owned policy and authority

- `active-authority.schema.json`
- `project-profile.schema.json`
- `risk-policy.schema.json`
- `data-policy.schema.json`
- `evidence-policy.schema.json`
- `gate-set.schema.json`

### Worker, task, and evidence

- `writer-profile.schema.json`
- `capability-certificate.schema.json`
- `intent-brief.schema.json`
- `retrieval-manifest.schema.json`
- `task-packet.schema.json`
- `evidence-manifest.schema.json`
- `worker-receipt.schema.json`
- `review-bundle.schema.json`
- `external-human-receipt.schema.json`
- `continuation-anchor.schema.json`
- `failure-record.schema.json`
- `tool-registry.schema.json`
- `evaluator-registry.schema.json`

### Protocol 0.5 assurance modules

- `protocol-bundle.schema.json`
- `core-lock.schema.json`
- `typed-reference.schema.json`
- `context-delivery.schema.json`
- `evaluation-pack.schema.json`
- `evaluation-result-manifest.schema.json`
- `resource-envelope.schema.json`
- `adoption-efficacy-plan.schema.json`
- `adoption-efficacy-report.schema.json`
- `task-rigor-decision.schema.json` — optional advisory selector

Schemas live under `spec/schemas/`; matching inert JSON templates live under
`templates/`. `spec/README.md` explains structural versus operational proof.

## Canonical registries

- `spec/registries/roles.json`
- `spec/registries/evidence-classes.json`
- `spec/registries/terminal-statuses.json`
- `spec/registries/failure-classes.json`
- `spec/registries/maturity-ceilings.json`
- `spec/registries/subject-selectors.json`
- `spec/registries/task-rigor-profiles.json`

Every registry is reference-only. `blueprint.json` binds its canonical digest.

## Human-readable templates

- `templates/AGENTS.template.md`
- `templates/STATUS.template.md`
- `templates/MANIFEST.template.md`
- `templates/WORKFLOW.template.md`
- `templates/LIGHT_TASK.template.md`
- `templates/BOUNDED_WORKER_PACKET.template.md`
- `templates/TASK_BRIEF.template.md`
- `templates/HUMAN_ACCEPTANCE_CARD.template.md`
- `templates/EVALUATOR_CARD.template.md`
- `templates/FAILURE_RECORD.template.md`

These are selective starting points. No adopter should copy all templates by default.

## Executable Level 0 conformance

| Path | Purpose |
|---|---|
| `tools/Test-Blueprint.ps1` | Runs the six dependency-free validation slices |
| `tools/validate_all.py` | Cross-platform Python entrypoint for all six slices |
| `tools/validate_blueprint.py` | Main structural, path, lifecycle, continuation, and malicious checks |
| `tools/validate_context_authority_v05.py` | Context/core-lock/maturity/authority semantics |
| `tools/validate_protocol_security_v05.py` | Typed-reference, subject, evidence, and attack semantics |
| `tools/validate_adoption_v05.py` | Qualification, resource, and efficacy semantics |
| `tools/validate_task_rigor_v05.py` | Adaptive-rigor semantics |
| `tools/validate_release_bundle_v05.py` | Explicit authenticated artifact inventory |
| `tools/validate_release.py` | Version/changelog/notes/tag agreement and in-memory negative checks |
| `tools/build_level0_artifacts.py` | Deterministically refreshes inert registry bindings, synthetic fixture references, and release bundle |
| `tests/path-vectors.json` | 122 portable-path cases |
| `tests/receipt-lifecycle-vectors.json` | External 33-row closed-world table over 44,100 tuples |
| `tests/lifecycle-semantic-vectors.json` | Claim aggregates, 15 unique lifecycle shapes, and single-field denials |
| `tests/context-authority-vectors.json` | Context/authority/maturity cases |
| `tests/protocol-security-vectors.json` | Protocol-security cases |
| `tests/adoption-vectors.json` | Adoption/qualification/resource/efficacy cases |
| `tests/task-rigor-vectors.json` | Adaptive-rigor cases |
| `tests/fixtures/continuation-valid/` | Exact-byte synthetic continuation chain |

The generator writes only inert local Level 0 artifacts. The validators are read-only.
None contact a provider, execute a model, mutate a target, accept real evidence, or grant
authority.

## Synthetic examples and drafts

| Path | Purpose |
|---|---|
| `examples/two-repository-product/` | Fictional split-owner product showing shared protocol without shared authority |
| `examples/mixed-claim-semantic-feature/` | Compact mixed deterministic/semantic evaluated example |
| `drafts/agentic-episode.schema.json` | Preserved non-normative integrated-episode structural draft |
| `drafts/agentic-episode.template.json` | Preserved non-normative integrated-episode instance draft |
| `drafts/episode-vectors.interrupted.json` | Preserved non-normative ideas from the unfinished integrated-episode draft |
| `drafts/promotion/` | Non-executable future promotion design |
| `reference/` | Reserved for a separately authorized operational reference implementation |
| `adapters/` | Reserved for target-owned/provider adapter guidance; none implemented |

The three interrupted episode artifacts are explicitly excluded from the authenticated
normative conformance inventory. They preserve design evidence, but no adopter may treat
schema validity as semantic episode admission.
