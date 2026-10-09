**1. Reply to owner:**

> Happy to. "Lived-in" can mean a few things. Some of them (lighting mood, ambient sound, NPCs, interiors) are listed as out of scope in the outpost spec, so I'd like to know which one you mean before I build anything.
>
> **A (my pick):** signs of daily life in the yard. Crates and barrels by the gate, a water trough and a cart at the tower base, a campfire ring, sandbags and a washing line. All of it stays off the walking path, away from both spawns and out of the view of the tower. I'd build it from simple shapes, with no new downloaded assets.
> **B:** A, plus mood: lantern light and campfire/wind sounds. This would move lighting and audio into scope.
> **C:** something else. Describe it in a sentence, or send a picture that has the feel.
>
> Also, your "feels like a frontier outpost" goal is still a draft. I'd reword it to "feels like a **lived-in** frontier outpost."
>
> Reply: A, B or C, plus "agree" if that wording is right.
>
> When it's built and my own checks pass, I'll send you one short checklist: run the tests on your PC, then do a quick walk-through.

**2. Next actions:**

Rigor: evaluated. The result is judged by feel, and the new solid objects sit next to the agreed routes, spawns and sightlines. A normal revert undoes everything.

1. After the reply (shown for A), write the checks first. The generator and `UnitTests/` are not in this folder, so I'd open them in the project.
   - Extend lint-layout (OUT-DATA-01) to cover a new `props` array: unique IDs, and everything inside the bounds. A control fixture with a duplicate prop ID must fail.
   - Add engine control fixtures: a prop on the gate-to-tower segment, one on top of `spawn.north`, and one between `spawn.south` and the tower top. OUT-ROUTE-01, OUT-SPAWN-01 and OUT-SIGHT-01 must each fail on these.
   - The spawn test needs an enclosure probe. Mesh collision is hollow, so `StartedSolid` won't catch a player standing inside a prop.
2. `OutpostGenerator`: build props through the API (create the MeshComponent disabled, assign the mesh, then enable it, with collision on). No hand-edited scene data.
3. `spec/outpost.layout.json`: add about 12 `props` entries `{id, kind, position, yaw, size}` along the walls, beside the gate and at the tower base. Keep them clear of the x=0 and y=0 route lines, both spawns, and the sightlines from each spawn to `[400,0,480]`.
4. `spec/outpost.spec.md`:
   - Reword OUT-FEEL-01 and the FEEL-1 question to "does it feel lived-in?"
   - Mark it `agreed` only if the owner replied "agree".
   - If the owner picks B, also amend Out of scope and add draft requirements for light and sound.
5. Run lint-layout and lint-scene, and fix until both pass.
6. Send one card, with the commit hash:
   1. Run the tests. If anything is red, stop and send the result plus `logs\testhost.log`.
   2. SAVE-1.
   3. NET-1, reopened because the generator output changed. Same-machine is not clean-client proof.
   4. FEEL-1.
7. Record each reply in `spec/ACCEPTANCE.md` and report:

```
OUT-DATA-01               static   pass                    <commit>
OUT-ROUTE/SPAWN/SIGHT-01  engine   pending, run on owner's PC  <commit>
OUT-SAVE/NET/FEEL-01      editor/session/owner  card sent
```
