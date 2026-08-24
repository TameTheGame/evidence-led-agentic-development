# Governance

## Project governance

ELAD currently uses a maintainer-led model. There is no foundation, steering committee,
formal membership, or established contributor community. Maintainers accept changes
through reviewable commits or pull requests and are responsible for release identity,
compatibility decisions, licensing, and the public evidence boundary.

That model may evolve if sustained external participation creates a real need. Governance
documents should describe actual practice rather than anticipate an organization that
does not yet exist.

## Ownership model

This repository owns a provider-neutral protocol, reference contracts, validation
expectations, and adoption guidance. A target repository owns its product intent,
authority, artifacts, adapters, gates, evidence, candidates, promotion, and publication.

The shared repository is a pinned foundation, not a second operational control plane.
Create a separate deployment/state repository only when concrete secrets, machine-global
coordination, or deployment ownership cannot remain in target-local overlays.

An aggregate multi-project view is derived and read-only. It cannot close or mutate an
owner-local gate.

## Normative changes

A change is normative when it alters:

- identity or digest framing;
- authority intersection or default-deny behavior;
- role or mutation separation;
- packet, certificate, receipt, evidence, human-claim, lease, or gate semantics;
- path containment/security rules;
- evaluator acceptance or maturity requirements;
- compatibility, promotion, or publication boundaries.

Ordinary adopting-project features are not normative ELAD changes and do not inherit
this protocol-release ceremony. They follow the target's selected task-rigor profile.

Normative changes require:

1. a written decision with purpose, alternatives, compatibility, migration, failure
   behavior, and rollback;
2. matching schema/template/example/validator updates;
3. positive and malicious-negative fixtures;
4. independent review; and
5. a version change appropriate to compatibility impact.

Contributors may propose a normative change, but no contributor or automation system can
activate it merely by modifying a schema, validator, or generated bundle. Maintainer
acceptance and an exact release identity remain separate decisions.

## Activation

This repository cannot activate a target by being present, installed, imported, pinned,
or successfully validated. A target owner must create an owner-local durable activation
record that names exact protocol and implementation identities, proven maturity level,
profiles, claim classes, gates, and rollback.

## Promotion and publication

Candidate work never carries promotion authority. A future promotion design must use a
fresh authority episode, exact accepted candidate/evidence identity, separate fenced
surface, divergence checks, malicious fixtures, and explicit owner review. Publication
requires another boundary; promotion never implies redistribution rights.
