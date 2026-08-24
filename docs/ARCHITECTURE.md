# Architecture

## Three orthogonal control planes

ELAD separates:

```text
project capability maturity  -> what infrastructure has been proven
task rigor                   -> how much evidence this step warrants
effect authority             -> what this episode may read or change
```

The effective workflow is the intersection of these decisions, not a single universal
pipeline. A high-maturity project can run a `light` task. An `assured` read-only
review can have zero mutation authority.

## Adaptive delivery topology

```text
product authority
      |
learning question + observable outcome
      |
task-rigor selector ---- project maturity ---- effect authority
      |
cheapest reliable evidence + smallest useful experiment
      |
      +---- deterministic operation
      +---- bounded candidate worker
      +---- evaluated behavior/runtime loop
      +---- assured isolated episode
      |
observe -> evaluate -> analyze first causal error
      |                         |
      +------ next change <-----+
      |
enough evidence -> compact result -> separate acceptance/promotion if applicable
```

The neutral blueprint owns methodology and reusable conformance. Each target repository
owns its project rules, active authority, evidence policy, artifact lanes, adapters,
gates, evidence, finalization, promotion, and publication.

## Effective authority

A future mutating operation may be admitted only by the intersection of:

```text
repository workflow envelope
∩ project profile and maturity ceiling
∩ active target authority
∩ risk and data policy
∩ exact tool/effect capability
∩ model+harness capability when formal qualification is required
∩ active fenced lease when the surface requires one
```

Every term can narrow authority; none can create it. A callable tool, green evaluator,
qualified model, selected rigor profile, or acquired lease is never a substitute for
target-repository authority. Unknown dimensions fail closed on consequential effects.

Task rigor selects evaluation and handoff depth. It does not grant effects. Maturity
describes the maximum proven infrastructure; it does not require maximum ceremony.

## Four execution shapes

### Light

Use the target's ordinary workflow. The contract may be an issue or prompt with one
observable outcome, allowed scope, a named deterministic check and expected result, a
stop condition, and a reversibility statement. The same worker may implement and run a
trustworthy existing check.

### Bounded

Use a compact task brief and selected context. A worker returns focused test results and
a concise handoff. Add a separate fixture or verifier when implementation could generate
its own expected answer. Formal manifests are conditional.

### Evaluated

Freeze representative examples, baseline behavior, or an eval sample before the change.
Collect runtime outputs or traces, classify errors, and choose the next experiment. Use
calibrated model or human judgment only for the semantic or experiential dimensions that
deterministic evaluators cannot prove.

### Assured

Use the strict protocol modules: immutable intent and context, exact qualification where
required, isolated candidate, typed claims/subjects, evidence manifest, lifecycle
receipt, independent verification, recovery, and adversarial or retained-human review.
Activation, promotion, and publication remain separate.

No normative integrated agentic-episode contract exists yet. The preserved draft cannot
return to `spec/` until it composes the current component contracts and an independent
semantic validator rejects contradictory authority, qualification, packet, receipt,
claim, and human-decision states.

## Reusable infrastructure and conditional records

| Scope | Examples | Normal frequency |
|---|---|---|
| Foundational reusable | schemas, path grammar, lifecycle rules, validators, malicious vectors, policies, authority boundaries | build once; run cheaply on relevant changes/CI |
| Periodic qualification | evaluator cards, model+harness certificates, resource envelopes, target-adapter golden paths | run on adoption and invalidating drift |
| Conditional per task | compact brief, runtime sample, selected trace, task-specific negative | only when the task's uncertainty needs it |
| Assured per episode | intent, retrieval/context delivery, packet, evidence manifest, receipt, review bundle, continuation anchor, lease | only for cross-context/high-consequence autonomous work |
| Human-retained | concise acceptance card and external decision | only for claims automation cannot reliably close |

A protocol compiler should inherit target defaults and generate normalized assured
records. Humans and workers should not manually reproduce stable policy fields.

## Roles

Roles are separated to the degree required by task rigor and effect risk:

| Role | Normal purpose | Boundary |
|---|---|---|
| Product authority | intent, priorities, retained decisions, activation/publication | not routine tool/log operation |
| Orchestrator | shape work, select rigor and worker, consume compact results | avoid raw repetitive tool traces and implicit mutation |
| Deterministic worker | exact transforms and checks | no semantic/product acceptance |
| Candidate worker | one bounded implementation on an allowed surface | no authority expansion or promotion |
| Independent verifier | read-only expectations/candidate/evidence inspection | no candidate mutation |
| Target executor | one narrow target-owned plan | no generic console/filesystem/process/package gateway |
| Promotion writer | integrate an accepted candidate under fresh authority | no worker-lease reuse or scope expansion |

