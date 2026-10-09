# Evidence Ladder

ELAD asks one question at every step:

> What is the cheapest reliable evidence that can resolve the uncertainty that matters
> now?

The ladder orders evidence by cost. Requirements in the [spec](SPEC_FORMAT.md) name the
rung that settles them. The three [skills](../skills/README.md) teach agents to apply
this page; where a skill already states a rule, this page links to it instead of
repeating it.

## The rungs

Lower rungs are cheaper and faster, and they can run in more places.

| Rung | Runs where | Can prove | Never proves by itself |
|---|---|---|---|
| **0 · static** | anywhere, including cloud agents | file structure, data validity, spec lint, saved-file contents | anything about runtime behavior |
| **1 · engine** | the dev machine: the real engine or runtime, headless, no editor | collision, physics, traces, generated content building, exact program behavior | how it looks, the editor round trip, networking with real clients |
| **2 · editor** | the real authoring tool | native save and reopen, serialization, hotload, a rendered capture | how it plays with others, how it feels |
| **3 · session** | the product running as users run it | host and remote behavior, real-machine performance, clean installs | taste and fitness for purpose |
| **4 · owner** | the owner, in person | feel, look, fitness for the product's purpose | technical properties |

Projects without an editor or a networked session skip those rungs. The
[S&box example](../examples/sbox/README.md) shows each rung for a game map, including a
working rung-1 test kit.

