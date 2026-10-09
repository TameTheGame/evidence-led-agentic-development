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
- **Saved scenes:** can a test load the project's own saved scene and query its collision?

These settle open questions 1–3 in [the ladder doc](../SPEC_AND_LADDER.md#open-questions-before-adoption):
a code project hosts the tests (1), generated meshes and traces need a default surface (2),
and saved scenes load headlessly (3).

## Contents

| Path | Purpose |
|---|---|
| `Code/SpikeGeometry.cs` | Builds synthetic box geometry. It lives in the game code, so the tests also prove they can use project code. |
| `UnitTests/TestInit.cs` | Starts and stops the engine once for the test run, and provides a default physics surface. |
| `UnitTests/TestSurfaces.cs` | Added after run 2: makes a `default` physics surface available, public route first. |
| `UnitTests/EngineRungTests.cs` | S0–S8, each isolating one capability, plus the shared stuck check. |
| `UnitTests/MeshDiagnosticsTests.cs` | D1–D7: diagnostics that located the mesh-build and stuck-detection failures. |

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
| S7 control: stuck player is detected | S6's stuck check can actually fail, even inside mesh collision | S6 passing means nothing; stuck checks need another approach |
| S8 saved scene loads with collision | The project's own saved startup scene loads, and a trace hits its floor (route printed) | Saved scenes can't be checked headlessly; build the area in-test instead |

S8 uses `scenes/minimal.scene`, the startup scene S&box's new-game template creates. Its
`Plane` has a box collider whose top is at z = 0. Keep that scene unmodified.

The stuck check (`BodyStartsInsideGeometry`) has two parts:

1. **`StartedSolid`.** A body trace that starts inside convex collision, or touches a mesh
   face, reports it.
2. **Enclosure probe.** This catches a body wholly inside mesh collision (added after run 4).
   - Cast a ray up from the body's centre to the first face visible from there, then a ray
     back down.
   - A face hit on the way back faces away from the centre, so the centre is inside a
     closed solid.
   - It works because traces don't see mesh faces from behind (D6). It assumes closed meshes
     with outward-facing faces, which `PolygonMesh` boxes are.

Expected outcome: S0–S8 pass. D1–D5 and D7 pass. D6 fails while mesh faces are one-sided,
which the enclosure probe relies on. If D6 ever passes, re-check S7 and D7.

## Diagnostics

| Test | Checks | Reading |
|---|---|---|
| D1 mesh rebuilds into a model | `PolygonMesh.Rebuild()` called directly, outside any component | Fails: building the mesh itself fails headlessly, and its stack trace says why |
| D2 component state after enable | Whether the component became active, and whether it built | `Active=False`: an enable problem. Active but no model: the build was skipped or failed silently |
| D3 floor in an editor scene | The same floor in `Scene.CreateEditorScene()` | Passes while S4 fails: rung-1 tests can build geometry in editor scenes |
| D4 body inside a hull block | S7's placement, with hull (convex) collision | Passes: `StartedSolid` detects bodies inside convex collision |
| D5 body crossing a mesh face | Mesh collision, body crossing the block's top face | Passes: `StartedSolid` detects bodies that touch a mesh face |
| D6 ray from inside a mesh block | Whether a trace sees a mesh face from behind | Fails: mesh faces are one-sided for traces. The enclosure probe relies on this |
| D7 player under a ceiling | The enclosure probe's false-positive control | Fails: the probe flags a standing player as stuck; S6 results can't be trusted |

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
   Editor's console shows no compile errors, then close the Editor. Later kit files dropped
   into `UnitTests\` are picked up without reopening.
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

7. **Keep the engine log.** S&box catches errors thrown inside components and writes them
   only to `logs\testhost.log` in the install folder, which each run overwrites. Copy it
   next to that run's `spike-results.txt`.

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

### Run 3 — default surface setup

Same environment as run 1. Kit at `e644ae1`. S0 printed the route used:
`internal fallback: registered a stand-in default surface`.

| Test | Result | Note |
|---|---|---|
| S0 default surface setup | pass | The public route found nothing; the internal fallback worked |
| S1 engine starts | pass | |
| S2 default surface | pass | The stand-in surface is found by name |
| S3 player lands on box collider | pass | |
| S4 mesh floor builds collision | pass | One collision mesh |
| S5 ray hits mesh floor | pass | |
| S6 player lands on mesh floor | pass | |
| S7 stuck-player control | **fail** | `a player placed inside a solid block was not detected`: the first real failure |
| D1–D3 | pass | D2 now prints `HasModel=True` |

Findings:

- **The missing surface was the only blocker** for generated-mesh collision, traces, and
  landing (S4–S6). The engine log shows no component errors.
- **No public route provides the surface on this build.**
  - `ResourceLibrary.Get` only looks up resources that are already registered.
    `core\surfaces\default.surface` is on disk, but headless test startup never registers it.
  - `GameResource.LoadFromJson` is public but doesn't run the `PostLoad` step that registers
    a surface.
  - `ResourceLoader.LoadAllGameResource` is internal.
  - Facepunch's integration tests set `Surface.All[0]` directly for the same reason
    (`engine/Tests/Sandbox.Test.Integration/Assembly.cs`).
  - The labelled reflection fallback stays as test scaffolding.
- **`PolygonMesh.Rebuild()` needs a surface even without collision.** It calls
  `AddSurface` for every submesh, and D1's render-only rebuild crashed in run 2.
  `AddSurface` doesn't check for a null fallback, while the engine's own
  `Surface.FindByIndex` falls back safely.

### Run 4 — stuck-detection diagnostics

Same environment. Kit changes:

- `CreateBlock` takes an optional collision type. The default is still mesh.
- The stuck check became `internal`, so diagnostics use the same code.
- D4–D6 were added.

| Test | Result | Note |
|---|---|---|
| S0–S6 | pass | As run 3 |
| S7 stuck-player control | fail | Unchanged |
| D1–D3 | pass | |
| D4 body inside a hull block | pass | `StartedSolid` detects bodies inside convex collision |
| D5 body crossing a mesh face | pass | `StartedSolid` detects bodies touching a mesh face |
| D6 ray from inside a mesh block | fail | `Hit=False StartedSolid=False EndZ=256 Normal=0,0,0` |

Root cause:

- `MeshComponent.CollisionType.Mesh` is concave collision (`IsConcave`): a triangle surface
  with no interior.
- A body wholly inside it touches no triangle, so `StartedSolid` stays false.
- Traces don't see mesh faces from behind (D6).
- This is how concave mesh collision works, not an engine fault. Facepunch's own
  `StartedSolid` test uses a `BoxCollider`, which is convex.

### Run 5 — enclosure probe

Same environment. Fix attempt 1:

- **Enclosure probe added.** The shared stuck check keeps `StartedSolid` and adds the
  enclosure probe described under [The tests](#the-tests). It uses the public trace API only.
- **No assertion was changed.** S6 gets stricter.
- **D7 added** as the probe's false-positive control.

| Test | Result | Note |
|---|---|---|
| S0–S7 | pass | S7 now detects the player wholly inside the mesh block |
| D1–D5 | pass | |
| D6 ray from inside a mesh block | fail | As run 4: the one-sidedness the probe relies on |
| D7 player under a ceiling | pass | The probe doesn't flag a ceiling |

### Run 6 — saved scene

Same environment. Added S8 for open question 3. S8 printed the route used:
`public: SceneFile.LoadFromJson on the saved file, then Scene.Load`.

| Test | Result | Note |
|---|---|---|
| S0–S8 | pass | S8: the ray hit the saved `Plane` at z ≈ 0 |
| D1–D5, D7 | pass | |
| D6 ray from inside a mesh block | fail | As expected |

Findings:

- **Loading by resource path fails headlessly.** `Scene.LoadFromFile( "scenes/minimal.scene" )`
  logs `LoadFromFile: Couldn't find scenes/minimal.scene`. The cause is the same as for the
  surface: headless tests register no project resources.
- **Loading the saved file's JSON works.** Reading the `.scene` file, then
  `SceneFile.LoadFromJson` and `Scene.Load`, are all public. The saved box collider was
  traceable.
- **Not covered:**
  - saved scenes whose objects reference other resources, such as prefabs or collision
    models; and
  - generated mesh geometry saved inside a scene.

### Run 7 — final check

Same environment. This run used the kit exactly as committed; only a doc comment had
changed since run 6. Both route lines matched run 6, and the build had no warnings or errors.

| Test | Result | Note |
|---|---|---|
| S0–S8 | pass | |
| D1–D5, D7 | pass | |
| D6 ray from inside a mesh block | fail | As expected |

### Final result

On S&box `26.10.02`, a project's own tests can run these rung-1 checks headlessly:

| Check | Status | Evidence |
|---|---|---|
| Engine starts from project tests | Proven | S1 |
| Collision from generated `PolygonMesh` geometry | Proven, with default-surface scaffolding | S4, D1–D3 |
| Traces against generated geometry | Proven, with the same scaffolding | S5 |
| Spawn landing, with room to stand | Proven | S3 (primitive), S6 (generated) |
| Stuck detection | Proven, with the enclosure probe | S7, D4, D5, D7 |
| Saved project scene loads with traceable collision | Proven for primitive colliders, through the JSON route | S8 |

**Still unproven:**

- **A public way to provide the default surface.** None exists on this build.
- **Saved scenes that reference other resources,** and generated meshes saved into scenes.
- **The enclosure probe on open or inward-facing meshes.**
- **Other S&box builds.** Source checks used `sbox-public` at `3915f1a`, which is newer than
  the installed build.
- **Other platforms.** The runs were on Windows only.
- **Anything above rung 1.**

## What to report

- pass or fail for each of S0–S8 and D1–D7;
- the route lines S0 and S8 print;
- for each failure, its first error message and the top of its stack trace;
- any component errors in that run's `logs\testhost.log`;
- the S&box version or build number, and the output of `dotnet --version`.

The complete `spike-results.txt` and `testhost.log` stay with the scratch project. Bring
back only the summary.

## Afterwards

The scratch project can be deleted. Whatever the outcome, the result belongs in the
ladder doc's open questions, not in any game repository.

## S&box lessons found by this kit

1. **Outside an editor scene, `MeshComponent` builds its model only when the component is
   enabled.** `RebuildMesh()` returns early unless `Scene.IsEditor`
   (`engine/Sandbox.Engine/Scene/Components/Mesh/MeshComponent.cs`, `Facepunch/sbox-public`
   at `3915f1a69810026e23d331581266636de89411d5`). A generator that runs in a game scene must:
   1. create the component disabled;
   2. assign `Mesh` and `Collision`; then
   3. enable it.

   Otherwise the geometry renders nothing and has no collision.
2. **Headless project tests register no game resources.** There is no `default` surface,
   and project scenes can't be found by path. Anything that resolves a resource by path
   needs another route.
3. **Component errors don't reach the test output.** A component that throws during
   `OnEnabled` is logged only to `logs\testhost.log`.
4. **Mesh collision is a surface, not a volume.** `StartedSolid` misses a body wholly inside
   it. Use hull collision for convex solids, or an enclosure probe.
