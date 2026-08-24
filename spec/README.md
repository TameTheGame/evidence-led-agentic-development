# Draft Protocol Specification

Version 0.3 contains 29 closed structural schema contracts and matching inert templates.
They document optional target-policy, worker, qualification, evidence, adaptive-rigor,
and assured-handoff records. They are Level 0 reference data, not an operational
controller.

## Structural versus semantic proof

JSON Schema checks shape. It does not prove that:

- a writer exists, is capable, or has target authority;
- a task-rigor decision is correct or grants effects;
- a model/harness certificate was empirically earned;
- a path remains contained after real filesystem resolution;
- policy, profile, tool, evaluator, budget, and effect intersections admit a request;
- evidence proves the exact candidate/runtime subject;
- an evaluator can detect realistic failures;
- a human reviewed the asserted bytes;
- a lease exists or stale completion is fenced;
- a gate may transition;
- a candidate may be promoted or published.

The dependency-free semantic suites exercise selected Level 0 rules with synthetic data.
A live Level 1+ implementation still needs target-owned admission, runtime, identity,
replay, recovery, and clean-environment evidence.

## Selective use

The schemas are not one enormous required record set.

- A `light` task may use no JSON artifact at all.
- `bounded` and `evaluated` tasks add only the context/evidence records they need.
- `assured` cross-context or high-consequence work may selectively use the normative
  intent, qualification, context, packet, evidence, receipt, review, and continuation
  components.
- The integrated agentic-episode schema/template remain under `drafts/`: their internal
  shape is not semantic proof that the component states form an admitted episode.
- Capability, resource, evaluator, and efficacy records are reusable or periodic
  infrastructure, not automatic per-task work.

## Inventory and inertness

`blueprint.json` explicitly lists normative schemas, registries, and conformance
vectors. `protocol-bundle.json` authenticates that inventory. Unknown schema/registry/
vector files do not become normative through a filename glob.

Templates use `template_inert`, `held`, `unqualified`, `inactive`, `unrun`, or
equivalent refusal states. Passing schema and semantic conformance grants no authority.
