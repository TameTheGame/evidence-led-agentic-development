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

## Adaptive task loop

1. Confirm exact scope and effect authority.
2. Select rigor and evidence layers.
3. Reuse current evaluator calibration; add task-specific negatives only for new or
   consequential false-green risks.
4. Compile only the needed context. Generate full packets/manifests only for assured or
   cross-context work.
5. Execute one coherent change on the appropriate surface.
6. Run the cheapest discriminating check first.
7. Retry only with a causal hypothesis and changed layer, inside the task's experiment
   budget.
8. Return a compact result; keep raw logs file-backed.
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
