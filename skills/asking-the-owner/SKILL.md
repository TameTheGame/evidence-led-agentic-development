---
name: asking-the-owner
description: Use when a decision or observation needs the project owner — product intent, feel, visuals, risk acceptance, agreeing requirements, merging, releasing or publishing — or when a check can only be run by a person.
---

# Asking the owner

The owner's time is the most expensive resource in the project. Ask rarely, ask late,
and make every question quick to answer.

## Decisions the owner keeps

- what the product is for, its priorities, and real tradeoffs;
- agreeing, changing, or retiring a spec requirement;
- feel, look, sound, tone, and usability;
- unsettled architecture, permissions, privacy, persistence, security, and rights;
- accepting a known risk or limitation;
- adopting a new model, tool, or kind of evaluator; and
- merging to the main branch, releasing, and publishing.

Everything objective is yours to settle first: compiling, tests, traces, file checks,
logs, paths, hashes, and cleanup.

## Never ask the owner to

- find paths, calculate hashes, read logs, or reconstruct what you did;
- repeat a check that already passed on the same commit;
- run a check you could have run yourself; or
- decide something technical you can settle with evidence.

## Ask last, and together

- Prepare a card only after every cheaper check it depends on passes.
- Put several questions in one message instead of interrupting repeatedly.
- Write for a smart non-specialist: say what to click and where, and avoid jargon.

## Card format

```text
NET-1 — remote player collides with the walls     (commit a1b2c3d)

1. Host the map. Join from a second client.
2. On the client, walk into the north wall, then through the gate.

Pass: the wall blocks you and the gate lets you through, on both machines.
Fail: you pass through the wall, or the gate blocks you.
Stop if: the client can't join.

Reply: GREEN, or RED plus what you saw and on which machine.
Limit: same-machine host and client is fine here; it is not a clean-install check.
```

Every card needs:

- the exact commit or build;
- numbered actions;
- what passing and failing look like;
- a stop condition;
- the reply format; and
- any limit on what the answer proves.

## Record the answer

Add one line to `spec/ACCEPTANCE.md`:

```text
2026-10-09 · OUT-NET-01 · GREEN · a1b2c3d · Owner · client blocked by north wall, gate passable
```

A GREEN closes only the named requirement, at that commit. A later change to something
the requirement depends on reopens it.

## Red flags

| Thought | Reality |
|---|---|
| "I'll ask the owner whether this compiles or passes." | That's your job. Run it. |
| "I'll send the card now and fix the tests meanwhile." | A card on a moving target wastes the owner's time. Finish the checks first. |
| "The owner said GREEN last week, so it's still fine." | Only if nothing it depends on has changed since that commit. |
| "I'll pick a sensible product direction myself." | Product intent is the owner's. Offer options with a recommendation and ask. |
| "It's only a wording change that follows from what they asked." | Changing an agreed requirement's text is the owner's decision. Propose the new wording and wait. |
| "A model reviewed the screenshots, so it's accepted." | Model review is advice. Acceptance is the owner's. |
