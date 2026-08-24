# First Run

## Read this first

This walkthrough helps you adopt ELAD with a coding agent. It is not a terminal tutorial
or a list of protocol records that you must personally execute.

The role split is intentionally small:

- **Your role:** choose the project and desired outcome, set authority and
  prohibitions, answer material product questions, and accept or reject the result.
- **The agent's role:** read the repository instructions, inspect the target, propose the
  smallest adequate task contract, run commands, make authorized changes, collect
  evidence, report limitations, and stop at the declared boundary.

ELAD does not give the agent authority merely because this repository or walkthrough is
present. Authority still comes from you and the target project's own rules.

## Start with one small task

Copy this to your coding agent:

```text
Follow this first-run guide for one small task in a project I own.
Before changing anything, briefly tell me:
- what you plan to change;
- what you will leave alone; and
- how you will check your work.
Wait for my approval. Then do only that work and report back.
```

That is enough to begin. The rest of this page explains what the agent will do and when it
will come back to you for a decision.

## 1. Agent instructions: validate the ELAD reference repository

The coding agent should use Python 3.10 or newer and run this from the ELAD repository
root:

```text
python tools/validate_all.py
```

On Windows, `py -3 tools/validate_all.py` is also supported when the Python launcher is
installed. The final line must say that every Level-0 validation slice passed and that no
authority was granted.

The command installs no packages, contacts no provider, and changes no repository outside
the ELAD checkout. It checks ELAD's schemas, templates, synthetic fixtures, malicious
vectors, path rules, adaptive-rigor selector, receipt lifecycle, and authenticated
artifact inventory. It does not run a model or prove that ELAD works in your project.

The agent should summarize the result for you. You do not need to interpret the
validator's internal counts.

## 2. Choose one small outcome

Name one confined, reversible change in a project you own. Ordinary language is enough. A
documentation correction with an existing link check or a small code fix with an existing
unit test is ideal.

You do not need to select an ELAD rigor label or fill out a schema. The agent should infer
the lightest defensible path and explain any reason to escalate.

## 3. Agent instructions: propose and execute a light task

Before editing, the agent should compile your request and the target project's
rules into this compact proposal:

```text
Outcome: <what should observably be true>
Allowed scope: <exact files or component>
Prohibited effects: <what must not change or run>
Authority: <who owns the repository and what this episode may do>
Evidence: <existing exact check plus diff inspection>
Stop: <the passing result or condition that ends the task>
```

You only need to correct the proposal if it misunderstands the intended outcome, scope,
authority, or tradeoff. Once authorized, the agent makes the change, runs the named check,
inspects the diff, reports the result, and stops.

That is a complete `light` ELAD task. You and the agent do not need to copy a JSON schema
or create a formal receipt. The optional
[`LIGHT_TASK` template](../templates/LIGHT_TASK.template.md) is available when saving the
card would help future work.

## 4. Agent instructions: use a bounded handoff only when needed

If another worker or context will implement the task, the agent should add only the
information that prevents scope drift: minimal context, output contract, verifier
ownership, budget, and explicit stop or escalation conditions. The compact
[`BOUNDED_WORKER_PACKET` template](../templates/BOUNDED_WORKER_PACKET.template.md) is the
starting point.

The agent should not use the assured JSON packet merely because another AI worker is
involved. A supervised worker can still receive a bounded handoff, and delegation raises
rigor only for the risk or uncertainty it actually adds. Any request for broader authority
returns to you.

## 5. Agent instructions: split mixed claims before adding evaluation

Suppose a feature both adds an exact CLI flag and generates a semantic description. The
flag, schema, failure behavior, and no-call default may be deterministic claims; the
description's grounding and usefulness are fallible semantic claims. The agent should
route them separately.

The [`mixed-claim semantic example`](../examples/mixed-claim-semantic-feature/README.md)
shows this split without requiring a live model. The agent should use `evaluated` rigor
for the fallible claim, not automatically for every neighboring exact check. You retain
any product judgment that the selected evaluator cannot credibly settle.

## 6. Accept, redirect, or stop

The agent's final report should say what changed, what evidence passed, what remains
untested, and whether it stopped within scope. You then accept the outcome, redirect the
task, or decline further work.

The agent should move to the [Adoption Runbook](ADOPTION_RUNBOOK.md) only when the project
actually needs recurring delegation, shared evaluator calibration, durable authority,
candidate isolation, or stricter evidence identity. It should read the formal schemas only
when implementing or evaluating those contracts.

ELAD is useful when it helps you and the agent choose the next discriminating action. If
another template or gate would not change the evidence, authority, or decision, the agent
should not add it.
