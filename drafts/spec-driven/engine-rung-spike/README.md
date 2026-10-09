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
| `UnitTests/TestInit.cs` | Starts and stops the engine once for the test run. |
| `UnitTests/EngineRungTests.cs` | Seven tests, each isolating one capability. |

## The tests

| Test | Proves | If it fails |
|---|---|---|
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
4. **Point the tests at the engine.** Set `FACEPUNCH_ENGINE` to the S&box install folder,
   the folder that contains `sbox-dev.exe` and `bin\win64\`. With a default Steam install
   that is usually `C:\Program Files (x86)\Steam\steamapps\common\sbox`.
5. **Run the tests.** From the project root:

   ```powershell
   $env:FACEPUNCH_ENGINE = "<S&box install folder>"
   dotnet test .\UnitTests\ --logger "console;verbosity=detailed" *> spike-results.txt
   ```

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
