# Operations and Learning

Operational records should answer a few useful questions:

- What happened?
- What evidence supports that conclusion?
- If it failed, where did the first causal failure occur?
- What should change next?
- Is the process still worth its recurring cost?

Record only information that can change a decision. A light task may need the command,
result, changed paths, and inspected diff. Repeated autonomous or assured work may also
need exact model, harness, candidate, evaluator, target, budget, cost, authority, and
drift identities. Leave unknown measurements unknown and say why.

## Keep agent context compact

Raw traces, transcripts, screenshots, and runtime logs should stay file-backed. A worker
normally returns:

- the outcome and exact changed subject;
- focused checks and verdicts;
- the first causal failure or important limitation;
- evidence locations when they must persist; and
- the requested next action.

Bring raw evidence into the orchestrator's context only when it answers a causal question.
A compact result is a context-control tool, not a requirement to create a formal receipt
for every edit.

## Measure whether autonomy is helping

The central question is:

> Does this workflow increase evidence-backed useful outcomes while reducing unnecessary
> supervision, context, latency, cost, and risk?

Useful measures include accepted outcomes, manual operations, review time, orchestrator
context, retries, escalations, false greens, candidate-to-acceptance yield, latency, cost,
resource use, and scope or target-integrity events. Compare similar task classes and keep
security, privacy, authority, and evidence quality as boundaries rather than values that
can be traded away inside one score.

Separate one-time experiment or integration setup from steady-state cost. An early harness
trial can be expensive without showing what repeated, already-integrated delegation will
cost.

## Learn from the first causal failure

```text
observe the failure
  → identify the first responsible layer
  → choose the smallest discriminating experiment
  → change only that layer
  → rerun focused evidence
  → continue, stop, or escalate
```

Do not retry blindly. Each attempt should name what it is testing and what changed.

Ambiguous authority, privacy, persistence, native-state, or shared-target failures usually
stop immediately. Two materially different attempts are a useful ordinary default. Cheap,
reversible experiments can receive more attempts when each one teaches something and the
task sets a clear limit.

If an aggregate score passes while a case designed to catch a real defect still fails,
make one cheap causal correction and rerun that evidence. Do not hide the failure inside
the score or chase perfection indefinitely.

## Preserve only reusable lessons

Create a durable failure record when the lesson is novel, recurring, high impact, or
changes a reusable evaluator, route, qualification, or policy. Reference the raw evidence
instead of copying full transcripts into shared context.

An ordinary typo or one-off failed test does not need incident ceremony. A reusable lesson
becomes active only after its causal explanation and affected check are reviewed. Workers
cannot change their own authority, qualification, or routing policy.

Reuse current evaluator and route qualifications until a named invalidation trigger fires.
After drift, rerun the affected slice. Reserve broad fresh-environment suites for first
proof, material runtime or schema changes, suspected cache dependence, release, or a
failure that calls earlier proof into question.

## Simplification counts as progress

Periodically ask:

- Which artifacts are actually used to make decisions?
- Which checks catch realistic failures?
- Which steps can now be automated cheaply?
- Which fields can be inherited or generated?
- Which reviews can be removed without weakening evidence or authority?

The right operational decision may be to advance, hold, roll back, or simplify. A method
that only grows has stopped evaluating itself.
