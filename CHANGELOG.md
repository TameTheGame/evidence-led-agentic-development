# Changelog

## Unreleased

- **The two older skill-test runners load project settings only.** `run_skills_test.ps1` and
  `run_sbox_skill_test.ps1` now pass `--setting-sources project,local`, as `run_live_test.ps1`
  already did, so skills and instructions installed for the test machine's user stay out of
  test sessions. Checked on Claude Code `2.1.237`: with the setting, a session saw the
  project's skill but none of the user's. Earlier results are unchanged.
- **The S&box example's editor rung runs unattended.** S&box `26.10.13` added `sbox-cli`,
  which drives the Editor over a local named pipe. The new `examples/sbox/tools/editor_check.ps1`
  uses it to save a scene, close the Editor, reopen it, and check that nothing changed, with a
  screenshot from a fixed camera. The outpost spec's OUT-SAVE-01 now names that check, and its
  owner card SAVE-1 is gone. Verified on `26.10.13`: a scratch scene passed, and a control
  scene that changes itself on load failed.
- **The rung-1 starter suggests running the engine-source sync on a schedule.** Steam
  updates S&box only when S&box starts, so an open session misses an update from a launch
  made by hand. An hourly Windows scheduled task covers it; one was checked on 2026-10-14.
- **Removed the Harness Readiness Suite section** from `docs/EMPIRICAL_STATUS.md`. The
  owner retired that companion repository. Nothing in ELAD used it, and it was not part of
  the evidence this document lists. Older tags still mention it.

## 0.8 — 2026-10-13

The S&box example gains a rung-1 starter and an engine-source sync, and three tests in
acting sessions checked them and the example's domain skill. No skill changed, and nothing
breaks.

- **New evidence: `skills/evidence/SBOX_SKILL_TEST.md`.** It is the first test of the
  example `sbox-engine-reference` skill: 18 acting sessions on a synthetic S&box game
  project, with and without it, scored blind against a frozen rubric. The skill passed. It
  loaded in 9 of 9 runs, and with it agents fixed the planted enable-order bug in 6 of 6
  runs, against 0 of 6 without it. No run could write the default-surface scaffolding. No
  skill changed.
- **New evidence: `skills/evidence/LIVE_TEST.md`.** It reran those scenarios in 24 acting
  sessions in compiled S&box projects with the rung-1 starter, where agents could run the
  engine tests, and added the shared-generator refactor. It failed its frozen rule on the
  refactor scenario alone: the project had one area, so agents asked which refactor was
  meant. Every geometry test had a default surface, tests failed before fixes in 11 of 12
  runs, and reference probes confirmed the fix in 12 of 12, with or without the domain
  skill. No skill changed.
- **New evidence: `skills/evidence/REFACTOR_TEST.md`.** It reran the shared-generator
  refactor alone, in 6 acting sessions in a compiled project whose two areas share the
  generator, with a request that names the change. Every run refactored and reran every
  shared check afterwards, and reference probes confirmed the build in 6 of 6. It failed its
  frozen rule because no run ran those checks before the change. No skill changed.
- **Test tools.**
  - Added `run_sbox_skill_test.ps1` and `run_live_test.ps1`. The live runner also builds
    the two-area refactor project (scenario `G2`) and has a build-only phase.
  - `analyze_transcripts.py` gains `--context` and `--new-files`, and scrubs local paths
    from diffs. It also captures engine-runner output, including runs started in the
    background, and marks a non-zero exit apart from a permission refusal.
  - `blind_extracts.ps1` gains `-Messages`, `-Fixture`, and `-HideSkills`.
- **Added `examples/sbox/rung1-starter/`.** It is a copyable starting point for a project's
  engine tests, packaged from the engine-rung spike:
  - the default-surface scaffolding;
  - player and stuck-check helpers;
  - the saved-scene loader;
  - one requirement test with its control case; and
  - `tools/run_engine_tests.ps1`. It saves the engine log with each run, lists the
    component errors the engine caught, and makes concurrent runs wait.

  Verified on S&box `26.10.02`: 5 of 5 passed. In a control run with the default surface
  disabled, the runner reported the hidden `MeshComponent` error at `ModelBuilder.AddSurface`.
- **Added `sync_engine_source.ps1` to the rung-1 starter.** It reads the installed S&box
  release from `.version` and checks the matching tag out in a local clone of
  `Facepunch/sbox-public`, so agents read the source of the engine they run. It refuses a
  clone with local changes and changes no branch. The runner calls it before each run when
  `SBOX_PUBLIC` names the clone. Verified on a real clone, 74 commits past `26.10.02`.
- **Docs.** `README.md`, `STATUS.md`, and `docs/EMPIRICAL_STATUS.md` now report the S&box
  tests. `STATUS.md` no longer lists the refactor rerun as the next S&box step.

## 0.7 — 2026-10-10

The skills engage on their own in real installs, and they now leave agreed requirements to
the owner. No breaking changes.

- **Skill edits.** All three were tested in acting headless sessions; see
  `skills/evidence/ENGAGE_TEST.md`.
  - The `choosing-rigor` description now also covers requests to run a check, and
    requests that set an attempt limit or a stop condition.
  - The `matching-evidence-to-claims` description adds "running" tests and checks.
  - `asking-the-owner` gains a red flag: a "wording change" to an agreed requirement is
    still the owner's decision.
- **Added `skills/AGENTS_SNIPPET.md`.** It is an optional block for `AGENTS.md` mapping
  moments to skills, for projects whose agents don't pick up the skills. Testing found the
  skills engaged without it, and a typo fix stayed lighter without it, so it is not a
  quick-start step.
- **Added `examples/sbox/tools/spec_lint.py`.** It is an example rung-0 spec lint, with
  fixtures and `test_spec_lint.py`.
  - Its format checks fail the run.
  - Its owner gate reports any change to an agreed requirement since the last commit as
    `NEEDS OWNER`, without blocking.
  - `docs/SPEC_FORMAT.md` now recommends an owner gate and points to this example.
- **New evidence in `skills/evidence/`.**
  - `TRIGGERING_TEST.md`: 9 sessions with the v0.6 skills. They were used in every working
    run but loaded through the skill mechanism in only 4 of 6, and all three east-spawn
    runs edited an agreed requirement.
  - `ENGAGE_TEST.md`: 33 acting sessions scored blind against frozen rules.
    - The original rule and its one correction cycle failed on a wordier typo control with
      the snippet.
    - The release configuration (edited skills, the lint, no snippet) then passed its own
      check: 3 of 3 east spawn, 2 of 3 probe, and 3 of 3 control.
- **Test tools in `skills/evidence/tools/`.** These are `analyze_transcripts.py`,
  `run_skills_test.ps1`, and `blind_extracts.ps1`, so each skill change can be pressure-
  tested cheaply.
- **Docs.**
  - `README.md` and `docs/EMPIRICAL_STATUS.md` now report the headless-install evidence.
  - `ROADMAP.md` lists the next S&box steps: testing the S&box domain skill, and a rung-1
    starter.
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
