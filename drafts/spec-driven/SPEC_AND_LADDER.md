# Spec-Driven Evidence: Requirement Format and Evidence Ladder

> **Draft — non-normative.** This is a proposal for how ELAD could support spec-driven
> projects. It does not change any v0.5 contract, schema, or validator. Nothing here
> grants authority. A worked, clearly target-specific example lives in
> [`example-sbox-outpost.spec.md`](example-sbox-outpost.spec.md).

## Why this exists

ELAD already says *use the cheapest reliable evidence for each claim*
([Evaluation and Evidence](../../docs/EVALUATION_AND_EVIDENCE.md)). Today those claims
live in per-task records: a packet names them, a receipt reports them, and an evidence
manifest binds the proof. That works for one-off tasks. In spec-driven work, the same
claims come up in every task that touches the same part of the product, so they belong
in the spec.

This draft puts the claims in the spec. Each requirement carries its own ID, the rung of
evidence that settles it, and the check that proves it. A task then becomes "make these
requirement IDs pass." The proof is the named check passing at a known commit.

Two pieces:

1. **A requirement format** that people can write and agents can parse without extra
   tooling.
2. **An evidence ladder** that orders checks by cost, plus rules for climbing it.

## Part 1 — The requirement format

### Where specs live

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

### Spec file shape

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

### Field rules

| Field | Rule |
|---|---|
| ID | `AREA-TOPIC-NN`. Stable forever. Never reuse a retired ID. |
| Sentence | One observable claim. If it says "and," consider splitting it. |
| `state` | Agents may add or edit `draft` requirements. Only the owner moves a requirement to `agreed` or `retired`. This is the human decision boundary in one field. |
| `rung` | The **cheapest** rung that can actually settle the claim *today* (see Part 2). |
| `check` | Machine rungs: the test or script name, which must contain the ID (for example `OUT_SPAWN_01_...`). Human rungs: a card ID defined in the spec. |
| `target-rung` | Records evidence debt. Use it when a cheaper rung would work but isn't built yet. For example, `rung: session` with `target-rung: engine` until the engine test harness exists. |
| `touches` | Lets a change re-open only the requirements it can affect. |

### Splitting mixed claims

Write mixed claims as separate requirements. "The water tower is visible from both spawns
and the outpost feels lived-in" becomes two requirements:

- an **engine**-rung line-of-sight check, which a trace can prove; and
- an **owner**-rung judgment of feel, which only the owner can give.

Splitting stops the cheap check from being skipped and the expensive one from being
diluted.

### Results stay out of the spec

The spec says what must be true. It does not hold pass/fail state, which would drift.

- **Machine rungs** report through test output. The ID is in the test name.
- **Human rungs** add one line to `spec/ACCEPTANCE.md`:

  ```text
  2026-10-09 · OUT-NET-01 · GREEN · a1b2c3d · Josh · remote client collided with the gate
  ```

A requirement is **met** when its check last passed at a commit and nothing in its
`touches` has changed since.

### The only machinery

One small rung-0 lint, about 50 lines of script with no dependencies, checks the spec
files themselves:

- IDs are unique and well-formed, and no retired ID has been reused;
- `state` and `rung` use allowed values;
- every `agreed` requirement has a `check`;
- every machine-rung `check` name exists in the test sources; and
- every human-rung `check` names a card defined in the spec.

That lint replaces the per-task packet, receipt, evidence manifest, and review bundle
*for spec-driven work*. Git commits supply identity. Test output and `ACCEPTANCE.md`
supply results.

## Part 2 — The evidence ladder

The rungs below refine ELAD's existing claim table by adding the order in which to build
and climb them. Lower rungs are cheaper, faster, and can run in more places.

| Rung | Runs where | Can prove | Never proves by itself | S&box map example (non-normative) |
|---|---|---|---|---|
| **0 · static** | anywhere, including cloud agents | file structure, data validity, spec lint, saved-file contents | anything about engine behavior | layout data is valid; spawn IDs are unique; the saved `.scene` JSON contains exactly one main camera |
| **1 · engine** | the dev machine, headless: real engine, no renderer, no editor | collision exists, physics settles, traces are clear, generated content builds | how it looks, the editor round trip, networking with real clients | a `UnitTests/` project starts the engine through `TestAppSystem`, builds the area with the same generator code, then checks collision, spawn grounding, and route traces |
| **2 · editor** | the real authoring tool | native save, close, and reopen; serialization; hotload; a rendered capture | how it plays with others, how it feels | the generated scene survives save → close → reopen unchanged; a screenshot from a fixed camera |
| **3 · session** | the product running as players run it | host and remote behavior, real-machine performance, clean-client delivery | taste and fitness for purpose | the remote client sees and collides with the same walls; same-machine host/remote is *not* clean-client proof |
| **4 · owner** | the owner, in person | feel, look, fitness for the product's purpose | technical properties | "walking spawn → gate → tower feels like a frontier outpost" |

