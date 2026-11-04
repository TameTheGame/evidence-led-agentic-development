# Outpost

A small S&box (Facepunch, Source 2) game project. Its one area is a walled outpost.

- `spec/outpost.spec.md` is the area spec, and `spec/outpost.layout.json` is its layout data.
- `Code/OutpostGenerator.cs` builds the outpost into a scene from the layout data.
- `Assets/scenes/outpost.scene` is the playable scene. The owner built it with the
  generator in the S&box Editor, reshaped the ground by hand, and saved it. Its ground,
  walls, gate apron and tower are editable meshes, and the Editor keeps their mesh data in
  `outpost.scene_d` beside the scene.
- `Code/GateDecal.cs` puts the sign over the south gate when the scene starts.
- `UnitTests/` holds the engine start-up and the test helpers the project started from.
  No project tests are written yet.

The owner runs the engine tests on their Windows machine, where S&box is installed, with
`dotnet test .\UnitTests\`. The owner is not a professional programmer.
