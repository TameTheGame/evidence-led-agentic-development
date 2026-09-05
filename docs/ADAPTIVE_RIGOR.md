# Adaptive Rigor

ELAD does not ask every task to carry the same process. It asks:

> What is the cheapest reliable evidence that can resolve the uncertainty that matters
> now?

A small documentation fix with a dependable link check should stay small. A feature
whose quality depends on model behavior, live runtime state, or a consequential external
effect needs more evidence. Right-sizing the scaffolding keeps agents moving without
removing the controls that make their autonomy trustworthy.

## The seven-question loop

These are questions for the agent or orchestrator to answer from the owner's request,
project rules, and available evidence. They are not a questionnaire for the owner.

For each useful step, the agent asks:

1. What observable outcome does the request imply?
2. What uncertainty could prevent it?
3. What is the cheapest evidence that can settle that uncertainty?
4. What is the smallest useful change or experiment?
5. What did the result and first meaningful failure reveal?
6. Should the work continue, change direction, escalate, or stop?
7. Is there enough evidence to consider the step complete?

For a light task, the request, repository rules, one existing test, and a diff may contain
the whole loop. Add durable records only when work crosses contexts, authority boundaries,
scarce targets, or consequential decisions.

## Keep three decisions separate

- **Project maturity:** what the project has already proven it can support.
- **Task rigor:** how much evidence this particular task needs.
- **Effect authority:** what the current work may read, change, run, publish, or accept.

A mature project can still use a light task. A read-only audit can still require strong
review. Selecting a rigor profile never grants authority; permission comes from the
target project and its owner.

## Choose the lightest defensible profile

| Profile | Use it when | Typical path |
|---|---|---|
| `light` | The task is confined, reversible, low consequence, and settled by a trustworthy exact check. | contract → change → deterministic check → diff → stop |
| `bounded` | Moderate coupling, regression risk, managed rollback, or a finite handoff adds ordinary engineering uncertainty. | light path + explicit limits, failure stop, and focused integration or recovery evidence |
| `evaluated` | A material claim is semantic, stochastic, experiential, or dependent on live runtime behavior. | bounded contract + representative cases, error analysis, and a deliberate iteration decision |
| `assured` | Failure could affect security, privacy, rights, durable data, production, publication, or another difficult-to-reverse surface. | evaluated path + stronger identity binding, independent expectations, verification, and effect-specific safeguards |

Start with `light`. Move up only when a known fact requires it. A short implementation can
still be assured if its consequences are high, while a large but deterministic cleanup
may remain bounded.

Ask these questions when the choice is unclear:

- Are the expected outputs exact, or is quality partly a matter of behavior or judgment?
- Is the change local, integrated across components, or foundational?
- Can an ordinary source revert recover it?
- What happens if the evidence gives a false green?
- Can an exact check settle each claim, or is a fallible evaluator involved?
- Does work cross into another context, worker, runtime, repository, or external system?

Do not average away one decisive risk. A security or irreversible-effect concern can set
the floor for the task even when everything else looks simple.

## Match evidence to each claim

Use the lowest-cost check that can reliably distinguish success from failure:

1. an existing compiler, type check, unit test, calculation, or exact comparison;
2. a focused regression with expected behavior defined independently of the code under
   test;
3. a live observation, trace, log, screenshot, or saved-and-reloaded result;
4. a calibrated semantic evaluator for behavior exact code cannot judge;
5. retained owner judgment for product meaning, experience, trust, rights, or adoption;
6. independent or adversarial verification when consequence warrants it.

One task can contain several kinds of claims. A command-line feature might have exact
claims about its flag, exit code, and schema, plus a semantic claim about a generated
summary. Keep the exact claims deterministic and evaluate only the semantic claim.

Evaluator maturity is classified per claim. A newly written exact regression is not
automatically a fallible evaluator if its expected result comes from an independent
requirement. A semantic judge in the same task may still be unproven and need calibration.

Executing a program does not by itself make a claim runtime/operational. Exact output,
exit status, fixtures, and mocked failure behavior may remain deterministic. Require live
runtime evidence when truth depends on timing, persistence, native effects, distributed
state, or another property an exact comparison cannot establish.

For practical examples, see [Evaluation and Evidence](EVALUATION_AND_EVIDENCE.md).

## Avoid circular proof

