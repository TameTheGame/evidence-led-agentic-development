# Archive

ELAD 0.6 removed the v0.5 protocol machinery from `main`. Nothing was deleted from history:
every file below is still at the immutable
[`v0.5` tag](https://github.com/TameTheGame/evidence-led-agentic-development/tree/v0.5),
and earlier versions are at `v0.4.0` and `v0.3.0`. To keep using the protocol, pin one of
those tags.

The reasons and the approved plan are in the
[promotion proposal](https://github.com/TameTheGame/evidence-led-agentic-development/blob/da84803/drafts/spec-driven/PROMOTION_PROPOSAL.md)
and [Decisions](docs/DECISIONS.md).

## Removed groups

| Group | At `v0.5` |
|---|---|
| 29 JSON schemas and 7 registries | [`spec/`](https://github.com/TameTheGame/evidence-led-agentic-development/tree/v0.5/spec) |
| 29 JSON templates and 10 Markdown templates | [`templates/`](https://github.com/TameTheGame/evidence-led-agentic-development/tree/v0.5/templates) |
| Validators and the bundle builder | [`tools/`](https://github.com/TameTheGame/evidence-led-agentic-development/tree/v0.5/tools) |
| Validator vectors and fixtures | [`tests/`](https://github.com/TameTheGame/evidence-led-agentic-development/tree/v0.5/tests) |
| Authenticated protocol bundle | [`protocol-bundle.json`](https://github.com/TameTheGame/evidence-led-agentic-development/blob/v0.5/protocol-bundle.json) |
| Version, contract, and capability claims | [`blueprint.json`](https://github.com/TameTheGame/evidence-led-agentic-development/blob/v0.5/blueprint.json) |
| Episode design drafts and the promotion placeholder | [`drafts/`](https://github.com/TameTheGame/evidence-led-agentic-development/tree/v0.5/drafts) |
| Protocol examples | [`examples/two-repository-product/`](https://github.com/TameTheGame/evidence-led-agentic-development/tree/v0.5/examples/two-repository-product), [`examples/mixed-claim-semantic-feature/`](https://github.com/TameTheGame/evidence-led-agentic-development/tree/v0.5/examples/mixed-claim-semantic-feature) |
| Future-runtime placeholders | [`adapters/`](https://github.com/TameTheGame/evidence-led-agentic-development/tree/v0.5/adapters), [`reference/`](https://github.com/TameTheGame/evidence-led-agentic-development/tree/v0.5/reference) |
| Orientation pages, replaced by the README | [`START_HERE.md`](https://github.com/TameTheGame/evidence-led-agentic-development/blob/v0.5/START_HERE.md), [`MANIFEST.md`](https://github.com/TameTheGame/evidence-led-agentic-development/blob/v0.5/MANIFEST.md), [`docs/FIRST_RUN.md`](https://github.com/TameTheGame/evidence-led-agentic-development/blob/v0.5/docs/FIRST_RUN.md) |

## Removed documents

### Folded into the evidence ladder

The rules in these documents now live in [`docs/EVIDENCE_LADDER.md`](docs/EVIDENCE_LADDER.md)
and the [skills](skills/README.md):

- [`ADAPTIVE_RIGOR.md`](https://github.com/TameTheGame/evidence-led-agentic-development/blob/v0.5/docs/ADAPTIVE_RIGOR.md)
- [`EVALUATION_AND_EVIDENCE.md`](https://github.com/TameTheGame/evidence-led-agentic-development/blob/v0.5/docs/EVALUATION_AND_EVIDENCE.md)
- [`HUMAN_DECISION_BOUNDARY.md`](https://github.com/TameTheGame/evidence-led-agentic-development/blob/v0.5/docs/HUMAN_DECISION_BOUNDARY.md)
- [`OPERATIONS_AND_LEARNING.md`](https://github.com/TameTheGame/evidence-led-agentic-development/blob/v0.5/docs/OPERATIONS_AND_LEARNING.md)

### Carried forward in Authority and Safety

The general rules in these documents now live in
[`docs/AUTHORITY_AND_SAFETY.md`](docs/AUTHORITY_AND_SAFETY.md). Their protocol detail stays
at `v0.5`:

- [`ARCHITECTURE.md`](https://github.com/TameTheGame/evidence-led-agentic-development/blob/v0.5/docs/ARCHITECTURE.md)
- [`THREAT_MODEL.md`](https://github.com/TameTheGame/evidence-led-agentic-development/blob/v0.5/docs/THREAT_MODEL.md)
- [`MODEL_QUALIFICATION.md`](https://github.com/TameTheGame/evidence-led-agentic-development/blob/v0.5/docs/MODEL_QUALIFICATION.md)
- the v0.5 [`SECURITY.md`](https://github.com/TameTheGame/evidence-led-agentic-development/blob/v0.5/SECURITY.md)

### Protocol reference, archived as is

- [`PROTOCOL_05_CONFORMANCE.md`](https://github.com/TameTheGame/evidence-led-agentic-development/blob/v0.5/docs/PROTOCOL_05_CONFORMANCE.md)
- [`LIFECYCLE_ORACLE_ASSESSMENT.md`](https://github.com/TameTheGame/evidence-led-agentic-development/blob/v0.5/docs/LIFECYCLE_ORACLE_ASSESSMENT.md)
- [`PATH_IDENTITY.md`](https://github.com/TameTheGame/evidence-led-agentic-development/blob/v0.5/docs/PATH_IDENTITY.md)
- [`MATURITY_MODEL.md`](https://github.com/TameTheGame/evidence-led-agentic-development/blob/v0.5/docs/MATURITY_MODEL.md)
- [`MODEL_HARNESS_READINESS_EVALUATION.md`](https://github.com/TameTheGame/evidence-led-agentic-development/blob/v0.5/docs/MODEL_HARNESS_READINESS_EVALUATION.md)
- [`OPERATING_MODES.md`](https://github.com/TameTheGame/evidence-led-agentic-development/blob/v0.5/docs/OPERATING_MODES.md)
- [`ADOPTION_RUNBOOK.md`](https://github.com/TameTheGame/evidence-led-agentic-development/blob/v0.5/docs/ADOPTION_RUNBOOK.md)
