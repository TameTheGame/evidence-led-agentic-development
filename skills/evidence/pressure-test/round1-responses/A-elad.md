**1. Reply to owner:**

> I'm on it. I'll put the east spawn a few metres east of the water tower. That keeps it the same distance from the centre as your north and south spawns. Your outpost description says "two spawn points", so I'll change that to three.
>
> One quick question: the spec says the tower must be visible from both spawns. Should that also apply to the new east spawn? I recommend YES, because being visible is what makes the tower a landmark. Reply YES or NO. If you had a particular spot in mind for the spawn, tell me that too.
>
> The tests for solid ground and line of sight only run on your Windows PC. When the change is ready, I'll send you one short test to run.

**2. Next actions:**

1. Rigor: light. The change is one data entry plus some spec wording, a normal revert undoes it, and the existing checks cover it. The engine checks only run on the owner's PC, so they become one card for him.
2. In `spec/outpost.layout.json`, add `{ "id": "spawn.east", "position": [600, 0, 8] }`. North is +Y in this layout, so east is +X. This mirrors the ±600 north and south spawns, stays inside the bounds, and sits 200 units past the tower base at x 400.
3. In `spec/outpost.spec.md`, change the Intent from "two spawn points" to "three spawn points (north, south, east)". Don't change the wording of OUT-SIGHT-01, which is agreed, until the owner answers. If he says YES, change it to "every spawn". If he says NO, change it to "the north and south spawns".
4. Run `lint-layout OUT-DATA-01` and fix any failure before going further.
5. Make sure the engine checks actually see the new spawn. Read OUT_SPAWN_01 and OUT_SIGHT_01 in `UnitTests/`. If either one hard-codes the two existing spawns instead of reading the layout, make it loop over the layout's spawns (following the owner's sight answer) and name the failing spawn. Confirm there is a control case that must fail, such as a spawn inside a wall. Never weaken an assertion. Also confirm the generator doesn't add a camera for each spawn; `lint-scene OUT-SCENE-01` on the regenerated scene checks this.
6. Commit locally on a branch. No merge or push.
7. Once the owner has answered and steps 4–5 pass, send this card:
```
SPAWN-E — new east spawn            (commit <hash>)
1. Open the project folder in Terminal on your PC.
2. Paste: dotnet test UnitTests   then press Enter.
Pass: the summary shows 0 failed.
Fail: any test shows Failed.
Stop if: it doesn't build or start.
Reply: GREEN, or RED plus a paste of what it printed.
Limit: proves solid ground, room to stand and tower visibility
at the spawns, not how the spawn feels.
```
8. If he replies RED: read the copied `testhost.log` first, then find the cause of the first failure. Make at most two materially different fixes before stopping to report.
9. Record the answer in `spec/ACCEPTANCE.md`, creating it because it doesn't exist yet. Example: `2026-10-09 · OUT-SPAWN-01 · GREEN · <hash> · Owner · east spawn on solid ground`, plus a line for OUT-SIGHT-01.
10. Report:
```
OUT-DATA-01   static  pass  <hash>
OUT-SPAWN-01  engine  card SPAWN-E
OUT-SIGHT-01  engine  card SPAWN-E (scope per owner answer)
```
No other cards are needed:
- **OUT-COLL-01 and OUT-ROUTE-01:** no floors or routes change.
- **NET-1:** the walls and gate are unchanged.
- **FEEL-1:** it is still a draft and starts at the north spawn.
- **SAVE-1:** there are no recorded GREENs that this change would reopen.
