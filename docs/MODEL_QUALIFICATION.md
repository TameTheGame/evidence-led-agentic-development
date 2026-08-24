# Model and Harness Qualification

Formal qualification answers a practical routing question:

> What work can this exact agent setup complete reliably, within what limits and effects?

It is worth the setup cost for repeated autonomous delegation, constrained local workers,
broader candidate or runtime effects, machine evidence acceptance, or recurring tasks
where a routing mistake would be expensive. A one-off supervised light task can stay
owner-bounded and independently checked without earning a reusable certificate.

## Qualify the complete setup

Capability does not belong to a model name alone. Bind the result to the material parts
of the execution route:

- exact provider/model revision or local artifact and quantization;
- backend, runtime, and material hardware configuration;
- harness and adapter versions;
- system prompt, task template, context compiler, and tool schemas;
- configured context, output, tool, attempt, time, cost, and resource limits;
- eligible task classes, data/risk classes, effects, and evidence roles;
- evaluator and held-out-case identities; and
- expiry and invalidation triggers.

The same model in two harnesses is two qualification subjects. A coding-agent harness and
a product inference API are also different subjects even when they load the same weights.
For stochastic product behavior, bind material request settings such as temperature,
thinking mode, and output-token limit.

## Measure only the scope you intend to grant

A request is eligible only when its task, limits, tools, evidence, and effects fit one
proven qualification scope and the target project's authority. Do not combine favorable
parts of several qualification records.

Measure usable context and sequential tool horizon rather than relying on advertised
capacity. When resource limits matter, confirm that the configured ceiling covers the
measured-safe ceiling, the task request, and observed use. Missing measurements mean the
route is unproven for that dimension, not unlimited.

## Move through stages

| Stage | Maximum use |
|---|---|
| Unqualified | design or an explicitly supervised one-off task; no reusable routing claim |
| Shadow | read-only observation that cannot affect the outcome |
| Canary | small read-only or disposable candidate cases |
| Candidate-only | eligible isolated candidate work; no target or promotion authority |
| Qualified | exact proven classes inside project policy and active authority |
| Narrowed | reduced scope after drift or failure |
| Expired or revoked | no autonomous routing |

Moving up a stage is a separate owner decision. Demonstrated capability does not grant
permission to use that capability on a target.

## Build a proportionate evaluation pack

Choose cases that expose the route's expected failure boundary, not the largest possible
case count. Depending on the claimed capability, include:

- representative successful tasks;
- deliberate implementation failures;
- misleading or prompt-injected source material;
- missing, stale, wrong, excessive, or inaccessible context;
- unsupported tools and out-of-scope effects;
- evaluator skip, crash, timeout, and false-green cases;
- identity or subject substitution;
- cold repeats when variance matters;
- budget exhaustion and clean refusal; and
- a compact result that another context can continue from.

A narrow read-only classifier needs much less than a broad target-mutating worker.

## Package constrained workers deliberately

Give a bounded worker one objective, selected source slices below its measured context,
a small tool set, explicit budgets, a supplied verifier, and one compact return. Default
to read-only or candidate-only effects until stronger capability and authority are proven.

Use the [bounded-worker template](../templates/BOUNDED_WORKER_PACKET.template.md) when a
saved handoff helps. A supervised worker can also receive a bounded handoff; escalate only
for the uncertainty or risk introduced by the boundary.

For orchestrators, qualify long-horizon planning, ambiguity resolution, worker selection,
and compact-result consumption. Keep repetitive worker transcripts out of orchestrator
context unless a selected causal slice is needed. If an orchestrator later becomes a
writer or promoter, begin a new authority episode for that effect.

## Reuse the result until it drifts

Store the qualification and evaluator calibration once. Recheck the affected slice after
material changes to the model, quantization, backend, hardware, harness, adapter, prompt,
context compiler, tool schema, protocol, evaluator, target profile, or runtime.

A worker cannot renew its own qualification. Unaffected expensive cases do not need to be
rerun merely because another task used the same route.
