# Example: an S&box map

> **Target-specific and non-normative.** This shows the spec format and the evidence ladder
> applied to a small game map on S&box (Facepunch, Source 2). The outpost is synthetic.

| Path | What it is |
|---|---|
| [`outpost.spec.md`](outpost.spec.md) | A worked spec, with a layout data file, requirements at each rung, owner cards, and a rung-1 test sketch |
| [`engine-rung-spike/`](engine-rung-spike/README.md) | A runnable kit that proved rung 1 works for a project's own tests, with results from seven runs |
| [`rung1-starter/`](rung1-starter/README.md) | A copyable starting point for a project's engine tests: the default-surface scaffolding, helpers, a requirement test with its control, a runner that keeps the engine log, and a script that keeps a local `sbox-public` clone on the installed release |
| [`skills/sbox-engine-reference/`](skills/sbox-engine-reference/SKILL.md) | An example of a project's domain skill: verified S&box behavior and where to look in the engine source. Tested in the [domain-skill test](../../skills/evidence/SBOX_SKILL_TEST.md) |
| [`tools/compile_check.ps1`](tools/compile_check.ps1) | A rung-0 check that compiles `run_csharp` scripts against the installed engine's assemblies without starting S&box. See [The compile check](#the-compile-check) |
| [`tools/editor_check.ps1`](tools/editor_check.ps1) | A rung-2 check that runs unattended: it saves a scene in the Editor, closes it, reopens it, and checks that nothing changed, with a screenshot from a fixed camera before and after. Needs S&box `26.10.13` or later. See [The editor check](#the-editor-check) |
| [`tools/spec_lint.py`](tools/spec_lint.py) | A rung-0 spec lint: format and card checks that fail the run, a lookup that reports checks not found in the test and script folders, and an owner gate that reports any change to an agreed requirement since the last commit. Run `python tools/test_spec_lint.py` to check it against its fixtures. |

## The ladder for a map

| Rung | Example check |
|---|---|
| **0 · static** | The layout data is valid, spawn IDs are unique, and the saved `.scene` JSON has exactly one main camera. The project's code and its `run_csharp` scripts compile against the installed engine. |
| **1 · engine** | A `UnitTests/` project starts the engine through `TestAppSystem` and builds the area with the same generator code. It then checks collision, spawn grounding, and route traces. |
| **2 · editor** | The generated scene survives save, close, and reopen unchanged. A screenshot from a fixed camera. |
| **3 · session** | A remote client sees and collides with the same walls. Same-machine host and client is not clean-client proof. |
| **4 · owner** | Walking from spawn to gate to tower feels like a frontier outpost. |

## What the spike settled

The spike ran on S&box `26.10.02`. Source references are to `Facepunch/sbox-public` at
`3915f1a69810026e23d331581266636de89411d5`. On that build, headless project tests can check
collision, traces, spawn landing, and stuck detection against generated geometry.

1. **Tests need a code project.**
   - S&box generates a `UnitTests` project only for `game`, `library`, and `addon`
     projects (`Project.Solution.cs`).
   - A `content` map needs a small companion code project to host its rung-1 tests. That
     point comes from the source; the spike didn't create a content project.
2. **Generated meshes need a default physics surface.**
   - Building any `PolygonMesh` throws in `ModelBuilder.AddSurface` when no `default`
     surface is loaded, and headless tests load none.
   - No public API provides one on this build.
   - The kit's `TestSurfaces` registers a stand-in through reflection, as Facepunch's own
     tests do. It is labelled test scaffolding and may break on an engine update.
3. **Stuck checks need more than `StartedSolid`.**
   - Mesh collision is a surface with no interior, and traces don't see its faces from
     behind.
   - The kit's enclosure probe, which uses only public trace calls, detects a body wholly
     inside a closed mesh.
4. **Saved scenes load from their JSON.**
   - `Scene.LoadFromFile` fails headlessly.
   - Reading the `.scene` file through `SceneFile.LoadFromJson` and `Scene.Load` works, and
     its box collider is traceable.
   - Found later, on `26.10.13a`: a scene with editable meshes or terrain keeps their data
     in a `<scene>_d` file beside it. `LoadFromJson` drops that data, so those meshes load
     empty and traces pass through them. The starter's loader reads the `_d` file through
     the internal `SceneFile.FromSource` the editor uses
     (`26.10.13:engine/Sandbox.Tools/Scene/SceneSource.cs`, approximate: `26.10.13a` has
     no source tag yet), and `Setup_SavedSceneKeepsMeshData` checks it.
5. **Rung 1 is Windows-only.** It needs the installed engine (`FACEPUNCH_ENGINE`) and the
   .NET 10 SDK. Cloud or Linux agents can run rung 0 only.

Still open: saved scenes that reference prefabs or collision models, and generated geometry
saved into a scene. See the [roadmap](../../ROADMAP.md).

## The compile check

A `run_csharp` script is the body of an async method, not a C# file, so nothing compiles it
until the Editor runs it. `tools/compile_check.ps1` wraps each script the way `run_csharp`
does and builds it against the installed engine's assemblies, without starting S&box:

```powershell
powershell -File tools\compile_check.ps1 -Scripts tools\place_player.cs
```

- **It proves names, not behavior.** A pass means every type, member, and signature the
  script uses exists in the installed build. It runs nothing, so it is a rung-0 check.
- **It needs the dev machine, but only for seconds.** It reads
  `<engine>\bin\managed\*.dll` and needs the .NET 10 SDK. It starts nothing, so run it
  before any check that starts the engine or the Editor.
- **Errors point at the script.** Each error names the script's own file and line.
- **The project's own code compiles through its test project.** `dotnet build UnitTests`
  builds the code and the tests S&box generated, without starting the engine.

Verified on S&box `26.10.13a`, in Windows PowerShell 5.1 and PowerShell 7. A script using
engine and editor APIs passed in about two seconds. The same script with one misspelled
member failed with `CS1061` at the script's own file and line. A script calling a helper
class passed with `-Include` on the helper's folder and failed without it. A script using a
component whose code calls `Log` passed with `-Include` on that `Code` folder. A wrong
`-Engine` stopped with `NOT RUN` and exit 2. No S&box process started during these runs or
during `dotnet build UnitTests`. The first run found that a script using `Log` failed, because
`run_csharp` also brings in the game's global names
(`26.10.13:engine/Sandbox.Engine/Systems/Mcp/ScriptTools.cs`, approximate for `26.10.13a`).
The check now does too, for scripts and for included code, as a project's own build does.

## The editor check

S&box `26.10.13` added `sbox-cli`, which agents use to drive the Editor over a local named pipe.
It replaced the Editor's built-in HTTP server on port 7269. With it, rung 2 runs unattended,
so the example's save-and-reopen requirement no longer needs an owner card.

From the project root, with the project closed in every editor:

```powershell
powershell -File tools\editor_check.ps1 -Scene scenes/outpost.scene
```

- **It owns its editors.** It opens the project in an editor that `sbox-cli` owns, so the
  editor closes if the script stops. It refuses to run while another editor has the project
  open.
- **What fails it.** It saves the scene, quits, reopens it, and fails on:
  - unsaved changes as soon as the scene opens;
  - error-level console lines on reopen;
  - any saved object whose name, parent, enabled state, or components changed; or
  - a second save that doesn't write a byte-identical file.
- **Saves are forced.** The Editor skips a save when nothing changed, so the script adds a
  marker object and undoes it first. The content stays the same, and the Editor writes the
  scene out from what it loaded.
  - Setting the session's `HasUnsavedChanges` to true would force a save too; it has a
    public setter (`26.10.13:engine/Sandbox.Tools/Scene/Session/SceneEditorSession.cs`).
    But only `run_csharp` can set it, and this check uses `sbox-cli`'s own tools. A build
    script that already runs through `run_csharp` may find the setter simpler. That is
    from the source and untested.
- **A project without code works too.** A project with code must report a finished,
  successful compile. A content project, such as a map, has no `Code` or `Editor` folder
  and never compiles, so the check doesn't wait for a compile result.
- **The screenshot is a record.** `-Camera` and `-Angles` fix the view. The script reports
  how much the two captures differ but doesn't score it, because the byte-identical save
  already proves the scene came back unchanged.
- **It leaves no trace.** It puts the scene file back as it was, and saves results in
  `test-results\editor-<time>\`: both captures, both saved files, the object lists, and the
  console errors.
- **It keeps each editor's own account.** It saves the output of the `sbox-cli` process that
  owns each editor, and the editor log from `<engine>\logs\`, with the results. On a failure
  it prints the last lines of both, so a failed start says why.
- **Steam must be running.** S&box starts through Steam. The check stops with `NOT RUN`
  when Steam isn't running, and doesn't start it, because a Steam start can update S&box.

Verified on S&box `26.10.13`, in Windows PowerShell 5.1 and PowerShell 7. A scratch scene
passed in about a minute. A control scene with a component that changes its own saved value
each time it loads failed on the second save, and passed once that object was removed.

On `26.10.13a`, a content project with no `Code` or `Editor` folder passed in both shells.
The previous version of the script stopped on it with `NOT RUN: the project has 0 compile
error(s)`. A new project made from the new-game template passed too.

Also verified on `26.10.13a`, in both shells: a scratch scene passed in about a minute, and
its results held both editors' `sbox-cli` output and editor logs. The Editor writes its log
to `<engine>\logs\sbox-dev.log` and keeps earlier ones under dated names. With
`-TimeoutSeconds 5`, the check failed with `the editor wasn't ready`, printed the last lines
of both files, and left no S&box process. Steam stayed open throughout, so the `NOT RUN`
branch for a closed Steam was read, not run.

## A map with no code

A first real project kept its map in a content project, with no code of its own. On S&box
`26.10.13a` it found:

- **Engine tests run from a companion code project.** S&box generates no test project for a
  content project (point 1 under [What the spike settled](#what-the-spike-settled)). A
  small game project's tests read the map's saved scene from its file and passed.
- **Play the map in its own editor.** A content project can't run as a game, but its
  editor has play mode. Nothing in the map spawns a player, so the project's play check
  starts play mode with `sbox-cli`'s `play_start`, then runs a committed `run_csharp`
  script that places a `PlayerController` at a spawn point and checks it lands.
  - The script stops unless `Game.IsPlaying` is true and `Game.ActiveScene` isn't the
    editor scene, because `run_csharp` has no undo.
  - Checking the scene alone isn't enough: outside play mode, `Game.ActiveScene` can be an
    empty runtime scene.
- **Another local project can't load the map yet.** The Editor loads the open project, the
  library projects in that project's own `Libraries\` folder
  (`26.10.13:engine/Sandbox.Tools/Editor/LibrarySystem/LibrarySystem.cs`), and built-in
  content. A reference to another local project, such as `local.outpost`, finds only
  packages already loaded
  (`26.10.13:engine/Sandbox.Engine/Services/Packages/PackageManager/PackageManager.cs`).
  - So a separate game project can't use the map's files through a package reference.
  - Placing the map in the game's `Libraries\` folder wasn't tested.
  - Testing the map inside a game is a later requirement, with its own check.
