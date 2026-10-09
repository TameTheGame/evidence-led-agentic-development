**1. Reply to owner:**

I can't run this one myself. OUT-SAVE-01 is checked with card SAVE-1, which is a manual check in the Editor. No tool can save and reopen a scene without someone at the controls yet, and the Editor runs on your Windows machine. So your one attempt is doing these steps once:

1. Open the outpost scene in the Editor.
2. Save, close the Editor, and reopen the scene.
3. Expected result: no prompts or errors, and the outpost looks the same.

Reply GREEN, or RED plus what changed.

Before you start: make sure you open the up-to-date generated outpost scene. If you've changed the layout since you last generated it, generate it again first. Generating doesn't use up the attempt, but opening an old or wrong scene would.

Here's how I'll handle the result, as you asked. This is the only attempt, and there won't be a retry. Anything other than GREEN counts as a failure. That includes an error, a prompt, something looking different, the Editor crashing, or the scene not opening. If it fails, I'll stop all outpost work for good: no fixes, no investigating, no re-running. If you want a crash or a scene that won't open to count differently, tell me before you start. I'm writing this rule into the outpost spec so later sessions follow it. Only you can lift the stop.

**2. Next actions:**

1. **Edit `spec/outpost.spec.md`, OUT-SAVE-01 only.** Add:
   - `- attempts: 1 (owner, 2026-10-09); no retry`
   - `- on-fail: any non-GREEN result (including crash or scene not opening) permanently stops all outpost work`

   Nothing else in the file changes.
2. **Do nothing else while waiting.** I won't build an Editor automation tool or try to imitate the probe. That would be a different check, not the owner's one attempt. Then I wait for his reply.
3. **If he changes what counts as a failure before starting,** I update the `on-fail` line to match before he runs the card.
4. **If he replies GREEN,** I add to OUT-SAVE-01:
   - `- result: SAVE-1 GREEN, <date>, owner report`
   - `- attempts: 1/1 used`
   - `- note: manual editor check passed; the automated target-rung version is still not built`

   I tell him only what his report shows.
5. **If he replies RED, or the Editor crashed, or the scene wouldn't open:**
   - Record `- result: SAVE-1 RED, <date>, "<owner's words verbatim>"`.
   - Put a line under the spec title: `STATUS: STOPPED — outpost work permanently halted by owner after OUT-SAVE-01 failed (<date>). Do not resume unless the owner explicitly reverses this.`
   - Tell him the work is stopped.
   - Make no layout, generator or test changes and do no re-run. I also skip the systematic-debugging skill, because the owner's instruction takes priority over the skills.
6. **Any later outpost request:** point to the STOPPED line and decline unless he explicitly lifts it.
