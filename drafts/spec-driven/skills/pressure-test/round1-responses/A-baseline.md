**1. Reply to owner:**

> Will do. I'll put the new spawn on the east side, which is the side the water tower is on. It will be about as far from the centre as the north and south spawns, just past the tower. I'll also update the spec to match:
> - The intent will say three spawn points instead of two.
> - The tower check will say "every spawn" instead of "both spawns", so the tower has to be visible from the new spawn too.
>
> If you'd rather the tower rule not apply to this spawn, or you want the spawn somewhere else, just tell me.
>
> I can check the layout file here, but I can't run the engine. Once I've made the change, I'll need you to do this on your PC:
> 1. Regenerate the outpost and run the unit tests. The spawn test and the tower-visibility test are the ones that matter.
> 2. Run card SAVE-1 again, because the scene will change.
>
> You don't need to redo NET-1 or FEEL-1, since the walls, gate and north spawn stay the same. I won't call this done until you report GREEN on those.

**2. Next actions:**

1. **Edit `spec/outpost.layout.json`:** add `{ "id": "spawn.east", "position": [600, 0, 8] }` to `spawns`. This matches the 600-unit distance of the other two spawns. +X counts as east because north is +Y.
2. **Edit `spec/outpost.spec.md`:**
   - In Intent, change "two spawn points" to "three spawn points (north, south, east)".
   - Rename OUT-SIGHT-01 to "…visible from eye height at every spawn".
   - Add no new requirement, because OUT-SPAWN-01 already covers every spawn.
   - Leave the cards unchanged; FEEL-1 still uses the north spawn.
3. **Static check for OUT-DATA-01:** run `lint-layout OUT-DATA-01` if it's available. If not, check by hand without changing anything:
   - The JSON parses.
   - `spawn.east` is the only spawn with that ID.
   - The position is inside the bounds: x 600 ≤ 1024, y 0, z 8 within 0–512.
4. **Check the generator and tests:** make sure `OutpostGenerator` and `OUT_SPAWN_01` / `OUT_SIGHT_01` read every spawn from the layout and don't assume exactly two. They aren't in this folder, so I'd ask the owner for `UnitTests/` and the generator code. If either one hardcodes two spawns, I'd change it to loop over `layout.spawns`.
5. **Send the owner the exact steps:**
   - Regenerate the scene.
   - Run `lint-scene OUT-SCENE-01` (it should still find one main camera).
   - Run the full UnitTests. SPAWN and SIGHT test the change; COLL and ROUTE check that nothing else broke.
   - Run card SAVE-1.
6. **Risk:** the spawn is only about 200 units from the tower, so the line of sight to the top is steep, and the tank could hide its own top. If OUT_SIGHT_01 fails for `spawn.east`, move the spawn further out and off the tower's line, for example `[700, 350, 8]`. If OUT_SPAWN_01 fails, the spawn is probably inside the east wall; move it inward. Then ask for one more test run.
7. **Close out:** record GREEN for OUT-SPAWN-01, OUT-SIGHT-01, OUT-SCENE-01 and OUT-SAVE-01 only after the owner reports them for this layout. NET-1 and FEEL-1 results still stand, since nothing they test changes.
