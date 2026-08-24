# Research Basis

## Andrew Ng sources

The design was informed by two public articles by Andrew Ng:

| Source | Published | Primary URL |
|---|---|---|
| *The AI Engineering Skills Map* | 2026-08-14 | [Andrew Ng on LinkedIn](https://www.linkedin.com/pulse/ai-engineering-skills-map-andrew-ng-m479c) |
| *AI Engineering Skills Map: Building and Deploying AI Applications* | 2026-08-21 | [Andrew Ng on LinkedIn](https://www.linkedin.com/pulse/ai-engineering-skills-map-building-deploying-applications-andrew-ng-gyn5e) |

The articles and their images are not copied into this repository. ELAD paraphrases the
relevant guidance, attributes it, and identifies its own additions separately. No
endorsement is implied.

## What the guidance contributes

The earlier map treats building/deploying AI applications, software-engineering
fundamentals, effective use of coding agents, and shaping the build as complementary
capabilities. The later map expands AI application delivery into LLM foundations,
grounding, agentic systems, evaluation-driven development, production operation, and
machine-learning foundations.

The map is a taxonomy, not a mandatory stage sequence. The most important methodological
guidance for ELAD is:

- AI components are less predictable than ordinary deterministic code.
- Effective development is iterative: build, inspect outputs, evaluate, analyze errors,
  decide what to try next, and build again.
- Evaluation strategy varies by project and development stage.
- Deterministic checks, LLM judging, traces, and human evaluation each have appropriate
  roles.
- Evaluators themselves need calibration.
- Context, tools, memory, model limits, cost, and latency shape agent design.
- Engineers should know when a quick experiment is appropriate and when to slow down for
  a careful build.
- Production operation adds observability, reliability, security, privacy, deployment,
  and optimization concerns.

## Translation into ELAD

| Guidance | ELAD mechanism |
|---|---|
| Shape the build | Observable outcome, material uncertainty, non-goals, cheapest discriminating evidence, maximum useful experiment, stop/escalation |
| Iterate from examples and errors | Build/observe/evaluate/error-analysis loop; first-causal-failure classification; next-smallest experiment |
| Vary evaluation by project and stage | Orthogonal `light`, `bounded`, `evaluated`, and `assured` task profiles |
| Choose code/workflow/agent deliberately | Least-adaptive-reliable routing and explicit delegation |
| Manage agent context | Precompiled worker slices, file-backed traces, compact orchestrator receipts |
| Understand model limits | Exact model+harness subjects and empirical qualification for repeated autonomy |
| Evaluation-driven development | Existing deterministic tests, runtime probes, frozen eval sets, calibrated semantic judges, adversarial review, human judgment |
| Evaluate evaluators | Reusable calibration receipts, counterexamples, holdouts, drift-triggered reruns |
| Operate reliably | Identity, authority, isolation, fencing when needed, observability, rollback, privacy/security, target-owned execution |
| Preserve software fundamentals | Reproducibility, versioning, testability, maintainability, regression suites, exact diffs |
| Optimize the system | Efficacy metrics that include human attention, context, cost, latency, and recurring scaffolding |
| Know when to prototype or slow down | Proportional task rigor and escalation/simplification rules |

## ELAD synthesis boundary

The four rigor profiles, authority intersection, hash-bound assured handoff chain,
closed-world lifecycle, fencing, and maturity model are ELAD's engineering synthesis.
They are not presented as mechanisms prescribed verbatim by Ng.

The blueprint also applied the iterative method to itself:

- version 0.1 exposed authority and evidence-design defects;
- version 0.2 preserved that baseline and corrected foundational contract semantics;
- an early version 0.3 draft accumulated strong assurance machinery but made it look too
  universal;
- the completed 0.3 design preserves the reusable machinery, adds true evaluator
  independence where cheap, and introduces adaptive rigor so process cost tracks actual
  uncertainty and consequence.

ML training and serving are not inherent requirements for adopting ELAD. They become
relevant when a project fine-tunes workers, builds representative datasets, measures
variance, or operates model infrastructure.
