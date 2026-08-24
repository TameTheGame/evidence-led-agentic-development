# Start Here

ELAD helps coding agents do meaningful engineering work with evidence strong enough to
justify each next step. It is designed to reduce routine supervision without confusing
agent capability with permission or agent confidence with proof.

If this is your first visit, start with [First Run](docs/FIRST_RUN.md). It gives your
coding agent a small procedure for one task and keeps the decisions that matter with you.

## The method in one minute

For each step:

1. Say what outcome you want and what the agent may change.
2. Identify the uncertainty most likely to change the plan.
3. Choose the cheapest check that can reliably resolve it.
4. Let the agent make the smallest useful change and inspect the result.
5. Continue, increase rigor, or stop based on the evidence.

That loop can fit inside one prompt and one test. It does not require a protocol packet,
receipt, or independent reviewer unless the task gives those things a real job.

## The agent chooses the smallest useful path

- **Light:** a confined change with a trustworthy deterministic check.
- **Bounded:** a task with moderate coupling or a handoff that needs a short written
  boundary.
- **Evaluated:** behavior that needs representative examples, runtime observation, or a
  fallible semantic judge.
- **Assured:** consequential work that warrants isolation, independent expectations,
  recovery evidence, or separate review.

Start with `light`. Escalate when evidence reveals more uncertainty, consequence, or
coupling than expected. Simplify when a reusable check has made the work predictable.

These profiles describe evidence effort, not permission. Scope and authority come from
you and the project being changed.

## What you do not need for a small task

You do not need to create every schema, manifest, receipt, capability certificate, gate,
or review. A clear request plus an existing test can be a complete light task.

For one small written card, use
[`LIGHT_TASK.template.md`](templates/LIGHT_TASK.template.md). For a finite handoff to
another worker, use
[`BOUNDED_WORKER_PACKET.template.md`](templates/BOUNDED_WORKER_PACKET.template.md).

## Read the next page only when you need it

| Your next question | Read |
|---|---|
| How do I try one task? | [First Run](docs/FIRST_RUN.md) |
| How do I choose a rigor profile? | [Adaptive Rigor](docs/ADAPTIVE_RIGOR.md) |
| How do I adopt this across a project? | [Adoption Runbook](docs/ADOPTION_RUNBOOK.md) |
| What evidence fits an uncertain claim? | [Evaluation and Evidence](docs/EVALUATION_AND_EVIDENCE.md) |
| When should I qualify a model or harness? | [Model and Harness Qualification](docs/MODEL_QUALIFICATION.md) |
| What decisions should remain with me? | [Decisions You Keep](docs/HUMAN_DECISION_BOUNDARY.md) |
| What can a project safely automate today? | [Maturity Model](docs/MATURITY_MODEL.md) |
| How do I implement the formal protocol? | [Architecture](docs/ARCHITECTURE.md) and [Conformance](docs/PROTOCOL_030_CONFORMANCE.md) |
| What has ELAD actually demonstrated? | [Empirical Status](docs/EMPIRICAL_STATUS.md) |

> ## Agent instructions: entering this repository

Read only what the task needs:

1. `AGENTS.md`
2. `STATUS.md`
3. `blueprint.json`
4. `MANIFEST.md`
5. the exact task-selected document, schema, fixture, or test

Do not preload the repository or infer permission to change another project, run a model,
start a target runtime, accept evidence, or promote a candidate.

## What success looks like

- Small deterministic work stays small.
- Uncertain behavior produces examples and error analysis that guide the next change.
- Consequential work receives stronger and more independent evidence.
- Agents return compact results instead of making you follow every tool call.
- Reusable checks reduce future work instead of creating recurring paperwork.
- The process stops when enough evidence exists.

ELAD is a **Level 0 reference blueprint**, not a live controller. Its current evidence is
bounded; see [Empirical Status](docs/EMPIRICAL_STATUS.md). The target project always owns
its code, authority, evidence, and final decisions.
