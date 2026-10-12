# Outpost

A small S&box (Facepunch, Source 2) game project. Its one area is a walled outpost.

- `spec/outpost.spec.md` is the area spec, and `spec/outpost.layout.json` is its layout data.
- `Code/OutpostGenerator.cs` builds the outpost into a scene from the layout data. The game
  runs it when the outpost scene starts.
- `UnitTests/` holds the headless engine tests, set up from a rung-1 starter: engine start-up,
  test helpers, and setup checks. `UnitTests/OutpostTests.cs` has the engine checks for
  OUT-COLL-01 and OUT-SPAWN-01; the other engine checks named in the spec aren't written yet.

The owner is not a professional programmer.
