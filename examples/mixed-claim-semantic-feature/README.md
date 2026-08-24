# Mixed-Claim Semantic Feature — Small Evaluated Example

This fictional, non-operational example shows how one low-consequence feature can contain
both exact and semantic claims without turning every check into LLM evaluation.

## Feature

An opt-in local command reads a bounded metadata bundle and emits a short purpose summary.
Ordinary use never calls a model. Model failure is isolated to the summary field and does
not discard the underlying record.

## Claim split

| Claim | Domain | Evaluator class | Cheapest reliable evidence |
|---|---|---|---|
| opt-in flag and unchanged default path | `static_deterministic` | exact deterministic | CLI unit checks with exact call counts and output fixtures |
| bounded metadata selection | `static_deterministic` | exact deterministic | fixture comparison against independently specified limits |
| service failure does not discard the record | `static_deterministic` | exact deterministic | mocked endpoint failure and exact result assertion |
| summary states supported purpose without inventing a synthesis | `semantic_or_stochastic` | fallible, initially unproven | frozen cases, concise rubric, calibrated model judge, and two generator draws |

The task minimum is `evaluated` because one product claim is semantic. The exact claims
remain ordinary deterministic checks; the semantic evaluator's maturity does not smear
calibration requirements onto them. Calling a local inference service is a prerequisite,
not by itself a `runtime_or_operational` claim.

## Small evaluation shape

`cases.json` contains independent facts and failure discriminators. A small project can
pair it with a short local runner that:

1. records the exact inference subject and material generation settings;
2. generates a small proportional sample (two draws here, not a Monte Carlo campaign);
3. checks mechanical forbidden facts in code;
4. asks a calibrated judge to score only the semantic rubric;
5. preserves case-level results and the first causal error; and
6. changes one causal factor before a focused rerun.

If the aggregate threshold passes but the conflict case still invents a merged purpose,
make one cheap prompt correction, rerun the affected set, and then stop when the designed
discriminator passes. A model-judge score remains model evidence, not external-human
acceptance.

This compact shape is distinct from `templates/evaluation-pack.template.json`, which is
available only when an assured or durable cross-context workflow needs the full contract.
