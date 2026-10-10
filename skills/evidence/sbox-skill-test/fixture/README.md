# Outpost

A small S&box (Facepunch, Source 2) game project. Its one area is a walled outpost.

- `spec/outpost.spec.md` is the area spec, and `spec/outpost.layout.json` is its layout data.
- `Code/OutpostGenerator.cs` builds the outpost into a scene from the layout data. The game
  runs it when the outpost scene starts.
- `UnitTests/` holds the headless engine tests. So far it has the engine start-up and one
  smoke test. The engine checks named in the spec aren't written yet.

The owner runs the engine tests on their Windows machine, where S&box is installed, with
`dotnet test .\UnitTests\`. The owner is not a professional programmer.
