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

Don't ask for the same release permission again, and don't call a push alone a completed
delivery. Unaccepted contributor changes don't carry this permission.

This permission covers this public repository only. It grants no authority over projects
that use ELAD, their models, or their releases.

## Version numbers

- **Format.** Versions use `MAJOR.MINOR`: `0.5`, `0.6`, `0.7`, and so on. Tags and GitHub
  Releases use a `v` prefix, as in `v0.6`, never `v0.6.0`.
- **Minor numbers.** Increment the minor number for each coherent completed update,
  including a fix or a documentation-only release. Don't release each intermediate commit.
- **Breaking changes in 0.x.** A `0.x` minor release may include breaking changes; its
  release notes say what broke and how to stay on the previous version.
- **When 1.0 comes.** `1.0` is reserved for two conditions:
  - automatic skill triggering has been tested in a real install; and
  - ELAD has been used on one real project.

  The number grants no maturity or authority.
- **Number style.** Use numeric components without leading zeroes, and no patch component.
  This is not strict Semantic Versioning.
- **Old tags never change.** Keep `v0.3.0`, `v0.4.0`, and `v0.5` exactly as they are: never
  rename, move, or delete a tag.

## Delivery loop

1. **Pick the version.** Choose the next unused version from `VERSION` and the published
   releases.
2. **Update the version everywhere.** That means `VERSION`, the README's version line, and
   `STATUS.md`. Move finished changelog entries from `Unreleased` into a dated section.
   Add `releases/vMAJOR.MINOR.md`, covering:
   - highlights;
   - compatibility and migration;
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
