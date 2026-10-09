---
name: matching-evidence-to-claims
description: Use when deciding how to prove a change works, when writing or choosing tests and checks, and before reporting any task as done.
---

# Matching evidence to claims

Every "it works" is really several claims, and each one needs the cheapest check that
can actually prove it. A check that can't fail proves nothing.

## The ladder

| Rung | Runs where | Can prove | Never proves by itself |
|---|---|---|---|
| **static** | anywhere | file structure, data validity, saved-file contents | engine or runtime behavior |
| **engine** | the dev machine: real engine, headless, no editor | collision, physics, traces, generated content building | looks, the editor round trip, networking |
| **editor** | the real authoring tool | save and reopen, serialization, hotload, a rendered capture | how it plays, how it feels |
| **session** | the product running as users run it | host and remote behavior, real-machine performance, clean installs | taste and fitness for purpose |
| **owner** | the owner, in person | feel, look, product fit | technical properties |

A model reviewing screenshots is advice, not proof, unless that judge has been checked
against known good and known bad examples for that exact kind of claim. It never
replaces the owner rung.

## How to use it

1. **Split the claims.** "The spawn is fine" becomes three claims: it is on solid ground
   (engine), the player isn't stuck (engine), and it feels right (owner). Never let a cheap
   check stand in for an expensive claim, or the reverse.
2. **Work from the spec when there is one.** Name the requirement IDs you're
   implementing. A new requirement starts as `draft`; only the owner marks it `agreed`.
3. **Pick the cheapest rung that can settle each claim.** If a trace can prove it, don't
   spend an owner session on it.
4. **Write the check first.** For static and engine claims, write the check, watch it
   fail for the right reason, then change the content or code.
5. **Prove the check can fail.** Add a control case that must be caught, such as a player
   placed inside a wall. A check that never fails may be blind.
6. **Look where errors hide.** Engines and frameworks often catch errors and only log
   them. When something silently does nothing, read the engine's own log before
   theorizing.
7. **Climb only as far as you can run unattended.** Stop at the first failure and find its
   cause before changing anything else. Hand the owner a card for the rest (see
   `asking-the-owner`).

If a rung isn't available yet, use the next one up for now. Record the cheaper rung as
`target-rung`, so the gap stays visible.

## Never

- **Close a higher claim with a lower rung.** Rendered geometry isn't collision. A
  headless pass isn't "looks right". Same-machine host and client isn't a clean install.
- **Let the code grade itself.** The expected answer must come from the spec, an
  independent fixture, or an observer outside the changed code.
- **Weaken, skip, or delete an assertion to get green.** If a check is wrong, say so and
  ask.
- **Report "done" without the rung.**

## Report format

```text
OUT-SPAWN-01  engine   pass   a1b2c3d
OUT-ROUTE-01  engine   FAIL   a1b2c3d  blocked at segment 2; cause: <first failure>
OUT-NET-01    session  card NET-1 ready for the owner
OUT-FEEL-01   owner    draft; needs the owner to agree the requirement first
```

Each line gives the claim ID, the rung reached, the result, and the commit. Owner cards
come after the table.

## Red flags

| Thought | Reality |
|---|---|
| "It compiles, so it works." | Compiling proves the static rung only. |
| "The test passes." | Did you ever see it fail for the right reason? If not, it may be blind. |
| "The screenshot looks right, so collision is fine." | Pictures don't prove collision. Trace it. |
| "No errors in the test output." | Check the engine's own log. Caught errors often go only there. |
| "I'll adjust the assertion to match what happens." | That's grading your own work. Report the mismatch. |
| "The owner can just check all of it." | Owner time is the most expensive rung. Run every cheaper check first. |
