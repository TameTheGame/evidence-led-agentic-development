# Governance

## Project governance

ELAD currently uses a maintainer-led model. There is no foundation, steering committee,
formal membership, or established contributor community. Maintainers accept changes
through reviewable commits or pull requests and are responsible for:

- release identity;
- compatibility decisions;
- licensing; and
- the public evidence boundary.

That model may evolve if sustained external participation creates a real need. Governance
documents should describe actual practice rather than anticipate an organization that
does not yet exist.

## Ownership model

**This repository owns** the method: the spec format, the evidence ladder, the skills, the
authority and safety rules, and synthetic examples.

**A project that uses ELAD owns** everything else:

- its product intent and specs;
- its authority and `AGENTS.md`;
- its code and artifacts;
- its target-specific skills; and
- its merges and releases.

ELAD is a pinned reference, not a control plane over any project.

## Changes to the method

A change is a method change when it alters any of these:

- the spec format or its field rules;
- the ladder's rungs or rules;
- a skill's text;
- the authority and safety rules; or
- compatibility or the version policy.

**Method changes require:**

1. a written decision in [Decisions](docs/DECISIONS.md), covering purpose, alternatives,
   compatibility, and rollback;
2. for a skill change, a pressure test that shows the intended behavior change (see
   [Contributing](CONTRIBUTING.md));
3. a passing `tools/check.py`; and
4. a version change suited to the compatibility impact.

Contributors may propose a method change. Accepting it and releasing it remain separate
maintainer decisions.

## Adoption

A project never becomes bound by ELAD through its presence, installation, or a passing
check. A project adopts a pinned version through its own owner's decision, and moves to a
new version the same way.

## Releases

This repository's own releases follow the standing maintainer decision in
[Releasing](docs/RELEASING.md). That permission covers this repository only. Merging,
releasing, and publishing in any project that uses ELAD are that owner's decisions; see
[Authority and Safety](docs/AUTHORITY_AND_SAFETY.md).
