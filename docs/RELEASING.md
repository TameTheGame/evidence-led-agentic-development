# Releasing ELAD

## Default completion

The maintainer's September 5, 2026 decision makes a versioned GitHub Release part of
completing an authorized user-facing blueprint update. Unless the owner explicitly
requests draft, local-only, or unreleased work, the delivery agent owns the version bump,
release notes, validation, push, tag, and verification that the release was published.
Do not request the same release permission again or call a push alone completed delivery.
Unaccepted contributor changes do not carry this permission.

This is limited to the canonical public ELAD blueprint. It grants no authority over
adopting repositories, models, native resources, runtime gates, deployments, or their
publication. Existing rights/provenance checks and the Level-0 boundary still apply.

## Version numbers

- Starting with this release, use `MAJOR.MINOR`: `0.5`, then `0.6`, `0.7`, and so on.
- Git tags and GitHub Releases use the matching `v` prefix: `v0.5`, not `v0.5.0`.
- Increment the minor number for each coherent completed update, including a fix or
  documentation-only release. Do not make a release for each intermediate commit.
- Reserve a major increment for a deliberately announced major compatibility or maturity
  transition; the number itself grants no maturity or authority.
- Use numeric components without leading zeroes. Do not add a patch component or claim
  strict Semantic Versioning compatibility for this two-component convention.
- Preserve old tags such as `v0.3.0` and `v0.4.0` exactly; do not rename, move, or delete
  them. Historical draft identities and other projects' versions are not reformatted.

## Delivery loop

1. Select the next unused version from current `VERSION` and published releases.
2. Update `VERSION`, current status/readme/manifest, active protocol/schema/registry/
   template/example/vector/validator identities, and their references together. Preserve
   explicitly historical records and drafts. Regenerate the authenticated bundle and
   synthetic continuation bindings with `tools/build_level0_artifacts.py`; reseal the
   trusted continuation anchor after independently checking the exact changed chain.
3. Move completed changelog entries out of `Unreleased` into the dated version section.
   Add `releases/vMAJOR.MINOR.md` with highlights, compatibility/migration, evidence limits,
   and rollback. Its first heading identifies the exact release.
4. Run `python tools/validate_all.py`, `git diff --check`, the appropriate bounded review,
   and a fresh-checkout/export validation. Review generated identity changes; unchanged
   synthetic raw payloads and preserved drafts must remain unchanged.
5. Commit and push the accepted source to public `main`. Wait for the full hosted
   Windows/Ubuntu/macOS and Python matrix to pass for that exact commit.
6. Create an annotated `vMAJOR.MINOR` tag at that exact green commit and push the tag.
   The tag workflow validates its name against `VERSION`, repeats the conformance matrix,
   and only then publishes `releases/vMAJOR.MINOR.md` as the latest GitHub Release.
7. Verify the published release is neither draft nor prerelease, names the correct tag,
   resolves to the intended commit, is marked latest, and contains the intended notes.
   Report the release URL and final Git state. Delivery is not complete without this check.

If validation or publication fails, report the precise incomplete step and repair within
scope. Before retrying publication, inspect whether a release already exists; do not
overwrite an existing published release or move a released tag. If hosted publication
is unavailable, the delivery agent may publish the same verified tag and checked-in notes
through GitHub CLI after the matrix passes, then perform the same final checks.

Rollback is an adopter's explicit return to a previous immutable release. This repository
does not automatically repin a target or rewrite its historical evidence.
