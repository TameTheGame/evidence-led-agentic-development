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
| `UnitTests/StarterTests.cs` | Five setup checks, and one requirement written as project tests should be: named after its check, with a control case that must fail |
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
   [Matching the engine source](#matching-the-engine-source). Set both for the user. The
   scripts read the user's values when a shell started before they were set.
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
| `NEAREST` | The installed hotfix has no tag yet, so the clone is at the nearest tagged release before it. |
| `UNKNOWN` | The install is a staging build, which has no public tag. |
| `NOT SYNCED` | The script left the clone where it was, with the reason. Most often the clone has local changes; read the release with `git show <tag>:<path>`. |
| `NOT CHECKED` | No install or clone was given. |

- **The runner calls it before each run** when `SBOX_PUBLIC` or `-Source` names the clone,
  and prints the result as its `Source:` line. Unless that line says `MATCH` or `SYNCED`,
  the runner ends with a `Warning:` line, because engine facts read from the clone may not
  match the engine that ran.
- **It changes nothing else in the clone.** It leaves branches alone and doesn't commit or
  push. The checkout is a detached HEAD; `git switch master` returns to the latest source.
- **Run it after anything that can update S&box,** such as a launch through Steam. A
  project can also run it at the start of each agent session.
- **Run it on a schedule too.** Steam updates S&box only when S&box starts, so a session
  that is already open doesn't see an update from a launch made by hand. An hourly Windows
  scheduled task closes that gap.
- **Have each agent session run it first,** so no agent has to remember to. In Claude Code,
  a `SessionStart` hook in the project's `.claude/settings.json` puts the line in the
  session's context:

  ```json
  {
    "hooks": {
      "SessionStart": [
        { "hooks": [ { "type": "command", "command": "powershell -NoProfile -File tools/sync_engine_source.ps1" } ] }
      ]
    }
  }
  ```

  It needs `FACEPUNCH_ENGINE` and `SBOX_PUBLIC` set for the user.

### A hotfix without a tag

Facepunch can ship a hotfix, such as `26.10.13a`, hours or days before it tags it in
`sbox-public`. Until the tag appears, the script checks out the nearest tagged release
before the hotfix, usually the release it patches, and prints `NEAREST`. Every later run
looks for the tag again and prints `SYNCED` once it is there.

While the line says `NEAREST`:

- **Say engine facts are approximate.** Cite the tag the line names, such as
  `26.10.13:<path>`, and say the installed hotfix may differ.
- **Suspect the hotfix when the source doesn't explain a result.** If an engine test fails
  in a way the nearest source can't explain, record that and check again once the tag
  appears.

### After a new release

When the line says `SYNCED`, the engine changed under the project:

- **Rerun the machine checks** before trusting earlier results: the engine tests, and the
  editor check if the project has one.
- **Recheck the engine facts the project relies on.** For each source path its notes or
  domain skill cite, read what changed with `git diff <old>..<new> -- <path>`.

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

All seven tests should pass, and `Setup_DefaultSurfaceIsAvailable` should print the route
`internal fallback: registered a stand-in default surface`. `Setup_SavedSceneLoads` and
`Setup_SavedSceneSimulates` are inconclusive if the project has no
`Assets/scenes/minimal.scene`. `Setup_SavedSceneKeepsMeshData` saves its own scene to a
temporary folder, so it runs in any project. It is inconclusive only if the engine's save
internals moved.

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

### Saved mesh data

Verified on 2026-10-18, on S&box `26.10.13a` with .NET SDK `10.0.401`, in a scratch game
project with the template's `minimal.scene`:

| Run | Result |
|---|---|
| Clean, in PowerShell 7 | All 7 passed. |
| Control, with `ReadSceneFile` ignoring the `_d` file, in Windows PowerShell | 1 failed: `Setup_SavedSceneKeepsMeshData`, with `ray missed the saved block`. The other 6 passed. |
| Clean again, in Windows PowerShell, after changing the restored file's date | All 7 passed. |
| A scene the Editor saved | A `run_csharp` script added a mesh block to a new scene, and `save_scene` wrote a `_d` file beside it. A test that loaded the scene with `LoadSavedScene` hit the block's top. With the control loader, the ray missed. |

**Not covered:** scene files in KeyValues3 form, which start with `<`. The Editor's reader
unwraps them (`26.10.13:engine/Sandbox.Tools/Scene/SceneSource.cs`, approximate for
`26.10.13a`); the starter's loader doesn't.

### Untagged hotfix and the runner's warning

Verified on 2026-10-18, with S&box `26.10.13a` installed and no `26.10.13a` tag in
`Facepunch/sbox-public` yet. Every script run used Windows PowerShell 5.1 and PowerShell 7.

| Run | Result |
|---|---|
| The script, on the real clone | `NEAREST` at `26.10.13`. The clone had no changes, and `master` didn't move. |
| A throwaway repository | With only `26.10.13` tagged, an installed `26.10.13a` gave `NEAREST` and moved the clone there; a rerun said it was already there. Once `26.10.13a` was tagged, `SYNCED`. An installed `26.10.13b` gave `NEAREST` at `26.10.13a`. A missing `26.10.20` gave `NOT SYNCED` with `origin has no tag 26.10.20 yet`. Local changes gave `NOT SYNCED` on the release path and the nearest-tag path, and left the clone and the change alone. |
| The `SessionStart` hook | In a scratch project with the hook above, and `SBOX_PUBLIC` set for that session, `claude -p --setting-sources project,local` quoted the `NEAREST` line from its context. Without the hook, it found no such line. |
| The runner, with `FACEPUNCH_ENGINE` and `SBOX_PUBLIC` cleared in the shell | It found the install through the user's `FACEPUNCH_ENGINE`. `NOT CHECKED`, with no clone and with a folder that isn't a clone, ended with the `Warning:` line, and so did `NEAREST` on the real clone. `MATCH` and `SYNCED`, on throwaway clones at and behind the installed tag, didn't. |

**Not covered:** the user-level `SBOX_PUBLIC` fallback, because the test machine doesn't set
it for the user, and a hotfix tag appearing on GitHub.
