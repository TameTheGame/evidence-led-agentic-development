# Evaluation and Evidence

Evaluation is how ELAD decides what to build next and when to stop. It starts with a
question, not a demand for the largest possible test suite:

1. What behavior or fact must this step establish?
2. Which uncertainty could change the next decision?
3. What is the cheapest check that can reliably settle it?
4. What did the output, behavior, or trace reveal?
5. What is the smallest useful next change—or is the work complete?

An existing test may answer all five questions for a light task. Uncertain behavior may
need representative examples, a rubric, sampled outputs, and several focused iterations.
High-consequence work may justify independent expectations, malicious cases, recovery,
and adversarial review.

## Match evidence to the claim

Different checks establish different facts:

| Claim | Useful evidence | What it does not prove by itself |
|---|---|---|
| Exact structure or logic | compiler, type check, unit test, calculation, fixture comparison | live behavior or product quality |
| Integrated behavior | integration test or headless service run | rendered experience or real remote delivery |
| Live operational behavior | bound runtime observation, trace, log, or saved-and-reloaded result | authority or subjective quality |
| Semantic or stochastic quality | frozen examples, rubric, calibrated evaluator, sampled outputs | exact identity, security, rights, or permission |
| Product experience or consequential tradeoff | focused owner review after objective checks pass | unrelated technical properties |

Select the lowest layer that can actually resolve the claim. A screenshot cannot prove
authorization. A warm cache cannot prove clean delivery. A model's confidence cannot
prove its own correctness.

For light and many bounded tasks, an expected result and inspected diff are enough. Exact
claim IDs, subject selectors, manifests, and receipts become useful when evidence crosses
contexts, several sources must reconcile, the subject could be confused, or closure has
material consequences.

## Split mixed claims

A single feature often contains both exact and uncertain behavior. Write the split down
before implementation:

| Claim | Kind | Cheapest reliable evidence |
|---|---|---|
| opt-in flag, schema, bounded input, failure isolation | exact | deterministic tests against independent fixtures |
| purpose, grounding, uncertainty handling, usefulness | semantic | small frozen case set, rubric, calibrated judge, sampled outputs |

The task may use `evaluated` rigor because of the semantic claim while its exact tests
remain ordinary deterministic evidence.

Executing a program does not make every claim operational. Exact output, exit status,
JSON shape, fixtures, and mocked service failures can remain deterministic. Use live
runtime evidence when truth depends on timing, persistence, distributed state, native
effects, or another property an exact comparison cannot establish.

## Avoid circular proof

The implementation should not generate both its behavior and the expected answer. An
independent expectation can come from:

- an existing specification or test;
- a separately authored fixture, truth table, rule, or test oracle;
- a runtime observer outside the changed component;
- worker-inaccessible held-out cases;
- a calibrated semantic evaluator; or
- an independent reviewer when the consequence warrants it.

The same worker may run a trustworthy exact test. Stronger separation is useful when the
evaluator is fallible, derived from the implementation, exposed to its held-out answers,
or vulnerable to a consequential false green.

## Calibrate fallible evaluators once, then reuse them

Before relying on a rubric or model judge, show that it can recognize representative
known-good and known-bad cases. Check the failures relevant to its job, such as stale or
wrong subjects, missing output, crashes, silent skips, adversarial cases, and variance
across repeated runs.

Record what the evaluator supports, its exact identity, and what changes invalidate that
result. Routine tasks can cite the current calibration and run focused cases. Recheck only
the affected slice after its model, prompt, adapter, schema, runtime, policy, or relevant
environment changes—or when a new false-green pattern appears.

Evaluator maturity belongs to each claim. A new exact regression with independently
defined expected behavior does not need a semantic calibration pack merely because it is
new. A semantic judge beside it may still be unproven.

Generator sampling and evaluator sampling answer different questions. A few product
draws can expose obvious output instability. Repeated judge runs measure evaluator
variance. Bind both to the exact subject and material settings, such as temperature,
thinking mode, and output limit.

## Use live, model, and owner evidence for their actual jobs

- **Live evidence** establishes behavior that static inspection cannot. Bind it to the
  exact executable, configuration, data root, candidate, and environment the claim needs.
- **Traces and logs** help locate the first causal failure. Keep them file-backed and bring
  only the relevant slice into agent context.
- **A model judge** can evaluate a narrow semantic class after calibration. It cannot
  establish permission, security, privacy, rights, persistence, exact runtime identity,
  promotion, publication, or final product taste by confidence alone.
- **Owner judgment** remains appropriate for product meaning, subjective experience,
  trust, consequential tradeoffs, rights, and real-world conditions automation cannot
  reliably observe. Present a small review card only after objective prerequisites pass.

If a numeric threshold passes while a case designed to catch a real defect still fails,
do not hide the failure inside the score. Make one cheap causal correction, rerun the
affected evidence, and stop when the claim is supported.

## Keep evidence compact and useful

- Keep raw logs, traces, screenshots, and transcripts outside routine model context.
- Preserve enough identity and content to reproduce the conclusion.
- Redact secrets and private data before wider routing.
- Use path and hash manifests when evidence must cross contexts, survive interruption, or
  support consequential closure.
- For a one-context light task, a test result and inspected diff may be sufficient.

Assured work may need exact claim identities, evidence ownership, subject binding, and a
formal receipt that fails closed. Those contracts are reusable infrastructure, not the
default task experience. See [Protocol 0.5 Conformance](PROTOCOL_05_CONFORMANCE.md) when
you are implementing or auditing that layer.
