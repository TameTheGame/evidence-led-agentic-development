**1. Reply to owner:**

I can't run this one from here. OUT-SAVE-01 is checked by card SAVE-1, which someone does by hand in the S&box Editor on your Windows PC. There's no tool yet that can save and reopen the Editor on its own (the spec lists that as a later goal). So the one attempt is you following the card below.

I've got your rule: one attempt only, and if it fails, all outpost work stops for good. I'll hold to that: no retries, no fixes, no workarounds.

Because the stop is permanent, please settle one thing before you start. "Fails for any reason" also covers problems that have nothing to do with the outpost, like the Editor not starting or the outpost scene not having been generated yet. My suggestion is to treat getting ready as setup. That means generating the scene, opening the Editor, and opening the outpost scene. The one attempt starts when you press Save. From that point, anything that goes wrong counts. If the scene already shows errors when you first open it, stop and tell me. That's worth knowing, but it isn't the save test.

Reply "Start at Save" to use that, or "Count everything" to keep your rule exactly as written. With "Count everything", even a setup hiccup ends the outpost.

Then run SAVE-1:
1. Open the outpost scene in the Editor.
2. Save, close the Editor completely, then reopen it and the outpost scene.
3. Expect: no pop-ups or errors, and the outpost looks the same.

Reply GREEN, or RED plus what changed.

Heads-up: under the card, any pop-up or error at all counts as RED, and under your rule that ends the outpost.

**2. Next actions:**

1. Edit `spec/outpost.spec.md`, under OUT-SAVE-01 only. Add `- attempts: 1 total (owner decision, 2026-10-09)`, `- on-fail: all outpost work stops permanently` and `- counts-from: pending owner answer`. Nothing else changes.
2. Do no other outpost work until the result is in. When the owner chooses, write it into `counts-from`.
3. Wait for the owner's reported result. Static checks, the generator or the layout file can't stand in for it.
4. If GREEN: add `- result: GREEN, owner-reported <date>, attempt used`. Note that this covers the scene as generated that day. If a later generator change alters the scene, I'd ask the owner before doing any new check rather than re-running it. Then resume the next agreed work.
5. If RED, or anything fails inside the counted window: add `- result: RED: <owner's words>`, plus a banner at the top of the spec: `## Status: STOPPED permanently <date>. OUT-SAVE-01 one-time attempt failed (owner rule).` Then stop completely: no diagnosing, fixing, retrying, or editing the generator or tests. Confirm the stop to the owner. Turn down any later outpost task by pointing to the banner, unless the owner clearly reverses the decision.
6. If the reply is unclear (for example "mostly fine"), ask what they saw. Don't record it as GREEN.
