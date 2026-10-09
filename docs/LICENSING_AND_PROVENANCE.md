# Licensing and Provenance

## Project license

ELAD source code, documentation, skills, and original synthetic examples and fixtures are
licensed under the Apache License, Version 2.0. The SPDX identifier is `Apache-2.0`.
See the repository-root `LICENSE` and `NOTICE.md` files.

Contributions intentionally submitted for inclusion are accepted under the same license,
as described by Apache-2.0 section 5, unless they are conspicuously marked otherwise.
This repository does not require copyright assignment or a contributor license agreement.

## Original material included

- original provider-neutral prose and agent skills;
- original synthetic examples, including the S&box example's C# test kit. That kit is
  written against S&box's public APIs and contains no engine source;
- original pressure-test materials: prompts, rubrics, and agent responses produced
  against a synthetic fixture;
- original dependency-free check code; and
- attributed paraphrase and engineering synthesis of research guidance.

No third-party source code, research article, research image, model artifact, dataset, or
target adapter is vendored in the repository.

The skills' description style and red-flag tables follow techniques from the
`writing-skills` skill in [obra/superpowers](https://github.com/obra/superpowers) (MIT,
© Jesse Vincent). No text was copied, and Superpowers is not vendored.

## External CI dependencies

The optional GitHub Actions workflow invokes two external actions by immutable commit:

| Dependency | Pinned release and commit | License | Role |
|---|---|---|---|
| `actions/checkout` | `v6.0.2`, `de0fac2e4500dabe0009e67214ff5f5447ce83dd` | MIT | Read-only checkout with persisted credentials disabled |
| `actions/setup-python` | `v6.2.0`, `a309ff8b426b58ec0e2a45f0f869d46889d02405` | MIT | Selects the matrix Python runtime |

These actions run in GitHub-hosted CI; they are not vendored or imported by ELAD's local
check. Continued suitability and release identity should be rechecked when their
pins change.

## Material deliberately excluded

- research article and image bytes;
- product source, gates, evidence, screenshots, coordinates, or native assets;
- engine or other third-party source/resources;
- credentials, endpoints, model files, prompts containing secrets, and customer data;
- unverified third-party examples or license-incompatible code.

## Research provenance

Andrew Ng's public AI Engineering Skills Map articles informed the build/evaluate/error-
analysis framing. ELAD paraphrases that guidance and separates it from the project's own
engineering synthesis. The verified primary URLs and translation boundary are recorded
in `docs/RESEARCH_BASIS.md`. Its dated non-normative Astra note also attributes OpenAI
and Eric Provencher's prompt guidance through concise paraphrase. No source prompts,
articles, images, or private target evidence are redistributed. No endorsement is implied.

## Generated artifacts

v0.6 has no generated artifacts. The v0.5 generated files (`blueprint.json`,
`protocol-bundle.json`, and the synthetic continuation fixture) are archived at the `v0.5`
tag under the same license; see [Archive](../ARCHIVE.md).

## Publication-history boundary

Pre-publication development history contained terminology excluded from the public
source set. The public repository was initialized instead from one clean root commit
built from the verified sanitized tree. This is a publication boundary, not a claim
that prior commits contained credentials. Development now proceeds solely from that
public history; there is no separately maintained internal blueprint. Earlier private
history is retired to an external recovery archive and must not be merged into public
branches.

## Publication record and release rule

- [x] One explicit code-and-documentation license is selected.
- [x] Current-tree provenance and secret-oriented scans cover tracked text and generated artifacts.
- [x] Reachable development history is reviewed and excluded from the first public branch.
- [x] External CI dependencies have exact release commits and license dispositions.
- [x] Research attribution uses verified primary URLs and does not imply endorsement.
- [x] Synthetic examples contain no known product topology or identifiers.
- [x] Target-specific adapters remain target-local or require a separate provenance review.
- [x] The initial public root commit passed every configured hosted CI matrix cell.
- [x] The public host's private-vulnerability-reporting path is enabled.
- [x] Publication was authorized separately from candidate preparation.

Every release tag must identify an exact commit that has passed the full hosted matrix;
the tag is created only after that run succeeds. The tag's own matrix must also pass
before the repository's release job publishes its checked-in notes. The maintainer's
standing completion rule, two-component numbering, and publication verification are
defined in [Releasing](RELEASING.md). Historical tags are never renamed or moved.

This is an engineering provenance review, not legal advice or a legal-opinion letter.
