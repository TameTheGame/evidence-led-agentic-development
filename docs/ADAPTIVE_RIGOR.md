# Adaptive Rigor

Evidence-Led Agentic Development does not require the same process for every task. Its
default question is not “Which available controls can we add?” but:

> What is the cheapest reliable evidence that resolves the uncertainty which matters
> now, at a cost proportionate to the complexity, reversibility, and consequence of the
> work?

This is how the methodology turns evaluation into a development instrument instead of
a final certification ritual. AI and other behaviorally uncertain components require a
disciplined build-and-observe loop, but the right evaluation strategy varies by project,
task, and development stage. A deterministic one-line correction and a new autonomous
production writer should not carry the same scaffolding.

## The seven-question loop

Every development step reasons through the same seven questions, even when the answers
fit in one sentence:

1. What are we trying to learn or establish in this step?
2. What uncertainty currently matters most?
3. What is the cheapest reliable evidence that would resolve it?
4. Should that evidence come from deterministic code, runtime behavior or traces, a
   calibrated model, a human, or a combination?
5. What did the evidence reveal?
6. What should change next?
7. Has enough evidence accumulated to consider this step complete?

The resulting loop is:

```text
smallest useful build or experiment
  -> observe outputs, traces, runtime, or deterministic results
  -> evaluate against an independent expectation
  -> analyze the first causal error
  -> choose the next smallest useful change
  -> repeat or stop
```

An agent need not create a separate document for every pass. For a light task, the task
prompt, existing repository authority, one test command, and its result may contain the
whole loop. Durable machine-readable records become useful when work crosses contexts,
models, authority boundaries, scarce targets, or consequential decisions.

## Three orthogonal decisions

Do not collapse these axes:

1. **Project maturity** says which infrastructure and authority a project has proven.
2. **Task rigor** says how much evaluation this task needs to resolve its uncertainty.
3. **Effect authority** says what this episode may read or change.

A mature project can use `light` rigor for a confined deterministic correction. A
read-only security or privacy assessment can require `assured` rigor. Selecting a rigor
profile never grants a write, runtime, promotion, publication, evidence-acceptance, or
other effect. Those permissions continue to come only from the target's independent
authority intersection.

## The four profiles

Profiles define claim-neutral evidence bases, not enormous fixed workflows. The optional
selector adds only the closed evidence modules required by declared claim domains, task
effect, and evaluator maturity. A project may use a stricter profile when justified, but
it records why the additional cost is expected to resolve meaningful uncertainty.

| Profile | Use when | Base plus applicable modules |
|---|---|---|
| `light` | The outcome is deterministic, confined, easy to reverse, low consequence, and covered by a proven evaluator. | contract + result inspection; a static/deterministic claim adds its deterministic check |
| `bounded` | Moderate coupling, a new regression, a bounded cross-context handoff, or managed reversal creates material but ordinary engineering uncertainty. | light base + explicit failure stop; claim/effect modules add only their discriminating evidence |
| `evaluated` | Product behavior or a product claim is semantic, stochastic, runtime-dependent, or backed by an unproven/partial fallible evaluator. | contract + inspection + error analysis + iteration decision, then semantic/runtime/evaluator/recovery modules only when applicable |
| `assured` | The component is foundational, high-consequence, security/privacy sensitive, difficult to reverse, externally mutating, or capable of changing durable authority. | evaluated base + independent expectation, bound identity, independent verification, and adversarial/recovery; claim/effect modules remain conditional |

The registry in `spec/registries/task-rigor-profiles.json` is the machine-readable version
of these bases and modules. `evidenceApplicability.claims` lists one or more closed claim
classes. Each class binds a domain (`static_deterministic`, `semantic_or_stochastic`, or
`runtime_or_operational`), an exact-deterministic or fallible evaluator class, and the
fallible evaluator's maturity when applicable. The selector computes the union of the
selected-profile base, every claim-domain and per-claim evaluator module, and the
task-effect module. Mixed work lists every domain rather than hiding them behind a
`mixed` escape hatch. The selector is advisory:
it cannot authorize the work or prove that a self-declared classification is truthful.
An orchestrator or packet compiler derives and binds the classification from the accepted
task contract; exact per-claim IDs and effects remain in the applicable full contracts.

Evaluator maturity is classified per claim, not once for the whole task. A newly written
exact regression against independently grounded expected values uses
`exact_deterministic` / `not_applicable`; it does not become a fallible, unproven
evaluator merely because the test is new. A semantic judge in the same episode can still
be `fallible` / `unproven`, raising only that semantic claim's evaluator requirements.

