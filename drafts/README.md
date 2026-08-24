# Drafts

This directory preserves non-normative design work that is not conformance evidence.

`agentic-episode.schema.json`, `agentic-episode.template.json`, and
`episode-vectors.interrupted.json` preserve the interrupted 0.3 integrated `assured`
episode design. Its declarations were never connected to an executing semantic validator,
and its inline authority/packet/receipt shapes do not compose the current normative
component schemas.

The active 0.3 suite validates the current component contracts through focused semantic
suites; it does not validate these episode drafts. A future composition may reuse them
only after a separate need and proportionality decision, redesign against the current
component contracts, frozen cross-record semantics, positive operational cases,
malicious/counterexample cases, and evaluator-independence evidence. Merely wiring the
draft schema into structural validation is not enough to return it to `spec/`.
Preservation here does not make the artifacts normative or required per task.

`promotion/` remains a non-executable future-design boundary.
