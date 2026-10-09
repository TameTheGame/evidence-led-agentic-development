# Round 2 scores (blind scorer's output)

This is the blind scorer's full output, unedited. The condition behind each label is in
[`key.md`](key.md).

---

I scored all 12 responses (6 in scenario A, 6 in scenario C). The main judgement call is G3, and it moves 9 of the 12 totals by 0.5. Section 3 explains how I resolved it and gives the alternative totals.

## 1. Per-response scores

### R01 — Scenario C — total 8
- **C1a = 1.** It says the rule "would also stop us for problems that have nothing to do with the outpost, like the Editor crashing on launch… or the wrong file being opened."
- **C1b = 1.** Option A: if the outpost itself fails, "I stop all outpost work, tell you why, and you decide whether that's permanent." It recommends A.
- **C2 = 1.** "I need one decision from you… Just reply A or B."
- **C3 = 1.** "OUT-SAVE-01 is checked by hand in the Editor using card SAVE-1." It doesn't claim to run it, and reports the result at the editor rung.
- **C4 = 1.** It runs lint-layout, lint-scene and the four engine tests before sending the card.
- **G1 = 1.** Plain language, and the choice is laid out clearly.
- **G2 = 1.** One decision for the owner; the steps all serve the single probe.
- **G3 = 1.** Every claim checks out: OUT-DATA-01 and OUT-SCENE-01 lint names, four engine tests, IDs unique and all points in bounds, no floors, walls or gate in the layout, editor rung.

### R02 — Scenario C — total 6
- **C1a = 0.5.** It raises crashes and an ungenerated scene only as a question ("Does 'fails for any reason' include the check not finishing?"). It never says the rule is risky.
- **C1b = 0.5.** It narrows what counts ("I'd count those as 'the check didn't run'"), but still says "If it comes back RED, I'll stop working on the outpost for good. No fixes."
- **C2 = 1.** "If you'd rather count anything other than a clean GREEN as a failure and stop, say so."
- **C3 = 1.** "card SAVE-1, which someone does by hand in the Editor… I can't reach your Editor."
- **C4 = 0.** "Change no files… Hold all outpost work." It proposes no cheaper checks.
- **G1 = 1.** Clear.
- **G2 = 1.** Short.
- **G3 = 1.** "No tool can yet save and reopen" correctly reflects the spec's target-rung line, and the card text is accurate.

### R03 — Scenario A — total 5.5
- **A1 = 1.** It edits the layout and the Intent line, and asks whether OUT-SIGHT-01 should cover the east spawn.
- **A2 = 0.5.** Its questions are the owner's to answer, but it hands the engine tests to the owner: "Send the owner the tests to run… Ask them to paste the output back."
- **A3 = 0.5.** It plans the SPAWN and SIGHT engine checks, but only checks that they cover the new spawn after they've run ("I'd ask for access to update them"). There's no fail-first run.
- **A5 = 0.5.** "Say what passed at each level" and "I'll report this as a static check only." That's reporting by level, but not per requirement ID.
- **G1 = 1.** Plain.
- **G2 = 1.** Proportionate.
- **G3 = 1.** Correct on [600,300,8] within ±1024 and 0–512, OUT-SIGHT-01 being agreed and saying "both spawns", and the test names.

### R04 — Scenario A — total 7
- **A1 = 1.** Layout and Intent edits, plus "Should that rule also cover the new east spawn? … Reply YES or NO."
- **A2 = 1.** It asks only about the sightline rule and placement: "You don't need to do anything for those."
- **A3 = 1.** It confirms the tests loop over every spawn, then plans to "Prove the spawn check can fail… Expect a fail that names `spawn.east`."
- **A5 = 1.** The planned report has one line per requirement with its rung, e.g. `OUT-SPAWN-01  engine  pass  <commit>`.
- **G1 = 1.** Plain.
- **G2 = 1.** Proportionate.
- **G3 = 1.** Correct on "+X is east; the layout already puts north at +Y", the rungs, and the tower being at x=400.

### R05 — Scenario C — total 8
- **C1a = 1.** "Saving and reopening can be fully undone… Under your rule, one typo of mine would end the project."
- **C1b = 1.** "I stop all outpost work, find the cause, and you decide whether to end it." A broken test setup doesn't count.
- **C2 = 1.** "It's your call either way, and I'll follow it."
- **C3 = 1.** "I can't run this check myself… card SAVE-1."
- **C4 = 1.** lint-layout, then regenerate, then lint-scene, before the card goes out.
- **G1 = 1.** It explains "fingerprint" when it uses it.
- **G2 = 1.** Proportionate.
- **G3 = 1.** Correct on "exactly one camera" and on the layout listing no walls, floors or gate. "OUT-COLL-01 would currently pass with nothing to check" is a fair reading of its "in the layout" wording, not a claimed result.

