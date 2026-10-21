# Releasing ELAD

## Default completion

The maintainer's September 5, 2026 decision makes a versioned GitHub Release part of
completing an authorized user-facing update. Unless the owner explicitly asks for draft,
local-only, or unreleased work, the delivery agent owns these steps:

- the version bump;
- the release notes;
- the check;
- the push and the tag; and
- verifying that the release was published.

Each release waits for the owner's typed GREEN before it reaches `main` and is tagged. Ask
for it once per release; it covers that release's push and tag. Don't ask again for each
step, and don't call a push alone a completed delivery. Unaccepted contributor changes
don't carry this permission.

This permission covers this public repository only. It grants no authority over projects
that use ELAD, their models, or their releases.

## Version numbers

- **Format.** Versions use `MAJOR.MINOR`: `0.5`, `0.6`, `0.7`, and so on. Tags and GitHub
  Releases use a `v` prefix, as in `v0.6`, never `v0.6.0`.
- **Two-digit minor numbers from 1.0 on.** After `1.0` come `1.01`, `1.02`, and so on, up
  through `1.09` and on to `1.10`; after `2.0` come `2.01`, `2.02`, and so on. Never write
  a one-digit minor number after a major release: some version tools read `1.01` as `1.1`,
  so `1.1` would collide with it. See ADR-0021 in [Decisions](DECISIONS.md).
- **Minor numbers.** Increment the minor number for each coherent completed update that
  doesn't break existing projects, including a fix or a documentation-only release. Don't
  release each intermediate commit, but don't leave `main` ahead of the latest tag either:
  each coherent update that lands on `main` ships as the next release, with its changelog
  section, notes, and tag.
- **Breaking changes in 0.x.** A `0.x` minor release may include breaking changes; its
  release notes say what broke and how to stay on the previous version.
- **Breaking changes from 1.0 on.** A release that breaks existing projects takes the next
  major number, so the first after `1.xx` is `2.0`. A change breaks existing projects when
  a project that moves to it has to change its own files, beyond its pin and the copies it
  takes, for its specs and checks to keep working: for example, a spec field renamed or
  removed, or an example script whose arguments changed. Its release notes say what broke,
  what a project must change, and how to stay on the previous release.
- **When 1.0 comes.** `1.0` is reserved for two conditions:
  - automatic skill triggering has been tested in a real install; and
  - ELAD has been used on one real project.

  The number grants no maturity or authority.
- **Number style.** Use no patch component. Before `1.0`, numbers have no leading zeroes;
  from `1.0` on, the minor number's leading zero is part of it. This is not strict
  Semantic Versioning, which forbids that zero. Nothing in this repository parses
  versions; the release job compares the tag with `VERSION` as text.
- **Old tags never change.** Keep `v0.3.0`, `v0.4.0`, and `v0.5` exactly as they are: never
  rename, move, or delete a tag.

## Delivery loop

1. **Pick the version.** Choose the next unused version from `VERSION` and the published
   releases. A release that breaks existing projects takes the next major number.
2. **Update the version everywhere.** That means `VERSION`, the README's version line,
   `STATUS.md`, and `SECURITY.md`. Move finished changelog entries from `Unreleased` into a
   dated section.
   Add `releases/vMAJOR.MINOR.md`, covering:
   - highlights;
   - compatibility and migration, which always tells projects that name their pinned
     version to update it, even when nothing else needs to change (see
     [Moving to a new release](../README.md#moving-to-a-new-release));
   - evidence limits; and
   - rollback.

   Its first heading names the exact release.
3. **Check.** Run `python tools/check.py` and `git diff --check`, review proportionally,
   and run the check on a fresh clone.
4. **Push.** Commit and push the accepted source to `main`. Wait for the hosted Ubuntu and
   Windows checks to pass for that exact commit.
5. **Tag.** Create an annotated `vMAJOR.MINOR` tag at that commit and push it. The tag
   workflow confirms that the tag matches `VERSION` and that the release notes exist,
   reruns the check, and only then publishes the notes as the latest GitHub Release.
6. **Verify.** Confirm the published release:
   - isn't a draft or prerelease;
   - names the right tag and commit;
   - is marked latest; and
   - has the intended notes.

   Report the release URL and the final Git state. Delivery isn't complete without this.

**If validation or publication fails,** report the exact incomplete step and repair it
within scope. Before retrying, check whether the release already exists. Never overwrite a
published release or move a released tag. If hosted publication is unavailable, publish
the same verified tag and notes with the GitHub CLI after the checks pass, then do the
same final checks.

**Rollback** is a project's explicit return to an earlier immutable release. This
repository never repins a project or rewrites its history.
