# Yard

owner: Owner

## Intent
A small fenced yard with one gate and two spawn points.

## Requirements

### YARD-DATA-01 — The layout file is valid
- state: agreed
- rung: static
- check: lint-layout YARD-DATA-01

### YARD-DATA-01 — The layout file has no duplicate spawns
- state: draft
- rung: static
- check: lint-layout YARD-DATA-01

### YARD-SIGHT-01 — The gate is visible from eye height at both spawns
- state: approved
- rung: engine
- check: YARD_SIGHT_01_GateVisibleFromSpawns

### YARD-FEEL-01 — Walking from spawn to gate feels calm
- state: agreed
- rung: vibes

## Cards

### FEEL-1 (owner)
1. Spawn and walk to the gate.
Reply: GREEN, or RED plus what felt wrong.
