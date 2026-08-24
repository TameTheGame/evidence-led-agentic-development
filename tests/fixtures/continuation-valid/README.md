# Valid Continuation Fixture

This directory contains a complete synthetic protocol 0.2.0 continuation chain.
It proves that a fresh validator can start from one independently pinned anchor,
resolve every immutable reference, verify canonical JSON or raw payload bytes as
appropriate, enforce claim ownership and receipt lifecycle semantics, and reconstruct
the final bounded outcome without a prior conversation transcript.
The four payload paths are explicitly marked `-text` in `.gitattributes`, so Git cannot
rewrite their line endings during a Windows, Linux, or macOS checkout.

The stable raw payloads are:

- `retrieval/subject.txt` — the source subject admitted by the retrieval manifest;
- `candidate/output.txt` — the synthetic candidate result;
- `evidence/machine-evidence.txt` — machine-verifier output bound to the candidate; and
- `human/human-acceptance-card.md` — an external synthetic human decision payload.

The structured chain contains separate authority and policy records, an exact writer
profile and capability certificate, a frozen retrieval manifest, an admitted packet,
a sealed evidence manifest, a sealed review bundle, an external-human receipt, an
await-human worker receipt, a final worker receipt, and `anchor.json`. JSON references
use the protocol's canonical structured-document digest; payload entries use the exact
raw file bytes. The validator pins the anchor digest outside the fixture and therefore
does not trust a self-asserted fixture hash.

These files are inert conformance data. Their active/qualified/accepted states exist
only inside the synthetic `repo:continuation_fixture` world. They do not accept a real
product, activate authority in another repository, qualify a real model or harness, or
authorize a live operation.
