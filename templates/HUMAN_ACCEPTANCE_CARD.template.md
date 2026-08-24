# Human Acceptance Card — <Claim/outcome>

## Exact subject

- Project/candidate/build/run: <identity>
- Packet/protocol identity: <immutable references>
- Claim ID/class and evidence class: <exact IDs>
- Resolved subject: <kind/repository/id/base HEAD/SHA-256>
- Sealed review bundle: <immutable reference and SHA-256>
- Artifact/resource/package/data identity: <hashes>
- Objective checks already green: <checks/evidence>
- Human claim(s) remaining: <claim IDs and descriptions>

## Reviewer eligibility

- Reviewer ID: <eligible human ID from the active evidence-policy rule>
- Evaluator ID: <exact external-human evaluator ID>
- Superseded human receipt: <immutable reference or none>

## Prerequisites

<What is already prepared. The reviewer should not need to discover paths or schedule
tests.>

## Actions

1. <Exact action. Use H/R labels if applicable.>
2. <Exact action.>

## Pass/fail

- Pass: <visible/experiential result>
- Fail: <contradictory result>
- Stop immediately if: <condition>

## Evidence to return

<Short natural-language observation and optional screenshot/recording.>

## Reply format

`<CLAIM ID> — PASS|FAIL|INCONCLUSIVE — <one-sentence observation>`

The returned durable receipt records the exact reviewer/evaluator pair, packet,
candidate, resolved subject, review bundle, decision, limitations, time, and immutable
supersession link. It closes only the named human claim. It does not promote or publish
the candidate.
