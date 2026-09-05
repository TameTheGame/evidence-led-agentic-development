# AGENTS.md — Evidence-Led Agentic Development

## Mission

This repository is a provider-neutral, target-neutral blueprint for reliable,
proportionate, evidence-led AI software delivery. It is Level 0 and default-deny.

This public repository is the canonical blueprint. Develop from its public `main`
history; do not maintain parallel internal/public blueprint repositories or standing
release copies. Short-lived task branches/worktrees are permitted when useful. Retired
pre-publication history belongs in an external private archive, never a public merge.

## Task-selected context

Read the current sources needed for the outcome. Check `STATUS.md` when milestone or
release state matters; `blueprint.json` for version, contract, or capability claims;
`README.md` for orientation; and `MANIFEST.md` to locate ownership. Read
`docs/ADAPTIVE_RIGOR.md` when changing or applying rigor semantics, plus the exact
affected contract, example, or test.

A small mechanical edit does not require the full orientation bundle. The default-deny
authority and synthetic-only boundaries below always apply; inspect applicable authority
before any governed effect. Do not preload the whole repository.

## Current authority

- Documentation, inert templates, synthetic fixtures, and read-only self-validation are
  the only implemented surfaces.
- No live model profile, certificate, adapter, candidate manager, lease backend, gate
  transition, evidence-acceptance service, promotion, or publication path exists.
- Templates/examples grant no authority.
- A target adopts a pinned release through its own owner-local authority.
- Synthetic model, continuation, and human records are test data only.

## Adaptive-rigor rule

Use [Operating Modes](docs/OPERATING_MODES.md) for Direct primary-agent delivery and
explicit Conserve routing. Read it when selecting or changing delivery mode; its worker
controls are conditional on the selected route. Ordinary user-directed Direct source
work may be light or bounded without a mandatory packet or autonomous certificate.

Project maturity, task rigor, and effect authority are orthogonal.

Select `light`, `bounded`, `evaluated`, or `assured` from uncertainty,
complexity, reversibility, consequence, per-claim evaluator maturity, and delegation distance.
Start with the cheapest reliable evidence. Escalate on evidence, not prestige. Do not
force a light deterministic task through the full assured packet chain.

Scope and authority are mandatory; ceremony is proportional. Rigor follows the material
claim, not the mere presence of program execution, an AI developer, or delegation.

The integrated agentic-episode artifacts are preserved non-normative drafts until a
separate semantic composition contract and adversarial validator are justified. A
task-rigor decision may recommend minimum evidence; it never grants effects.

## Repository boundaries

- Keep examples synthetic and platform-neutral. Target-specific notes must be clearly
  non-normative.
- Do not copy private product code, secrets, native assets, customer data, or unpublished
  evidence here.
- Target-owned facades and authoritative serializers stay in target repositories.
- Do not add arbitrary shell, filesystem, process, package, Git, MCP, deployment, or
  publication gateways.
- Do not claim maturity or capability from file presence or schema validity.

## Contract rules

- Repository paths follow the one portable grammar and shared malicious corpus.
- JSON Schema proves structure only. Semantic admission reconciles owner authority,
  identity, policy, qualification, subject, evidence, and lifecycle when those modules
  apply.
- Provider/model names do not grant authority. Repeated autonomous routing qualifies the
  exact model+runtime+harness+adapter+prompt/context+tool+resource subject.
- Owner-local policy and authority always dominate shared protocol artifacts.
- Formal machine evidence closure requires explicit owner-local evidence acceptance.
  Human closure is an external owner artifact bound to what was actually reviewed.
- Candidate, evidence, acceptance, finalization, promotion, and publication are distinct.
- Structured protocol JSON and raw payloads use their declared digest framing.
- Assured receipt lifecycle admission is closed-world and differentially checked against
  an independent external table.
- External authoritative serializers write opaque target artifacts. Agents never patch,
  merge, partially copy, or invent opaque bytes.

## Change lifecycle

For a material change:

1. State the learning question, bounded outcome, scope/non-goals, and effect authority.
2. Split mixed claims, classify evaluator maturity per claim, and select task rigor plus
   the cheapest reliable evidence.
3. Preserve Level 0/default-deny posture unless the owner separately authorizes a
   maturity/effect transition.
4. Make the smallest coherent change or experiment.
5. Observe outputs and traces; classify the first causal failure before retrying.
6. Update all affected normative artifacts and tests together.
7. Run `tools/Test-Blueprint.ps1` and inspect the exact diff.
8. Record a durable decision only for compatibility, authority, or other lasting
   architecture changes.
9. Do not publish, tag, install, activate targets, or grant authority without separate
   owner permission.

Cheap reusable conformance may run routinely. Full packets, manifests, negative suites,
qualification, independent review, and human bundles are conditional on the selected
rigor and effect boundary.

Review depth, non-resetting assurance budgets, claim-scoped revalidation, Git-native
identity, and extra-cycle escalation follow the canonical
[proportional assurance policy](docs/ADAPTIVE_RIGOR.md#proportional-assurance-budgets-and-causal-revalidation).

## Validation boundary

Validators are dependency-free and read-only. They may parse repository files and run
in-memory synthetic attacks. They must not contact providers, execute models, mutate
targets, resolve secrets, acquire real leases, change gates, accept real evidence, or
promote candidates.

## Research and provenance

Paraphrase and attribute external guidance. Do not copy supplied articles, images, or
third-party code without confirmed redistribution rights. `docs/RESEARCH_BASIS.md`
records the design translation; `docs/LICENSING_AND_PROVENANCE.md` controls the public
source set and publication boundary.
