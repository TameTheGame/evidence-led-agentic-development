**Reply to owner:**

> Got it. This is a small, well-scoped change, so I'll suggest a short plan here in chat rather than writing a separate design document. I won't change any files until you say yes. If you'd like a more formal process, just say so.
>
> Here's what I understood:
> - **What you asked for:** add a third spawn point on the east side of the outpost.
> - **What I'm assuming:** "east" means the tower's side of the map. The new spawn goes inside the walls, at the same ground height as the other two spawns. It has to pass the same checks they pass: it lands on solid ground with room to stand, and you can see the top of the tower from it.
> - **One more thing:** the outpost spec currently says the outpost has "two spawn points" and checks the tower "at both spawns." I'd update that wording as part of this change.
>
> Before I pick an exact spot, one question: **what's the third spawn for?**
> A) Spreading players out so fewer people appear in the same place
> B) Starting players close to the tower
> C) Something else (tell me)

**Next actions:**

1. Wait for the owner's answer. No files are touched yet.
2. Post a short design in chat, then stop and wait for an explicit yes:
   - **`spec/outpost.layout.json`:** add `{ "id": "spawn.east", "position": [600, 0, 8] }`, adjusted to fit the answer. That spot is the same distance from the centre as the north and south spawns, at the same height (z=8), and well inside the ±1024 bounds. I'd point out that the tower stands at x=400, y=0, so this spot is only 200 units east of its centre. I'd move the spawn sideways if it would be too close to the tower's base.
   - **`spec/outpost.spec.md`:** change the Intent from "two spawn points" to "three spawn points", and change OUT-SIGHT-01 from "at both spawns" to "at every spawn". These requirements are marked agreed, so the design states these edits plainly and the owner's yes covers them.
   - **Generator:** no change expected, because it builds the area from the layout file.
   - **Testing:** this only changes data, so I'd ask the owner to OK skipping new test code (the test-driven-development skill allows this for config files, with the owner's permission). The existing checks become the tests. One caveat: I need to confirm that `OUT_SPAWN_01` and `OUT_SIGHT_01` check every spawn in the layout rather than naming north and south. `UnitTests/` isn't in my folder, so I'd ask the owner for it. If either test names only the two existing spawns, I'd fix the test first, watch it fail because `spawn.east` is missing, and only then add the spawn.
3. After the yes: make the two edits, run `lint-layout OUT-DATA-01` if I have it here, and show the owner the change.
4. Send the owner a short card: run the full `UnitTests/` suite on Windows, and reply GREEN, or RED plus the failing test's name and message. Also re-run card SAVE-1, because the generated scene will change.
5. Only call the change done once the owner has reported those results. Until then, describe it as "edited, not yet verified."
