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

It also fails when a tracked file, a file name, or a commit message contains a private
word: a word or a phrase of up to three words, such as a private project's name, that must
never appear in this public repository. `tools/private-words.sha256` holds only SHA-256
fingerprints of them; the owner keeps the readable list outside the repository. If the
check flags a line, remove or reword it; if it flags a commit message, reword that commit
before pushing. A short word's fingerprint can be found by trying every short word, so the
list keeps words out of the repository but doesn't keep them secret.

It also fails when a commit reachable from `HEAD` credits an AI coding tool, such as Claude,
Cursor, or Copilot: an author or committer whose name or email names one, a trailer such as
`Co-authored-by:` or `Assisted-by:` naming one, a trailer named for one such as
`Claude-Session:`, or a line such as "Generated with Claude Code". Ordinary mentions pass,
such as "Add a Claude Code hook". The tools it knows are `AI_TOOLS` in `tools/check.py`; a
person whose name contains one, such as Claude, is flagged too. If it flags a commit that
isn't pushed yet, fix that commit's author or message before pushing. A pushed one can only
be fixed by rewriting history and force-pushing, which needs the owner's yes.

`python tools/test_check.py` tests both checks with made-up words and identities.

In a Claude Code session started in this repository, a hook in `.claude/settings.json`
runs the check before every `git push` and blocks the push if it fails. It needs `py -3` on
Windows or `python3` elsewhere. A session started in a parent folder, such as a cloud
session with several repositories, doesn't load that hook. For those, and for pushes from
outside Claude Code, turn on the git hook in `.githooks/` once per clone:

```text
git config core.hooksPath .githooks
```

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
