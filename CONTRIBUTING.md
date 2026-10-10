# Contributing

ELAD is a maintainer-led open-source project. Contributions that make the method clearer,
more portable, better evidenced, or leaner are welcome. A contribution grants no authority
in any project that uses ELAD.

## Before changing anything

1. Read `AGENTS.md` and the README.
2. State one bounded outcome, the affected files, what is out of scope, and how you'll
   check it.
3. Open an issue first for a change to the spec format or the ladder rules, or for
   anything that would add a dependency or runtime machinery.

## Skill changes need a pressure test

A skill is kept only if it changes what agents do. A pull request that changes what a skill
tells an agent to do (its instructions, description, or red flags) must include a pressure
test:

- **Compare:** agents with the changed skill against a baseline, on the scenarios the
  change targets.
- **Freeze the rubric:** write it before reading any response.
- **Score blind:** shuffle the responses and remove anything that names the condition.
- **Record the result:** add it to [`skills/evidence/`](skills/evidence/PRESSURE_TEST_RESULTS.md),
  with the responses and the key.

Mechanical fixes that don't change meaning (paths, links, typos) need only `tools/check.py`
and a CHANGELOG line.

The [skills README](skills/README.md) describes the method and lists the standing
scenarios. Run them against the synthetic fixture, never against private project data.

## Checks

Run:

```text
python tools/check.py
```

Then run `git diff --check` and read the exact diff. The check lints every skill's
frontmatter and confirms every relative link resolves.

## Scope

Keep examples synthetic. Never contribute credentials, private product source, native
assets, raw agent transcripts from private projects, or runtime gateways. Target-specific
material goes under `examples/` and is marked non-normative.

## Contribution license

Unless explicitly marked otherwise, a contribution intentionally submitted for inclusion is
provided under Apache-2.0, consistent with section 5 of the project license. Don't submit
material you don't have the right to contribute.

## Review expectations

- Small documentation fixes may take the light path.
- Changes to the spec format, the ladder rules, or what a skill tells an agent to do need a
  recorded decision or pressure test, and review proportional to their reach.
- A pull request should say what its evidence proves and what remains untested.
- Maintainers may decline additions that don't catch a realistic failure or change a
  decision.

## Completing an update

Follow [Releasing](docs/RELEASING.md). Maintainer-authorized user-facing updates include a
version bump, changelog and release notes, a passing check, a matching tag, and a verified
GitHub Release. Drafts and unaccepted pull requests don't authorize publication.
