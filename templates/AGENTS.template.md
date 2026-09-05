# AGENTS.md — <Project name>

## Mission

<One paragraph describing the product and the bounded role of agents.>

## Task-selected context

Read only the current context needed for the outcome. Check `STATUS.md` when milestone or next-action state matters. Before a governed effect, inspect <active authority record, if implemented> and its applicable current fields. Read the relevant `WORKFLOW.md` section for delivery rules; use `MANIFEST.md` to locate ownership; select the exact product, architecture, source, and evidence records needed for the change.

A small mechanical edit does not require the entire orientation bundle. Scope, authority, hold, data, and acceptance boundaries remain mandatory for their applicable effects.

## Authority

- Product intent owner: <owner>
- Delivery workflow authority: `WORKFLOW.md`
- Current facts/next action: `STATUS.md`
- Machine hold/activation: <record or not implemented>
- Unknown consequential scope, risk, data, effect, or identity: deny.
- A tool, packet, profile, rigor selection, certificate, or lease never grants authority.
- Scope and authority are mandatory; ceremony is proportional.

## Adaptive task rigor

Project maturity, task rigor, and effect authority are separate.

- `light`: confined/reversible/low consequence with a proven deterministic check.
- `bounded`: moderate coupling/regression or a compact handoff.
- `evaluated`: stochastic, semantic, experiential, runtime-dependent, or otherwise
  behaviorally uncertain product claims.
- `assured`: foundational, security/privacy, irreversible, target-native, production,
  promotion, or other high-consequence work.

Start with the cheapest reliable evidence. Escalate when evidence reveals a weaker
oracle, wider scope, worse reversibility, higher consequence, or unresolved human claim.
Agentic development does not by itself make a deterministic product claim stochastic.
Executing a program does not by itself make an exact claim runtime/operational.

## Repository zones

| Path | Role | Write policy |
|---|---|---|
| `<path>` | <source/generated/native/evidence/etc.> | <policy> |

## Artifact routing

- Ordinary source: <writer/checks>
- Target-native/opaque artifacts: <authoritative serializer and target-owned facade>
- Runtime/deployment: <registered harness>
- Human-only decisions: <list>

## Lifecycle

1. State the learning question, outcome, scope, and effect authority.
2. Split mixed claims, classify evaluator maturity per claim, and select rigor plus the
   cheapest reliable evidence.
3. Compile only the context the worker needs.
4. Reuse current evaluator calibration; add a negative only for evaluator changes, new
   failure modes, or consequential false-green risk.
5. Execute the smallest useful change or experiment.
6. Observe, evaluate, classify the first causal failure, and choose the next change.
7. Return a compact result; use full manifests/receipts only when the selected profile or
   handoff warrants them.
8. Request retained human judgment after objective prerequisites pass.
9. Finalize, promote, and publish separately.

## Non-goals and safety

- <Project-specific forbidden actions.>
- Do not promote or publish from a candidate-worker context.
- Do not edit opaque target-owned bytes outside their authoritative serializer.
- Preserve unrelated work.
- Never retry blindly. Use the task's experiment budget; ambiguous consequential state
  normally stops immediately.