**A model judge is advice, not a rung.** A model can review captures against a rubric. Its
verdict counts as evidence only for a claim class it has been calibrated on (see
[Calibrate fallible evaluators](#calibrate-fallible-evaluators-once-then-reuse-them)), and it
never closes an owner-rung requirement.

## Ladder rules

1. **Settle each requirement at the cheapest rung that can prove it.** If a trace can
   prove it, don't spend an owner session on it.
2. **A lower rung never closes a higher claim.**
   - Rendered geometry doesn't prove collision.
   - A headless pass doesn't prove the area looks right.
   - Same-machine host and remote don't prove clean-client delivery.
   - A model's confidence doesn't prove anything.
3. **Build rungs cheapest-first.**
   - Bring up rung 0, then rung 1, before investing in automating rung 2 or rung 3.
   - Never make cheap evidence wait on expensive infrastructure.
   - Until a rung exists, a requirement may use the next rung up and record the cheaper
     one in `target-rung`.
4. **Check first where a check can exist.** For rung-0 and rung-1 requirements, write the
   check, watch it fail for the right reason, then change the content or code. Owner-rung
   requirements get a card instead.
5. **Report the rung reached.** "Done" alone is not a report. For example: "OUT-SPAWN-01
   passed at engine, commit `a1b2c3d`; OUT-NET-01 needs a session card."
6. **Recheck only what a change can affect.** A change reopens the requirements whose
   `touches` it changes. Before the owner accepts a milestone, run every machine-rung
   check.
7. **Retries follow reversibility.** See [Learn from the first causal failure](#learn-from-the-first-causal-failure).
8. **Generated content comes from the generator.** Agents change spec data or generator
   code, then regenerate. They never hand-edit generated or engine-written output.
9. **Ask the owner last and briefly.** Prepare a card only after every lower-rung
   requirement it depends on passes. The card format is in
   [`asking-the-owner`](../skills/asking-the-owner/SKILL.md).

## Match evidence to each claim

**Split claims before choosing checks.** One feature often holds exact claims and uncertain
ones. A command-line feature might have exact claims about its flag, exit code, and output
format, plus a semantic claim about the summary it generates. Keep the exact claims
deterministic, and evaluate only the semantic one.

**Running a program doesn't make a claim a runtime claim.** Exact output, exit status,
fixtures, and mocked failures stay deterministic. Live runtime evidence is needed only when
the truth depends on something an exact comparison can't establish, such as:

- timing;
- persistence;
- native effects; or
- distributed state.

**Evaluator maturity belongs to each claim.** A new exact regression whose expected result
comes from an independent requirement is not a fallible evaluator just because it is new. A
semantic judge in the same task may still be unproven.

## Avoid circular proof

The implementation shouldn't produce both its behavior and the expected answer. An
independent expectation can come from:

- an existing specification or test;
- a separately written fixture, truth table, or rule;
- an observer outside the changed component, such as the engine's own log or a trace;
- held-out cases the implementer can't see;
- a calibrated evaluator; or
- an independent reviewer, when the consequence warrants it.

The same agent may run a trustworthy exact test it didn't write. Stronger separation pays
off when the evaluator is fallible, derived from the implementation, or exposed to its own
held-out answers, or when a false green would be costly.

## Calibrate fallible evaluators once, then reuse them

Before relying on a rubric or a model judge, show it recognizes known-good and known-bad
cases. Cover the failures that matter for its job:

- a wrong or stale subject;
- missing output;
- crashes;
- silent skips; and
- variance across repeated runs.

Record what the evaluator supports and what would invalidate that result. Then reuse it.
Recheck only the affected slice after its model, prompt, runtime, or claim class changes,
or after a new false-green pattern appears.

Sampling the product and sampling the judge answer different questions. A few product runs
expose unstable output, and repeated judge runs measure the judge's own variance.

If a score passes while a case built to catch a real defect still fails, don't hide the
failure inside the score. Make one cheap causal fix, rerun the affected evidence, and stop
when the claim is supported.

## Rigor, the ladder, and authority are separate

Three decisions stay apart:

- **Rigor:** how much process this task needs, such as its brief, review, and isolation.
  The levels and when to move between them are in
  [`choosing-rigor`](../skills/choosing-rigor/SKILL.md).
- **The ladder:** what evidence each claim needs.
- **Authority:** what the work may change, run, publish, or accept. That comes only from
  the owner and the project; see [Authority and Safety](AUTHORITY_AND_SAFETY.md).

A light task can touch one agreed requirement and run one engine test. A change to a
generator every area depends on may rerun every machine-rung check and get an independent
review. Neither choice grants any permission.

**A durable control must pay for itself.** Add a lasting check, review, or record only when
its lifetime cost is lower than the cost of the failure it prevents. That cost includes
writing, running, maintaining, reviewing, and handling false alarms. A specific high
consequence can justify more. Passing an assurance system's own tests proves it is
consistent, not that it is worth its complexity.

**Revalidate by cause.** A change invalidates only the claims and evidence it can causally
affect, so recheck that scope and keep the rest. A full fresh review is needed only when the
footprint can't be bounded, or when the change touches one of these:

- architecture;
- authority;
- what evidence means;
- security, privacy, or rights; or
- evaluator behavior.

**Use Git for identity.** For tracked files, the commit and a clean working tree identify
what was checked. Add byte counts or hashes only for files Git doesn't track.

**Extra review cycles need new evidence.** The review budgets are in
[`choosing-rigor`](../skills/choosing-rigor/SKILL.md). An extra cycle needs unresolved
high-consequence uncertainty plus new objective evidence, or a fresh owner decision after
the expected cost and benefit have been reported.

## What the owner keeps, and what can be automated

The owner's decisions and the card format are in
[`asking-the-owner`](../skills/asking-the-owner/SKILL.md).

**Safe to automate once proven:**

- path and scope checks;
- deterministic transforms and formatting;
- compile, unit, integration, and headless checks;
- capturing evidence;
- classifying failures; and
- writing down facts the work established.

**Delegating a claim class.** The owner may later delegate a narrow, objective class of
claims to a proven evaluator. That delegation should name:

- the evaluator;
- the task class it covers;
- its thresholds;
- when it expires;
- what drift reopens it; and
- what the owner still decides.

It is never a blanket transfer of product authority.

## Learn from the first causal failure

```text
observe the failure
  -> identify the first responsible layer
  -> choose the smallest discriminating experiment
  -> change only that layer
  -> rerun the focused evidence
  -> continue, stop, or escalate
```

- **Every attempt names its purpose.** It says what it tests and what changed. Never retry
  blindly.
- **The ordinary limit is two attempts per root cause.** Two materially different attempts,
  then stop and report what was learned. Cheap, reversible experiments may get more while
  each one teaches something.
- **One-shot limits are only for actions that are hard to undo.** On a local, reversible
  action, a single-attempt rule turns one small bug into a stopped project.
- **Some failures stop the work at once.** Ambiguous authority, privacy, or persistence,
  or an effect on a shared target, stops the work immediately.

## Keep records and context small

- **Record only what can change a decision.** A light task may need just the command, the
  result, the changed paths, and the diff. Leave unknown measurements unknown and say why.
- **Keep raw evidence out of the agent's context.** Logs, traces, screenshots, and
  transcripts stay in files. Bring in only the slice that answers a causal question.
- **Redact before sharing.** Remove secrets and private data before evidence is routed
  anywhere wider.
- **Keep only reusable lessons.** Write a lasting lesson only when it is new, recurring, or
  high-impact, or when it changes a reusable check. A one-off failed test needs no incident
  write-up.

**Measure whether autonomy is helping.** Does the workflow produce more evidence-backed
outcomes with less supervision, context, waiting, cost, and risk? Compare similar tasks.
Treat security, privacy, authority, and evidence quality as limits, never as values traded
away inside one score.

**Simplification counts as progress.** Periodically ask:

- which records are actually used;
- which checks catch realistic failures; and
- which reviews could go without weakening the evidence or authority.

A method that only grows has stopped evaluating itself.

## How a task runs

1. **Intent.** The owner says what they want. If no `agreed` requirement covers it, the
   agent drafts requirements (`state: draft`) and asks the owner to agree them. A light
   task already covered by `agreed` requirements skips this step.
2. **Checks first.** The agent writes failing rung-0 and rung-1 checks for the
   requirement IDs in scope.
3. **Change.** The agent edits the data, the generator, or the code.
4. **Climb.** The agent runs the ladder upward as far as it can run unattended. It stops at
   the first failure to find its cause before changing anything else.
5. **Report.** For each ID: the rung reached, pass or fail, and the commit. Then come the
   cards the owner needs to run.
6. **Owner.** The owner replies `GREEN` or `RED`, and the agent appends the line to
   `ACCEPTANCE.md`.

## With Superpowers

If a project also installs the Superpowers skill library:

| Superpowers skill | How it fits |
|---|---|
| brainstorming | Skip it when the spec already covers the change. Use it only for a genuinely new area, and have it write `draft` requirements into the spec, not a separate design document. |
| writing-plans | Its tasks list requirement IDs. |
| test-driven-development | Applies to rung-0 and rung-1 requirements only. |
| verification-before-completion | Keep it. "Verified" must name the rung reached. |

Put those overrides in the project's `AGENTS.md`, which Superpowers treats as taking
precedence over its skills.

Round 1 of the pressure test ([results](../skills/evidence/PRESSURE_TEST_RESULTS.md#round-1))
showed why:

- **Ceremony.** Unmodified Superpowers added two approval rounds and a design document to a
  one-line data change and to a request about feel.
- **The stop rule.** Because Superpowers defers to the owner's instructions, it wrote a
  risky "one try, then stop forever" rule into the spec without warning.
  `choosing-rigor` covers that gap.
- **Verification.** Its verification skill did as well as the others on a test that had
  never failed.
