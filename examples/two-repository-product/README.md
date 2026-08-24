# Synthetic Two-Repository Product

This fictional product has:

- `world-content`, which owns map-like native content and its target facade; and
- `simulation-app`, which owns application behavior, persistence, networking, and tests.

Both may pin the same Evidence-Led Agentic Development protocol. They do **not** share a
universal writer, active-authority record, evidence-acceptance policy, or promotion
decision.

```text
neutral protocol and conformance
             |
      exact version/digest
       /                 \
world-content          simulation-app
authority A (held)     authority B (held)
evidence policy A      evidence policy B
facade/evaluators A    facade/evaluators B
```

The fictional repositories may refer to the same product-wide risk and data policies,
but those policies are narrowing inputs only: they cannot grant repository authority,
delegate evidence acceptance, or permit a cross-repository mutation. Each project
profile instead binds its own held authority and inactive evidence policy by exact
repository-local identity.

The example intent and review packet belong only to `simulation-app`. Their claim binds
a pre-run candidate subject selector. The receipt resolves that selector to the exact
unchanged fictional candidate identity while recording that no evaluation occurred.
The separately named writer profile and capability certificate are deliberately
unqualified, both project profiles and registries are inactive, and the app authority
is held. The packet can therefore be inspected and reconciled with its
retrieval/evidence manifests, but an operational admission would have to refuse it as
`OUT_OF_SCOPE` rather than run.

The checked-in receipt is only the inert structural illustration of that refusal. Its
`recordState` is `template_inert` and its evidence manifest remains `draft`; it is not a
sealed lifecycle outcome, accepted evidence, or proof that a worker ran. Lifecycle
admission must reject it until a separately authorized implementation produces a sealed,
hash-bound record that satisfies the closed-world lifecycle oracle.

The packet, receipt, retrieval manifest, and evidence manifest carry the same exact
project, app authority, app evidence policy, shared narrowing policies, writer,
tool-registry, and evaluator-registry references. This demonstrates fresh-context
continuation without a worker transcript. The placeholder SHA-256 values are synthetic
contract data chosen for structural illustration; they are not computed hashes,
attestations, signatures, or evidence about the example files' current bytes.

A future content-to-app
integration would use:

1. a content-owned packet/candidate/receipt;
2. an explicit integration decision;
3. an application-owned packet/candidate/receipt; and
4. separate owner-local promotion.

No single mutation would span both repositories. Both repository-owned authority
examples hold all mutation, evidence-acceptance, promotion, and publication permissions
false. Both evidence policies are inactive and delegate nothing to the unqualified
writer.
