---
name: sbox-engine-reference
description: Use when writing, testing, or debugging S&box (Facepunch, Source 2) C# code, scenes, components, or map geometry, or when S&box behaves differently than expected.
---

# S&box engine reference

> **Target-specific, non-normative.** This skill is drafted in ELAD as an example of a
> project's domain layer. Once adopted, it belongs in the S&box project that uses it.
> Facts marked *(spike)* were verified on S&box `26.10.02` by the engine-rung spike in
> `examples/sbox/engine-rung-spike/`. Facts marked *(source)* come from reading
> `Facepunch/sbox-public` and were not run.

## The engine source is ground truth

- **Read the declaration before you use an API.** Check the exact declaration, its
  implementation, and its immediate collaborators in the project's local clone of
  `Facepunch/sbox-public`; the project's `AGENTS.md` says where that clone is. Don't guess
  from Unity, Unreal, or older S&box knowledge.
- **The installed build can differ from the source.** The installed engine records its
  version in `.version` in the install folder. Facepunch changes code weekly, so compare
  dates. Run `git log -- <file>` on the clone to see what changed after your build.
- **Facepunch's own tests are the best worked examples.** See
  `engine/Tests/Sandbox.Test.Integration/`, especially `Scene/Components/` and
  `Scene/Trace/`. They show how to drive scenes, meshes, colliders, and the player
  controller from code.
- **Cite what you checked.** When code depends on engine behavior, record the source path
  and the commit you read.

## Where map-related code lives *(source)*

| Topic | Path in `sbox-public` |
|---|---|
| Editable mesh geometry | `engine/Sandbox.Engine/Scene/Components/Mesh/` (`PolygonMesh*.cs`, `MeshComponent.cs`) |
| Terrain | `engine/Sandbox.Engine/Resources/Terrain/`, `engine/Sandbox.Engine/Scene/Components/Terrain/` |
| Scenes and scene files | `engine/Sandbox.Engine/Scene/Scene/`, `engine/Sandbox.Engine/Resources/Scene/` |
| Colliders and traces | `engine/Sandbox.Engine/Scene/Components/Collider/`, `Scene/Scene/Scene.Trace.cs` |
| Player movement | `engine/Sandbox.Engine/Scene/Components/Game/PlayerController/` |
| Physics surfaces | `engine/Sandbox.Engine/Resources/Surface*.cs` |
| Test project generation | `engine/Sandbox.Engine/Systems/Project/Project/Project.Solution.cs` |

## Known behavior

**Writing code**
- **Write explicit usings.** Some project templates don't add `global using Sandbox;`, and
  none cover `System.*`, so write `using Sandbox;` and `using System;` yourself.
- **Mark editor-visible fields with `[Property]`.** `[Sync]` alone only replicates over
  the network *(observed in an S&box project)*.
- **Scenes need their own camera.** `PlayerController` adjusts an existing main camera but
  never creates one, so a scene without a `CameraComponent` renders black *(source)*.
- **Component errors don't surface as exceptions.** Errors thrown in a component's
  `OnEnabled` and other callbacks are caught and logged, not rethrown *(source, spike)*. A
  component that silently does nothing usually threw.
- **Don't hand-edit engine-written data.** Mesh geometry is saved inside scenes as an
  engine-written blob. Change the generator or its input and regenerate through the API.

**Generated geometry**
- **In a game scene, create `MeshComponent` disabled, then assign, then enable.** In a
  game (non-editor) scene, `MeshComponent` builds its model only when it is enabled.
  Assigning `Mesh` later does nothing *(source)*.
- **Mesh collision is a hollow surface, not a solid.** A body wholly inside a
  mesh-collision block touches no face, so `StartedSolid` stays false. Traces also don't
  see mesh faces from behind. To detect "stuck inside", use an enclosure probe: ray
  outward to the first face, then trace back *(spike: S7, D4–D7)*.
- **`PolygonMesh.Rebuild()` needs a loaded `default` physics surface.** It needs one even
  when no collision is requested. Without one, it throws a `NullReferenceException` in
  `ModelBuilder.AddSurface` *(spike: D1)*.

**Headless tests (the engine rung)**
- **Only code projects get a test project.** S&box generates a `UnitTests` project only
  for `game`, `library`, and `addon` projects. A `content` (map) project needs a small
  companion game project *(source)*.
- **Machine requirements:** Windows only, the .NET 10 SDK (projects target `net10.0`), and
  `FACEPUNCH_ENGINE` set to the install folder. Start the engine with `TestAppSystem` in
  `[AssemblyInitialize]` *(spike)*.
- **Base content isn't mounted, so no `default` surface is loaded.** Register a stand-in
  in test setup; see the spike kit's `TestSurfaces.cs`. That code uses engine internals
  through reflection, is test-only scaffolding, and may break on an engine update
  *(spike)*.
- **Read `logs\testhost.log` in the install folder.** Engine errors from a test run land
  there, not in the test output. It's overwritten every run, so copy it per run
  *(spike)*.
- **To drive a player,** create a `PlayerController` with `UseInputControls = false` and
  `EnableFootstepSounds = false`, then call `scene.GameTick()` in a bounded loop
  *(source, spike)*.
- **Loading a project scene:** `Scene.LoadFromFile` fails headlessly. Reading the
  `.scene` file and passing it through `SceneFile.LoadFromJson` and `Scene.Load` works for
  simple scenes *(spike: S8)*. Scenes that reference prefabs or models are still untested.

## When S&box surprises you

Record a lesson in the project's engine-lessons file before moving on:

- **What happened:** the observed behavior and the build it happened on.
- **Root cause:** the source path and commit that explain it.
- **Rule:** what to do next time.
- **Evidence:** the test, log, or card that showed it.

## Red flags

| Thought | Reality |
|---|---|
| "Unity does it this way, so S&box probably does too." | Read the S&box source. |
| "The component exists, so it built." | Check its result, such as `Model` or the shapes. Its errors were probably caught and logged. |
| "No exception in the test, so the engine is fine." | Read `logs\testhost.log`. |
| "The source on GitHub says X, so my build does X." | Check the installed `.version` against the source history. |
| "I'll patch the scene's mesh data by hand." | Regenerate it through the API. |
