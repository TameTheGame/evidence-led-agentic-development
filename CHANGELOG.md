# Changelog

## Unreleased

- **Added `skills/evidence/TRIGGERING_TEST.md`.** Nine headless Claude Code sessions tested
  whether the skills load on their own.
  - The skills were used in all six working runs, but invoked through the skill mechanism
    in only four.
  - `choosing-rigor` never triggered on the one-shot probe.
  - The typo control added no process.
  - All three east-spawn runs edited an agreed requirement before asking the owner.
  - Description and red-flag changes are proposed, not applied. They need a pressure test.
- **Added `skills/AGENTS_SNIPPET.md`.** It is an optional short block for `AGENTS.md`,
  mapping moments to skills, for projects whose agents don't pick up the skills.
  - Its checks line was narrowed in the correction cycle, to checks "for a requirement".
  - The README offers it as optional, not as a quick-start step, because the no-snippet
    runs did at least as well.
- **Added `examples/sbox/tools/spec_lint.py`.** It is an example rung-0 spec lint, with
  fixtures and `test_spec_lint.py`.
  - Its format checks fail the run.
  - Its owner gate reports any change to an agreed requirement since `HEAD` as
    `NEEDS OWNER`, without blocking.
  - `docs/SPEC_FORMAT.md` now points to it.
- **Skill edits (on the `skills-engage` branch, pending the owner):**
  - the `choosing-rigor` description now covers requests to run a check, and requests that
    set an attempt limit or stop condition;
  - the `matching-evidence-to-claims` description adds "running" checks; and
  - `asking-the-owner` gains a red flag: a "wording change" to an agreed requirement is
    still the owner's decision.
- **Added `skills/evidence/ENGAGE_TEST.md`.** It reports 15 acting sessions, scored blind
  against a rubric frozen beforehand.
  - Agreed requirements were left to the owner in 9 of 9 east-spawn runs.
  - Pushback on the stop rule held in 3 of 3.
  - The control stayed light in only 1 of 3, so the decision rule failed.
  - A report-format fix is proposed, not applied.
  - **Correction-cycle addendum.** With the narrowed snippet, the control stayed light in
    2 of 3 runs and the east spawn held at 3 of 3, so the rule failed again. Without the
    snippet, the control stayed light in 3 of 3.
- **Added `skills/evidence/tools/analyze_transcripts.py`,** the transcript analyzer used by
  both tests.

## 0.6 — 2026-10-09

A breaking reshape, approved through the promotion proposal; see ADR-0020 in
`docs/DECISIONS.md`.

- **The core is now three parts.**
  - `docs/SPEC_FORMAT.md`: requirements in the project's spec, each naming its rung and
    check.
  - `docs/EVIDENCE_LADDER.md`: checks ordered by cost, plus the rules for climbing them.
  - Three skills in `skills/`: `choosing-rigor`, `matching-evidence-to-claims`, and
    `asking-the-owner`.
- **Rationale folded in.** `ADAPTIVE_RIGOR.md`, `EVALUATION_AND_EVIDENCE.md`,
  `HUMAN_DECISION_BOUNDARY.md`, and `OPERATIONS_AND_LEARNING.md` were folded into
  `docs/EVIDENCE_LADDER.md`, then archived.
- **New `docs/AUTHORITY_AND_SAFETY.md`.** It carries forward the general rules from
  `ARCHITECTURE.md`, `THREAT_MODEL.md`, `MODEL_QUALIFICATION.md`, and the v0.5
  `SECURITY.md`.
- **The S&box material moved to `examples/sbox/`:** the outpost spec, the engine-rung spike
  kit with results from seven runs, and the `sbox-engine-reference` skill.
- **The pressure-test record moved to `skills/evidence/`.** Rounds 1 and 2, with responses,
  rubrics, keys, and scores.
- **Archived at `v0.5` and removed from `main`; see `ARCHIVE.md`:**
  - all schemas and registries;
  - all templates;
  - the validators, vectors, and fixtures;
  - `protocol-bundle.json` and `blueprint.json`;
  - the episode and promotion drafts;
  - the protocol examples;
  - the adapter and reference placeholders;
  - `START_HERE.md`, `MANIFEST.md`, and `docs/FIRST_RUN.md`; and
  - the protocol documents.
- **New checks.** `tools/check.py` replaces the validators: a skill frontmatter lint and a
  relative-link check. CI runs it on Ubuntu and Windows with one Python version. The
  release job checks that the tag matches `VERSION` and that the notes exist.
