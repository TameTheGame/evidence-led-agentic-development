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
| `UnitTests/StarterTests.cs` | Four setup checks, and one requirement written as project tests should be: named after its check, with a control case that must fail |
| `tools/run_engine_tests.ps1` | Runs the tests and saves the engine's own log with the results, because engine errors appear only there |
| `tools/sync_engine_source.ps1` | Moves a local clone of `Facepunch/sbox-public` to the release that is installed, so agents read the source of the engine they run. The runner calls it first. |

## Using it

1. **Use a code project.** S&box generates a test project only for `game`, `library`, and
   `addon` projects. A `content` (map) project needs a small companion code project.
2. **Copy the starter in.** Copy `UnitTests\` into the project root, next to the `.sbproj`,
   and copy both scripts in `tools\` into the project's `tools\`.
3. **Generate the test project.** Open the project in the S&box Editor, check the console
   for compile errors, and close it. S&box generates `UnitTests\<project>.unittest.csproj`.
4. **Set up the machine.** Rung 1 needs Windows, the .NET 10 SDK (`dotnet --list-sdks` must
   show `10.x`), and `FACEPUNCH_ENGINE` set to the S&box install folder, the one containing
   `sbox-dev.exe`. If agents read engine source from a local clone of
   `Facepunch/sbox-public`, also set `SBOX_PUBLIC` to that clone; see
   [Matching the engine source](#matching-the-engine-source).
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

## Matching the engine source

Agents read engine source from a clone of `Facepunch/sbox-public`, but they run the engine
Steam installed, and the two drift apart. Facepunch tags each public Steam release in that
repository, such as `26.10.02`, or `26.07.08b` for a hotfix. The install names its release
on the first line of its `.version` file.

`tools/sync_engine_source.ps1` reads that release and checks the matching tag out in the
clone, fetching the tag first if the clone lacks it. It prints one line and always exits 0:

| Line | Meaning |
|---|---|
| `MATCH` | The clone is already at the installed release. |
| `SYNCED` | The script moved the clone to the installed release. Engine facts read earlier may be stale. |
| `UNKNOWN` | The install is a staging build, which has no public tag. |
| `NOT SYNCED` | The script left the clone where it was, with the reason. Most often the clone has local changes; read the release with `git show <tag>:<path>`. |
| `NOT CHECKED` | No install or clone was given. |

- **The runner calls it before each run** when `SBOX_PUBLIC` or `-Source` names the clone,
  and prints the result as its `Source:` line.
- **It changes nothing else in the clone.** It leaves branches alone and doesn't commit or
  push. The checkout is a detached HEAD; `git switch master` returns to the latest source.
- **Run it after anything that can update S&box,** such as a launch through Steam. A
  project can also run it at the start of each agent session.
- **Run it on a schedule too.** Steam updates S&box only when S&box starts, so a session
  that is already open doesn't see an update from a launch made by hand. An hourly Windows
  scheduled task closes that gap.

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

All six tests should pass, and `Setup_DefaultSurfaceIsAvailable` should print the route
`internal fallback: registered a stand-in default surface`. `Setup_SavedSceneLoads` and
`Setup_SavedSceneSimulates` are inconclusive if the project has no
`Assets/scenes/minimal.scene`.

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

### Saved scenes that simulate

Verified on 2026-10-17, on S&box `26.10.13a` (Steam build 25964806) with .NET SDK
`10.0.401`, in a new project made from the new-game template:

| Run | Result |
|---|---|
| Clean | All 6 passed. |
| Control, with `LoadSavedScene` calling `scene.Load( file )` as before | 1 failed: `Setup_SavedSceneSimulates`, on its check that the scene had finished loading. The other 5 passed. |
| Clean again | All 6 passed. |

- **A copied file can hide a change.** `dotnet test` rebuilds only when a source file is
  newer than the last build. Restoring the fixed file by copying kept its old date, so the
  first rerun still used the control build and failed. It passed once the file's date
  changed.

### Source check

Verified on the same day, on a shallow clone of `Facepunch/sbox-public` that was on
`master`, 74 commits past `26.10.02`:

| Run | Result |
|---|---|
| The script, on the real clone | `SYNCED`: it checked out `26.10.02` in under a second. `master` stayed where it was, and the clone had no changes. |
| The script again | `MATCH`. |
| The runner, in both shells | All 5 tests passed in each shell, and the `Source:` line read `SYNCED` when the clone started on `master` and `MATCH` otherwise. `SBOX_PUBLIC` ended in a backslash for one run. |
| A throwaway repository, in both shells | It fetched a tag the clone lacked, including a hotfix tag. It reported `UNKNOWN` for a staging version and `NOT SYNCED` for a missing tag, for local changes, and for a fetch that timed out, and left the clone where it was each time. The timeout left no git process running. Two runs started together gave one `SYNCED` and one `MATCH`. A clone path with a space, a trailing backslash, or a relative form worked. |

On 2026-10-14 an hourly Windows scheduled task ran the script through `conhost --headless`,
so no window opened. It printed `MATCH`, and the task returned 0.

**Not covered:** fetching a real new release from GitHub, because none had shipped yet.
