**1. Reply to owner:**

Happy to. "Lived-in" can mean a few different things, and some of them are marked out of scope in the outpost spec right now. Before I change anything, which of these did you mean?

1. **Outdoor clutter.** This is where I'd start: crates and barrels by the gate, a cold campfire, a water trough and tools at the tower base, a washing line along a wall. It fits the current spec.
2. **Wear and tear.** Dirt paths, scuffed walls, patched boards.
3. **Life and atmosphere.** Lit windows, background sounds, people, building interiors. The spec lists these as out of scope today, so if you want them we'd update the spec first.

Any mix is fine. A screenshot or a game you have in mind would help a lot. If you already have props you want to use, tell me. Otherwise I'll suggest a short list for you to approve.

Whatever we add, both spawns stay clear, the walk from spawn to gate to tower stays open, and the tower stays visible. The existing tests will tell us if I break any of that. After the change I'll send you a short checklist to run the tests on your PC. Then you walk it and tell me if it feels right. That last part is your call, not something a test can decide.

**2. Next actions:**

1. Wait for the owner's answer and change no files yet. While waiting, find and read `OutpostGenerator` and the `lint-layout` tool. They aren't in this folder, so I'd ask the owner where they are.
2. Assuming option 1 (if option 3, edit "Out of scope" first), change `spec/outpost.spec.md`:
   - Add **OUT-PROP-01** (static, `lint-layout OUT-PROP-01`). Every prop has a unique ID, sits inside the bounds, uses an approved kind, and leaves player-sized space around both spawns and every route segment.
   - Note that OUT-COLL, OUT-SPAWN, OUT-ROUTE and OUT-SIGHT now also cover props.
   - Add "does it feel lived-in?" to card FEEL-1. Keep OUT-FEEL-01 as `draft` until the owner confirms.
3. Change `spec/outpost.layout.json`:
   - Add the route `spawn-north-to-gate`: `[[0,600,0],[0,0,0],[0,-900,0]]`. FEEL-1's walk from the north spawn isn't covered by any listed route today, so new clutter could block it without any test noticing.
   - Add `"props": [{ "id", "kind", "position", "yaw" }]`, about 8–12 items placed along the walls and around the tower base. Keep them off the x≈0 walkway and the gate-to-tower route, and out of the sightlines from each spawn to the tower top at (400,0,480).
4. Generator: read `props`, map each `kind` to an approved model through a small table, and stop with a clear error on an unknown kind. Props stay put and have collision, so the host and client agree.
5. Extend `lint-layout` for OUT-PROP-01, then run `lint-layout` and `lint-scene`.
6. Confirm that the engine tests build the full generated scene, props included. Then send the owner a numbered card:
   - Run `UnitTests` (COLL, SPAWN, ROUTE, SIGHT) on the Windows PC.
   - Run SAVE-1 and NET-1 again, because the scene changed.
   - Do FEEL-1.

   Report each one as GREEN or RED. Nothing is called done until those results come back.
