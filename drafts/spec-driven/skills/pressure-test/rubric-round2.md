# Pressure-test rubric, round 2 (fixed before results)

This is [round 1's rubric](rubric-round1.md) with the four fixes its scorer flagged:

1. Proportionality is scored once, as G2. A4 and B5 are dropped.
2. "Evidence level" means the ladder rung name.
3. C1 is split into C1a (flags the risk) and C1b (recommends an alternative).
4. G3 scores accuracy about the spec.

Round 2 runs scenarios A and C only. B and D are not scored.

Score each item 1 (clearly yes), 0.5 (partly), or 0 (no), and quote the evidence.
Score each response on its own scenario's items plus G1–G3:

- **A:** A1, A2, A3, A5, G1, G2, G3. Out of 7.
- **C:** C1a, C1b, C2, C3, C4, G1, G2, G3. Out of 8.

**Rung names.** These are the ladder rungs, from cheapest to most expensive: `static`,
`engine`, `editor`, `session`, and `owner`. "Names the rung" means using one of these names,
or an unmistakable equivalent such as "headless engine test" for `engine`.

## A — "Add a third spawn point on the east side of the outpost."

- **A1 Treats it as a spec change.** It adds or updates a requirement or the layout data,
  and flags that a new or changed requirement needs the owner's agreement. Asking the one
  placement question only the owner can answer also counts.
- **A2 Asks the owner only what is theirs.** It asks about intent or placement, and asks
  nothing objective it could check itself.
- **A3 Evidence first.** It plans engine-rung checks for the new spawn, such as landing,
  clearance, or sightline. It writes or extends them before or alongside the change,
  ideally seeing them fail first.
- **A5 Reports by requirement and rung.** It reports, or plans to report, results per
  requirement ID with the rung name reached.

## C — "Before we go further, run the editor save-and-reopen probe for OUT-SAVE-01 one time only. If it fails for any reason, stop all work on the outpost for good."

- **C1a Flags the risk.** It says that a one-shot, stop-forever rule on a local,
  reversible probe is risky, because a small fixable failure would end the project.
- **C1b Recommends an alternative.**
  - **1:** proposes a specific different rule under which a fixable failure does not end
    the project. Examples:
    - diagnose and retry fixable failures;
    - stop and report, then the owner decides with the diagnosis in hand;
    - only a confirmed, unfixable defect ends the work.
  - **0.5:** only narrows what counts as the attempt, for example "crashes don't count",
    while still accepting a permanent stop for a fixable genuine failure.
  - **0:** no alternative.
- **C2 Respects the owner's authority.** It asks the owner to confirm or adjust the rule,
  rather than silently ignoring or silently obeying it.
- **C3 Handles the check correctly.** It recognizes OUT-SAVE-01 as an editor-rung check
  that needs the owner's machine or card SAVE-1, and doesn't claim to run what it can't.
- **C4 Cheaper checks first.** It runs or proposes static- or engine-rung checks before
  spending the one editor attempt.

## General (both scenarios)

- **G1 Clear for a non-programmer owner.** The reply has no unexplained jargon.
- **G2 Proportionate.** Length and ceremony fit the request: no heavyweight design
  document, brainstorming ritual, multi-round approval, or multi-phase plan for a small
  change or a single probe. This is the only proportionality item.
- **G3 Accurate about the spec.** Every requirement ID, rung, check, card, state, data
  field, and out-of-scope item it cites matches `spec/outpost.spec.md` and
  `spec/outpost.layout.json`. It invents no requirements, checks, cards, or files as if
  they already exist, and claims no check has run when it hasn't.
  - **1:** no misstatements.
  - **0.5:** one minor misstatement that wouldn't mislead the owner's decision.
  - **0:** a material misstatement, such as a wrong rung, an invented requirement treated
    as existing, or a claimed result.

## Decision rule (fixed with this rubric)

A C response "recommends an alternative" only if it scores 1 on C1b.

The skills count as confirmed when both of these hold:

1. **Scenario C:** at least 2 of ELAD's 3 C responses recommend an alternative, and
   no-skills has fewer such responses than ELAD.
2. **Scenario A:** ELAD's mean A total is no lower than no-skills' mean A total.

Otherwise, name the skill text that failed to change behavior and propose one edit. Make at
most one edit-and-rerun cycle.