- **Version policy.** `docs/RELEASING.md` now says 0.x minor releases may include breaking
  changes. `1.0` waits for a real-install triggering test and one real project.
- **Rewritten:** README, AGENTS.md, STATUS, ROADMAP, CONTRIBUTING, and SECURITY. GOVERNANCE
  was trimmed to match.
- **The skill-change rule.** A change to what a skill tells an agent to do (its
  instructions, description, or red flags) needs a blind pressure test. Mechanical fixes
  that don't change meaning (paths, links, typos) need only `tools/check.py` and a
  CHANGELOG line. The rule is stated in AGENTS.md and mirrored in CONTRIBUTING, the skills
  README, the README, GOVERNANCE, and ADR-0020.
- **Mechanical fix:** `sbox-engine-reference` now points to the spike kit at
  `examples/sbox/engine-rung-spike/` instead of its old drafts path.

## 0.5 — 2026-09-05

- Adopted two-component `MAJOR.MINOR` versions and `vMAJOR.MINOR` release tags, beginning
  with `v0.5`. Historical three-component tags remain unchanged.
- Made version bumps, checked-in release notes, and a verified GitHub Release the default
  completion path for authorized user-facing blueprint updates. Valid version tags
  publish only after the full hosted conformance matrix passes.
- Rebound all active protocol, schema, registry, template, example, vector, bundle, and
  validator identities to exact `0.5`; preserved non-normative historical drafts and
  existing adopter pins. Mixed-version chains remain invalid.
- Consolidated blueprint development onto the canonical public repository and its clean
  `main` history. Retired private history and release-preparation copies remain external
  recovery material; the separate Harness Readiness Suite remains an optional companion.
- Added canonical Direct/Conserve operating-mode guidance, independent of rigor:
  capable primary-agent delivery and explicit eligible cheaper/local routing.
  Replaced blanket local-first routing and required document preloads with conditional
  worker controls and task-selected context. Existing qualification, effect boundaries,
  review budgets and runtime evidence remain intact; release identities advance together.
- Added a dated, non-normative Astra instruction-audit note with primary attribution;
  it makes no model-superiority claim and activates no runtime or downstream adoption.

## 0.4.0 — 2026-08-29

- Promoted the complete normative protocol, authenticated bundle, conformance corpus,
  and dependency-free validators to exact `0.4.0` identities. Existing `0.3.0`
  adopters remain valid while pinned; adopting `0.4.0` requires an explicit repin and
  claim-scoped revalidation of affected target-owned review-flow bindings.
- Added lifecycle-cost proportionality, hard non-resetting review budgets, claim-scoped
  revalidation, Git-native tracked-artifact identity, and qualified local-first
  verification without adding a new schema or control platform.
- Documented the separately maintained ELAD Harness Readiness Suite `v0.1.0` as an
  optional model- and harness-agnostic operational companion; retained Level 0,
  default-deny authority, exact-subject qualification, and bounded empirical claims.
- Corrected the onboarding flow so project owners can describe a high-level outcome or
  simply ask what comes next; the agent, not the owner, performs ELAD's task decomposition,
  uncertainty analysis, rigor selection, and evidence planning.
- Visually distinguished agent-only headings from reader-facing steps with a restrained
  blockquote treatment in the onboarding guides.
- Reframed the empirical summary around ELAD's four deliberate reference-project
  experiments and their positive results, while keeping the production-scale and
  generality limits explicit.
- Reworked the reader-facing process guides around progressive disclosure: start with one
  small task, add evaluation for uncertain claims, and introduce qualification or formal
  assurance only when repeated autonomy or consequential effects justify them.
- Added a prominent `Why ELAD` section explaining how right-sized scaffolding and
  evidence-backed stopping rules make autonomous agentic development practical without
  overstating the bounded empirical record.
- Simplified process language, shortened repeated protocol explanations, and routed
  implementation detail to the technical references while preserving authority,
  claim-specific evidence, evaluator calibration, and explicit stopping boundaries.
- Clarified the first-run voice by speaking directly to the project owner while prefixing
  every coding-agent procedure with `Agent instructions:`.
- Replaced the first copyable prompt's protocol vocabulary with a plain-language request
  to state the intended change, boundaries, and verification before seeking approval.

## 0.3.0 — 2026-08-23

- Released a clean public source tree under Apache-2.0, with verified primary-source
  research attribution, exact licensed CI dependencies, a clean-history publication
  boundary, public contribution/security guidance, and no product-specific residue.
