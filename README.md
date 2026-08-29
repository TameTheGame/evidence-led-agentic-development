# Evidence-Led Agentic Development

**Use the cheapest reliable evidence that can justify the next action.**

Evidence-Led Agentic Development (ELAD) is a provider-neutral method for building
software with coding agents. It helps agents do substantial work without treating model
confidence as proof or forcing every task through the same amount of process.

This repository is a **Level 0 reference blueprint**. It provides guidance, optional
templates, synthetic examples, and dependency-free checks. It does not run a model,
control another repository, or grant an agent permission to change anything.

## Why ELAD

Coding agents are capable of more than completing isolated snippets. They can inspect a
project, plan a change, implement it, run checks, analyze failures, and try again. The
hard part is deciding how much structure that work needs and what evidence is strong
enough to continue.

Too little structure can let an agent drift beyond the request, confuse activity with
progress, or judge its own work too generously. Too much structure can turn a small fix
into a pile of briefs, manifests, gates, and reviews that cost more than the change.

ELAD is designed for the useful middle:

- **Right-size the scaffolding.** A small deterministic fix can stay small. Uncertain or
  consequential work earns stronger evaluation, isolation, and review only when those
  safeguards can resolve a real risk.
- **Enable evidence-backed autonomy.** Clear scope, trustworthy checks, and explicit stop
  conditions let an agent plan, build, test, diagnose, and iterate without you supervising
  every tool call.
- **Let results guide the next step.** Evaluation happens during development, so failures
  point to the next useful change instead of appearing only at the end.
- **Keep authority separate from capability.** An agent may be capable of doing something
  without being allowed to do it. Permission still comes from you and the project being
  changed.
- **Reuse what is expensive.** Good tests, calibrated evaluators, project rules, and
  qualification evidence can be built once and reused instead of recreated for every
  task.

This is what makes autonomous agentic development practical: the agent has room to do the
engineering work, while evidence and explicit boundaries decide whether it should
continue. The goal is not maximum automation or maximum process. It is reliable progress
with less routine supervision and no more machinery than the work can justify.

ELAD has been tested beyond its own conformance suite. In a four-part reference project,
it guided deterministic single-agent development, cold adoption, bounded delegation to a
different model, and a semantic feature whose evaluation caught a real defect that the
deterministic tests missed. Those results are meaningful empirical support for the method
in a bounded software project. They are not yet proof of production-scale automation or
universal applicability. See [Empirical Status](docs/EMPIRICAL_STATUS.md) for the results
and their limits.

## Start here

- **Trying ELAD for the first time:** give your coding agent the
  [First Run](docs/FIRST_RUN.md) guide.
- **Want the short explanation:** read [Start Here](START_HERE.md).
- **Choosing how much process a task needs:** read
  [Adaptive Rigor](docs/ADAPTIVE_RIGOR.md).
- **Adopting ELAD across a project:** use the
  [Adoption Runbook](docs/ADOPTION_RUNBOOK.md).
- **Implementing the protocol:** begin with [Architecture](docs/ARCHITECTURE.md),
  [Conformance](docs/PROTOCOL_040_CONFORMANCE.md), and the [manifest](MANIFEST.md).
- **Comparing local coding models or harnesses for repeated ELAD work:** read
  [Model and Harness Readiness Evaluation](docs/MODEL_HARNESS_READINESS_EVALUATION.md)
  and use the separately authorized
  [ELAD Harness Readiness Suite](https://github.com/TameTheGame/elad-harness-readiness-suite).

## How it works

Describe the outcome you want in ordinary language—or give the agent the project and ask
what the next useful step should be. The agent handles the ELAD loop:

```text
define the outcome and boundaries
  -> find the most important uncertainty
  -> choose the cheapest reliable check
  -> make the smallest useful change
  -> inspect the result and analyze failures
  -> repeat, escalate, or stop
```

For an ordinary task, the request, existing project rules, one trustworthy test, and an
inspected diff may be the entire process. More formal records become useful only when
work crosses contexts, depends on fallible evaluation, affects a live system, or has
consequences that make stronger evidence worthwhile.

You do not complete this loop as a questionnaire. The agent derives it from your request
and the project, then surfaces only the decisions that require your authority or judgment.

## Use only as much rigor as the task needs

| Profile | Use it when | Typical shape |
|---|---|---|
| `light` | The change is confined, reversible, low-risk, and covered by a trustworthy check. | change -> check -> inspect -> finish |
| `bounded` | The task has moderate coupling, a new regression risk, or a handoff to another context. | short brief -> focused work -> focused checks -> concise result |
| `evaluated` | Success is semantic, stochastic, experiential, runtime-dependent, or judged by a fallible evaluator. | representative cases -> inspect outputs -> analyze errors -> iterate |
| `assured` | The work is difficult to reverse, security/privacy sensitive, production-facing, or otherwise high-consequence. | isolated work -> independent expectations -> stronger verification -> separate approval |

The agent starts with `light`, moves up only when the facts require it, and moves back down
when a reusable check has made the work predictable. You do not need to choose the label.

Rigor describes how much evidence a task needs. It does not grant permission. A mature
project can still use `light` for a typo, and a read-only decision can deserve `assured`
review. [Adaptive Rigor](docs/ADAPTIVE_RIGOR.md) explains the distinction.

## Match the evidence to the claim

Use the simplest check that can reliably tell success from failure:

1. Prefer an existing deterministic check for exact behavior.
2. Add a focused regression when the expected result is independently known.
3. Observe runtime behavior when the claim depends on live state.
4. Use representative examples and a calibrated judge for semantic or stochastic
   behavior that code cannot settle.
5. Keep product meaning, trust, subjective quality, and consequential tradeoffs with the
   project owner.

Mixed work can use mixed evidence. A feature may need exact tests for its command-line
contract and a small semantic evaluation for the text it generates. The uncertain part
does not make every neighboring claim uncertain.

See [Evaluation and Evidence](docs/EVALUATION_AND_EVIDENCE.md) when choosing or building
evaluators.

## Add deeper machinery only when a trigger appears

| When you encounter... | Add or read... |
|---|---|
| One small task | [First Run](docs/FIRST_RUN.md) |
| Repeated project adoption | [Adoption Runbook](docs/ADOPTION_RUNBOOK.md) |
| Uncertain or mixed product behavior | [Evaluation and Evidence](docs/EVALUATION_AND_EVIDENCE.md) |
| Repeated autonomous delegation | [Model and Harness Qualification](docs/MODEL_QUALIFICATION.md) |
| A need to separate task rigor from project capability | [Maturity Model](docs/MATURITY_MODEL.md) |
| Live, scarce, or overlapping target effects | [Architecture](docs/ARCHITECTURE.md) and [Threat Model](docs/THREAT_MODEL.md) |
| Formal packets, receipts, or lifecycle implementation | [Conformance Contract](docs/PROTOCOL_040_CONFORMANCE.md) |

Stop reading when the next layer would not change the task, evidence, authority, or
decision.

## Validate this repository

A coding agent or CI normally runs the checks. Python 3.10 or newer is required; no
third-party packages are installed.

```text
python tools/validate_all.py
```

Windows users may also run `py -3 tools/validate_all.py`. A green result validates this
repository's inert reference artifacts. It does not prove a live model, target, runtime,
or project outcome, and it grants no authority.

## License and provenance

ELAD code and documentation are licensed under [Apache-2.0](LICENSE). Research influence,
generated artifacts, dependencies, and excluded material are documented in
[Licensing and Provenance](docs/LICENSING_AND_PROVENANCE.md) and
[Research Basis](docs/RESEARCH_BASIS.md).
