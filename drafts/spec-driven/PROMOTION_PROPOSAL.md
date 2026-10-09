# Promotion Proposal: a leaner ELAD

> **Proposal only.** Nothing here has been done. Josh approves it before anything touches
> `main`. Until then, no file moves, no tag, and no release.

## Summary

ELAD v0.5 is a protocol blueprint:

- 29 JSON schemas and 7 registries;
- 29 JSON templates and 10 Markdown templates;
- 10 validation and build scripts, with their test vectors and fixtures;
- an authenticated protocol bundle; and
- a preserved, never-finished episode design.

None of it runs anything; it is Level 0 and inert.

The spec-driven drafts on this branch showed that a much smaller set changes what agents
actually do:

- a requirement format that lives in the project's spec;
- an evidence ladder that orders checks by cost; and
- three short skills.

This proposal makes those the core of ELAD:

- **The protocol machinery leaves `main`.** It stays reachable at the immutable `v0.5` tag.
- **ELAD's own checks shrink** to a skill lint and a link check.
- **The release is `v1.0`.**

## Why

| Evidence | What it showed | Limits |
|---|---|---|
| [Pressure test, round 1](skills/PRESSURE_TEST_RESULTS.md#round-1) | With the skills, agents pushed back on a one-shot stop rule and kept owner questions to what only the owner can answer. Unmodified Superpowers added ceremony and read the stop rule at its broadest. | One sample per cell; dry runs |
| [Pressure test, round 2](skills/PRESSURE_TEST_RESULTS.md#round-2) | It confirmed round 1 under a rubric frozen beforehand and blind scoring. On the one-shot rule, the skills recommended a better rule in 2 of 3 runs against 0 of 3 without them, and ran cheaper checks first (3 of 3 against 0 of 3). On the east spawn, 7.0 against 5.8 of 7: they ran the checks themselves and reported by requirement and rung. | Three samples per cell; dry runs; a model scored them, with partial blinding |
| [Engine-rung spike](engine-rung-spike/README.md#final-result) | The ladder's machine rungs work in a real engine. Headless project tests checked collision, traces, spawn landing, stuck detection, and a saved scene in S&box. | One engine build; Windows only |

The evidence is small and honest about it:

- **Untested:** automatic skill triggering in a real install.
- **Unproven:** production use across several projects.

The proposal keeps those limits visible and claims no new maturity.

**Superpowers is used only where it helped.**

- **Borrowed:** its `writing-skills` techniques, namely trigger-style descriptions and
  red-flag tables. They are credited, not copied.
- **Kept:** `verification-before-completion`.
- **Skipped:** `brainstorming`, when the spec already covers the change.

Nothing from Superpowers is forked or vendored.

## What moves into the core

Each move is a `git mv`, so file history follows.

| From (this branch) | To (`main`) | Notes |
|---|---|---|
| `drafts/spec-driven/SPEC_AND_LADDER.md`, Part 1 | `docs/SPEC_FORMAT.md` | The requirement format, field rules, acceptance log, and the rung-0 spec lint description |
| `drafts/spec-driven/SPEC_AND_LADDER.md`, Part 2 and "How a task runs" | `docs/EVIDENCE_LADDER.md` | The rungs, ladder rules, and task flow |
| `drafts/spec-driven/skills/choosing-rigor/` | `skills/choosing-rigor/` | General skill |
| `drafts/spec-driven/skills/matching-evidence-to-claims/` | `skills/matching-evidence-to-claims/` | General skill |
| `drafts/spec-driven/skills/asking-the-owner/` | `skills/asking-the-owner/` | General skill |
| `drafts/spec-driven/skills/README.md` | `skills/README.md` | Install steps, the scenario table, and the Superpowers notes |
| `drafts/spec-driven/skills/PRESSURE_TEST_RESULTS.md` and `pressure-test/` | `skills/evidence/` | The evidence for keeping each skill |
| `drafts/spec-driven/skills/sbox-engine-reference/` | `examples/sbox/skills/sbox-engine-reference/` | Target-specific example of a project's domain skill, marked non-normative |
| `drafts/spec-driven/example-sbox-outpost.spec.md` | `examples/sbox/outpost.spec.md` | Worked example of the format and ladder |
| `drafts/spec-driven/engine-rung-spike/` | `examples/sbox/engine-rung-spike/` | Evidence that rung 1 is buildable; target-specific |

**The ladder doc's open questions are split.**

- The answered ones move into `examples/sbox/README.md`.
- Anything still open moves to `ROADMAP.md`.

**Four v0.5 documents hold the reasoning behind the skills:** `ADAPTIVE_RIGOR.md`,
`EVALUATION_AND_EVIDENCE.md`, `HUMAN_DECISION_BOUNDARY.md`, and `OPERATIONS_AND_LEARNING.md`.

- **Recommended:** fold what they add beyond the skills into `docs/EVIDENCE_LADDER.md`, then
  archive them, so each rule has one home.
- **Alternative:** keep them trimmed as background reading (decision 3 below).

**These documents stay, updated:** `PRINCIPLES.md`, `RESEARCH_BASIS.md`,
`LICENSING_AND_PROVENANCE.md`, `RELEASING.md`, `DECISIONS.md`, and `EMPIRICAL_STATUS.md`.
`EMPIRICAL_STATUS.md` gains the pressure-test and spike results.

## What gets archived and removed from `main`

Nothing is deleted from history. The `v0.5` tag points at `112aef8` and keeps every file
below reachable, as do `v0.3.0` and `v0.4.0`. A short `ARCHIVE.md` lists each removed group
with a link to it at `v0.5`, for example `…/tree/v0.5/spec/schemas`. No archive branch is
needed, because tags don't move.

| Group | Paths | Files |
|---|---|---|
| Schemas and registries | `spec/schemas/` (29), `spec/registries/` (7), `spec/README.md` | 37 |
| JSON templates | `templates/*.template.json` | 29 |
| Protocol Markdown templates | `templates/*.template.md` except `AGENTS.template.md` | 9 |
| Validators | `tools/validate_*.py` (8), `tools/build_level0_artifacts.py`, `tools/Test-Blueprint.ps1` | 10 |
| Validator vectors and fixtures | `tests/` | 31 |
| Protocol bundle and identity | `protocol-bundle.json`, `blueprint.json` | 2 |
| Episode drafts | `drafts/agentic-episode.schema.json`, `drafts/agentic-episode.template.json`, `drafts/episode-vectors.interrupted.json`, `drafts/promotion/README.md`, `drafts/README.md` | 5 |
| Protocol examples | `examples/two-repository-product/` (20), `examples/mixed-claim-semantic-feature/` (2) | 22 |
| Future-runtime placeholders | `adapters/README.md`, `reference/README.md` | 2 |
| Protocol documents | `docs/ARCHITECTURE.md`, `PROTOCOL_05_CONFORMANCE.md`, `LIFECYCLE_ORACLE_ASSESSMENT.md`, `PATH_IDENTITY.md`, `THREAT_MODEL.md`, `MATURITY_MODEL.md`, `MODEL_QUALIFICATION.md`, `MODEL_HARNESS_READINESS_EVALUATION.md`, `OPERATING_MODES.md`, `ADOPTION_RUNBOOK.md` | 10 |
| Replaced by the README | `START_HERE.md`, `MANIFEST.md` | 2 |

The new `skills/` folder and README replace `templates/AGENTS.template.md`, unless Josh
wants a short AGENTS example kept (decision 4).

## What ELAD's own checks become

One dependency-free script, `tools/check.py` (Python 3.10 or newer), with two parts:

1. **Skill lint.** It checks every `SKILL.md` under `skills/` and `examples/*/skills/`:
   - YAML frontmatter with exactly `name` and `description`;
   - `name` equal to its folder name;
   - `description` starting with "Use when" and within the Agent Skills format's length
     limit; and
   - a non-empty body.
2. **Link check.** Every relative Markdown link and `#anchor` resolves inside the
   repository.

**CI** runs `tools/check.py` on Ubuntu and Windows. The release job keeps one shell step
comparing `VERSION` with the tag, and still publishes the checked-in notes. That replaces
the schema, vector, lifecycle, bundle, and release validators. The rung-0 spec lint stays
a description in `docs/SPEC_FORMAT.md` for projects to write; ELAD doesn't ship it.

## Rewrite outlines

### README.md

1. **Promise:** keep "Use the cheapest reliable evidence that can justify the next action."
2. **What ELAD is:** a spec format, an evidence ladder, and three skills. It grants no
   authority and runs nothing.
3. **Quick start:**
   - copy the three skill folders into the agent's skill folder, such as
     `.claude/skills/`;
   - write `spec/<area>.spec.md`; and
   - point `AGENTS.md` at it.
4. **The format** in one short requirement example.
5. **The ladder table** and its rules in brief.
6. **The skills table:** when each one triggers.
7. **Evidence and limits:** pressure tests and the spike, with their sample sizes.
8. **Example:** the S&box outpost, marked target-specific.
9. **Where v0.5 went:** the archive note and the `v0.5` tag, for anyone who needs the
   protocol.
10. **Checks and license:** `python tools/check.py`; Apache-2.0.

### AGENTS.md

- **Mission:** a public, provider-neutral method made of a spec format, a ladder, and
  skills. It grants no authority.
- **Context:** read the README, then only the skill or document being changed.
- **Boundaries:**
  - examples stay synthetic;
  - no private or target data;
  - target-specific material lives under `examples/` and is marked non-normative; and
  - external guidance is paraphrased and attributed.
- **Changing a skill:** show a behavior change against a no-skill baseline in a pressure
  test before merging, and record the result under `skills/evidence/`.
- **Checks:** run `tools/check.py` and read the diff.
- **Releases:** follow the simplified `RELEASING.md`.
- **Kept:** one canonical public repository, developed on `main` with short-lived branches.
- **Dropped:** Level-0 and default-deny protocol wording, the schema, digest, and lifecycle
  rules, and Direct/Conserve routing.

### Other files

| File | Change |
|---|---|
| `STATUS.md` | A few lines: version, what's in the core, open evidence gaps |
| `ROADMAP.md` | Test automatic triggering in a real install; a second target example; open spike questions |
| `CHANGELOG.md`, `releases/v1.0.md` | What moved, what was archived, and how to stay on v0.5 |
| `RELEASING.md` | Drop the bundle-regeneration and identity-rebinding steps |
| `CONTRIBUTING.md` | The pressure-test rule for skill changes |
| `SECURITY.md` | One paragraph: no runtime, no network, no secrets |
| `GOVERNANCE.md`, `NOTICE.md`, `LICENSE` | Unchanged |

## Version

**Proposed: `v1.0`.** `VERSION` would read `1.0`.

`RELEASING.md` reserves a major increment for "a deliberately announced major compatibility
or maturity transition". Removing the schemas, templates, validators, and bundle that a
v0.5 adopter could pin is that kind of compatibility break.

The number claims no maturity. The README and release notes say so, along with the evidence
limits above. If Josh prefers to keep a pre-1.0 signal until automatic triggering is tested,
`v0.6` is the alternative. It would need a one-line exception in `RELEASING.md`
(decision 2).

## Impact on Desert

None. Desert pins ELAD `v0.3.0`, and nothing in this proposal changes that pin or any file
in Desert's repositories. Adopting the new version there is a separate decision for Josh.

## After approval

1. **Branch.** This branch is `main` (`112aef8`) plus the drafts. Cut a working branch from
   it and move the drafts into place with `git mv`.
2. **Archive.** Remove the archived paths and add `ARCHIVE.md`.
3. **Checks.** Write `tools/check.py` and switch CI to it.
4. **Rewrite.** Rewrite the README, AGENTS.md, and the other files above.
5. **Review.** Run the checks and a fresh-checkout check, then get an independent review.
6. **Merge and release.** Josh reviews and merges to `main`. Then tag `v1.0` and verify the
   GitHub Release.

## Decisions for Josh

1. Approve the direction: the core becomes the spec format, the ladder, and three skills,
   and the protocol is archived at `v0.5`.
2. Version: `v1.0` (recommended) or `v0.6`.
3. Fold the four rationale documents into `docs/EVIDENCE_LADDER.md` and archive them
   (recommended), or keep them trimmed.
4. Keep a short AGENTS example, or let the README and skills cover it (recommended).
5. Homes for the spike kit and the pressure-test materials: `examples/sbox/` and
   `skills/evidence/` (recommended).
6. CI matrix: Ubuntu and Windows on one Python version (recommended), or the current
   three-OS, two-Python matrix.

## Risks

- **Adopters lose files on `main`.** Anyone using the v0.5 schemas from `main` would lose
  them. The `v0.5` tag keeps them, and the release notes say to pin it.
- **External links may break.** The separate Harness Readiness Suite and other pages may
  link to documents on `main`. Check them before the merge, and point them at `v0.5`.
- **The skills' evidence is thin.** It comes from small dry-run samples scored by a model.
  The README must not overstate it, and each future skill change needs a pressure test.
- **Machine checks shrink.** The removed validators checked inert artifacts that no target
  used at runtime. What remains checks the files people do use: the skills and the links.