Runtime evidence is required for a runtime/operational claim. Executing a program does
not by itself make a claim runtime/operational: exact CLI stdout, exit status, schema,
fixture comparisons, and mocked endpoint-failure isolation can remain deterministic.
Use `runtime_or_operational` when the claim's truth materially depends on live state,
timing, distributed behavior, traces, persistence, native effects, or another property
an exact comparison cannot establish. Rollback proof is required
for a stateful reversible effect. A read-only assured audit requires neither runtime nor
rollback unless its claims independently call for runtime. A static task escalated only
because its evaluator is immature needs evaluator calibration, not an invented runtime
trace. An irreversible or durable external effect remains `assured` but must not fabricate
rollback proof for an effect that cannot be reversed.

## Selection dimensions

Choose a profile from the known facts, not from model confidence:

- **Uncertainty:** Are expected outputs exact and known, partly unknown, or inherently
  behavioral/stochastic?
- **Complexity and coupling:** Is the change local, integrated across components, or
  foundational across systems?
- **Reversibility:** Is an ordinary source revert enough, is a managed rollback needed,
  or can the effect be difficult or impossible to undo?
- **Consequence:** Would failure be a nuisance, materially waste effort or trust, or
  affect security, privacy, rights, durable data, production, or other high-impact state?
- **Evaluator class and maturity, per claim:** Can exact deterministic comparison settle
  this claim, or is its evaluator fallible? If fallible, is it proven, partially
  calibrated, unproven, or absent?
- **Delegation distance:** Is one actor working in one episode, is a supervised worker
  involved, or must evidence cross an autonomous context or external target boundary?

The minimum profile is the highest floor produced by any task dimension, declared claim
class and its evaluator maturity, task effect, plus the registry's small set of compound
escalation rules. A
runtime claim is at least `evaluated`; a stateful reversible effect is at least `bounded`;
an irreversible/durable external effect is `assured`. A high-consequence result is
`assured` even if the implementation is short. High uncertainty with a missing fallible evaluator
is at least `evaluated`. Difficult reversibility combined with high uncertainty or
complexity is `assured`.

This is deliberately not a weighted score. Averages can hide a single decisive
high-consequence fact.

## Choose the cheapest reliable evidence

For each material claim, select the lowest-cost evaluator that can actually distinguish
success from failure:

1. Existing deterministic check, type checker, compiler, linter, unit test, calculation,
   or exact comparison.
2. A focused new regression or integration check with expected behavior defined
   independently of the implementation under test. Its newness alone does not require
   fallible-evaluator calibration.
3. Runtime behavior, traces, logs, screenshots, or system observations tied to the exact
   subject.
4. A calibrated semantic evaluator or LLM judge for a narrowly defined class that code
   cannot decide reliably.
5. Human judgment for retained product, experiential, trust, rights, adoption, or
   similar decisions.
6. Independent or adversarial verification when consequence or evaluator weakness
   warrants it.

Do not add a model judge when exact code can decide. Do not use a screenshot to prove a
runtime or authority property it cannot observe. Do not treat a model's confidence or
self-review as evidence of its own correctness.

## Proportional epistemic independence

Expected behavior must not simply be generated by the same implementation logic being
tested. The required separation scales with the work:

- `light`: an existing test, predeclared expected value, or independently specified
  invariant is enough; a second agent is not inherently useful.
- `bounded`: use an independent fixture, regression expectation, or separate system
  observation where circularity is plausible. A new exact check needs an independently
  grounded expected value and a realistic failure it can detect, not a semantic
  calibration pack.
- `evaluated`: keep holdouts or expected cases outside the worker's context when useful;
  calibrate stochastic evaluators with known-good and known-bad cases; inspect traces and
  errors rather than relying on one aggregate score.
- `assured`: separate implementation, expected behavior, verification, and acceptance
  roles where practical, and include adversarial or recovery evidence appropriate to the
  consequence.

Evaluator qualification is reusable infrastructure. A stable evaluator does not need a
new malicious corpus for every routine invocation. Recalibrate it when its logic,
runtime, dependencies, target, claim class, or relevant inputs drift, or when a task
reveals a new false-green mode.

## Escalate and simplify from evidence

Escalate the current or next episode when evidence reveals:

- unexpected nondeterminism;
- an oracle that cannot discriminate the result;
- expanded scope or coupling;
- worse reversibility or higher consequence than declared;
- evaluator drift, false green, silent skip, crash, or zero discovery;
- a longer autonomous handoff or an external/native effect;
- unresolved human judgment; or
- a security, privacy, rights, persistence, or authority concern.

Escalation never widens authority. If the new evidence exceeds the active episode's
scope, stop and create a fresh, separately admitted episode.

A numeric threshold is not permission to ignore a correctness defect on a discriminator
the evaluation was explicitly designed to catch. When that happens and one cheap causal
fix is available, make that one factor change, rerun the affected slice, and then stop if
the completion claim is supported. This avoids both premature closure and open-ended
optimization toward perfect scores.

Simplify later work when evidence shows that:

- uncertainty has become deterministic;
- a reusable evaluator is now calibrated;
- scope or effects were removed;
- delegation became shorter or supervised;
- a proven platform capability can be cited rather than reproven; or
- an extra verification layer repeatedly adds cost without discriminating any realistic
  failure.

Simplification does not erase evidence already required by consequence, nor does it
silently downgrade a running episode. Record the reason and apply it to a fresh decision.

## Reusable infrastructure versus recurring work

Classify scaffolding explicitly:

### Reuse existing

Examples include project authority, policies, path rules, a pinned protocol bundle,
calibrated evaluators, test harnesses, model/harness certificates, lifecycle validators,
malicious corpora, and serializer adapters. Verify their identity or freshness; do not
rebuild them for each task.

### Create once or periodically

Examples include a new evaluator pack, model+harness qualification, recovery proof,
adoption efficacy baseline, target adapter, or foundational gate. Their initial cost is
justified only when future work can reuse the result and invalidation rules are clear.

### Recur per task

Examples include the selected implementation, the smallest relevant evaluator run, the
result needed for this task's claim, and a concise completion or failure record. Full
manifests, receipts, review bundles, and independent reviews recur only when this task's
profile or handoff actually requires them.

If the recurring scaffolding is larger than a task and does not resolve proportionate
uncertainty, simplify the workflow or compile the heavier records automatically from a
small human/agent-facing contract.

## The genuine lightweight path

For a low-risk deterministic task, this is sufficient:

```text
contract -> implementation -> deterministic test -> completion
```

The contract may be the existing issue, user request, or a few lines based on
`templates/LIGHT_TASK.template.md`. There is no mandatory JSON task-rigor decision,
capability certificate, retrieval manifest, evidence manifest, independent model review,
or human receipt. Existing repository authority still applies, and the check must be
capable of detecting the realistic failure.

Use the machine-readable task-rigor decision only when a router, cross-context handoff,
audit boundary, or consequential workflow benefits from a durable selection record.

## Heterogeneous models and harnesses

Rigor describes the task, while routing describes who can perform it. Select a worker
whose exact model+harness profile can fit the task and produce the selected evidence:

- A cloud orchestrator should shape work, route compact packets, and consume concise
  results rather than filling its context with repetitive tool transcripts.
- A constrained local worker should receive one small objective, preselected context,
  capped tools and outputs, a supplied verifier, and explicit stop states.
- Different harnesses for the same model are different qualification subjects when the
  workflow relies on autonomous routing.
- A one-off supervised light task may be assigned manually inside existing authority;
  it does not gain broader authority or a transferable capability certificate from that
  success.

`supervised_worker` means the assigning context remains present, owns verification, and
can stop or correct the worker inside the episode. `bounded_handoff` means the worker
receives a finite packet and returns a result across a context boundary. One assignment
may have both properties; choose the higher floor only for the material uncertainty or
risk the boundary actually introduces. The presence of another model does not turn an
exact product claim stochastic, and agentic software development does not imply agentic
product behavior.

Decompose when the task exceeds a worker's measured context, tool horizon, planning
ability, or evidence-return capability. Escalate uncertainty rather than silently asking
a stronger model to absorb an unbounded transcript.

## Adoption rule

Scope and authority are mandatory; ceremony is proportional. Unknown authority causes a
stop or owner escalation, never inferred permission. Start with the light path and existing tests. Add reusable infrastructure when repeated
work, agent uncertainty, context handoffs, target effects, or consequence make it pay
for itself. Activate strict packets, receipts, evidence chains, model qualification,
fencing, or independent review only for the profiles and project capabilities that need
them.

The desired outcome is not the largest control plane. It is the highest reliable
engineering closure per unit of human attention, context, compute, latency, cost, and
risk.