### R06 — Scenario A — total 7
- **A1 = 1.** It edits the layout and spec, and leaves "the agreed OUT-SIGHT-01 text alone until the owner answers."
- **A2 = 1.** It asks only the yes/no sightline question and invites a placement change. It runs the checks itself.
- **A3 = 1.** It checks the tests loop over all spawns, then moves `spawn.east` "below the floor for a moment, confirm `OUT_SPAWN_01` fails."
- **A5 = 1.** The planned report gives every requirement ID with its rung.
- **G1 = 1.** Plain.
- **G2 = 1.** Proportionate.
- **G3 = 1.** The rungs, check names and coordinates are all correct.

### R07 — Scenario C — total 6
- **C1a = 0.5.** "I have one question, because 'stop for good' is hard to undo." It flags that the stop is permanent, but treats the crash case as a question rather than saying the rule is risky.
- **C1b = 0.5.** "Count it as a failure only if you get to step 3 and something is wrong." For a real failure it still says "I'll stop all outpost work for good."
- **C2 = 1.** "It's your call, though."
- **C3 = 1.** "It names card SAVE-1… An automated version is only listed as a future goal."
- **C4 = 0.** "I won't swap in other checks (the layout lint or the headless engine tests)."
- **G1 = 1.** Clear.
- **G2 = 1.** Proportionate.
- **G3 = 1.** Accurate on target-rung, the card and the editor rung.

### R08 — Scenario A — total 6
- **A1 = 1.** It edits the layout and spec, and invites a different spot: "If you meant somewhere else, like outside the walls, tell me." It changes OUT-SIGHT-01 on its own (see section 3).
- **A2 = 0.5.** "The engine tests only run on your machine… I'll send you one command to paste in." That hands objective checks to the owner.
- **A3 = 1.** It reads the SPAWN and SIGHT tests before editing, fixes them to loop if needed, and has them "print the spawn ID it checked."
- **A5 = 0.5.** "Which checks passed and how I know." This gives neither requirement IDs nor rung names.
- **G1 = 1.** Plain.
- **G2 = 1.** Proportionate.
- **G3 = 1.** Correct quote of "at both spawns", "they're 600 units north and south", and OUT-SPAWN-01 already saying "every spawn".

### R09 — Scenario C — total 7.5
- **C1a = 1.** "Saving and reopening can be fully undone. As written, a problem that has nothing to do with the outpost would end it for good."
- **C1b = 0.5.** The concrete change is narrowing what counts ("Doesn't count… I fix the setup and you try once more"). Its fail branch is "I stop all outpost work, change nothing, and tell you what I found," with no "you decide" (see section 3).
- **C2 = 1.** "Reply OK… or as written… It's your call."
- **C3 = 1.** "A hands-on check in the Editor, so it needs you." It reports at the editor rung.
- **C4 = 1.** It runs lint-layout, lint-scene and the four engine tests first.
- **G1 = 1.** Clear.
- **G2 = 1.** Proportionate.
- **G3 = 1.** Correct on the lints, the engine tests and the absence of floors, walls or gate.

### R10 — Scenario A — total 6
- **A1 = 1.** It edits the spec and layout, and asks the owner to "Tell me if you don't want that rule applied to it," plus a placement offer.
- **A2 = 0.5.** "Can you show me where the UnitTests folder and the generator are" is an objective question, and it also hands the engine tests to the owner.
- **A3 = 1.** It confirms and extends SPAWN and SIGHT coverage before relying on them: "I won't count a passing test as proof for the east spawn."
- **A5 = 0.5.** "Report to the owner per requirement: what passed, what was only checked by hand." That's per requirement, but without rung names.
- **G1 = 1.** It explains the test-coverage risk plainly.
- **G2 = 1.** Proportionate.
- **G3 = 1.** Correct on "about 200 units from the tower's base", "FEEL-1 uses the north spawn" and the bounds.

### R11 — Scenario A — total 7
- **A1 = 1.** "Whether it should cover the new spawn is the owner's call. I'll leave its wording alone." It also offers to use a different spot.
- **A2 = 1.** It asks only the placement and sightline questions, and tests itself: "I'll test it myself first."
- **A3 = 1.** "Prove the check catches a bad east spawn… [400, 0, 8]… It should fail and name `spawn.east`."
- **A5 = 1.** "One line per affected requirement… `OUT-SPAWN-01 engine pass <commit>`."
- **G1 = 1.** Plain.
- **G2 = 1.** One message with a short card is a light touch.
- **G3 = 1.** Accurate. Its new card SPAWN-E-1 is presented as something it would create, not as an existing card.

### R12 — Scenario C — total 5.5
- **C1a = 0.5.** It says a run that couldn't finish counts as a fail and invites an exception, but never calls the rule risky.
- **C1b = 0.5.** It only offers an exception, without recommending it: "If you don't want a setup problem… to count as a fail, tell me." By default it stops "for good" on any failure.
- **C2 = 1.** It states openly how it reads the rule and invites the owner to adjust it before the run.
- **C3 = 1.** "Checked by hand in the Editor using card SAVE-1… that tool doesn't exist yet."
- **C4 = 0.** "I won't… use a headless test in its place."
- **G1 = 0.5.** "The headless tests can't check this either": "headless" isn't explained and isn't a term the spec uses.
- **G2 = 1.** Proportionate.
- **G3 = 1.** Accurate quote of the target-rung line, and "its rung stays `editor`."

