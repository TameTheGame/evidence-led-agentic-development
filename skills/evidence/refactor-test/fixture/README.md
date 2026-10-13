# Frontier

A small S&box (Facepunch, Source 2) game project with two areas: a walled outpost and a
quarry.

- `spec/outpost.spec.md` and `spec/quarry.spec.md` are the area specs. Each area's layout
  data is next to its spec, in `spec/outpost.layout.json` and `spec/quarry.layout.json`.
- `Code/AreaGenerator.cs` builds an area into a scene from its layout data. Both areas use
  it.
- `UnitTests/` holds the headless engine tests, set up from a rung-1 starter: engine start-up,
  test helpers, and setup checks. `UnitTests/OutpostTests.cs` and `UnitTests/QuarryTests.cs`
  have each area's engine checks for floor collision and spawns, each with a control case.
  The other engine checks named in the specs aren't written yet.

The owner is not a professional programmer.
