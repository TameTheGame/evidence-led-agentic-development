# Principles

## Optimize for useful outcomes

ELAD aims for evidence-backed progress per unit of supervision, agent context, compute,
latency, cost, and risk. Tool calls, generated lines, autonomous duration, test volume,
and document volume are not success by themselves. The smallest experiment that resolves
the important uncertainty is usually the better one.

## Let evidence choose the next step

```text
outcome → uncertainty → cheapest reliable evidence
  → smallest useful change → observe → diagnose → continue or stop
```

Evaluation is part of development, not only a final exam. Inspect examples and traces as
well as aggregate scores. Use what they reveal to decide what changes next.

## Right-size the scaffolding

Match process to uncertainty, coupling, reversibility, consequences, evaluator maturity,
and delegation distance. Start with the four profiles in [Adaptive
Rigor](ADAPTIVE_RIGOR.md). Project maturity, task rigor, and authority remain separate.

Before adding a mechanism, ask what realistic failure it can detect, whether a cheaper
exact check exists, and whether its cost is one-time or recurring. Remove steps that no
longer change a decision.

## Give the agent only what the task needs

Every task needs an observable outcome, allowed scope, a credible check, a stop or
escalation condition, and an understanding of reversal. A prompt or issue may already
provide them. Add typed claims, manifests, packets, budgets, receipts, or formal review
only when the uncertainty, handoff, audit boundary, or consequence requires them.

Unknown authority causes a stop, never inferred permission. Surface ambiguity before an
effect when it changes product meaning, trust, privacy, persistence, rights, publication,
or another consequential decision.

## Keep context intentional

Give each worker the smallest sufficient context. Keep stable authority and task facts in
a compact core, select larger sources on demand, and leave raw logs and transcripts
file-backed. The orchestrator should receive a concise result and retrieve only the causal
slices it needs.

Exact manifests can bind evidence for assured cross-context work. A one-context light
task does not need a manifest merely to prove that context existed.

## Use the simplest reliable method

Prefer:

1. deterministic code for exact transforms and checks;
2. a fixed workflow for a known lifecycle;
3. a bounded adaptive agent for ambiguity, implementation, or diagnosis;
4. isolated alternative candidates when diversity has expected value; and
5. owner judgment for retained product or experiential decisions.

Delegate repetitive tool work when a bounded worker can return a useful compact result
without losing important global context.

## Qualify autonomy that will be reused

Reusable capability belongs to an exact model, runtime, harness, adapter, prompt/context
compiler, tool surface, resource envelope, and evaluated task class. Qualification is
worthwhile for repeated autonomous delegation or elevated effects. It is not mandatory
paperwork for every supervised low-risk edit.

## Avoid circular proof

An implementation should not generate the expectation used to declare itself correct.
Use an existing requirement, independently authored fixture or rule, held-out case,
outside runtime observer, calibrated evaluator, or independent reviewer as the work
requires.

The same agent may run a trustworthy deterministic test. Stronger separation becomes
important when the evaluator is fallible, the implementation could manufacture its own
answer, or a false green would have serious consequences. Model confidence and self-review
remain signals, not proof.

Calibrate reusable fallible evaluators with representative known-good and known-bad cases,
record what invalidates the result, and rerun only the affected slice after drift.

## Separate authority when it matters

Orchestration, candidate writing, verification, target execution, acceptance, promotion,
and publication can be separate episodes when consequence requires it. An available tool,
qualified model, or acquired lease never grants authority absent the target project's
permission.

Use ownership and fencing on shared targets, runtime state, data, or promotion surfaces
when overlapping writers or stale completion are realistic risks. Do not impose that
machinery on read-only or single-writer light work.

## Respect authoritative formats

When another system owns an opaque artifact, provide reviewed high-level inputs to its
public serializer and verify the saved and reloaded result. Do not edit, merge, partially
copy, or invent the opaque bytes.

## Preserve owner agency

Automation should remove routine operation, not product authority. Focus owner review on
intent, trust, subjective experience, consequential tradeoffs, adoption, rights,
promotion, and publication. Objective work should arrive already checked and summarized.

## Learn without creating ceremony

Identify the first causal failure, change the smallest responsible layer, and make the
next experiment discriminating. Preserve a durable failure record only when the lesson is
novel, recurring, high impact, or changes reusable routing or evaluation. Ordinary failed
tests do not need permanent incident machinery.