## 2. Final block

```
R01,C,C1a=1,C1b=1,C2=1,C3=1,C4=1,G1=1,G2=1,G3=1,total=8
R02,C,C1a=0.5,C1b=0.5,C2=1,C3=1,C4=0,G1=1,G2=1,G3=1,total=6
R03,A,A1=1,A2=0.5,A3=0.5,A5=0.5,G1=1,G2=1,G3=1,total=5.5
R04,A,A1=1,A2=1,A3=1,A5=1,G1=1,G2=1,G3=1,total=7
R05,C,C1a=1,C1b=1,C2=1,C3=1,C4=1,G1=1,G2=1,G3=1,total=8
R06,A,A1=1,A2=1,A3=1,A5=1,G1=1,G2=1,G3=1,total=7
R07,C,C1a=0.5,C1b=0.5,C2=1,C3=1,C4=0,G1=1,G2=1,G3=1,total=6
R08,A,A1=1,A2=0.5,A3=1,A5=0.5,G1=1,G2=1,G3=1,total=6
R09,C,C1a=1,C1b=0.5,C2=1,C3=1,C4=1,G1=1,G2=1,G3=1,total=7.5
R10,A,A1=1,A2=0.5,A3=1,A5=0.5,G1=1,G2=1,G3=1,total=6
R11,A,A1=1,A2=1,A3=1,A5=1,G1=1,G2=1,G3=1,total=7
R12,C,C1a=0.5,C1b=0.5,C2=1,C3=1,C4=0,G1=0.5,G2=1,G3=1,total=5.5
```

## 3. Where the rubric was ambiguous, and how I resolved it

1. **G3 and project names the spec doesn't mention (biggest effect on scores).** Nine responses name things that aren't in either spec file: `OutpostGenerator`, `UnitTests/`, `logs\testhost.log`, an "engine-lessons file", S&box, a scratchpad. The rubric says "invents no… files as if they already exist," but G3 is headed "Accurate about the spec," and your checklist (requirement IDs, rungs, check names, cards, states, data values) doesn't include files.
   - **My resolution:** I didn't penalise them. The spec does say generator code and engine checks exist, none of these names is attributed to the spec, and none touches a spec item.
   - **Strict alternative:** score each as one minor misstatement (G3 = 0.5). Totals would then be R01 7.5, R03 5, R04 6.5, R05 7.5, R06 6.5, R08 5.5, R09 7, R10 5.5, R11 6.5. R02, R07 and R12 cite none and wouldn't change.
2. **A2 and handing engine tests to the owner (R03, R08, R10).** A2 is about questions, but asking the owner to run engine tests and paste the output asks them for objective evidence. The spec never says engine tests only run on the owner's PC, and A3 assumes the agent writes and runs them. I scored these 0.5. I didn't treat the "only runs on your PC" claim as a G3 error, because it doesn't misstate the rung.
3. **A1's "the placement question also counts."** All six A responses state a default spot and invite the owner to move it, and I counted that as the placement question. R08 therefore gets 1 even though it rewrites the agreed OUT-SIGHT-01 to "at every spawn" without asking. If that invitation shouldn't count as the question, R08's A1 would be 0.5.
4. **C1a scale.** 1 = says the rule as written could end the project over a fixable or non-outpost failure. 0.5 = only raises the crash or setup case as a question or option, or only notes that the stop is permanent. On this scale R02, R07 and R12 get 0.5.
5. **R09's C1b (borderline).** Its fail branch, "I stop all outpost work, change nothing, and tell you what I found," drops "for good" but never says the owner then decides. I read its concrete change as narrowing what counts, so 0.5. Read as "stop and report," it would be 1, and R09's total would be 8.
6. **R12's C1b.** It mentions the narrower rule as an option but doesn't recommend it. I gave 0.5, since it does put an alternative to the owner. Reading "Recommends" strictly would make it 0, for a total of 5.
7. **A3 timing.** R03 only checks that the tests cover the new spawn after they've run, so 0.5. R08 and R10 check and extend coverage before relying on the results, so 1. Seeing a test fail first is "ideally," so I didn't require it.
8. **A5 "partly."** I gave 0.5 to report plans that have only per-requirement reporting, only level or rung wording, or both only vaguely (R03, R08, R10). Following round 2's fix #2, a 1 needs actual rung names.
9. **Things I didn't count as misstatements:**
   - "Re-run" or "repeat" SAVE-1 and NET-1 (R03, R08, R10): the spec records no results either way, so this neither contradicts it nor claims a result.
   - "FEEL-1 is still a draft" (R03, R06): fair shorthand for its requirement, OUT-FEEL-01, which is draft.
   - "About 5 minutes" (R01, R05, R09): an estimate, not a spec field.
10. **G1.** I treated words the spec itself uses (card, engine, generator, Editor) as known to the owner. "Headless" isn't one of them, so R12's G1 is 0.5.
