# Model and Harness Readiness Evaluation

ELAD qualifies an exact coding-worker subject rather than assuming a model name or a
harness reputation is enough. A qualification subject includes the model artifact and
configuration, runtime and hardware, harness and adapter, prompt/context compiler,
tools and permissions, resource budgets, task corpus, evaluators, and evidence policy.
A material change creates a new subject.

Use readiness evaluation when a project is choosing among local coding models or
harnesses for repeated ELAD work, or when the cost of adopting the wrong worker is high
enough to justify a controlled comparison. Do not add it to an ordinary task that is
already covered by a trustworthy check.

## Public operational companion

The separately maintained
[ELAD Harness Readiness Suite](https://github.com/TameTheGame/elad-harness-readiness-suite)
implements this comparison method without adding an operational surface to this Level-0
blueprint. The first public release is
[`v0.1.0`](https://github.com/TameTheGame/elad-harness-readiness-suite/releases/tag/v0.1.0),
resolved at commit
[`d2922f9`](https://github.com/TameTheGame/elad-harness-readiness-suite/commit/d2922f9259bf24e5fbb75dfca371e7623c7940cd).

The companion is model-, provider-, runtime-, platform-, and harness-agnostic. It
provides:

- neutral JSON contracts for experiments, tasks, adapters, results, calibration,
  blinded review, and decisions;
- exact arm-specific qualification fingerprints;
- controlled-parity and production-realism lanes;
- lane-local counterbalanced schedules and fresh per-run home/cache/temp state;
- frozen deterministic and semantic evaluator calibration;
- hard resource, authority, protocol, measurement, and verifier-closure gates;
- hash binding from the frozen contract through raw results, blind review, and final
  decision;
- material-win thresholds that preserve `NO_CLEAR_WINNER`; and
- separate lanes or claims for explicit handoff, native long-session/compaction
  behavior, and OS-enforced restricted-data isolation.

Its deterministic synthetic demo and dependency-free runtime are hosted-tested on
Windows, macOS, and Ubuntu with Python 3.10 and 3.13. The release run is
[`32974345575`](https://github.com/TameTheGame/elad-harness-readiness-suite/actions/runs/32974345575).

## Fair comparison sequence

```text
bound the real work class and exact subjects
  -> calibrate deterministic and semantic evaluators
  -> freeze tasks, budgets, identities, thresholds, and anonymous schedule
  -> prove every arm is measurable under controlled parity
  -> run counterbalanced production-realism trials
  -> review semantic products without identity, timing, token, or reasoning leakage
  -> seal review, unblind, and apply the frozen lexicographic decision
  -> choose a material winner, retain the incumbent, or report no eligible subject
```

Equalize information, authority, resource envelopes, retry ownership, and evidence
obligations. Preserve normal harness behavior only where the decision is intentionally
about that behavior. Mark parity failures ineligible, do not average away hard failures,
and do not retroactively tune tasks or scoring around observed products.

## Authority and evidence boundary

The companion repository is operational code, but it grants no authority over a model,
harness, repository, network, result publication, or restricted data. Running an
experiment remains an owner-local decision. Its process runner is not an OS sandbox;
assigned-root read isolation and network containment require a common external boundary
and separate evidence.

A framework self-test proves only framework behavior on synthetic subjects. A real
readiness result applies only to the exact frozen subjects and declared work class. It
does not certify a model family, rank harnesses universally, prove production safety, or
promote this ELAD repository beyond Level 0.

Start with the companion's
[Start Here](https://github.com/TameTheGame/elad-harness-readiness-suite/blob/v0.1.0/START_HERE.md),
then use its methodology, adapter contract, neutral experiment template, and safe demo.
Keep proprietary fixtures, mappings, raw results, credentials, and model artifacts in
the adopting project's private evidence boundary.
