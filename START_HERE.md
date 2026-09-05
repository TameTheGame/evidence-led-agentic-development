# Start Here

ELAD helps coding agents do meaningful engineering work with evidence strong enough to
justify each next step. It is designed to reduce routine supervision without confusing
agent capability with permission or agent confidence with proof.

If this is your first visit, start with [First Run](docs/FIRST_RUN.md). It gives your
coding agent a small procedure for one task and keeps the decisions that matter with you.

## How you use it

Tell your coding agent what you want in ordinary language. You can also hand it a project
and ask, “What is the next useful step?”

```text
Use ELAD with this project. I want <high-level outcome>.
```

```text
Use ELAD with this project. What is the next useful step?
```

The agent—not you—turns that into the next bounded task. It reads the project rules,
chooses an appropriate check, does the work, inspects the result, and decides whether to
continue or stop. It comes back to you when a missing decision would change the intended
outcome, authority, or an important product tradeoff.

You do not need to complete a questionnaire, decompose the project, choose a rigor label,
or specify evidence for every step.

## The agent chooses the smallest useful path

Direct lets the capable primary agent complete your authorized outcome. Select Conserve
when you want eligible cheaper or local execution. [Operating Modes](docs/OPERATING_MODES.md)
defines this choice separately from the rigor profiles below.

- **Light:** a confined change with a trustworthy deterministic check.
- **Bounded:** a task with moderate coupling or a handoff that needs a short written
  boundary.
- **Evaluated:** behavior that needs representative examples, runtime observation, or a
  fallible semantic judge.
- **Assured:** consequential work that warrants isolation, independent expectations,
  recovery evidence, or separate review.

The agent starts with `light`, escalates when evidence reveals more uncertainty,
consequence, or coupling than expected, and simplifies when a reusable check has made the
work predictable.

You do not have to select a profile. These labels describe the evidence effort behind the
work, not permission. Scope and authority still come from you and the project being
changed.

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
| How does the agent choose a rigor profile? | [Adaptive Rigor](docs/ADAPTIVE_RIGOR.md) |
| How do I adopt this across a project? | [Adoption Runbook](docs/ADOPTION_RUNBOOK.md) |
| What evidence fits an uncertain claim? | [Evaluation and Evidence](docs/EVALUATION_AND_EVIDENCE.md) |
| When should I qualify a model or harness? | [Model and Harness Qualification](docs/MODEL_QUALIFICATION.md) |
| How do I compare exact local model-and-harness subjects fairly? | [Model and Harness Readiness Evaluation](docs/MODEL_HARNESS_READINESS_EVALUATION.md) |
| What decisions should remain with me? | [Decisions You Keep](docs/HUMAN_DECISION_BOUNDARY.md) |
| What can a project safely automate today? | [Maturity Model](docs/MATURITY_MODEL.md) |
| How do I implement the formal protocol? | [Architecture](docs/ARCHITECTURE.md) and [Conformance](docs/PROTOCOL_040_CONFORMANCE.md) |
| What has ELAD actually demonstrated? | [Empirical Status](docs/EMPIRICAL_STATUS.md) |

> ## Agent instructions: entering this repository

Read `AGENTS.md`, then its task-selected context. Consult `STATUS.md` for milestone or
release questions, `blueprint.json` for version or contract claims, and `MANIFEST.md` to
locate the exact affected document, schema, fixture, or test.

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
