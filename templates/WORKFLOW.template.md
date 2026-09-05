# Delivery Workflow

This document routes work. Product intent, architecture, security, acceptance, promotion,
and publication remain owned by their named authorities.

## Authority by domain

| Domain | Authority |
|---|---|
| Product direction | <owner/document> |
| Accepted architecture | <decision record> |
| Safety and data policy | `AGENTS.md` and <policy> |
| Delivery procedure | This file |
| Current facts and next action | `STATUS.md` |
| Machine hold/activation | <record or not implemented> |

## Universal learning loop

For each material step:

1. State what must be learned or established.
2. Identify the uncertainty that could change the decision.
3. Choose the cheapest reliable evidence.
4. Build the smallest useful change or experiment.
5. Observe outputs, behavior, and traces.
6. Analyze the first causal error.
7. Choose the next smallest change, stop, or escalate rigor.

## Select task rigor

Select Direct or explicit Conserve through the adopting project's pinned
[Operating Modes](../docs/OPERATING_MODES.md) guidance. Direct owns authorized delivery
end to end; Conserve uses eligible cheaper/local subjects with their required containment.
Mode is independent of rigor and authority. Neither label grants effects or lowers the
acceptance threshold. Keep this link bound to the adopted ELAD revision when copying.

Task rigor is independent of project maturity and effect authority.

| Profile | Use | Required recurring work |
|---|---|---|
| `light` | confined, reversible, low-consequence, exact existing oracle | outcome/scope, change, exact check, diff |
| `bounded` | moderate coupling/regression/cross-context handoff | compact brief, targeted checks, concise result |
| `evaluated` | stochastic/semantic/agentic/runtime uncertainty | baseline/eval cases, outputs/traces, error analysis, iteration |
| `assured` | foundational, security/privacy, irreversible, target-native, production/promotion | frozen contract, isolation, independent expectations, negatives, recovery, independent review |

Start at the cheapest profile supported by facts. Escalate on unexpected coupling,
evaluator weakness, stochastic failure, irreversible effects, or unresolved human
claims. Simplify when recurring ceremony does not alter decisions.

## Review budget and causal revalidation

Use the least expensive durable mechanism that prevents the validated failure. Select
assurance depth and verification frequency from uncertainty, consequence, reversibility,
recurrence, and expected lifecycle cost. Hard default limits are Quick: at most one
critic pass plus decisive checks; Standard: at most one complete review/correction cycle;
High assurance: at most two complete cycles. Corrections consume the current budget, and
candidate recreation, renaming, or reframing does not reset it.

Revalidate only the claims and evidence a change can causally affect. Require a complete
fresh review only when the causal footprint cannot be bounded or a specified
high-consequence shared surface changes. An extra cycle requires unresolved
high-consequence uncertainty plus new objective evidence, or fresh explicit owner
authorization after reporting expected cost and benefit. At exhaustion, stop with
`BLOCKED`, `REVISE`, or a narrower claim; never lower the acceptance threshold.

Use Git commit/blob identity and clean/dirty state for ordinary tracked artifacts. Add
raw hashes only when Git cannot identify external, ignored, generated, transported, or
otherwise non-Git evidence. Select delivery mode through Operating Modes; reuse sufficient
verification without an automatic duplicate cloud pass.

## Adaptive task loop

1. Confirm exact scope and effect authority.
2. Select rigor and evidence layers.
3. Reuse current evaluator calibration; add task-specific negatives only for new or
   consequential false-green risks.
4. Read only the needed context. Supply bounded packets and tool/resource limits for
   selected constrained delegates; full records remain conditional on the effect/handoff.
5. Execute one coherent change on the appropriate surface.
6. Run the cheapest discriminating check first.
7. Retry only with a causal hypothesis and changed layer, inside the task's experiment
   budget.
8. Complete authorized implementation, verification, and causal repair before returning
   a compact result; keep raw logs file-backed.
9. Request only retained human judgment after objective prerequisites are green.
10. Finalize, promote, and publish separately where applicable.
11. Record only durable facts or reusable causal lessons.

## Writer and concurrency

- Active writer: <exact identity or none>
- Candidate surface: <surface>
- Scarce target/runtime/data surfaces: <surfaces>
- Parallel read-only/isolated candidates: <policy>
- Lease/fencing trigger and maturity: <policy>

Do not require fencing for read-only or isolated light work. Use exact fenced ownership
for overlapping consequential effects.

## Human boundary

Retained decisions: <list>.

Human cards contain exact identity, short actions, expected result, stop evidence,
limitations, and reply format. They are used only when a human-observable claim remains.

## Finalization

Define candidate checkpoint, technical evidence, human acceptance, candidate
finalization, promotion, and publication separately. A worker cannot grant itself a
broader effect or acceptance state.
