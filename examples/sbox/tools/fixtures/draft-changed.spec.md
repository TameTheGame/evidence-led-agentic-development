# Yard

owner: Owner

## Intent
A small fenced yard with one gate and two spawn points.

## Requirements

### YARD-DATA-01 — The layout file is valid
- state: agreed
- rung: static
- check: lint-layout YARD-DATA-01

### YARD-SIGHT-01 — The gate is visible from eye height at both spawns
- state: agreed
- rung: engine
- check: YARD_SIGHT_01_GateVisibleFromSpawns

### YARD-FEEL-01 — Walking from either spawn to the gate feels calm
- state: draft
- rung: owner
- check: card FEEL-1

### YARD-GATE-01 — The gate opens inward
- state: retired
- rung: engine
- check: YARD_GATE_01_GateOpensInward
- why: the owner chose a gate that slides

## Cards

### FEEL-1 (owner)
1. Spawn and walk to the gate.
Reply: GREEN, or RED plus what felt wrong.
