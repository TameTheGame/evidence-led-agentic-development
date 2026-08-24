# Repository Path Identity

This document defines the single normative lexical grammar for every
`repositoryPath` value in the blueprint. The same verdicts must be enforced by every
applicable schema pattern and by the dependency-free semantic validator. The canonical
positive and negative corpus is `tests/path-vectors.json`; changing a verdict is a
protocol change, not a validator convenience.

## Normative lexical grammar

A repository path is a non-empty, repository-relative sequence of `/`-separated
segments. A valid value:

- uses `/` only, never `\`;
- is not rooted, drive-qualified, UNC-qualified, or URI-like;
- contains no empty segment, `.` or `..` segment, colon, control character, or the characters
  `<`, `>`, `"`, `|`, `?`, or `*`;
- has no segment ending in a space or period;
- does not contain a case-insensitive Windows device-name segment, with or without an
  extension: `CON`, `PRN`, `AUX`, `NUL`, `CLOCK$`, `CONIN$`, `CONOUT$`, `COM1` through
  `COM9`, or `LPT1` through `LPT9`; the Windows superscript aliases for 1, 2, and 3 are
  also denied; and
- otherwise preserves ordinary Unicode, interior spaces, periods, parentheses, `$`,
  `@`, and other characters not denied above.

The grammar is intentionally portable and case-preserving. It does not silently
rewrite separators, trim segments, fold case, resolve aliases, or normalize an invalid
input into a valid one. Producers must emit one canonical value; consumers fail closed
on a value outside the grammar.

## Canonical conformance corpus

`tests/path-vectors.json` is the shared executable corpus for this grammar. Each entry
contains a path and one expected `valid` verdict that both schema and semantic checks
must produce. Its set vectors additionally reject exact duplicates and case-fold
collisions. CI runs the same corpus on Windows, Ubuntu, and macOS under supported Python
versions so platform defaults cannot quietly redefine protocol identity.

The malicious corpus explicitly includes every reserved `COM2` through `COM8` and
`LPT2` through `LPT8` form that a partial range implementation commonly misses: bare
segments, mixed/lower case, extensions, and intermediate directory segments. Together
with the existing `COM1`/`COM9`, `LPT1`/`LPT9`, superscript aliases, special device names,
and valid near misses, this prevents a seemingly complete regex from passing an
incomplete test set.

When adding a path-shaped field:

1. use the common `repositoryPath` grammar in its schema;
2. pass the field through the same semantic path validator;
3. add adversarial vectors for any newly discovered alias class; and
4. require every platform/version cell to agree before accepting the change.

## Lexical identity is not filesystem authority

Level 0 validates strings and repository-local reference documents only. A portable
lexical path is not proof that an operational filesystem target is safe.

Before Level 2 candidate writes, the target implementation must additionally resolve
the path under an exact authorized root, reject escape after canonical resolution,
apply an explicit symlink/reparse-point policy, bind the base/candidate identity, and
recheck containment at the mutation boundary. Those checks narrow an already valid
repository path; they never make an invalid lexical path acceptable.
