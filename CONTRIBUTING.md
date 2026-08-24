# Contributing

ELAD is a maintainer-led Level-0 open-source project. Contributions that improve clarity,
portability, conformance, evidence quality, or proportionality are welcome. Contribution
does not grant authority in an adopting project or promote this blueprint to an
operational capability.

## Before changing anything

1. Read `AGENTS.md`, `STATUS.md`, `blueprint.json`, and `MANIFEST.md`.
2. State one bounded outcome, affected paths, non-goals, compatibility impact, and
   validation plan.
3. Preserve default-deny and non-operational posture unless an explicit owner decision
   authorizes a maturity transition.
4. Open an issue first for breaking protocol changes or additions that would introduce a
   dependency, network surface, operational adapter, or new authority class.

## Contract changes

Update every affected layer together:

- normative documentation;
- schemas and registries;
- inert templates;
- valid and malicious examples;
- validator controls;
- manifest/changelog/version; and
- a governance decision when semantics or compatibility change.

JSON Schema is not enough for composed identity, authority, containment, claim, evidence,
review-bundle, human-receipt, continuation-anchor, lifecycle, budget, or gate semantics.
Add semantic controls as soon as the contract depends on more than one document.

When protocol bytes are referenced, use the declared canonical structured-JSON framing;
when source, evidence, or review payload bytes are referenced, hash them raw. Do not add
a self-hash. Any new receipt state must be added to the external lifecycle oracle and
evaluated over the complete cross-product rather than copied into validator code.

## Validation

Run:

```text
python tools/validate_all.py
```

Then run `git diff --check` and inspect the exact diff, including generated counts and all
new files. Verify all 29 schema/template pairs, the external lifecycle oracle, exact-byte
continuation fixture, and malicious path corpus. Explain any change to a pinned digest,
lifecycle admission, malicious vector, or release inventory. Do not weaken a negative
control merely to make the suite green.

## Scope

Keep examples synthetic and dependencies absent unless the owner accepts a separately
reviewed dependency decision. Never contribute credentials, private product source,
external native assets, raw worker transcripts, or a generic mutation/promotion gateway.

## Contribution license

Unless explicitly marked otherwise, a contribution intentionally submitted for inclusion
is provided under Apache-2.0, consistent with section 5 of the project license. Do not
submit material you do not have the right to contribute.

## Review expectations

- Small documentation and test corrections may use the light path.
- Normative compatibility, authority, digest, or lifecycle changes require a durable
  decision, positive and malicious cases, and independent review proportional to risk.
- A pull request should state what the evidence proves and what remains untested.
- Maintainers may decline process or schema additions that do not catch a realistic
  failure or change a decision.
