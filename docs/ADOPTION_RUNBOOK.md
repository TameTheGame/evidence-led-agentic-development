# Adoption Runbook

Adopt the smallest part of ELAD that improves the work in front of you. A project can
begin with one small task and its existing tests. Add reusable evaluators, worker
qualification, or formal assurance only when repeated work or consequential effects make
them worthwhile.

> Scope and authority are mandatory; ceremony is proportional.

Begin with the target project's actual rules. If authority is missing or contradictory,
stop and ask the owner. ELAD never supplies permission that the project has not granted.

## 1. Start with one light task

Choose a confined, reversible, low-consequence change with a trustworthy exact check:

```text
observable outcome and allowed scope
  → implementation
  → named check and expected result
  → diff inspection
  → completion or escalation
```

An existing request plus a test command may be enough. The optional
[light-task template](../templates/LIGHT_TASK.template.md) is available when saving the
task card would help. Do not create JSON records, manifests, certificates, independent
reviews, or formal receipts unless they add evidence the task actually needs.

If this works, you have adopted the core method. You can stop here.

## 2. Establish a project baseline before broader autonomy

When an agent will work repeatedly or across a wider surface, first inspect the project
read-only. Find:

- the owner, repository instructions, allowed paths, and prohibited effects;
- existing tests, runtime checks, and known false-green cases;
- source, generated, secret, data, deployment, and publication boundaries;
- branch, worktree, review, promotion, and rollback rules; and
- the current amount of manual operation, retries, context, time, and cost.

Record only what is needed to make future decisions. Unknown values should remain unknown.
If the project consumes a formal ELAD release, pin its exact version and protocol bundle;
do not give a floating checkout authority over the project.

A small owner-local overlay might contain only:

```text
AGENTS.md
STATUS.md
WORKFLOW.md
```

The target project owns these files. Shared ELAD templates can help start them, but they
do not replace local authority.

If one-context tasks and existing checks remain sufficient, stop here.

## 3. Add evaluation when exact tests cannot settle quality

Use [Adaptive Rigor](ADAPTIVE_RIGOR.md) to choose the lightest defensible profile. Keep
each claim with its own evidence:

- exact behavior stays with deterministic checks;
- semantic or stochastic behavior uses representative cases and a calibrated evaluator;
- live operational behavior uses evidence from the relevant runtime; and
- product meaning or experience stays with the owner when automation cannot decide it.

Reuse existing evaluators. For a new fallible evaluator, establish known-good and
known-bad cases, failure behavior, identity, and invalidation triggers. Routine tasks can
then cite that calibration and run only the focused cases they need.

Do not escalate an entire task merely because one neighboring claim is uncertain. See
[Evaluation and Evidence](EVALUATION_AND_EVIDENCE.md) for mixed-claim examples.

If evaluation now gives the agent a reliable stopping rule, stop here.

## 4. Add bounded delegation when work crosses contexts

When another worker or context will implement a task, give it:

- one observable outcome;
- only the relevant context;
- allowed paths, tools, and effects;
- a supplied verifier or expected result;
- practical output, attempt, time, and resource limits; and
- explicit completion and escalation states.

Keep candidate work separate from target or promotion state, and have the worker return a
compact result with focused evidence rather than a full transcript. Start from the
[bounded-worker template](../templates/BOUNDED_WORKER_PACKET.template.md) when a saved
packet is useful.

Another model's participation does not make an exact product claim stochastic. Escalate
only for the uncertainty or risk the handoff actually adds.

If assignments are supervised, finite, and independently checked, stop here.

## 5. Qualify routes used for repeated autonomy

Formal model-and-harness qualification is useful when the same route will repeatedly act
without close supervision, when its safe context or tool horizon matters, or when it will
receive broader effects or machine-evidence authority.

Qualify the exact model, runtime, harness, adapter, prompt/context compiler, tool surface,
resource envelope, and task class. Test representative successes, proportionate failures,
inaccessible holdouts, and cold repeats when variance matters. Begin read-only or in
shadow, then move to disposable candidate work before granting a wider route.

Store the result once and reuse it until a named drift trigger fires. A worker cannot
renew its own qualification. See [Model and Harness Qualification](MODEL_QUALIFICATION.md).

If the route remains candidate-only and the target owner performs final verification,
stop here.

## 6. Add target controls only for consequential effects

Use stronger controls when work can affect shared runtime state, opaque native artifacts,
durable data, production, promotion, or publication.

- Let the target project own narrow tools for its own artifact and runtime surfaces.
- Use the target system's authoritative serializer for opaque formats, then save, reload,
  and verify the result.
- Add ownership leases or fencing only where overlapping writers or stale completion are
  realistic risks.
- Separate candidate finalization, target execution, acceptance, promotion, and
  publication when their consequences require separate decisions.
- Test recovery, uncertain ownership, stale/replayed completion, and cleanup before
  activating the effect.

Full assured packets and formal receipts belong here when exact identity and auditable
closure matter. Their implementation is described in the [protocol conformance
reference](PROTOCOL_040_CONFORMANCE.md).

## 7. Measure whether the method is helping

Compare the new workflow with the prior one using measures that can change a decision:

- accepted evidence-backed outcomes;
- manual operations and review time;
- orchestrator context and tool use;
- retries, escalations, and false greens;
- latency, cost, and local resource use; and
- security, privacy, scope, or target-integrity events.

Separate one-time setup from steady-state cost. Advance when the evidence supports the
next capability. Hold when proof is missing. Roll back for authority, security, privacy,
false-green, or target-integrity failures. Simplify when recurring scaffolding costs more
than the uncertainty it resolves.

Create durable gates for reusable capabilities or consequential transitions, not for
every ordinary feature. A project that never needs the later stages can remain a valid,
useful ELAD adopter at the light path.
