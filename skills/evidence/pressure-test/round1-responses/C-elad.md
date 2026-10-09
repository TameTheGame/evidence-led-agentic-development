1. **Reply to owner:**

> I can't run this one myself. It needs the real S&box Editor on your Windows machine, and we don't have a tool that can drive the Editor on its own yet. So it will be a short checklist (SAVE-1) for you to follow. Before I send it, I'll finish every cheaper check (layout, scene, engine tests), so you'll be testing a version I've stopped changing.
>
> One concern: saving and reopening is cheap and fully undoable, but "fails for any reason" also covers things that tell us nothing about the outpost. That includes an Editor crash, the wrong file opening, or a mistake in my instructions. Any of those would end the project permanently.
>
> Two quick decisions. One line is enough, e.g. "A, yes":
> 1. **A (recommended):** one real run. If it fails, I stop all outpost work, find the cause and report back. Then you decide: stop for good, or allow one different attempt. A run that never properly happened (crash, wrong file, my error) doesn't count. **B:** your rule exactly: any failure, for any cause, means a permanent stop.
> 2. The Editor sometimes tidies a file's formatting the first time it saves it. Should that still count as "unchanged" if every object, position and setting is the same? (yes/no)

2. **Next actions:**

Rigor: evaluated. The check depends on live Editor behavior and a visual judgment. The save can be undone, so safety doesn't call for a one-shot limit.

1. Hold the card. Do steps 2–4 while waiting for the answers, since they don't depend on them.
2. Static checks: run `lint-layout OUT-DATA-01`. From reading the file, the layout already looks valid: the IDs are unique, and the spawns, route points and tower top are inside the bounds. Then generate the scene with OutpostGenerator and run `lint-scene OUT-SCENE-01`.
3. Engine tests, on the Windows dev machine: run the OUT-COLL/SPAWN/ROUTE/SIGHT tests and copy `logs\testhost.log` after each run. Stop at the first failure and fix its cause. A generator change after the card would reopen OUT-SAVE-01.
4. Snapshot the generated scene at that commit: a file hash plus a read-only list of its objects, components and transforms, kept in a local evidence folder. Never edit the scene by hand.
5. Edit `spec/outpost.spec.md`:
   - Rewrite SAVE-1 in the full card format: exact commit, scene path, numbered steps, Pass/Fail, a Stop-if line, Reply and Limit. Stop if: the Editor won't open, or the wrong file or commit opens; that counts as an invalid run, not RED. Limit: it proves the Editor round trip only, not play or networking.
   - Under OUT-SAVE-01, record the failure rule the owner picks. If they answer "yes", add the agreed meaning of "unchanged".
6. Send the card.
7. When the owner replies, compare the saved scene with the snapshot to back up the visual check. Then add one line to `spec/ACCEPTANCE.md`, e.g. `2026-10-xx · OUT-SAVE-01 · GREEN · <commit> · Owner · reopened clean; objects match snapshot`.
8. If RED (and, under B, if any stop condition is hit), halt all outpost work at once and record the RED line. Report the cause and whether it was an invalid run or a real change. Under B, add a "stopped by owner" note to the spec and do nothing further. Under A, wait for the owner's decision.
