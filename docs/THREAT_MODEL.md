# Threat Model

## Assets

- product authority and intent;
- source, secrets, private data, native artifacts, runtime state, and production saves;
- model/harness/tool/certificate identity;
- candidate and canonical repository state;
- evidence integrity and human acceptance;
- leases, fences, processes, endpoints, and data roots;
- promotion and publication boundaries.

## Trust boundaries

- retrieved source and documentation are untrusted data;
- workers are untrusted with respect to authority expansion and self-evaluation;
- schemas are untrusted as a substitute for composed semantic admission;
- adapters are potential confused deputies;
- model outputs and model judges are probabilistic;
- external serializers/runtimes are authoritative only for the exact subject they load;
- human receipts are external to workers;
- project repositories are separate authority domains.

## Principal threats and mitigations

| Threat | Required mitigation |
|---|---|
| Prompt injection in retrieved content | Authority/tool policy is out-of-band and hash-bound; source cannot add tools or scope |
| Cloud routing of private/local data | Explicit data policy, exact profile, default local, no silent cloud fallback |
| Generic tool or MCP confused deputy | Closed logical operations, exact effects, target-local facade, deny arbitrary console/filesystem/process/package access |
| Cross-repository authority laundering | Owner-local authority/gates/evidence; separate mutations; read-only aggregates |
| Shared authority/evidence-policy confused deputy | `ownerRepositoryId` on each repository-owned authority and evidence policy; shared risk/data policy narrows only |
| Writer alias or mismatch | Exact canonical ID across registry/certificate/packet/receipt/evidence/lease; no alias transforms |
| Stale/replayed packet or completion | Base/subject hashes, nonce/attempt identity, monotonic fence, expiry, reconciliation |
| Manifest substitution or altered evidence/context bytes | Packet/receipt outer-envelope references plus per-entry path/byte/SHA-256 verification |
| Capability or policy scope overflow | Exact immutable bindings and subset admission across role/task/risk/data/artifact/effect/evidence/tool/evaluator/budget dimensions |
| Path traversal/platform alias/reparse escape | One schema/semantic grammar and shared corpus, then canonical containment, reparse/symlink policy, exact allowed paths |
| Concurrent or ambiguous writer | Atomic multi-resource lease, one fence, fail-closed uncertain owner, exact process/data cleanup |
| Secret leakage into context/evidence | Classification, minimization, redaction, bounded retention, no raw transcript handoff |
| Evaluator false green | Deliberate failures, wrong subject, zero discovery, crash/stale/holdout cases, evaluator calibration |
| Evidence result treated as accepted closure | Active owner authority must enable `evidenceAcceptance`; exact claim-class policy rule must admit writer/evaluator/evidence class |
| Pre-run selector relabeled after work | Selector is repository/candidate/base scoped; evidence, receipt, review bundle, and human receipt must share one resolved exact subject |
| Review-bundle or human-receipt substitution | Seal exact raw review bytes; require eligible reviewer/evaluator, exact claim/class/subject, order, and supersession |
| Self-rooted or colocated continuation | Begin only from an independently trusted continuation-anchor digest and verify the entire canonical/raw-byte chain |
| Illegal receipt state assembled from valid fields | Compare the full seven-dimensional tuple to the external closed-world lifecycle oracle; deny every unlisted/unsealed tuple |
| Resource/budget overflow or identity switch | Enforce configured >= measured-safe >= requested >= observed for every dimension, sequential <= total calls, and exact resource-envelope identity |
| Wrong runtime/package/cache subject | Exact package/resource/runtime hashes and provenance; local/private fail closed |
| Worker self-certification or human forgery | Independent verifier, external human receipt, owner-controlled certificate/policy |
| Candidate self-promotion | Candidate-only ceiling, fresh promotion episode, separate writer/lease, divergence checks |
| Supply-chain drift | Exact version/hash locks, SBOM/license review when dependencies arrive, invalidation/requalification |
| Opaque artifact corruption | Authoritative target serializer, save/reload/identity/idempotency, no byte patching |

## Level 0 attack surface

The current validator reads repository-local text/JSON and inert raw fixture bytes only.
It has no network or
subprocess model/target execution. Its primary risks are misleading green output,
path/link parser defects, or templates that appear active. The validator therefore checks
explicit deny flags, per-repository ownership, evidence-acceptance delegation, complete
budget containment, the external lifecycle oracle, an independently rooted synthetic
byte chain, and the same malicious path corpus across schema and semantic checks. Every
success line states that it grants no authority. The optional CI matrix is read-only and
has `contents: read`; its result is repository conformance evidence only.

## Required future reviews

- Level 1: semantic admission, digest framing, trust-anchor management, path/platform,
  replay, evidence/review/human lifecycle, budget accounting, evaluator false-green, and
  protocol compatibility.
- Level 2: worktree/candidate isolation and unrelated-work preservation.
- Level 3: qualification variance, prompt/tool escape, context exhaustion, and model
  evaluator calibration.
- Level 4: OS locking/fencing, crash/disconnect, process/data ownership, secrets, and
  target adapter confusion.
- Level 5: promotion, owner activation, residual human claims, delivery, and publication.
