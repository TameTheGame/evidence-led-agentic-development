# Spec Format

In spec-driven work, the same claims come up in every task that touches the same part of
the product, so ELAD puts them in the spec. Each requirement carries its own ID, the rung
of evidence that settles it, and the check that proves it. A task then becomes "make these
requirement IDs pass", and the proof is the named check passing at a known commit.

The rungs are defined in [Evidence Ladder](EVIDENCE_LADDER.md). A worked, target-specific
example is the [S&box outpost spec](../examples/sbox/outpost.spec.md).

## Where specs live

```text
spec/
  <area>.spec.md        # intent and requirements (this format)
  <area>.<data>.json    # optional project-owned data the generator reads
  ACCEPTANCE.md         # one line per human-rung result
```

ELAD defines only the `.spec.md` requirement format and the acceptance-log line. Data
files belong to the project and use whatever schema the project's generator needs.
Requirements may refer to that data. For example, "every spawn in the layout lands on
ground" applies to whatever spawns the data file lists, so checks don't hard-code values.

## Spec file shape

```markdown
# <Area name>

owner: <who agrees requirements>
data: <optional path(s) to project-owned data files>

## Intent
<A few sentences in the owner's words: what this area is for and what matters.>

## Out of scope
<What this spec deliberately does not cover.>

## Requirements

### <ID> — <one observable sentence>
- state: draft | agreed | retired
- rung: static | engine | editor | session | owner
- check: <test name, script name, or card ID>
- target-rung: <optional cheaper rung this should move to when one exists>
- touches: <optional paths or data keys this requirement depends on>
- why: <optional one line>
```

## Field rules

| Field | Rule |
|---|---|
| ID | `AREA-TOPIC-NN`. Stable forever. Never reuse a retired ID. |
| Sentence | One observable claim. If it says "and", consider splitting it. |
| `state` | Agents may add or edit `draft` requirements. Only the owner moves a requirement to `agreed` or `retired`. This is the owner's decision boundary in one field. |
| `rung` | The **cheapest** rung that can actually settle the claim *today*. |
| `check` | Machine rungs: the test or script name, which must contain the ID (for example `OUT_SPAWN_01_...`). Human rungs: a card ID defined in the spec. |
| `target-rung` | Records evidence debt. Use it when a cheaper rung would work but isn't built yet. For example, `rung: session` with `target-rung: engine` until the engine test harness exists. |
| `touches` | Lets a change reopen only the requirements it can affect. |

## Splitting mixed claims

Write mixed claims as separate requirements. "The water tower is visible from both spawns
and the outpost feels lived-in" becomes two requirements:

- an **engine**-rung line-of-sight check, which a trace can prove; and
- an **owner**-rung judgment of feel, which only the owner can give.

Splitting stops the cheap check from being skipped and the expensive one from being
diluted.

## Results stay out of the spec

The spec says what must be true. It doesn't hold pass or fail state, which would drift.

- **Machine rungs** report through test output. The ID is in the test name.
- **Human rungs** add one line to `spec/ACCEPTANCE.md`:

  ```text
  2026-10-09 · OUT-NET-01 · GREEN · a1b2c3d · Owner · remote client collided with the gate
  ```

A requirement is **met** when its check last passed at a commit and nothing in its
`touches` has changed since.

## A spec lint for projects

A project may add one small rung-0 lint, about 50 lines of dependency-free script, that
checks its spec files:

- IDs are unique and well-formed, and no retired ID has been reused;
- `state` and `rung` use allowed values;
- every `agreed` requirement has a `check`;
- every machine-rung `check` name exists in the test sources; and
- every human-rung `check` names a card defined in the spec.

**An owner gate is worth adding.** It compares each `agreed` requirement with the last
commit and reports any change to its sentence, state, rung, or check as needing the owner.
It reports and never blocks, because the owner may already have agreed the change.

The core doesn't ship a lint; each project owns its own. A worked example is
[`examples/sbox/tools/spec_lint.py`](../examples/sbox/tools/spec_lint.py). It covers the
format checks and the owner gate, with fixtures.

With a lint like this, spec-driven work needs no per-task records. Git commits supply
identity, and test output and `ACCEPTANCE.md` supply results.
