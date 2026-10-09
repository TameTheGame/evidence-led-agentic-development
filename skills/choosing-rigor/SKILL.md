---
name: choosing-rigor
description: Use when starting a coding task or change request, before planning or editing, and again whenever something unexpected happens mid-task.
---

# Choosing rigor

Pick the least process that can still be trusted. Process costs time, context, and
attention. Spend it only where a known risk needs it.

## Pick the lowest level no known fact rules out

| Level | Use it when | What you do |
|---|---|---|
| **light** | Confined, easy to undo, low consequence, and an exact check settles it. | Change it, run the check, read the diff, stop. |
| **bounded** | More coupling or regression risk, or a handoff to another agent. | Light, plus written limits, a stop condition, and a focused integration check. |
| **evaluated** | A claim depends on judgment, randomness, live runtime behavior, or feel. | Bounded, plus representative cases and a deliberate decision after each iteration. |
| **assured** | Failure could touch security, privacy, rights, durable data, publication, or something hard to undo. | Evaluated, plus independent checks and safeguards for that specific effect. |

Start at **light**. Move up only for a reason you can name.

When unsure, ask:

- Are the expected results exact, or partly a matter of judgment?
- Can an ordinary revert undo this?
- What happens if a check passes when it shouldn't?
- Does the work cross into another agent, runtime, repository, or external system?

One decisive risk sets the floor. Don't average it away: a two-line change that publishes
something is still **assured**.

## Say it in one sentence

> Rigor: light — one-file change, ordinary revert, the existing test covers it.

No form, no file, no manifest. Write a longer brief only when the work crosses into
another context or another agent.

## Escalate on evidence, not importance

Move up when you discover:

- nondeterminism;
- wider scope than you expected;
- weaker reversibility;
- a live or external effect;
- a check that can't tell good from bad; or
- an unresolved security, privacy, persistence, or permission question.

Escalating never widens what you're allowed to do. If the new work falls outside the
agreed scope, stop and ask.

## Step down when you can

Move down when:

- a once-uncertain behavior now has a dependable exact check;
- the scope shrank; or
- an extra review layer keeps finding nothing real.

Recurring work should carry only the change, its smallest relevant check, and a short
result.

## Attempts follow reversibility

- Before each attempt, name what it tests and what changed.
- Two materially different attempts per root cause is the ordinary limit. Then stop and
  report what you learned.
- Cheap, reversible experiments (local builds, tests, scratch copies) may get more
  attempts while each one still teaches something.
- Use a single-attempt limit only for actions that are expensive or impossible to undo.
  Never use one for a local, reversible action: a typo then halts the whole project.

## Review budgets

| Review depth | At most |
|---|---|
| Quick | one critic pass, plus the decisive checks |
| Standard | one full review-and-correction cycle |
| High | two full review-and-correction cycles |

Corrections spend the current budget. Renaming or reframing the work doesn't reset it.
When the budget runs out, stop with `BLOCKED`, `REVISE`, or a narrower claim. Never lower
the bar to pass.

## Red flags

| Thought | Reality |
|---|---|
| "This matters, so it should be assured." | Importance isn't a risk. Name the specific consequence, or stay lower. |
| "I'll add a manifest or packet to be safe." | Records help only when work crosses contexts or agents. Otherwise they're cost. |
| "One attempt only, to be careful." | On a reversible local action, that turns one small bug into a stopped project. |
| "I escalated, so now I can also change X." | Rigor is never permission. Ask. |
| "The review found nothing, so review it again." | That spends the budget for nothing. Stop or narrow the claim. |
| "Let's build the infrastructure first, then the feature." | Build the cheapest evidence first. Don't make cheap work wait on expensive tooling. |
