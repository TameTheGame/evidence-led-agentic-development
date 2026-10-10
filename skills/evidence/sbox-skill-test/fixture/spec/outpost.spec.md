# Outpost

owner: Owner
data: spec/outpost.layout.json

## Intent
A small walled frontier outpost players reach early. One gate, a water tower that works
as a landmark, and two spawn points. It should read clearly at a glance and be easy to
walk without snagging.

## Out of scope
Interiors, lighting mood, ambient audio, NPCs.

## Requirements

### OUT-DATA-01 — The layout file is valid
- state: agreed
- rung: static
- check: lint-layout OUT-DATA-01
- touches: spec/outpost.layout.json
- why: catches duplicate IDs and spawns outside the bounds before anything runs

### OUT-SCENE-01 — The generated scene has exactly one main camera
- state: agreed
- rung: static
- check: lint-scene OUT-SCENE-01
- touches: generated outpost scene
- why: PlayerController adjusts an existing main camera but does not create one

### OUT-COLL-01 — Every walkable floor in the layout has collision
- state: agreed
- rung: engine
- check: OUT_COLL_01_EveryFloorHasCollision
- touches: spec/outpost.layout.json, generator code

### OUT-SPAWN-01 — Every spawn lands on solid ground with room to stand
- state: agreed
- rung: engine
- check: OUT_SPAWN_01_EverySpawnLandsOnSolidGround
- touches: spec/outpost.layout.json, generator code

### OUT-ROUTE-01 — A standing player fits along every listed route segment
- state: agreed
- rung: engine
- check: OUT_ROUTE_01_RoutesAreClear
- touches: spec/outpost.layout.json, generator code
- why: listed segments are flat; slopes and stairs need a walk test instead

### OUT-SIGHT-01 — The tower top is visible from eye height at both spawns
- state: agreed
- rung: engine
- check: OUT_SIGHT_01_TowerVisibleFromSpawns
- touches: spec/outpost.layout.json, generator code

### OUT-SAVE-01 — The generated scene survives save, close, and reopen unchanged
- state: agreed
- rung: editor
- check: card SAVE-1
- target-rung: editor (automated) once an Editor tool can save and reopen unattended

### OUT-NET-01 — A remote client sees and collides with the same walls and gate
- state: agreed
- rung: session
- check: card NET-1

### OUT-FEEL-01 — Walking spawn to gate to tower feels like a frontier outpost
- state: draft
- rung: owner
- check: card FEEL-1
- why: draft until the owner confirms this is the feeling they want

## Cards

### SAVE-1 (editor)
1. Open the outpost scene in the Editor.
2. Save, close the Editor, and reopen the scene.
3. Expect: no prompts or errors, and the outpost looks the same.
Reply: GREEN, or RED plus what changed.

### NET-1 (session)
1. Host the map. Join from a second client.
2. On the client, walk into the north wall, then through the gate.
3. Expect: the wall blocks you and the gate lets you through, on both machines.
Reply: GREEN, or RED plus which machine and where.
Note: same-machine host and client is fine here. It is not clean-client proof.

### FEEL-1 (owner)
1. Spawn at the north spawn. Walk to the gate, then to the tower.
2. Judge: does it read as a frontier outpost, and is the path obvious?
Reply: GREEN, or RED plus what felt wrong.