The implementation should not manufacture the expectation used to declare itself
correct. The needed separation depends on the risk:

- A light task can use an existing test, independently specified invariant, or
  predeclared expected value.
- Bounded work may add an independent fixture, focused regression, or separate system
  observation.
- Evaluated work may need held-out cases and known-good and known-bad examples for a
  fallible evaluator.
- Assured work may separate implementation, expected behavior, verification, and
  acceptance roles.

Model confidence and self-review can be useful signals, but they are not proof. Reuse a
calibrated evaluator until its logic, runtime, dependencies, target, or claim class drifts,
or a new false-green pattern appears.

## Proportional assurance budgets and causal revalidation

A durable control is justified when its expected lifecycle cost is lower than the
expected cost of recurrence, unless a specifically identified high consequence warrants
more. Lifecycle cost includes authoring, execution, maintenance, review, invalidation,
and false-positive handling. Use the least expensive durable mechanism that prevents the
validated failure. Passing an assurance system's own tests proves internal consistency;
it does not prove that the system is worth its complexity.

Assurance depth and verification frequency are selected separately from task rigor
according to uncertainty, consequence, reversibility, recurrence, and expected lifecycle
cost. These hard defaults bound the review itself:

- Quick: at most one critic pass plus decisive checks.
- Standard: at most one complete review/correction cycle.
- High assurance: at most two complete review/correction cycles.

A complete cycle includes critique, adjudication, accepted correction, and decisive
verification. Corrections consume the current budget; renaming, recreating, or reframing
a candidate does not reset it. An extra cycle requires unresolved high-consequence
uncertainty together with new objective evidence, or fresh explicit owner authorization
after the expected cost and benefit have been reported. When the budget is exhausted,
stop with `BLOCKED`, `REVISE`, or a narrower claim. Never silently lower the acceptance
threshold.

A change invalidates only the claims and evidence it can causally affect. Revalidate that
scope and retain unaffected review evidence. Require a complete fresh review only when
the causal footprint cannot be bounded or the change alters architecture, authority,
evidence meaning, security/privacy/rights boundaries, evaluator semantics, or another
specified high-consequence shared surface.

For ordinary Git-tracked artifacts, use Git commit and blob identity together with
clean/dirty state. Add raw byte counts or hashes only for external, ignored, generated,
transported, or otherwise non-Git artifacts when Git cannot supply the needed identity.
Select delivery mode through [Operating Modes](OPERATING_MODES.md). Direct supports
primary-agent completion; Conserve explicitly selects eligible cheaper or local work.
Mode is independent of rigor and authority. Reuse sufficient verification without an
automatic duplicate cloud pass; require separate independence when the claim warrants it.

## Escalate only when evidence tells you to

Escalate when you discover unexpected nondeterminism, wider scope, weaker reversibility,
higher consequences, an evaluator that cannot discriminate the result, a live effect, or
an unresolved security, privacy, rights, persistence, or authority concern.

Escalation does not widen authority. If the new work falls outside the approved scope,
stop and ask for a fresh decision.

When one cheap causal fix can resolve a failure exposed by the evaluator, change that one
factor and rerun the affected evidence. Do not ignore a known defect because an aggregate
score passed, and do not turn every imperfection into open-ended optimization.

## Reusable infrastructure versus recurring work

Later tasks can use less scaffolding when:

- a once-uncertain behavior now has a dependable exact check;
- a reusable evaluator or worker route has been qualified;
- the scope, effects, or delegation distance has shrunk; or
- an extra review layer repeatedly fails to detect any realistic problem.

Keep reusable authority, evaluators, harnesses, recovery checks, and qualification records
instead of rebuilding them per task. Recurring work should usually contain only the
change, its smallest relevant check, and a concise result.

For a low-risk deterministic task, this is enough:

```text
request and repository authority → change → deterministic check → diff → completion
```

Use the optional [light-task template](../templates/LIGHT_TASK.template.md) when saving a
small task card would help. There is no mandatory JSON task-rigor decision. Use
machine-readable rigor decisions, manifests, packets, and receipts only when routing,
cross-context handoff, auditability, or consequence makes them useful. Their exact
implementation lives in the [protocol conformance
reference](PROTOCOL_05_CONFORMANCE.md), not in the everyday path.

The goal is not the largest control plane. It is reliable engineering progress with the
least routine supervision, context, compute, latency, cost, and risk the work requires.
