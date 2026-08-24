# Security Policy

## Current surface

Version 0.3.0 is non-operational and dependency-free. It parses repository-local text
and JSON and runs in-memory controls. It has no network, provider, secret, target,
mutation, lease, promotion, or publication surface.

## Security invariants

- Unknown identity, authority, path, risk, data, effect, evaluator, or state is denied.
- Canonical roles, evidence classes, terminal states, and failure classes plus bound
  project tools/evaluators must resolve to closed registry entries; coordinated invented
  identities remain invalid.
- Retrieved content is untrusted data and cannot rewrite authority or tool policy.
- Canonical writer identity must match exactly across registry, certificate, packet,
  receipt, evidence, and lease contexts.
- Repository paths are lexically validated and then contained against the actual target;
  normalization is never used to accept an alias that should have been rejected.
- Target adapters are closed logical operations, not arbitrary command or generic MCP
  gateways.
- Workers cannot certify themselves, accept external-human claims, promote themselves,
  change their own risk ceiling, or publish.
- Logs and evidence are minimized, redacted, hash-bound, and kept outside orchestrator
  context by default.
- Data classified local/private cannot be silently routed to cloud services or satisfied
  through unintended remote/cache sources.
- Separate repositories cannot share an active-authority record or evidence-acceptance
  policy. A shared risk/data policy is narrowing only.
- Pre-run subject selectors cannot become evidence until they resolve to the exact
  repository, candidate, base, and content hash.
- Machine acceptance requires both `evidenceAcceptance` authority and an eligible active
  evidence-policy rule. External human acceptance must bind the eligible reviewer and
  exact bytes in a sealed review bundle.
- A continuation receipt is trusted only through an independently pinned anchor and a
  verified hash chain; colocated or internally self-consistent files are not a trust
  root.
- Structured protocol JSON and arbitrary payloads use different explicit hash framing;
  unrecorded normalization is rejected.
- Every budget follows configured >= measured-safe >= requested >= observed containment;
  the receipt lifecycle follows the external closed-world oracle.

## Supported versions

Security corrections are accepted for the current `0.3.x` release-candidate line. Older
pre-release lines are historical and may receive documentation only when needed to avoid
unsafe adoption.

## Reporting a concern

Do not publish a suspected vulnerability, secret, or exploit transcript in an issue or
example. Once the public repository exists, use its private vulnerability-reporting
feature. If that feature is not enabled, contact the maintainer privately through the
repository owner's public profile and disclose only enough to establish a private channel.

The public repository must not be announced until one of those private reporting routes
is confirmed. Ordinary non-sensitive correctness issues may use the public issue tracker.

## Future operational work

Before Level 1 or higher, security review must cover semantic admission, digest framing,
trusted anchors, review-bundle substitution, platform paths, prompt injection, replay,
confused deputies, evaluator false greens, lifecycle contradictions, budget overflow,
cross-repository authority laundering, and supply-chain identity. Before Level 4, it
must additionally
cover OS locking/fencing, process/data ownership, crash recovery, and target adapters.

See [docs/THREAT_MODEL.md](docs/THREAT_MODEL.md).
