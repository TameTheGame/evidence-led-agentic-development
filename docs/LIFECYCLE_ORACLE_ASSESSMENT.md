# Lifecycle Oracle Assessment

## Decision

Retain and strengthen the lifecycle machinery.

It is inexpensive, reusable, platform-neutral conformance infrastructure. It should not
be removed because the number 44,100 looks large, and it should not be presented as
44,100 separately designed behavioral scenarios.

## What 44,100 represents

The assured worker-receipt lifecycle has seven finite dimensions:

| Dimension | Values |
|---|---:|
| Finalization ceiling | 3 |
| Terminal status | 5 |
| Finalization state | 5 |
| Candidate state | 3 |
| Claim aggregate | 7 |
| Evidence-manifest state | 4 |
| Next action | 7 |

The Cartesian product is:

```text
3 × 5 × 5 × 3 × 7 × 4 × 7 = 44,100
```

The external table admits 33 exact rows and denies 44,067. Ignoring compatible
finalization-ceiling expansion, the 33 rows represent 15 distinct semantic lifecycle
shapes.

Many denied tuples are deliberately contradictory or impossible. That negative space is
valuable because redundant fields must not be combined into false completion. For
example, a draft evidence manifest cannot support success, read-only work cannot claim a
finalized candidate, and unresolved human acceptance cannot silently become technically
complete.

## Cost

The full-domain enumeration is measured in milliseconds and streams tuples rather than
materializing 44,100 receipt files. Its cost is protocol-version maintenance, not
per-task labor. It is appropriate to run on protocol changes and in cheap conformance/CI
checks.

The expensive anti-pattern would be requiring every small implementation to construct a
formal seven-dimensional receipt. ELAD does not do that: the lifecycle applies only to
the optional assured receipt protocol.

## Independence correction

Version 0.2 loaded the 33 rows and checked operational admission by membership. It
exhaustively verified closed-world construction, but documentation overstated the
independence of its semantic oracle.

Version 0.3 corrects this by:

- preserving the external 33-row transition table;
- implementing a separately expressed lifecycle rule predicate that does not read the
  table;
- differentially comparing the table and predicate over all 44,100 tuples;
- testing focused claim-aggregate cases;
- covering all 15 unique admitted shapes;
- testing single-field denial mutations across every dimension;
- retaining checkpointed `NEED_CONTEXT` as denied until real workflow evidence
  justifies a policy change.

Expected answers are not generated from the production admission function. Mutating
either the table or rule predicate independently must cause conformance failure.

## Maintenance rule

Change lifecycle semantics only through a versioned protocol change that updates:

- the external transition table;
- the independent rule predicate;
- focused aggregate and shape vectors;
- integration fixtures and malicious controls;
- authenticated bundle digests;
- the human-readable 15-shape explanation.

Do not generate the expected table from the rule implementation under test. If a future
declarative source expands rows mechanically, it must remain independently reviewed.

## Final proportionality conclusion

- **Coverage value:** high for contradictory state and false-completion prevention.
- **Execution cost:** negligible.
- **Recurring task cost:** zero unless the task elects the assured receipt protocol.
- **Conceptual cost:** moderate and confined to protocol maintainers.
- **Simpler equivalent:** none that provides the same closed-world cross-field check;
  the 15-shape summary improves human understanding but cannot replace the exact table.
- **Disposition:** retained, honestly described, and given genuine differential
  independence.
