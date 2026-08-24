# Start Here

Evidence-Led Agentic Development is a practical way to let cloud and local AI agents do
substantial engineering work without asking a human to supervise every tool call—or
pretending uncertain behavior is correct because a model says so.

This repository is currently a **non-operational Level 0 blueprint**. Nothing here is a
live controller or permission grant.

If this is your first visit, use the [short first-run walkthrough](docs/FIRST_RUN.md) before
reading the formal contracts. For a precise account of what has and has not been tested,
see [Empirical Status](docs/EMPIRICAL_STATUS.md).

## In one minute

Every development step begins with seven questions:

1. What are we trying to learn or establish?
2. Which uncertainty matters most right now?
3. What is the cheapest reliable evidence that would resolve it?
4. Should that evidence come from code, runtime behavior, traces, a model, a human, or a
   combination?
5. What did the evidence reveal?
6. What should change next?
7. Is there enough evidence to stop?

The answer determines the task's rigor:

- **Light:** make the confined change, run the trusted deterministic check, inspect the
  diff, finish.
- **Bounded:** use a compact brief, focused tests, and a concise handoff.
- **Evaluated:** freeze representative cases, inspect outputs/traces, analyze errors,
  and iterate.
- **Assured:** use isolated candidates, independent expectations, negative controls,
  recovery, and independent or adversarial review.

These profiles describe evidence effort, not permission. Project maturity describes
what infrastructure is proven; target authority describes what an episode may change.
They are separate decisions. Scope and authority are mandatory at every profile;
ceremony is proportional. If authority is unknown, stop rather than infer it.

## How agents divide the work

A cloud orchestrator protects the long-horizon context: it shapes tasks, selects the
right worker and rigor, and reads compact results. Bounded sub-agents or local workers do
repetitive implementation, exploration, testing, and evidence collection. A local model
gets a smaller precompiled packet, capped tools and outputs, and explicit stop states
sized to its exact harness and measured capability.

The same model in two harnesses is two execution subjects. A coding-agent harness and a
product-inference API are also separate subjects even when they load the same weights.
A model or harness name never grants authority. Repeated autonomous delegation needs
empirical qualification; a supervised one-off light task may not. Delegation raises
rigor only for uncertainty or risk it actually adds—the mere presence of an AI developer
does not turn deterministic product behavior into a stochastic claim.

## What you do not need for a small task

You do not need to create every JSON template, evidence manifest, receipt, gate,
capability certificate, negative suite, or independent review. A clear issue or prompt
plus a named deterministic check can be a complete `light` contract. Use
[LIGHT_TASK.template.md](templates/LIGHT_TASK.template.md) only when a small written card
helps.

For an ordinary bounded worker handoff, use the compact
[BOUNDED_WORKER_PACKET.template.md](templates/BOUNDED_WORKER_PACKET.template.md). It is
deliberately smaller than the assured JSON task packet.

The strict packet and receipt chain remains available for cross-context autonomous or
high-consequence work. It is reusable assurance infrastructure, not everyday ceremony.

## If you are a project owner

Read:

1. [Adaptive Rigor](docs/ADAPTIVE_RIGOR.md)
2. [Principles](docs/PRINCIPLES.md)
3. [Adoption Runbook](docs/ADOPTION_RUNBOOK.md)
4. [Human Decision Boundary](docs/HUMAN_DECISION_BOUNDARY.md)
5. [Maturity Model](docs/MATURITY_MODEL.md)

Begin with the smallest workflow that resolves real uncertainty. Add machinery only
when it prevents a realistic failure, improves a recurring handoff, or unlocks useful
autonomy.

## If you are an agent entering this repository

Read only:

1. [AGENTS.md](AGENTS.md)
2. [STATUS.md](STATUS.md)
3. [blueprint.json](blueprint.json)
4. [MANIFEST.md](MANIFEST.md)
5. the exact task-selected document, schema, fixture, or test.

Do not preload the repository. Do not infer permission to change another repository,
run a model, start a target runtime, create a certificate, accept evidence, or promote a
candidate.

## If you are adopting ELAD

1. Pin a version/commit/digest instead of depending on a floating sibling checkout.
2. Inspect the target's authority, artifact lanes, tests, human decisions, and risks.
3. Name the material claim classes and their uncertainty; do not classify a claim as
   runtime merely because a program executes.
4. Select a task-rigor profile independently of the project's maturity level.
5. Reuse existing tests and calibrated evaluators before building new ones. Treat a new
   exact regression separately from an unproven fallible evaluator.
6. Add candidate isolation, strict packets, qualification, fencing, or target adapters
   only when the work's risks justify them.
7. Keep activation, promotion, and publication owner-local and separate.
8. Stop reading when another ELAD layer would not change the task, evidence, or authority
   decision.

The target owns its code, adapters, gates, evidence, and final decisions. This blueprint
cannot launder authority between repositories.

## What success looks like

- Small deterministic work stays small.
- Uncertain work produces visible examples, traces, and error analysis that guide the
  next experiment.
- High-consequence work has independent evidence and a recovery path.
- Orchestrators see compact receipts instead of hundreds of low-level tool calls.
- Local workers receive tasks that fit their measured context, tool, and resource
  envelope.
- Human attention is reserved for intent, product judgment, trust, subjective
  experience, publication, and conditions automation cannot reliably observe.
- Reusable validators are cheap to invoke; per-task paperwork exists only when it adds
  discriminating evidence or protects a meaningful boundary.

## Validate this blueprint

With Python 3.10 or newer:

```text
python tools/validate_all.py
```

Windows users may instead run `py -3 tools/validate_all.py`. The terminal output must
end by stating that no authority is granted. This validates only the inert reference
repository; it does not prove a live model, project, target, runtime, reviewer decision,
or cross-platform environment.