**Optional advisory: calibrated judge.** A model can review rung-2 captures against a
rubric. Treat that as advice unless the judge has been calibrated for that exact claim
class (see [Evaluation and Evidence](../../docs/EVALUATION_AND_EVIDENCE.md#calibrate-fallible-evaluators-once-then-reuse-them)).
It never closes an owner-rung requirement.

### Ladder rules

1. **Settle each requirement at the cheapest rung that can prove it.** If a trace can
   prove it, don't spend an owner session on it.
2. **A lower rung never closes a higher claim.**
   - Rendered geometry doesn't prove collision.
   - A headless pass doesn't prove the area looks right.
   - Same-machine host/remote doesn't prove clean-client delivery.
   - A model's confidence doesn't prove anything.
3. **Build rungs cheapest-first.** Bring up rung 0, then rung 1, before investing in
   automating rung 2 or rung 3. Never make cheap evidence wait on expensive
   infrastructure. Until a rung exists, a requirement may temporarily use the next rung
   up and record the cheaper one in `target-rung`.
4. **Check first where a check can exist.** For rung-0 and rung-1 requirements, write the
   check, watch it fail, then change the content or generator. This is where test-first
   coding fits. Owner-rung requirements get a card instead.
5. **Report the rung reached.** "Done" alone is not a report. Say, for example,
   "OUT-SPAWN-01 passed at engine, commit `a1b2c3d`; OUT-NET-01 needs a session card."
6. **Re-check only what a change can affect.** A change re-opens the requirements whose
   `touches` it changes. Before the owner accepts a milestone, run every machine-rung check.
7. **Retries follow reversibility.** Rungs 0–2 on local or disposable copies are
   reversible, so they get ELAD's ordinary default: two materially different attempts,
   more for cheap experiments that keep teaching something
   ([Operations and Learning](../../docs/OPERATIONS_AND_LEARNING.md)). Reserve one-shot
   attempt limits for actions that are expensive or impossible to undo.
8. **Generated content comes from the generator.** Agents change spec data or generator
   code, then regenerate. They never hand-edit generated or engine-owned output. This
   restates ELAD's existing rule that authoritative serializers write opaque artifacts.
9. **Ask the owner last and briefly.** Prepare an owner or session card only after every
   lower-rung requirement it depends on passes. A card has numbered steps, the expected
   result, and how to reply (`GREEN` or `RED` plus what you saw). See
   [Decisions You Keep](../../docs/HUMAN_DECISION_BOUNDARY.md).

## How a task runs

1. **Intent.** The owner says what they want. If no `agreed` requirement covers it, the
   agent drafts requirements (`state: draft`) and asks the owner to agree them. A light
   task already covered by `agreed` requirements skips this step.
2. **Checks first.** The agent writes failing rung-0 and rung-1 checks for the requirement
   IDs in scope.
3. **Change.** The agent edits the data, the generator, or the code.
4. **Climb.** The agent runs the ladder upward as far as it can run unattended, stopping
   at the first failure to find its cause before changing anything else.
5. **Report.** For each ID: the rung reached, pass or fail, and the commit. Then come the
   cards the owner needs to run.
6. **Owner.** The owner replies `GREEN` or `RED`. The agent appends the line to
   `ACCEPTANCE.md`.

Rigor and the ladder are separate decisions:

- **Rigor** decides how much process the task needs: its brief, review, and isolation
  ([Adaptive Rigor](../../docs/ADAPTIVE_RIGOR.md)).
- **The ladder** decides what evidence each claim needs.

A light task might touch one agreed requirement and run one engine test. A change to the
generator every area depends on might re-run every machine-rung check and get an
independent review.

## Fit with Superpowers-style skills (non-normative)

If a project also installs the Superpowers skill library:

| Superpowers skill | How it fits |
|---|---|
| brainstorming | writes `draft` requirements into the spec instead of a separate design document |
| writing-plans | its tasks list requirement IDs |
| test-driven-development | applies to rung-0 and rung-1 requirements only |
| verification-before-completion | "verified" must name the rung reached |

Put those overrides in the project's `AGENTS.md`, which Superpowers treats as taking
precedence over its skills.

## Open questions before adoption

These are the facts a short spike should settle for an S&box map project. References are
to `Facepunch/sbox-public` at `3915f1a69810026e23d331581266636de89411d5`.
[`engine-rung-spike/`](engine-rung-spike/README.md) is a ready-to-run kit for questions 1–3.
Its first run confirmed headless engine startup and player physics, and found that
generated-mesh collision does not yet build in a project test; see its Results section.

1. **Test projects need a code project.** `Project.Solution.cs` generates a `UnitTests`
   project only for `game`, `library`, and `addon` projects, not `content` projects. A
   content-type map needs a small companion code project to host its rung-1 tests.
2. **Traces without base content may need a surface.** The engine's own integration
   tests install a fallback surface before tracing because headless tests mount no base
   content (`engine/Tests/Sandbox.Test.Integration/Assembly.cs`). They do it through
   `Surface.All`, which is `internal`, so a project's tests can't copy it. Confirm whether
   traces work in a project test, or what public route replaces it.
3. **Loading the project's own saved scenes headlessly is unproven.** Building the area
   in-test with the same generator code avoids this question for most rung-1 checks.
4. **Rung 1 is Windows-only.** `TestAppSystem` needs the installed engine
   (`FACEPUNCH_ENGINE`) and its win64 native libraries, and the machine needs the .NET 10
   SDK because S&box projects target `net10.0` (confirmed by the spike's first run).
   Cloud or Linux agents can run rung 0 only.
5. **Automating rung 2 is optional.** A short owner card is an acceptable rung-2 check
   until automation is cheaper than the card.

## What this would replace if adopted

For spec-driven projects only, the following would reduce to spec files, test names,
`ACCEPTANCE.md`, and Git:

- the task-packet, worker-receipt, evidence-manifest, retrieval-manifest, and
  review-bundle chain; and
- most per-task claim bookkeeping.

The assured protocol remains available for work that genuinely crosses contexts or
owners. Adopting this draft would need its own release decision.
