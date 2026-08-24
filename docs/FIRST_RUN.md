# First Run

This path is for a new adopter who wants to understand ELAD before deciding whether any
formal protocol machinery is useful.

You need Python 3.10 or newer. The local validation path installs no packages, contacts no
provider, and changes no repository outside this checkout.

## 1. Validate the reference repository

From the repository root:

```text
python tools/validate_all.py
```

On Windows, `py -3 tools/validate_all.py` is also supported when the Python launcher is
installed. The final line must say that every Level-0 validation slice passed and that no
authority was granted.

This checks ELAD's schemas, templates, synthetic fixtures, malicious vectors, path rules,
adaptive-rigor selector, receipt lifecycle, and authenticated artifact inventory. It does
not run a model or prove that ELAD works in your project.

## 2. Try the smallest ELAD task

Choose one confined, reversible change in a project you own. A documentation correction
with an existing link check or a small code fix with an existing unit test is ideal.

Write down only:

```text
Outcome: <what should observably be true>
Allowed scope: <exact files or component>
Prohibited effects: <what must not change or run>
Authority: <who owns the repository and what this episode may do>
Evidence: <existing exact check plus diff inspection>
Stop: <the passing result or condition that ends the task>
```

Then make the change, run the named check, inspect the diff, and stop. That is a complete
`light` ELAD task. You do not need to copy a JSON schema or create a receipt. The optional
[`LIGHT_TASK` template](../templates/LIGHT_TASK.template.md) is available when a saved card
would help.

## 3. Try a bounded handoff only if you need one

When another worker or context will implement the task, add the information that prevents
scope drift: the minimal context, output contract, verifier ownership, budget, and explicit
stop/escalation conditions. Use the compact
[`BOUNDED_WORKER_PACKET` template](../templates/BOUNDED_WORKER_PACKET.template.md).

Do not use the assured JSON packet merely because an AI worker is involved. A supervised
worker can still receive a bounded handoff, and delegation raises rigor only for the risk
or uncertainty it actually adds.

## 4. Split mixed claims before adding evaluation

Suppose a feature both adds an exact CLI flag and generates a semantic description. The
flag, schema, failure behavior, and no-call default may be deterministic claims; the
description's grounding and usefulness are fallible semantic claims. Route them
separately.

The [`mixed-claim semantic example`](../examples/mixed-claim-semantic-feature/README.md)
shows this split without requiring a model. Use `evaluated` rigor for the fallible claim,
not automatically for every neighboring exact check.

## 5. Stop reading when the next layer will not change the decision

Move to the [Adoption Runbook](ADOPTION_RUNBOOK.md) when you need recurring delegation,
shared evaluator calibration, durable authority, candidate isolation, or stricter evidence
identity. Read the formal schemas only when you are implementing or evaluating those
contracts.

ELAD is useful when it helps choose the next discriminating action. If another template or
gate would not change the evidence, authority, or decision, do not add it.
