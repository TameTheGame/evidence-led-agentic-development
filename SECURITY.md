# Security Policy

## Current surface

ELAD is documentation, agent skills, synthetic examples, and one read-only check script
(`tools/check.py`). There is no runtime, no network access, no secrets handling, and no
dependency to install. The S&box example's C# code runs only inside a project that copies
it, on that project owner's machine.

The repository's own CI reads the source and runs the check. Only the release job can write
to this repository, and only to publish this repository's own GitHub Release.

For the rules agents follow when using ELAD, such as treating fetched content as data and
keeping secrets out of prompts, see [Authority and Safety](docs/AUTHORITY_AND_SAFETY.md).

## Supported versions

Security corrections are accepted for the current release, `0.6`. Fixes advance the minor
number under [Releasing](docs/RELEASING.md); there is no patch line. Earlier versions,
including the v0.5 protocol, are historical.

## Reporting a concern

Don't publish a suspected vulnerability, secret, or exploit transcript in an issue or
example. Use the repository's private vulnerability reporting. If that is unavailable,
contact the maintainer privately through the repository owner's public profile, and
disclose only enough to set up a private channel.

Ordinary non-sensitive correctness issues may use the public issue tracker.
