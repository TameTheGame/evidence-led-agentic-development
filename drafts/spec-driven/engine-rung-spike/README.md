# Engine-Rung Spike (S&box)

> **Non-normative, synthetic, target-specific.** This kit tests one assumption in
> [Spec-Driven Evidence](../SPEC_AND_LADDER.md): that a project's own tests can check map
> claims with the real S&box engine and no Editor. It contains no production content and
> grants no authority. Nothing here goes into a game repository.

## The question

Can a project's own `UnitTests/` check map claims through the real engine headlessly, from
an ordinary project on the owner's machine? Specifically:

- **Collision:** does geometry built from a `PolygonMesh` get collision in a normal game
  scene?
- **Traces:** do traces work without the internal fallback surface that Facepunch's own
  engine tests install?
- **Stuck detection:** can a test tell whether a player is standing on ground or stuck
  inside geometry?

These are open questions 1–3 in [the ladder doc](../SPEC_AND_LADDER.md#open-questions-before-adoption).

## Contents

| Path | Purpose |
|---|---|
| `Code/SpikeGeometry.cs` | Builds synthetic box geometry. It lives in the game code, so the tests also prove they can use project code. |
| `UnitTests/TestInit.cs` | Starts and stops the engine once for the test run, and provides a default physics surface. |
| `UnitTests/TestSurfaces.cs` | Added after run 2: makes a `default` physics surface available, public route first. |
| `UnitTests/EngineRungTests.cs` | Seven tests, each isolating one capability. |
| `UnitTests/MeshDiagnosticsTests.cs` | Follow-up after run 1: three tests that locate the failing step of the mesh build. |

## The tests

| Test | Proves | If it fails |
|---|---|---|
| S0 default surface setup | Which route provided the `default` physics surface (printed) | No route worked: generated meshes can't be built in project tests yet |
| S1 engine starts | `TestAppSystem` boots and a scene works | Setup problem: check `FACEPUNCH_ENGINE`, the project type, and solution generation |
| S2 default surface (diagnostic) | Whether base surfaces are loaded | Informational only. If S5–S7 still pass, it doesn't matter |
| S3 player lands on a box collider | Physics and `PlayerController` tick headlessly, using Facepunch's known-good pattern | The engine rung can't use player physics; stop and report |
| S4 mesh floor builds collision | A `PolygonMesh` becomes collision in a game scene | Generated geometry can't be checked headlessly as built |
| S5 ray hits mesh floor | Traces work in a project test | Traces need a surface workaround; the ladder doc needs revising |
| S6 player lands on mesh floor with room | The shape of a real spawn requirement | Spawn checks need another approach |
| S7 control: stuck player is detected | S6's stuck check can actually fail | S6 passing means nothing; stuck checks need another approach |

Expected outcome: all seven pass. S2 may fail without changing the conclusion.

## How to run

1. **Create the project.** In the S&box Editor, create a new, empty **game** project.
   - Put it outside every Git repository, for example
     `C:\Users\<you>\Documents\Projects\scratch\elad_engine_rung_spike`.
   - It has to be a game project: S&box generates test projects only for game, library,
     and addon projects (`Project.Solution.cs`).
2. **Add the kit.** Copy this kit's `Code\SpikeGeometry.cs` into the project's `Code\`
   folder, and copy the `UnitTests\` folder into the project root, next to the `.sbproj`.
3. **Generate the test project.** Close and reopen the project in the Editor. S&box then
   generates the solution, including `UnitTests\<project>.unittest.csproj`. Check that the
   Editor's console shows no compile errors, then close the Editor.
4. **Install the .NET 10 SDK if needed.** S&box projects target `net10.0`. The .NET 10
   runtime alone isn't enough; `dotnet --list-sdks` must show a `10.0.x` SDK.
5. **Point the tests at the engine.** Set `FACEPUNCH_ENGINE` to the S&box install folder,
   the folder that contains `sbox-dev.exe` and `bin\win64\`. With a default Steam install
   that is usually `C:\Program Files (x86)\Steam\steamapps\common\sbox`.
6. **Run the tests.** From the project root:

   ```powershell
   $env:FACEPUNCH_ENGINE = "<S&box install folder>"
   dotnet test .\UnitTests\ --logger "console;verbosity=detailed" *> spike-results.txt
   ```

## Results

### Run 1 — 2026-10-09

Environment: S&box `26.10.02` (build dated 2026-10-02, Steam build `25681412`),
.NET SDK `10.0.401`, Windows. No compile errors or warnings; no kit file was changed.

| Test | Result | Note |
|---|---|---|
| S1 engine starts | pass | Headless engine works from a project's own tests |
| S2 default surface | fail | No `default` surface is loaded in project tests |
| S3 player lands on box collider | pass | Player physics works headlessly |
| S4 mesh floor builds collision | **fail** | `MeshComponent.Model` is null: the first real failure |
| S5 ray hits mesh floor | fail | Depends on S4: no collision to hit |
| S6 player lands on mesh floor | fail | Depends on S4: the player fell to z ≈ −12499 |
| S7 stuck-player control | fail | Depends on S4: no block to be stuck in. The check itself is still untested |

Findings:

- **Rung 1 is viable for primitive colliders and player physics** (S1, S3).
- **The machine needs the .NET 10 SDK.** With only the .NET 8 SDK installed, the tests
  could not build.
- **Generated-mesh collision does not build in a project test yet** (S4). The test
  console output shows no engine error. S&box catches exceptions thrown in a component's
  `OnEnabled` and logs them, so an error may have gone only to the engine's own log.
- **The installed build predates a mesh change.** Facepunch changed `MeshComponent`
  build ordering on 2026-10-04 (`sbox-public` #5982), after the installed build. Both
  versions should build the mesh when it is enabled, so the version gap alone does not
  explain S4.

### Run 2 — mesh diagnostics

Same environment as run 1. The engine's own log (`logs\testhost.log` in the S&box
install folder) held the error the test console didn't show.

| Test | Result | Note |
|---|---|---|
| D1 mesh rebuilds into a model | fail | `NullReferenceException` in `ModelBuilder.AddSurface(Surface)`, called from `PolygonMesh.Rebuild()` |
| D2 component state after enable | fail | `Enabled=True Active=True ObjectActive=True HasMesh=True HasModel=False` |
| D3 floor in an editor scene | fail | Same `AddSurface` error in an editor scene |

Run 1's log shows the same exception five times as `OnEnabled on Sandbox.MeshComponent
failed`: S&box caught it and logged it, so the tests only saw a missing model.

Root cause, from `sbox-public` source:

- `ModelBuilder.AddSurface( null )` falls back to `Surface.FindByName( "default" )`, then
  reads `.Index` from the result.
- Headless project tests load no `default` surface (S2), so that read throws.
- The code is unchanged in current `sbox-public`, so updating S&box would not fix it.

The component, the enable order, and the scene type are not the problem.

Fix under test (run 3): `TestSurfaces.EnsureDefault()` runs once at startup. It first
tries the public route, loading the engine's `surfaces/default.surface` through
`ResourceLibrary`. If that finds nothing, it registers a stand-in surface the way
Facepunch's own `MeshComponentBuildTests` do. That fallback uses engine internals through
reflection, so an S&box update could break it. S0 prints which route worked.

Next: run S0–S7 and D1–D3 together.

When the engine catches a component error during a test, read the engine's
`logs\testhost.log`: the error isn't in the test output.

| Test | Checks | Reading |
|---|---|---|
| D1 mesh rebuilds into a model | `PolygonMesh.Rebuild()` called directly, outside any component | Fails: building the mesh itself fails headlessly, and its stack trace says why |
| D2 component state after enable | Whether the component became active, and whether it built | `Active=False`: an enable problem. Active but no model: the build was skipped or failed silently |
| D3 floor in an editor scene | The same floor in `Scene.CreateEditorScene()` | Passes while S4 fails: rung-1 tests can build geometry in editor scenes |

## What to report

- pass or fail for each of S1–S7;
- for each failure, its first error message and the top of its stack trace;
- the S&box version or build number, and the output of `dotnet --version`.

The complete `spike-results.txt` stays with the scratch project. Bring back only the
summary.

## Afterwards

The scratch project can be deleted. Whatever the outcome, the result belongs in the
ladder doc's open questions, not in any game repository.

## S&box lesson found while writing this kit

Outside an editor scene, `MeshComponent` builds its model only when the component is
enabled. `RebuildMesh()` returns early unless `Scene.IsEditor`
(`engine/Sandbox.Engine/Scene/Components/Mesh/MeshComponent.cs`, `Facepunch/sbox-public`
at `3915f1a69810026e23d331581266636de89411d5`). A generator that runs in a game scene must:

1. create the component disabled;
2. assign `Mesh` and `Collision`; then
3. enable it.

Otherwise the geometry renders nothing and has no collision.
