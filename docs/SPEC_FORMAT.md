# Spec Format

In spec-driven work, the same claims come up in every task that touches the same part of
the product, so ELAD puts them in the spec. Each requirement carries its own ID, the rung
of evidence that settles it, and the check that proves it. A task then becomes "make these
requirement IDs pass", and the proof is the named check passing at a known commit.

The rungs are defined in [Evidence Ladder](EVIDENCE_LADDER.md). A worked, target-specific
example is the [S&box outpost spec](../examples/sbox/outpost.spec.md). A project that
already has gates maps them onto its first spec; see
[Projects That Already Have Gates](EXISTING_GATES.md).

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

A spec can name a data file before it exists. Write `(not written yet)` after its path on
the `data:` line, and drop the note when the file is committed. Until then, requirements
that read it can't be met.

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
- touches: <optional paths or data keys this requirement depends on; without it, any change reopens it>
- why: <optional one line>
```

## Field rules

| Field | Rule |
|---|---|
| ID | `AREA-TOPIC-NN`. Stable forever. Never reuse a retired ID. |
| Sentence | One observable claim. If it says "and", consider splitting it. |
| `state` | Agents may add or edit `draft` requirements. Only the owner moves a requirement to `agreed` or `retired`. This is the owner's decision boundary in one field. |
| `rung` | The **cheapest** rung that can actually settle the claim *today*. |
| `check` | Machine rungs: the test or script name, which must contain the ID (for example `OUT_SPAWN_01_...`), or a script name followed by the ID (`editor-check OUT-SAVE-01`). Human rungs: a card ID defined in the spec. `static`, `engine` and `editor` are machine rungs and `owner` is human. `session` is a machine rung when a script runs the session, and human when a person does, by a card. |
| `target-rung` | Records evidence debt. Use it when a cheaper rung would work but isn't built yet. For example, `rung: session` with `target-rung: engine` until the engine test harness exists. |
| `touches` | Lets a change reopen only the requirements it can affect. Write paths, folders or data keys, such as `spec/outpost.layout.json` or `Code/OutpostGenerator.cs`, not prose, so a change can be matched against them. A requirement without `touches` depends on everything, so any change reopens it. |

## Splitting mixed claims

Write mixed claims as separate requirements. "The water tower is visible from both spawns
and the outpost feels lived-in" becomes two requirements:

- an **engine**-rung line-of-sight check, which a trace can prove; and
- an **owner**-rung judgment of feel, which only the owner can give.

Splitting stops the cheap check from being skipped and the expensive one from being
diluted.

## Results stay out of the spec

The spec says what must be true. It doesn't hold pass or fail state, which would drift.

- **Machine rungs** report through test output. The ID is in the test name, or next to
  the script's name in the `check` field, such as `editor-check OUT-SAVE-01`. When one
  script run settles several requirements, it prints one result line per ID, such as
  `OUT-SAVE-01 PASS` or `OUT-SAVE-01 FAIL - the second save changed the file`, and exits
  non-zero if any line fails. Keep each result on its one line: when it quotes text another
  program wrote, such as an engine test's assertion message, turn that text's line breaks
  into spaces first. A runner or a reader that judges a result by its own line otherwise
  finds its reason, or the word it looks for, on a later line. A line may end with the
  build it ran on, such as `OUT-SAVE-01 PASS · S&box 26.10.27c`, since an engine or runtime
  update can change a result with no commit.
- **Human rungs** add one line to `spec/ACCEPTANCE.md`, with the card's reply. The commit
  may carry the build the owner checked, in brackets:

  ```text
  2026-10-09 · OUT-NET-01 · GREEN · a1b2c3d · Owner · remote client collided with the gate
  2026-10-09 · OUT-FEEL-01 · GREEN · a1b2c3d (S&box 26.10.27c) · Owner · reads as an outpost
  ```

A requirement is **met** when its check last passed at a commit and nothing in its
`touches` has changed since. Without `touches`, any later commit reopens it. A human-rung
check passes only on the card's passing reply, such as `GREEN` or `GO`. A card the owner
hasn't answered leaves its requirement unmet.

## A spec lint for projects

A project may add one small rung-0 lint, a dependency-free script, that checks its spec
files:

- IDs are unique and well-formed, and no retired ID has been reused;
- `state` and `rung` use allowed values;
- every `agreed` requirement has a `check`;
- every machine-rung `check` names its requirement's ID;
- every `agreed` requirement's machine-rung `check` name exists in the test sources; and
- every human-rung `check` names a card defined in the spec.

**Report a missing machine check, or one that doesn't name its ID; don't fail on them.** A
check is written after the owner agrees its requirement, so a newly agreed requirement has
no check yet, and an older spec may hold checks named before this rule. The other items
fail the lint.

**A name in the test sources doesn't mean the check runs.** The lint finds the check, not
whatever runs it. A check that the project's suite and CI leave out passes nothing and
fails nothing, so a requirement or a record that cites it claims what nothing holds. In the
commit that brings a citation or its check, add the check to the runner for its rung, with a
planted fault it fails: rung-0 checks to the suite every change runs, and engine and editor
checks to the runner the machine that has the engine or editor uses.

**An owner gate is worth adding.** It compares each requirement with a base commit and
reports, as needing the owner, any change to an `agreed` requirement's sentence, state,
rung, or check, and any requirement newly `agreed` or `retired`. A spec the base lacks is
compared as empty. The gate reports and never blocks, because the owner may already have
agreed the change. Compare with the last commit the owner has seen: before each commit, or
against the commit the task started from, and in a suite or CI, against the point the
branch left the main branch. Once a change is committed, the last commit holds it, and the
gate has nothing left to report. Show the gate's output whether or not the lint fails, since
a wrapper that shows output only on failure drops every finding, and say so plainly when
the gate had no base to compare with.

**So is a hold on files built from an input the owner adopted.** A project may build part
of its spec, or of its rules, from an input the owner adopted, such as a plan. Pin the
input by its SHA-256 in the decision record, and have the lint hold the built parts to
their copy at the commit that last pinned it. Give the owner's later answers a route: a
commit that changes the built parts passes only when, in that same commit, it pins the new
input's SHA-256 and records the owner's answer that changed it. Every other change fails.
Without that route, the owner's first answer can only land by loosening the check. Unlike
the owner gate, this blocks, since a commit either carries the pin and the answer or it
doesn't. Have the build rewrite only the parts that answer names, so the rest can't change
with it. Don't trust that list of parts when it is made by hand: after the rebuild, build
the new input afresh into a scratch copy and compare it with the rebuilt files. Any
difference outside the values the project keeps on its own is a part the input changed that
the list missed. The hold can't see it, since it compares the built parts with their copy
at the last pin, not with the input. An answer that changes only a few parts can land
without a new input: commit it as an amendment file that names each part it changes and the
new value, pin the file's SHA-256 in the decision record, and hold the built parts to the
input with each amendment applied. A later new input must then carry each amended value, or
its decision must say it supersedes that amendment, since a rebuild from it would otherwise
undo the owner's answer while every check passes.

The core doesn't ship a lint; each project owns its own. A worked example is
[`examples/sbox/tools/spec_lint.py`](../examples/sbox/tools/spec_lint.py). It covers every
item in the list above and the owner gate, with fixtures, but not the hold. It looks check
names up only for `agreed` requirements, in the folders passed with `--sources`. With
`--owner-exit`, a change that needs the owner gets its own exit code.

With a lint like this, spec-driven work needs no per-task records. Git commits supply
identity, and test output and `ACCEPTANCE.md` supply results.