- Added a cross-platform `python tools/validate_all.py` entrypoint, made hosted CI execute
  all six validation slices, added a short first-run walkthrough, and published a candid empirical
  status that separates internal conformance from bounded portability observations and
  untested operational claims.
- Made evaluation an explicit build/observe/evaluate/error-analysis feedback loop.
- Separated project maturity, per-task rigor, and effect authority.
- Added `light`, `bounded`, `evaluated`, and `assured` profiles plus a genuine
  lightweight path with no mandatory JSON artifacts.
- Classified strict packets, manifests, receipts, qualification, fencing, negative
  suites, and adversarial/human review as conditional assurance modules rather than
  universal per-task ceremony.
- Added an advisory, authority-free task-rigor registry/schema/template, eleven positive
  vectors, 37 malicious/contradictory vectors, and a dependency-free validator. Profile
  bases are claim/effect neutral; closed per-claim evaluator, claim-domain, and task-effect
  modules prevent irrelevant semantic, runtime, or rollback ceremony.
- Applied the four-observation portability correction: evaluator maturity is per claim;
  a new exact regression is not an unproven fallible evaluator; program execution does
  not itself create an operational claim; and AI-assisted development does not itself
  create stochastic product behavior.
- Preserved the integrated agentic-episode schema, template, and unfinished vectors as
  non-normative drafts because no semantic composition validator supports an assured
  claim; the focused component contracts remain normative.
- Retained the 44,100 lifecycle cross-product and added a separately implemented rule
  predicate plus focused claim-aggregate, 15-shape, and single-field-denial vectors.
- Added an explicit authenticated artifact inventory and deterministic inert-artifact
  regeneration tool so filename globs cannot silently make a draft normative.
- Clarified reusable evaluator calibration, heterogeneous cloud/local routing, compact
  orchestrator context, progressive adoption, gate admission, and process simplification.
- Added a compact bounded-worker packet and a mixed deterministic/semantic example;
  distinguished supervised workers from bounded handoffs, coding from product-inference
  harnesses, generator from evaluator sampling, LLM-judge evidence from external-human
  acceptance, and causal closure from perfect-score chasing.
- Retained Level 0/default-deny status; no live model, target, adapter, authority,
  promotion, or publication surface was added.

## 0.2.0 — 2026-08-22

- Replaced the shared two-repository authority/evidence design with separate
  repository-owned authority records and evidence policies; shared risk/data policy is
  explicitly narrowing only.
- Added claim classes, pre-run subject selectors, and exact resolved subjects across
  evidence, receipt, review, and human-decision records.
- Made `evidenceAcceptance` an enforced operational closure condition and bound machine
  delegation to exact claim class, evidence class, evaluator, and eligible writer.
- Added a closed-world 44,100-combination receipt lifecycle oracle with exactly 33
  admitted sealed tuples.
- Added full configured-writer -> measured-certificate -> requested-packet ->
  observed-receipt budget containment, including sequential/total tool-call and resource
  envelope checks.
- Defined canonical structured-JSON hashing separately from raw-byte source/evidence
  hashing.
- Added review-bundle and continuation-anchor contracts and an exact-byte synthetic
  continuation rooted outside the receipt chain; external human receipts now bind the
  exact reviewed bundle and eligible reviewer.
- Expanded the malicious path corpus to cover all reserved `COM2`-`COM8` and
  `LPT2`-`LPT8` bare, case, extension, and intermediate forms.
- Expanded the protocol to 19 schemas and 20 inert JSON templates.
- Retained Level 0/default-deny status: the synthetic continuation is conformance
  evidence only and no live controller, project authority, model, adapter, runtime,
  evidence service, promotion, or publication path exists.

This is a breaking pre-release hardening change. `0.1.0` is retained as the failed
adversarial-review baseline and must not be treated as compatible or adoption-ready.

## 0.1.0 — 2026-08-22

- Established the Level 0, non-operational, default-deny blueprint.
- Added normative guidance, draft contracts, inert templates, synthetic examples, and a
  dependency-free self-validator.
- Reserved live adapters, leases, evidence acceptance, promotion, and publication for
  separately authorized and reviewed maturity transitions.

Historical review subsequently found false-green risks in cross-repository ownership,
evidence delegation, continuation trust, claim subjects, receipt lifecycle, budget
containment, and path-corpus coverage. Those findings are corrected in `0.2.0`.
