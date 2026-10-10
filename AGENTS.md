# AGENTS.md — Evidence-Led Agentic Development

## Mission

This repository is ELAD: a provider-neutral method for building software with coding
agents. It has three parts:

- the [spec format](docs/SPEC_FORMAT.md);
- the [evidence ladder](docs/EVIDENCE_LADDER.md); and
- three [skills](skills/README.md).

It runs nothing and grants no authority; see
[Authority and Safety](docs/AUTHORITY_AND_SAFETY.md).

This public repository is the only maintained copy. Develop on `main` with short-lived task
branches. Retired pre-publication history stays in an external private archive and is never
merged.

## Context

Read the README, then only the document, skill, or example the task touches. Check
`STATUS.md` when the version or release state matters. Don't preload the repository.

## Boundaries

- **Keep examples synthetic.** Never copy private product code, secrets, native assets,
  customer data, or unpublished evidence here.
- **Keep target-specific material in `examples/`.** It is marked non-normative. A
  target-specific skill belongs in the project that uses it.
- **Paraphrase and attribute external guidance.** Don't copy articles, images, or
  third-party code without confirmed redistribution rights; see
  [Licensing and Provenance](docs/LICENSING_AND_PROVENANCE.md). Superpowers is credited,
  never forked or vendored.
- **Don't add runtime machinery.** That means no gateways, adapters, or services. Don't
  claim capability from a file's presence.

## Changing a skill

A change to what a skill tells an agent to do (its instructions, description, or red flags)
needs a pressure test before it merges, scored blind against a rubric written beforehand,
recorded under [`skills/evidence/`](skills/evidence/PRESSURE_TEST_RESULTS.md). Mechanical
fixes that don't change meaning (paths, links, typos) need only `tools/check.py` and a
CHANGELOG line.

## Changing anything else

1. State the outcome, the scope, and what is out of scope.
2. Make the smallest coherent change, and update every document it affects.
3. Run `python tools/check.py` and read the exact diff.
4. Record a decision in [`docs/DECISIONS.md`](docs/DECISIONS.md) only for lasting changes
   to compatibility, authority, or the method itself.
5. Close authorized user-facing updates through [Releasing](docs/RELEASING.md): a version
   bump, notes, a validated commit, a tag, and a verified GitHub Release. That is the
   default, unless the owner asks for draft or local-only work.

The release permission covers this repository only. It grants no authority over any
project that uses ELAD.
