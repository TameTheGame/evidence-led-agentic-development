# Quarry

owner: Owner
data: spec/quarry.layout.json

## Intent
An open quarry next to the outpost, entered from a loading dock on its south side. Cliffs
on three sides, a rock crusher that works as a landmark, and two spawn points.

## Out of scope
Mining, moving machinery, lighting mood, ambient audio, NPCs.

## Requirements

### QRY-DATA-01 — The layout file is valid
- state: agreed
- rung: static
- check: lint-layout QRY-DATA-01
- touches: spec/quarry.layout.json
- why: catches duplicate IDs and spawns outside the bounds before anything runs

### QRY-COLL-01 — Every walkable floor in the layout has collision
- state: agreed
- rung: engine
- check: QRY_COLL_01_EveryFloorHasCollision
- touches: spec/quarry.layout.json, generator code

### QRY-SPAWN-01 — Every spawn lands on solid ground with room to stand
- state: agreed
- rung: engine
- check: QRY_SPAWN_01_EverySpawnLandsOnSolidGround
- touches: spec/quarry.layout.json, generator code
- why: the dock spawn stands on generated geometry, not on the ground

### QRY-FEEL-01 — Arriving at the dock, the quarry reads as a working quarry
- state: draft
- rung: owner
- check: card FEEL-Q1
- why: draft until the owner confirms this is the feeling they want

## Cards

### FEEL-Q1 (owner)
1. Spawn at the dock spawn. Walk into the quarry, then to the crusher.
2. Judge: does it read as a working quarry, and is the way in obvious?
Reply: GREEN, or RED plus what felt wrong.
