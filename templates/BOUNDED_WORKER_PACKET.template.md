# Bounded Worker Packet — <observable outcome>

Use this compact Markdown packet for an ordinary finite worker handoff. It is not the
assured JSON task packet, grants no authority, and should be shortened when the existing
task already supplies a field.

## Objective

<One observable outcome.>

## Scope and authority

- Repository, branch, and base: <exact identity>
- Allowed paths and effects: <finite scope>
- Actual authority source: <owner workflow or active record>
- Prohibited effects and non-goals: <including commit/push/publish, runtime, external
  mutation, recursive spawn, or other relevant denials>

Unknown authority means stop and return the ambiguity. This packet cannot expand it.

## Selected context

- Read first: <small ordered list>
- Relevant facts/constraints: <only what changes the task>
- Exact worker subject, if material: <model artifact/revision + runtime + harness/adapter
  + tool surface + context/resource envelope + task class>

## Output and evidence

- Expected result: <artifact or answer>
- Supplied verifier and expected discriminator: <exact check>
- Held-out verifier, if consequence or overfitting risk justifies one: <or not needed>
- Compact return: <outcome, changed paths, checks/verdicts, first causal failure or
  limitation, requested next action>

The orchestrator owns independent verification. A deterministic product claim remains
deterministic merely because a worker implemented it.

## Practical budgets

- Context/output/tool/time/attempt limits: <only material caps>
- Spawn policy: <normally none>
- Context-delta requests: <one bounded request or none>

## Stop or escalate

Stop on scope/authority ambiguity, prohibited effects, missing context that changes the
objective, an inconclusive verifier, unexpected nondeterminism, budget exhaustion, or a
failure requiring wider authority. Return the bounded result; do not improvise a broader
task.
