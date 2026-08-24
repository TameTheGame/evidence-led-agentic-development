# Evaluator Card — <Claim class>

Create this once per material evaluator version/claim class, not once per routine task.
Routine work cites the current card and runs focused cases. Rerun the affected
calibration slice after evaluator/tool/schema/runtime drift or a newly discovered
consequential false-green mode.

## Subject and scope

- Evaluator ID/version/hash: <identity>
- Claim class/evidence class: <classes>
- Eligible writer profile IDs: <exact IDs or none>
- Eligible external reviewer IDs: <exact human IDs or none>
- Accepted subject selector: <kind/selector/repository/id/base/SHA-or-null>
- Required resolved subject: <kind/repository/id/base/SHA>
- Explicit non-claims: <boundaries>

## Cases

| Case | Type | Expected result | False-green purpose |
|---|---|---|---|
| <known green> | positive | pass | baseline |
| <deliberate failure> | negative | fail | prove discrimination |
| <wrong/stale subject> | adversarial | fail | prove correlation |
| <zero discovery/silent skip> | harness | fail | prove discovery |
| <crash/timeout> | harness | inconclusive/fail | prevent missing evidence from green |
| <holdout> | qualification | <expected> | reduce overfitting |

## Thresholds and variance

<False-positive/negative ceilings, cold-run count, calibrated model threshold, and
inconclusive handling.>

## Retention and invalidation

<Evidence-manifest and review-bundle paths/hashes, expiry, and changes that require
requalification. A sealed bundle must bind the exact packet, candidate, resolved
subject, claim IDs, evidence IDs, and artifact bytes presented for review.>
