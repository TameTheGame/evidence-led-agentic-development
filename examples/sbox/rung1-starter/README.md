# Rung-1 Starter (S&box)

> **Non-normative, synthetic, target-specific.** This is a copyable starting point for a
> project's own engine-rung tests on S&box (Facepunch, Source 2). It packages what the
> [engine-rung spike](../engine-rung-spike/README.md) proved, so agents can wire up the
> scaffolding instead of only naming it. It grants no authority.

The [domain-skill test](../../../skills/evidence/SBOX_SKILL_TEST.md) found that agents with
the [S&box skill](../skills/sbox-engine-reference/SKILL.md) knew a default physics surface
was needed, but none could write the scaffolding without the spike kit's code. This starter
is that code, ready to copy.

## Contents

| Path | What it is |
|---|---|
| `UnitTests/TestInit.cs` | Starts the engine once per test run, then provides a `default` physics surface |
| `UnitTests/TestSurfaces.cs` | The default-surface scaffolding. **Test-only:** it uses engine internals through reflection when no public route works, and an engine update may break it. It records which route worked. |
| `UnitTests/EngineTestHelpers.cs` | A headless player, a bounded tick-until-grounded loop, the stuck check with its enclosure probe, and the saved-scene loader |
| `UnitTests/StarterGeometry.cs` | Stand-in box geometry, built in the order a game scene needs: create the `MeshComponent` disabled, assign the mesh, then enable it. Replace it with your own generator. |
| `UnitTests/StarterTests.cs` | Three setup checks, and one requirement written as project tests should be: named after its check, with a control case that must fail |
| `tools/run_engine_tests.ps1` | Runs the tests and saves the engine's own log with the results, because engine errors appear only there |

## Using it

1. **Use a code project.** S&box generates a test project only for `game`, `library`, and
   `addon` projects. A `content` (map) project needs a small companion code project.
2. **Copy the starter in.** Copy `UnitTests\` into the project root, next to the `.sbproj`,
   and copy `tools\run_engine_tests.ps1` into the project's `tools\`.
3. **Generate the test project.** Open the project in the S&box Editor, check the console
   for compile errors, and close it. S&box generates `UnitTests\<project>.unittest.csproj`.
4. **Set up the machine.** Rung 1 needs Windows, the .NET 10 SDK (`dotnet --list-sdks` must
   show `10.x`), and `FACEPUNCH_ENGINE` set to the S&box install folder, the one containing
   `sbox-dev.exe`.
5. **Run the tests.** From the project root:

   ```powershell
   powershell -File tools\run_engine_tests.ps1
   ```

   - The script saves results in `test-results\<time>\`, including `testhost.log`. Add
     `test-results/` to the project's `.gitignore`.
   - Runs on one machine wait for each other, because they share the engine log.
6. **Tell agents.** Add a line to the project's `AGENTS.md`, such as: "Run engine tests with
   `powershell -File tools\run_engine_tests.ps1`. Read its engine-log lines when a test fails
   without an exception."

## Writing a requirement's test

- **Name the test after the requirement's check,** for example
  `OUT_SPAWN_01_EverySpawnLandsOnSolidGround`.
- **Build the area with the project's own generator,** not `StarterGeometry`, so the test
  checks the code the game runs. Use a game scene (`new Scene()`), not an editor scene: game
  scenes build meshes only on enable, as the game does.
- **Give every stuck check a control case** that places a body inside a block and expects
  it to be caught. A check that has never failed may be blind.
- **Keep `Setup_DefaultSurfaceIsAvailable`.** If it ever fails, generated meshes can't
  build in tests on that engine build. Stop and report the route it prints.

## Expected results

On S&box `26.10.02` all five tests should pass, and `Setup_DefaultSurfaceIsAvailable`
should print the route `internal fallback: registered a stand-in default surface`.
`Setup_SavedSceneLoads` is inconclusive if the project has no `Assets/scenes/minimal.scene`.

## Results

Verified on 2026-10-12, on S&box `26.10.02` with .NET SDK `10.0.401` on Windows, in a new
**Game - Empty** project. The editor reported no compile errors.

| Run | Result |
|---|---|
| Clean | All 5 passed. The route was `internal fallback: registered a stand-in default surface`, and `Setup_SavedSceneLoads` passed on the template's `minimal.scene`. |
| Control, with `TestSurfaces.EnsureDefault()` commented out | 3 failed: `Setup_GeneratedMeshBuildsCollision` and both STARTER-SPAWN-01 tests. The test output showed only missing models. The runner listed `4x OnEnabled on Sandbox.MeshComponent failed`, at `Sandbox.ModelBuilder.AddSurface`, from the engine log. |
| Two runs started together | The second waited for the first. Both passed, each with its own engine log. |

- **Both shells.** Runs used Windows PowerShell 5.1 and PowerShell 7.
- **Start-up noise.** Every run logged 14 other error lines, passing ones included, such as
  missing shaders and mount plugins. The runner counts them separately from component errors.
- **A runner bug found and fixed first.** The first control run found it: in Windows
  PowerShell, dotnet's stderr stopped the script before it saved the engine log.

**Not covered:** other engine builds, projects that build their area with a real
generator, and saved scenes that reference prefabs or models.
