# Principles

## Optimize for engineering efficacy

The objective is:

> Evidence-backed progress and closure per unit of human attention, model context,
> compute, latency, cost, and risk.

Tool-call count, generated lines, autonomous duration, test volume, and document volume
are not success metrics by themselves. A smaller experiment or existing deterministic
check is better when it resolves the uncertainty reliably.

## Let evidence drive the next build

The universal loop is:

```text
learning question -> important uncertainty -> cheapest reliable evidence
  -> smallest useful build/experiment -> observe -> evaluate -> analyze errors
  -> choose the next change -> repeat or stop
```

Evaluation is a development instrument. It may also certify completion, but its first
job is to reveal what to do next. Inspect examples and traces, not only aggregate scores.

## Make rigor proportional

The scaffolding around a step should be proportional to its uncertainty, complexity,
reversibility, consequence, per-claim evaluator maturity, and delegation distance. Use the four
task profiles in [ADAPTIVE_RIGOR.md](ADAPTIVE_RIGOR.md). Project maturity, task rigor,
and effect authority are independent: none substitutes for another.

Before adding a mechanism, ask what uncertainty it resolves, what realistic failure it
detects, the consequence of that failure, whether cheaper deterministic evidence exists,
and whether the cost is one-time or recurring. Remove or simplify ceremony that no
longer changes a decision.

## Shape only what the task needs

Every task needs an observable outcome, allowed scope, a credible completion check, a
stop/escalation condition, and a reversibility understanding. A prompt or issue may
already provide them. Add typed claims, manifests, packets, budgets, fallback graphs,
receipts, or formal review only when delegation, uncertainty, auditability, or
consequence requires them.

Scope and authority are mandatory; ceremony is proportional. Unknown authority causes a
stop rather than inferred permission.

Ambiguity affecting product meaning, trust, privacy, persistence, rights, irreversible
state, or publication is surfaced before the relevant effect.

## Compile context instead of accumulating it

Give each worker the smallest sufficient context. Stable authority and task facts form a
compact core; larger sources are selected on demand. Raw logs and transcripts stay
file-backed, while the orchestrator receives compact results and selected causal slices.

For assured cross-context handoffs, exact retrieval and evidence manifests bind selected
bytes and subjects. For a light task in one context, do not manufacture manifests merely
to prove the context existed.

## Route by the least adaptive reliable method

Prefer, in order:

1. deterministic code for exact transforms and checks;
2. a fixed workflow for a known lifecycle;
3. a bounded adaptive worker for ambiguity, implementation, or diagnosis;
4. multiple isolated candidates when diversity has expected value; and
5. human judgment for retained product or experiential decisions.

An orchestrator delegates repetitive tool work when a bounded worker can return a
compact result without losing important global context.

## Qualify repeated autonomous workers

Capability belongs to an exact model, runtime, harness, adapter, prompt/context
compiler, tool schema, resource envelope, and evaluated task class. Separate harnesses
are separate subjects. Certificates are amortized routing infrastructure for repeated
autonomous delegation or elevated effects; they are not mandatory paperwork for every
supervised low-risk edit.

## Preserve proportional epistemic independence

An implementation cannot establish its own correctness through circular evidence. Use
an independently authored expected result, fixture, rule predicate, holdout, runtime
observer, calibrated semantic evaluator, independent agent, or human as the work
warrants.

The same worker may run a trustworthy deterministic test for a light task. A new exact
regression with independently grounded expected behavior is not an unproven fallible
evaluator merely because it is new. Stronger role separation is required when the
implementation could generate its own expected result, the evaluator is fallible or
stochastic, or a false green would matter.
Model confidence and self-review remain signals rather than proof.

## Evaluate evaluators—and reuse the result

Calibrate an evaluator against proportionate known-good, known-bad, stale-subject,
missing-output, crash, and adversarial cases. Record the exact evaluator/tool/schema/
environment identity and invalidation triggers. Routine tasks cite the current
calibration and run focused cases. Rerun affected calibration when that identity drifts
or the task introduces a new high-consequence failure mode.

## Separate authority episodes

Orchestration, candidate writing, deterministic operation, independent verification,
target execution, acceptance, and promotion are distinct when the selected rigor and
effect boundary require separation. A callable tool, qualified model, or acquired lease
cannot grant authority absent the target repository's permission.

## Contain consequential effects

Candidate work is isolated when reversal or overlap matters. Shared target, runtime,
data, and promotion surfaces use exact ownership and fencing when concurrency or stale
completion is a realistic risk. Do not impose a lease system on a read-only or
single-writer light task with no scarce surface.

## Respect authoritative serializers

When an external system owns an opaque artifact, provide reviewed high-level inputs to
its public serializer and verify the saved/reloaded result. Never edit, merge,
partially copy, or invent the opaque bytes. This is both a correctness boundary and an
automation design constraint.

## Preserve human agency

Automation should remove routine operation, not product authority. Human review is
focused on intent, trust, subjective experience, consequential tradeoffs, adoption,
rights, and publication. Objective work should arrive already tested and summarized.

## Learn through reviewed causality

Classify the first causal failure, change the smallest responsible layer, and make the
next experiment discriminating. Add a durable failure record only when the lesson is
novel, recurring, high-impact, or changes reusable routing/evaluation infrastructure.
Do not turn every ordinary failed test into permanent ceremony.