A light task need not instantiate seven agents. Assured target-native, shared-state, or
promotion work uses stronger separation.

## Context architecture

The orchestrator retains intent, dependency state, capability summaries, unresolved
decisions, and compact results. It delegates repetitive exploration and tool use.

A constrained local worker receives:

- one atomic objective;
- a prebundled source slice sized to measured usable context;
- a small fixed tool set and capped output;
- explicit stop/escalation states;
- no recursive spawn by default;
- a supplied evaluator where appropriate.

Raw logs remain file-backed. If diagnosis needs them, retrieve only the causal slice.

For assured cross-context work, retrieval manifests authenticate source bytes, context
delivery authenticates what became model-visible, and a continuation anchor roots the
receipt chain independently. A light one-context task does not create these artifacts.

## Model and harness subjects

Capability belongs to the exact model, runtime, harness, adapter, prompt/context
compiler, tool schema, resource settings, and evaluated task class. A model in harness A
and the same model in harness B are separate subjects. Advertised context length is not a safe
working horizon.

Formal qualification is required for repeated autonomous routing, elevated effects, or
machine evidence authority. A one-off supervised light task can be owner-bounded without
a transferable certificate.

## Immutable references in the assured profile

Strict cross-document bindings use typed references with:

- artifact kind;
- canonical ID;
- portable repository-relative path;
- byte count;
- SHA-256;
- schema version;
- digest mode.

Structured protocol JSON uses one canonical UTF-8 representation; arbitrary source,
evidence, and review payloads are hashed as raw bytes. Earlier compatibility schemas
retain a smaller immutable-reference shape, but strict 0.3 assurance components use typed
references where byte framing matters. Consumers must follow the bound schema rather
than infer missing fields.

The packet is the outer envelope for retrieval/context inputs. The receipt is the outer
envelope for evidence. No document contains its own digest.

## Claims and evidence in the assured profile

An assured claim predeclares a stable class, acceptance owner, subject selector, evidence
class, evaluator, and required roles. It may cite a reusable evaluator calibration
rather than repeat the entire negative pack. A task-specific negative is added when a
new failure mode or consequential false-green risk warrants it.

After execution, receipt and evidence entries resolve the selector to the same exact
repository/candidate/base/content subject. Human review binds an eligible reviewer to the
exact sealed material shown. A worker cannot accept itself.

## Closed-world receipt lifecycle

The external lifecycle table defines 33 admitted assured receipt states across a
44,100-value cross-product. A separately expressed rule predicate derives admission
without reading the table, and the validator compares both across the complete domain.
Focused vectors test claim aggregation, representative admitted shapes, and single-field
denials.

This catches contradictory completion, evidence, candidate, and next-action states. It
is cheap foundational conformance, not a required receipt format for light tasks.

## Resource budgets

When model/harness resources are material, strict admission follows:

```text
configured writer ceiling
  >= measured-safe certificate
  >= packet request
  >= observed consumption
```

Context, output, retrieval, sequential/total tools, attempts, spawn, time, cost, and local
resource dimensions are selected according to the subject. A stable resource-envelope
identity prevents mixing qualification conditions. Do not make every deterministic
script invent GPU or token fields when those resources are irrelevant.

## Repository paths

All formal `repositoryPath` fields use the single grammar and shared corpus in
[PATH_IDENTITY.md](PATH_IDENTITY.md). Lexical validity is not filesystem authority;
later operational containment must also resolve roots, links, and exact checkout
identity.

## Opaque target artifacts

The platform-neutral pattern is:

```text
reviewable high-level input
  -> target-owned executor
  -> authoritative external serializer
  -> save/reload
  -> logical and complete-resource identity verification
  -> idempotent no-change reapply
```

The neutral core never patches opaque bytes. Target-specific adapters remain in target
repositories or clearly non-normative examples.

## Fencing and promotion

Fencing is used for overlapping writers, scarce target/runtime/data state, uncertain
completion, or promotion. It is not imposed on read-only or isolated light work.

Candidate checkpoint, technical evidence, retained-human acceptance, candidate
finalization, promotion, and publication are distinct. Promotion is intentionally absent
from the executable 0.3 contract; a future design must use fresh target authority,
detect target divergence, and keep publication separate.
