# Bounded or Assured Task Brief — <Observable outcome>

Use this template only when evaluated/assured uncertainty or a consequential handoff
needs more than an issue/prompt and deterministic check. For a light task, see
`LIGHT_TASK.template.md`; for an ordinary bounded worker handoff, see
`BOUNDED_WORKER_PACKET.template.md`. Delete sections that are not material.

## Learning question and uncertainty

- What must this step establish? <answer>
- Which uncertainty could change the decision? <answer>
- Cheapest reliable evidence: <check/observation and expected discriminator>
- Selected rigor: <bounded / evaluated / assured, with reason>

## Authority and identity

- Repository/project: <identity>
- Branch/base/worktree: <identity>
- Active authority/writer/effect ceiling: <identity>
- Risk/data class, if material: <class and reason>

## Outcome, scope, and non-goals

- Observable outcome: <one outcome>
- Allowed paths/effects: <scope>
- Important non-goals/prohibitions: <scope>
- Reversibility/rollback: <statement>

## Context and routing

- Required source/artifacts: <small selected bundle>
- Worker/model/harness rationale: <why this route fits>
- Context/output/tool/time/attempt budget: <only material limits>
- Delegation and spawn policy: <policy>

Use a hash-bound retrieval/context manifest only when exact cross-context delivery,
auditability, or high consequence requires it.

## Evaluation and iteration

| Claim or learning target | Domain and evaluator class | Evidence source | Expected discriminator | Calibration or task-specific negative | Owner |
|---|---|---|---|---|---|
| <target> | static/runtime/semantic + exact/fallible | deterministic/runtime/trace/model/human | <expected result> | <current calibration ref, new negative, or not needed> | machine/external human |

- Baseline/eval sample, if behaviorally uncertain: <cases>
- Trace/output evidence to retain: <paths/roles>
- First-causal-error rule: <rule>
- Maximum useful experiment/retry budget: <adaptive budget>
- Escalation/simplification triggers: <conditions>

For stochastic product output, record the exact generation subject and a small
proportional sample count separately from evaluator-repeat sampling.

Use typed claims, exact subjects, evidence manifests, review bundles, and a formal
lifecycle receipt only for the assured profile or when the handoff truly needs them.

## Result and stopping

- Completion condition: <enough evidence to stop>
- Inconclusive/stop states: <conditions>
- Compact result format: <outcome, exact subject, checks, limitation, next action>
- Finalization ceiling: <read only / candidate / target; promotion and publication separate>
