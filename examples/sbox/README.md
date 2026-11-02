# Example: an S&box map

> **Target-specific and non-normative.** This shows the spec format and the evidence ladder
> applied to a small game map on S&box (Facepunch, Source 2). The outpost is synthetic.

| Path | What it is |
|---|---|
| [`outpost.spec.md`](outpost.spec.md) | A worked spec, with a layout data file, requirements at each rung, owner cards, and a rung-1 test sketch |
| [`engine-rung-spike/`](engine-rung-spike/README.md) | A runnable kit that proved rung 1 works for a project's own tests, with results from seven runs |
| [`rung1-starter/`](rung1-starter/README.md) | A copyable starting point for a project's engine tests: the default-surface scaffolding, helpers, a requirement test with its control, a runner with a time limit that reads each test's outcome and keeps the engine log, and a script that keeps a local `sbox-public` clone on the installed release |
| [`skills/sbox-engine-reference/`](skills/sbox-engine-reference/SKILL.md) | An example of a project's domain skill: verified S&box behavior and where to look in the engine source. Tested in the [domain-skill test](../../skills/evidence/SBOX_SKILL_TEST.md) |
| [`tools/compile_check.ps1`](tools/compile_check.ps1) | A rung-0 check that compiles `run_csharp` scripts against the installed engine's assemblies without starting S&box. See [The compile check](#the-compile-check) |
| [`tools/editor_check.ps1`](tools/editor_check.ps1) | A rung-2 check that runs unattended: it saves a scene in the Editor, closes it, reopens it, and checks that nothing changed, with a screenshot from a fixed camera before and after. Needs S&box `26.10.13` or later. See [The editor check](#the-editor-check) |
| [`tools/package_ids.cs`](tools/package_ids.cs) | The `run_csharp` script the editor check runs after each save, to read the IDs that editor session gives the store package files a scene uses. Copy it with the check. |
| [`IMPORTING.md`](IMPORTING.md) | The import reference: what works and what doesn't when bringing Source and other old content into S&box, sorted by topic, each entry with the S&box version it was checked on |
| [`tools/spec_lint.py`](tools/spec_lint.py) | A rung-0 spec lint: format and card checks that fail the run, a lookup that reports checks not found in the test and script folders, and an owner gate that reports any change to an agreed requirement since the last commit. Run `python tools/test_spec_lint.py` to check it against its fixtures. |
| [`tools/scene_refs.py`](tools/scene_refs.py) | A rung-0 check for clearing out generated files, such as old light bakes: it lists each file in a folder as in use or unused by the project's scenes and prefabs, and fails when one of them references a file that isn't there. See [Clearing out generated files](#clearing-out-generated-files). Run `python tools/test_scene_refs.py` to check it against its fixtures. |
| [`tools/check_metas.py`](tools/check_metas.py) | A rung-0 check that every file Git tracks under the assets folder has the `.meta` S&box writes for it, tracked beside it, with names compared in any letter case. Run it from the project's root before an editor run, so a missing `.meta` fails here and not in the run. See [More world-build lessons](#more-world-build-lessons). Run `python tools/test_check_metas.py` to check it on throwaway Git repositories. |

## The ladder for a map

| Rung | Example check |
|---|---|
| **0 · static** | The layout data is valid, spawn IDs are unique, and the saved `.scene` JSON has exactly one main camera. The project's code and its `run_csharp` scripts compile against the installed engine. |
| **1 · engine** | A `UnitTests/` project starts the engine through `TestAppSystem` and builds the area with the same generator code. It then checks collision, spawn grounding, and route traces. |
| **2 · editor** | The generated scene survives save, close, and reopen unchanged. A screenshot from a fixed camera. |
| **3 · session** | A remote client sees and collides with the same walls. Same-machine host and client is not clean-client proof. Until the game is published, host from the Editor; see [Lessons from a world build](#lessons-from-a-world-build). |
| **4 · owner** | Walking from spawn to gate to tower feels like a frontier outpost. |

**Check motion on the screen, not only in logs.** Positions a game logs each frame can be
smooth while the picture isn't. On `26.10.13a`, three in-game measurements said a lift
moved smoothly while a player riding it saw it judder, and a 60 fps recording of the game
window showed the judder at once. The cause is in the
[import reference](IMPORTING.md#map-logic-and-entities). So check motion a player sees by
recording the game window and measuring how far the picture moves from frame to frame: a
strip of the picture that shifts by uneven steps shows the beat. On Windows, FFmpeg's
`gfxcapture` source, in FFmpeg 8.1 and later, records one window, and it kept recording the
game while other windows covered it. It returns frames as fast as the compositor gives
them, up to its `max_framerate`
([FFmpeg filters](https://ffmpeg.org/ffmpeg-filters.html#gfxcapture)).

A check on a recording's size has to read the screen's real size. On Windows, a process
that isn't DPI aware is told the screen's size in 96 DPI units
([High DPI Desktop Application Development on Windows](https://learn.microsoft.com/en-us/windows/win32/hidpi/high-dpi-desktop-application-development-on-windows)),
so a 3840 x 2160 monitor at 150% scaling reads as 2560 x 1440, and a check for a full 4K
recording compares against the wrong size. Set the thread that reads the screens
per-monitor DPI aware (version 2), for example with `SetThreadDpiAwarenessContext`, so it
sees each display's raw pixels, and check what it reads against the video card's real
resolution. This was seen on Windows while building a check that a recording is 3840 x
2160.

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
- **It doesn't run S&box's code generator.** The Editor's compile rewrites some code before
  it compiles it, and a build outside S&box doesn't. So code that this check or
  `dotnet build UnitTests` passes can still fail to compile in the Editor. That is read
  from the source, not run. The [import reference](IMPORTING.md#tools-and-scripting) has
  the case found so far: a property initializer the generator copies into an attribute.

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
- **The project must leave its AI setting on.** An editor opens the pipe `sbox-cli` uses
  only when the project's `.sbproj` doesn't set `AI.EnableMcpCommunication` to `false`.
  With it off, the check stops with `NOT RUN` before it starts an editor, since `sbox-cli`
  would only wait out its start-up timeout. `-SelfTest` checks this reading on planted
  `.sbproj` text, including a planted fault: the setting turned off. The block, and where
  S&box writes it, are in the [starter's set-up](rung1-starter/README.md#using-it).
- **What fails it.** It saves the scene, quits, reopens it, and fails on:
  - unsaved changes as soon as the scene opens;
  - error-level console lines on reopen;
  - any saved object whose name, parent, enabled state, or components changed; or
  - a second save that differs from the first in any byte but a store package's ID, and
    then only an ID that its own session gave that path.
- **Saves are forced.** The Editor skips a save when nothing changed, so the script adds a
  marker object and undoes it first. The content stays the same, and the Editor writes the
  scene out from what it loaded.
  - Setting the session's `HasUnsavedChanges` to true would force a save too; it has a
    public setter (`26.10.13:engine/Sandbox.Tools/Scene/Session/SceneEditorSession.cs`).
    But only `run_csharp` can set it, and this check makes its edits with `sbox-cli`'s own
    tools. A build script that already runs through `run_csharp` may find the setter
    simpler. On `26.10.13a`, a `run_csharp` script that set it at its end, followed by
    `save_scene`, wrote the scene; the file's new timestamp and contents showed it.
- **It sets store package IDs aside, one at a time.** S&box can give a package's files new
  IDs in each editor session, and then the second save writes other `Id`s for them; see
  [More world-build lessons](#more-world-build-lessons). After each save the check runs
  `tools/package_ids.cs` through `run_csharp`. For each `{"Id", "Path"}` reference in the
  saved scene whose path is a store package's file, it returns the ID that session gives
  the path. A save passes if it is byte-identical, or if it differs only in such
  references' IDs, each exactly the ID its own session gave. A stale ID, a project asset's
  changed ID, a changed path, or any other changed byte, line endings included, still
  fails it. If the script can't run, the check notes why and compares the IDs as written.
  `-SelfTest` checks this comparison on planted saves, without S&box, including a planted
  break: a changed object name beside new package IDs.
- **A project without code works too.** A project with code must report a finished,
  successful compile. A content project, such as a map, has no `Code` or `Editor` folder
  and never compiles, so the check doesn't wait for a compile result.
- **The screenshot is a record.** `-Camera` and `-Angles` fix the view. The script reports
  how much the two captures differ but doesn't score it, because the resave check already
  proves the scene came back unchanged.
- **It leaves no trace.** It puts the scene file and the project's `.sbproj` back as they
  were, and saves results in `test-results\editor-<time>\`: both captures, both saved
  files, both sessions' package IDs, the object lists, and the console errors. The Editor
  can rewrite the `.sbproj` when it starts; see
  [Lessons from a world build](#lessons-from-a-world-build).
- **It keeps each editor's own account.** It saves the output of the `sbox-cli` process that
  owns each editor, and the editor log from `<engine>\logs\`, with the results. On a failure
  it prints the last lines of both, so a failed start says why.
- **Steam must be running.** S&box starts through Steam. The check stops with `NOT RUN`
  when Steam isn't running, and doesn't start it, because a Steam start can update S&box.
- **A failed start stops it in seconds.** When S&box can't start the project, it shows an
  error box and waits for a click; see [When S&box can't start a project](#when-sbox-cant-start-a-project).
  While the check waits for an editor, it looks for that box and for the failure in the
  editor log. On either, it saves the box's text to `error-box.txt`, closes the editor and
  the box with it, and stops with `NOT RUN` and the error's own words. If a call fails
  later while the editor shows a box, the check records the box the same way.

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

On `26.10.27c`, in both shells, in a scratch project: a scene with no store package
passed byte-identical. So did a scene with a model from a store package, installed with
`install_package` and placed with `spawn_model` in an earlier session: the model kept the
same `Id` in all five sessions run, so the compare never had a package ID to set aside, and
only the planted saves in `-SelfTest` exercise that part. `package_ids.cs` ran after each
save and read the scene's ten references without an error. The same scene plus a component
that changes its own saved value each time it loads failed with `the second save differs
from the first in more than store package IDs`. Each run left the scene and the `.sbproj`
as they were.

## When S&box can't start a project

If the Editor fails while it starts, it logs the exception, shows a native error box such
as "Bootstrap::Init Error", and waits there until someone clicks OK. Only then does it exit
(`26.10.13:engine/Sandbox.Engine/Core/Bootstrap.cs`, lines 331-348, and lines 113-127 for a
failure earlier in the start). It opens the pipe `sbox-cli` talks to only after the project
has loaded (lines 282-286 and 316-323), so nothing an agent sends reaches it. On
`26.10.13b`, editors that agents started left this box on the owner's desktop for minutes,
and one agent's work stopped until the owner clicked OK.

- **What sets it off.** Any exception while the Editor loads the project. On `26.10.13b` it
  was the parent game. An addon project loads its `ParentPackage` at start
  (`26.10.13:engine/Sandbox.Tools/StartupLoadProject.cs`, lines 149-156), and a remote game
  that comes with neither compiled code nor code archives throws "This game has no
  precompiled assemblies or code archives!"
  (`26.10.13:engine/Sandbox.Engine/Services/Packages/PackageManager/PackageManager.cs`,
  lines 114-127). Facepunch's Sandbox package came that way, so no addon of Sandbox could
  open, and pinning an older revision didn't help. A parent package that doesn't exist
  throws too (lines 77-80). When the project has compile errors, the box lists them in
  place of the exception (`Bootstrap.cs`, lines 335-341). A `.sbproj` that S&box can't read
  shows a "Couldn't open project" box before any of this
  (`26.10.13:engine/Sandbox.AppSystem/EditorAppSystem.cs`, lines 38-51). A library's
  `.sbproj` that isn't valid JSON marks that project broken
  (`26.10.13:engine/Sandbox.Engine/Systems/Project/Project/Project.cs`, lines 202-225), and
  adding it from the project's `Libraries` folder then throws "Couldn't add project."
  (`26.10.13:engine/Sandbox.Engine/Systems/Project/Project/Project.Static.cs`, lines
  266-277; `26.10.13:engine/Sandbox.Tools/Editor/LibrarySystem/LibrarySystem.cs`, lines
  21-40). On `26.10.27c` that showed as a "Bootstrap::Init Error" box. A static check that
  parses every tracked `.sbproj` as strict JSON catches both before an editor opens.
- **Start every editor so that a failed start can't hang.**
  1. Start it through `sbox-cli --project`, or a script that does, and keep that `sbox-cli`
     process. It starts the editor inside a Windows job that closes the editor, box and
     all, when `sbox-cli` exits or its input closes
     (`26.10.13:engine/Launcher/SboxCli/OwnedProcess.cs`, line 30;
     `26.10.13:engine/Launcher/SboxCli/Program.cs`, lines 94-97 and 169-188). It also gives
     up after `--startup-timeout`, 180 seconds by default (`Program.cs`, lines 193-221;
     `26.10.13:engine/Launcher/SboxCli/Options.cs`, line 39). An editor started any other
     way, such as with `Start-Process sbox-dev.exe`, has neither and waits on the box for
     good.
  2. While you wait for the editor, watch for the failure, not only the clock. Look for a
     visible dialog box (window class `#32770`) that belongs to the editor's process, and
     for an entry in `<engine>\logs\sbox-dev.log` whose stack ends in
     `Sandbox.Engine.Bootstrap.Init` or `PreInit`, where the exception was caught. Read
     only entries written after the start: the last run's log stays in place until the new
     editor starts logging (`26.10.13:engine/Sandbox.System/Logging/Logging.cs`, lines
     35-60). The box can come without such an entry, as "Couldn't open project" does, so
     watch for both.
  3. On either, save the box's text, close the editor, which takes the box with it, and
     report the error's own words. Retry only once the cause has changed. When it is a
     package from the cloud, the fix is Facepunch's.

  The [editor check](#the-editor-check) does all three, so a failed start costs it seconds,
  not its whole timeout. A game or dedicated server started for a check goes through the
  same `Bootstrap`, and logs to `sbox.log` or `sbox-server.log`, after its process name.

Checked on S&box `26.10.13b`, in Windows PowerShell 5.1 and PowerShell 7, with two scratch
projects that can't start. An addon whose `ParentPackage` doesn't exist shows "Bootstrap::Init
Error", and a project whose `.sbproj` isn't valid JSON shows "Couldn't open project". Each
time, the editor check stopped with `NOT RUN` within a minute, named the box and the error,
saved `error-box.txt`, and left no S&box process. A project made from S&box's own template
still passed. The source is read at `26.10.13`, which is approximate for `26.10.13b`.

## Throwaway projects

Opening a project in the Editor adds it to S&box's project list,
`<engine>\config\addons.json`, where S&box finds its recent projects, such as those on the
Editor's taskbar jump list (`26.10.13:engine/Sandbox.Tools/StartupLoadProject.cs`, lines
65-76; `26.10.13:engine/Sandbox.Tools/TaskbarJumpList.cs`, lines 20-36). Each entry names
the project's `.sbproj` under `Path`
(`26.10.13:engine/Sandbox.Engine/Systems/Project/Project/Project.cs`, lines 22-23). Nothing
takes an entry off while its folder is there. Once the folder is gone, S&box skips the entry
when it reads the list, and drops it from the file the next time it saves the list, which
it does each time the Editor opens a project (`26.10.13:engine/Sandbox.Tools/ProjectList.cs`,
lines 14-31). So scratch projects that agents open for checks and experiments pile up in the
owner's list. On `26.10.13b`, a project made for a check stayed in the list after the check,
and left it only once its folder was deleted and a later Editor start saved the list.

When a throwaway project is done:

1. Copy out anything worth keeping, such as its `test-results\` folder.
2. Close it, and make sure no S&box process is running, because S&box writes the list
   each time it opens a project.
3. Delete its folder. If the folder has to stay, remove its entry from `addons.json`
   instead, the one whose `Path` is its `.sbproj`, still with no S&box running.

A script or recipe that makes throwaway projects does this at its end, or says which
projects it leaves.

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

## Clearing out generated files

S&box writes light, envmap and navmesh bakes into a folder beside the scene,
`<scene>_scene_data/`
(`26.10.13:engine/Sandbox.Tools/Scene/Session/SceneEditorSession.cs`, lines 593-625;
`26.10.13:engine/Sandbox.Engine/Scene/Components/Light/EnvmapProbe.Baking.cs`, line 22;
`26.10.13:engine/Sandbox.Engine/Game/Navigation/NavMesh.Baking.cs`, lines 50-59). Each
light bake adds new files and leaves the old ones, so the folder grows. When Git doesn't
track the folder, a clean-up that takes a file still in use can't be undone, and getting
it back means baking again. A first real project lost its current light bake this way:
its clean-up compared the scene's references with the file names exactly, but the scene
stores them lower-cased and without `_c`
([the import reference](IMPORTING.md#tools-and-scripting) has the detail). To clear such
a folder out:

1. Make sure nothing still writes to the folder. After a `sbox-cli` call that timed out,
   check that it has finished: it keeps running in the editor. If the open scene holds a
   bake you want to keep, save it first. The check below reads saved files only, so the
   files of an unsaved bake show as unused.
2. Run [`tools/scene_refs.py`](tools/scene_refs.py) on the folder, such as
   `python tools/scene_refs.py Assets/scenes/outpost_scene_data/ddgi`. It reads every scene
   and prefab and lists each file in the folder as `IN USE` or `UNUSED`, comparing paths
   the way S&box does. Before you trust the list, check that the newest bake is `IN USE`.
3. Move only the `UNUSED` files, to a folder outside `Assets/`. Don't delete them yet.
4. Reopen the scene, read the editor log for files it can't find, and run `scene_refs.py`
   again. It fails when a scene or prefab references a file that isn't there. If anything
   fails, move the files back.
5. Then delete the moved files.

`python tools/test_scene_refs.py` checks the tool on a throwaway project laid out the same
way. Its controls delete a file the scene uses and a file a prefab uses, and the tool fails
both times.

## Lessons from a world build

The same project's world work on S&box `26.10.13a` turned up fourteen more. Each is read
from the engine source at `26.10.13`, which is approximate for `26.10.13a`.

- **Read scene-load errors from editor start.** The Editor loads its startup scene before a
  check can mark the log, and opening a scene that is already open logs nothing new. So a
  check that reads the console only after a mark, or only after opening the scene, misses
  load errors. `read_console` keeps the last 2,000 events from editor start
  (`26.10.13:engine/Sandbox.Engine/Systems/Mcp/LogBuffer.cs`). The editor check reads that
  buffer without a `since` cursor, so it sees them. A start that logs more than 2,000 events
  would push the earliest out; the editor log saved with the results keeps everything.
- **Don't end a scene string in a file extension.** When S&box compiles a scene, it treats
  any string value that ends in a known asset extension as a file reference
  (`26.10.13:engine/Sandbox.Tools/Assets/ResourceCompile/ResourceCompileContextImp.cs`,
  lines 252-290). An object named `outpost.terrain` makes S&box look for a compiled
  `outpost.terrain_c` that doesn't exist. Keep object names free of such endings, or have
  the layout lint reject them.
- **Check the `.sbproj` out the way S&box writes it.** Each time the Editor opens a project,
  it writes the project's `.sbproj` again if the file's text differs from what S&box would
  write (`26.10.13:engine/Sandbox.Tools/StartupLoadProject.cs`, line 190;
  `26.10.13:engine/Sandbox.Tools/Utility/Utility.Projects.cs`, line 12;
  `26.10.13:engine/Sandbox.Engine/Systems/Project/Project/Project.cs`, lines 395-420). On
  Windows it writes CRLF line endings. So a `.sbproj` that Git checks out with LF endings is
  rewritten on every editor start, and `git status` then lists it as modified though
  `git diff` shows nothing. A check that needs a clean working tree fails.
  - When line endings are the only difference, checking the file out with CRLF endings
    (`*.sbproj text eol=crlf` in `.gitattributes`) stops the rewrite.
  - Otherwise, put the file back after each editor run. The editor check does this, as it
    does for the scene.
- **A dedicated server reaches outside the project.** It always logs on to Steam and
  advertises itself on Steam's server list while it runs. A hidden setting only adds a tag
  that server browsers can filter on
  (`26.10.13:engine/Sandbox.Engine/Systems/Networking/System/GameNetworkSystem/GameNetworkSystem.Static.cs`,
  lines 246-366). So an agent-run dedicated-server check is an external effect, and it
  belongs on the owner's ask-first list, unlike the project's other checks.
- **A dedicated server can't host an unpublished game.** A client joining a dedicated server
  looks up the game's package, and a `local.` game has none, so the join fails
  (`26.10.13:engine/Sandbox.Engine/Services/Packages/Package.Static.cs`, lines 153-157;
  `26.10.13:engine/Sandbox.GameInstance/GameInstance.cs`, lines 181-186). An Editor host is
  a developer host
  (`26.10.13:engine/Sandbox.Engine/Systems/Networking/System/NetworkSystem.cs`, line 49) and
  tells joining clients so, and they skip that lookup
  (`26.10.13:engine/Sandbox.Engine/Systems/Networking/System/NetworkSystem.Handshake.cs`,
  line 73). So the session rung for an unpublished game runs against an Editor host.
- **A dedicated server doesn't mount a library's assets.** Started with a project's
  `.sbproj`, a dedicated server adds each project in `Libraries\` but puts only the game's
  own `Assets` folder on its search path
  (`26.10.13:engine/Sandbox.GameInstance/GameInstanceDll.cs`, lines 962-985; the mount is
  line 970). Only the Editor mounts a library's `Assets`
  (`26.10.13:engine/Sandbox.Tools/Editor/LibrarySystem/LibrarySystem.cs`, lines 287-306).
  So content that lives only in a library loads in the Editor, and the server reports it
  not found. Keep what the server needs in the game's own `Assets`, or link it there; a
  link fixed it on `26.10.13a`. A file changed behind a junction is hidden from the
  Editor's file watch, as [More world-build lessons](#more-world-build-lessons) says.
  - The same code runs when local automation starts a game with `-mcp`. That is from the
    source and untested.
- **Wait for an active scene, not just for loading to end.** While a game or dedicated
  server loads, `instance_status` can report `Game` set and `IsLoading` false before any
  scene is open. The game's ident is set during the load
  (`26.10.13:engine/Sandbox.GameInstance/GameInstance.cs`, line 190), and `IsLoading` reads
  false while no game instance is current
  (`26.10.13:engine/Sandbox.Engine/Systems/Mcp/InstanceTools.cs`, lines 22-25). The
  instance becomes current only after its load returns, and the startup scene opens after
  that (`26.10.13:engine/Sandbox.GameInstance/GameInstanceDll.cs`, lines 748, 793, and
  808). So a check that waits only for `IsLoading` can start before the scene exists. Wait
  until `ActiveScene` is set too. On `26.10.13a`, a dedicated-server check that didn't wait
  started about a second before the scene opened and failed; with the wait, it found the
  scene.
- **With its address hidden, a dedicated server doesn't listen on its game port.**
  `net_hide_address` is on by default
  (`26.10.13:engine/Sandbox.Engine/Systems/Networking/Networking.cs`, lines 142-143). The
  server then asks Steam for a FakeIP, and opens its game socket through Steam with that
  setting
  (`26.10.13:engine/Sandbox.Engine/Systems/Networking/System/GameNetworkSystem/GameNetworkSystem.Static.cs`,
  lines 264-269;
  `26.10.13:engine/Sandbox.Engine/Systems/Networking/Transports/SteamNetworkSockets/SteamSockets.cs`,
  line 39). On `26.10.13a`, nothing bound the `port` setting (27015 by default) as a plain
  UDP socket, and only the query port, `net_query_port` (27016 by default), was bound. So a
  check that waits for UDP on the game port fails every time.
  - Check what the server reports instead: ask it for `port`, `net_query_port`, and
    `net_hide_address`. With hiding on, confirm the query port is held and that the
    server's `status` lists a Steam socket under "Socket Information"
    (`26.10.13:engine/Sandbox.Engine/Systems/Networking/System/NetworkConsoleCommands.cs`,
    lines 137-156).
  - A check that wanted the game port failed on every run, and one built this way passed.
- **A GameObjectSystem runs in every scene.** Each new scene creates one instance of every
  non-abstract `GameObjectSystem` type in the project
  (`26.10.13:engine/Sandbox.Engine/Scene/Scene/Scene.System.cs`, lines 37-56, called from
  `26.10.13:engine/Sandbox.Engine/Scene/Scene/Scene.cs`, lines 167-178). A `NetworkHelper`
  also clones its player prefab for each connection
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/Networking/NetworkHelper.cs`, lines
  51-62). So a player spawner written as a system also runs in scenes that spawn players
  through a `NetworkHelper`, and on `26.10.13a` those scenes got a second player. Have the
  system skip scenes that have their own player route, such as a scene with a
  `NetworkHelper`.
- **Test walking without a keyboard.** With `UseInputControls` on, which is the default, a
  `PlayerController` sets `WishVelocity` from `Input.AnalogMove` on every fixed update
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/Game/PlayerController/PlayerController.DefaultControls.cs`,
  lines 65-77;
  `26.10.13:engine/Sandbox.Engine/Scene/Components/Game/PlayerController/PlayerController.Input.cs`,
  lines 6 and 91-94). With it off, `WishVelocity` keeps what a test sets, and the step
  before physics applies it through the move mode
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/Game/PlayerController/PlayerController.cs`,
  lines 204-211;
  `26.10.13:engine/Sandbox.Engine/Scene/Components/Game/PlayerController/Modes/MoveMode.cs`,
  lines 57-60). So a test can turn `UseInputControls` off, set `WishVelocity`, let the
  scene run, and read the position. Set it where the controller isn't a network proxy,
  because a proxy doesn't apply it (`PlayerController.cs`, line 208). A first real project
  tested walking this way on `26.10.13a`.
- **In a SceneLoaded hook, `Time.Now` is the caller's clock.** `Scene.Load` pushes the
  scene, which sets `Game.ActiveScene` and the clock from the scene
  (`26.10.13:engine/Sandbox.Engine/Scene/Scene/Scene.cs`, lines 515-526), only while it
  reads the file (`26.10.13:engine/Sandbox.Engine/Scene/Scene/Scene.LoadSave.cs`, lines
  108-151). It signals `Stage.SceneLoaded` after that scope ends (line 164), and stage
  callbacks run with no scope of their own
  (`26.10.13:engine/Sandbox.Engine/Scene/Scene/Scene.System.cs`, lines 122-125;
  `26.10.13:engine/Sandbox.Engine/Scene/GameObjectSystem/TimedCallbackList.cs`, lines
  41-50). So a SceneLoaded hook sees whatever clock its caller had. On `26.10.13a`, a scene
  loaded from the Editor gave the Editor's clock, not play time. `TimeSince` and
  `TimeUntil` count from `Time.NowDouble`
  (`26.10.13:engine/Sandbox.Engine/Utility/TimeSince.cs`, lines 22-25 and 73-75), so they
  read that clock too. Read times in the first update instead, or do the hook's work inside
  `using ( Scene.Push() )` (`Scene.cs`, lines 261-264); that and the same effect on
  `Game.ActiveScene` are inferred from the source.
- **`run_csharp` edits don't mark the scene unsaved, so `save_scene` writes nothing.**
  `run_csharp` creates no undo steps
  (`26.10.13:engine/Sandbox.Engine/Systems/Mcp/ScriptTools.cs`, line 23), and an editor
  session marks itself unsaved through undo scopes and undo or redo
  (`26.10.13:engine/Sandbox.Tools/Scene/Session/SceneEditorSession.Undo.cs`, lines 21-29
  and 786-789). `save_scene` calls the session's save
  (`26.10.13:game/addons/tools/Code/Mcp/Scene.cs`, lines 578-588), which returns without
  writing when the scene has no unsaved changes and its file exists
  (`26.10.13:engine/Sandbox.Tools/Scene/Session/SceneEditorSession.cs`, lines 356-360). On
  `26.10.13a`, edits made through `run_csharp` were not saved this way.
  - End the script by setting `Editor.SceneEditorSession.Active.HasUnsavedChanges = true`,
    then call `save_scene` (public setter, `SceneEditorSession.cs`, lines 277-290). On
    `26.10.13a` that wrote the scene. `run_csharp` wants editor types fully qualified
    (`ScriptTools.cs`, line 23), so use the full name.
  - Making the edits inside an undo scope, as `create_game_object` does (`Scene.cs` in the
    tools addon, line 265), should work too. That is from the source and untested.
- **`Editor.FileSystem.Content` is read-only.** It merges core, citizen, cloud, and addon
  content into one view (`26.10.13:engine/Sandbox.Tools/FileSystem.cs`, lines 53-55 and
  75-87), and that merged view is read-only
  (`26.10.13:engine/Sandbox.Filesystem/AggregateFileSystem.cs`, lines 3-8; `IsReadOnly`,
  `26.10.13:engine/Sandbox.Filesystem/BaseFileSystem.cs`, line 36). It wraps Zio's
  `AggregateFileSystem`, a `ReadOnlyFileSystem` whose writes throw an `IOException`, "This
  filesystem is read-only" (Zio `0.23.0`, `src/Zio/FileSystems/AggregateFileSystem.cs`,
  line 17; `ReadOnlyFileSystem.cs`, lines 20 and 38). So a write through it fails, as it
  did on `26.10.13a`. Write project files to a real path instead, such as under the
  project's `Assets` folder (inferred).
- **Expect a client to log a small resource as missing even when it loads.** A host sends a
  joining client the compiled files it networks. One under 64 KB reaches the client only in
  memory, unless it's of a type the native engine loads itself, such as `vmat_c`, `vtex_c`,
  `vsnd_c` or `vmdl_c`, which always goes to disk
  (`26.10.13:engine/Sandbox.GameInstance/GameInstanceDll.Network.cs`, lines 280-285;
  `26.10.13:engine/Sandbox.Engine/Systems/Networking/Tables/SmallNetworkFiles.cs`, lines 9
  and 27). When S&box's C# loads a resource, it also asks the native engine for the same
  path (`26.10.13:engine/Sandbox.Engine/Resources/GameResource.cs`, lines 181-196;
  `26.10.13:engine/Sandbox.Engine/Resources/AsyncResourceLoader.cs`, lines 52-59). The
  native engine can't see a file held in memory, so the client logs
  `Error loading resource file "<path>" (Error: ERROR_FILEOPEN: File not found)` for each
  such resource, though it loaded. A project's own terrain materials, sound events, decal
  definitions, soundscapes and surfaces are usually this small. On `26.10.13a`, a 2 KB
  terrain material logged the line on a client of an Editor host, and neither the host nor
  a dedicated server logged it. So a session check that scans the client's log for missing
  files fails on it, and one that reads only the host's log never sees it. Check on the
  client that each such resource loaded, from its values and any textures it makes, and
  excuse that exact line only for a resource whose check passed. On `26.10.27c` the same
  line can end in ` - from <path>`, naming the file that asked for the resource, such as a
  model or a sound event. The native engine writes the line, so the source doesn't say when
  it adds the ending. Let the excuse allow that one ending, and still match the whole line
  from start to end, so it excuses nothing else.

A static check over every C# file the project tracks can hold four of these before any
S&box run, since none is a compile error. It fails a `GameObjectSystem` that spawns a
player and never names `NetworkHelper`; a `Stage.SceneLoaded` handler that reads
`Time.Now`, `Time.NowDouble` or `Time.Delta`, or uses `TimeSince` or `TimeUntil`; a write
to `WishVelocity` before `UseInputControls` is turned off; and a write through
`Editor.FileSystem.Content`. Read the code with comments and the text of strings taken out,
and plant each fault in the check's self-test. One project's check holds all four this way
on its build scripts, harness and map code.

## More world-build lessons

Later world work, on S&box `26.10.13a` to `26.10.27c`, turned up twenty-three more. Each is
read from the engine source at `26.10.13` and again at `26.10.27`, and reads the same at
both unless it says otherwise. Each says what was seen, and on which build.

- **Commit the `.meta` files S&box writes beside new source files.** The Editor gives each
  asset it mounts a GUID and writes it under `guid` in a `.meta` file beside the source
  (`26.10.13:engine/Sandbox.Tools/Assets/NativeAsset/NativeAsset.cs`, lines 24 and 35-41;
  `26.10.13:engine/Sandbox.Tools/Assets/Asset.cs`, lines 168-189). A scene saves its
  reference to such a resource as that `Id` and the path
  (`26.10.13:engine/Sandbox.Engine/Resources/Resource.Json.cs`, lines 188-199). So the
  first editor to open a project after new images, models or sounds arrive writes a `.meta`
  for each, and a check that needs a clean working tree fails on them. Commit them with the
  change that added the sources, so their GUIDs stay put. On `26.10.27c` the first editor
  to open a project wrote one per new source file, and a `.slnx` solution file at the
  project's root, which belongs in `.gitignore`. The Editor writes them for every new
  source it mounts, in every folder at once, so a run that builds one scene also writes
  `.meta` files for sources another change added, and that run's clean-tree check fails on
  them. On `26.10.27c` that happened three times in one project before a static check
  caught it. When you add sources for something still to be built, open an editor to write
  their `.meta` files and commit both before the build. A static check that every tracked
  file under the assets folder has a tracked `.meta` beside it catches a missing one
  without S&box; [`tools/check_metas.py`](tools/check_metas.py) is one. Leave out the
  `.meta` files themselves, and compiled `*_c` files and a scene's `.scene_d`, which S&box
  treats as files that go with their source (`Asset.cs`, lines 10-16 and 168-189). On
  `26.10.27c` notes and scripts kept beside sources, such as `.md` and `.py` files, got no
  `.meta` either. Nor did a `.json` record that a project's own script wrote beside a probe
  bake: S&box keeps a `.meta` only for a file it takes as an asset (`Asset.cs`, lines
  168-189). Leave such a file out by its folder and name, not by its extension, so a real
  asset of that type still needs its `.meta`.
- **Allow for a store package's asset ID changing between editor sessions.** S&box writes
  no `.meta` for a file that a cloud package installed (`Asset.cs`, lines 107 and 173-176;
  still so at `26.10.27`), so no file in the project keeps its GUID, and the native
  resource database gives it one. On `26.10.13a` a scene's reference to a package's sky
  saved with one `Id` in the first session and another after reopening, with the same path
  and nothing else changed. On `26.10.27c` a scene's reference to a package's model kept
  one `Id` across five sessions, while in another project on the same build a package's
  material got a new `Id` between sessions. A project's own `.sound` kept its reference to
  the compiled `.vsnd` at one `Id` across three sessions there, an `Id` that isn't the GUID
  in the `.wav.meta`. Between `26.10.13` and `26.10.27` the managed side of that database
  changed: it now tells the database when a `.meta` is written or deleted, asks it whether
  it gave a file a new GUID, and takes GUID changes from a start-up scan
  (`26.10.27:engine/Definitions/engine/resourcesystem.def`, lines 18-20 and 43;
  `26.10.27:engine/Sandbox.Engine/Resources/Resource.cs`, lines 180-197). The database
  itself is native code outside the public source, so why some package files keep their ID
  and others don't is not known. So a check that compares saves from two sessions byte for
  byte can fail on a scene that uses packages, and a run can leave the scene changed in
  Git. Compare each package reference's `Id` with the GUID that session gives the same
  path, and every other byte as written. When a run started from the committed scene and
  only those IDs differ, put Git's copy back. The [editor check](#the-editor-check)
  compares saves this way.
- **Install a new package in an editor session of its own.** As the Editor opens a project,
  it uninstalls every installed package that no file in the project or its libraries lists
  in its `__references` (`26.10.13:engine/Sandbox.Tools/StartupLoadProject.cs`, lines
  264-269 and 390-425; `26.10.13:engine/Sandbox.Tools/Utility/CloudAsset.cs`, lines
  245-313). So a package installed in one editor and not yet in a saved file is gone in the
  next. On `26.10.13a` a sky from a package installed during a build's own session saved
  without an `Id`, and the next session gave it one. Build and save once so the scene lists
  the new package, then run the build that counts in a new editor.
- **To change a saved resource from a script, change the object S&box holds for its file.**
  `Asset.SaveToDisk` registers the object it saves under the file's path and gives it no
  GUID (`Asset.cs`, lines 548-581;
  `26.10.13:engine/Sandbox.Engine/Resources/GameResource.cs`, lines 210-223), and a scene
  writes a reference to a resource with no GUID as its path alone (`Resource.Json.cs`,
  lines 188-193). On `26.10.13a` a build that saved a `new TerrainMaterial()` over a file
  had its scene save the reference as a bare path, the reopened scene saved it with the
  file's `Id`, and a save-and-rebuild check failed. Get the held object with
  `ResourceLibrary.TryGet`, or else `Asset.TryLoadResource`, change it, and save that
  (`26.10.13:engine/Sandbox.Engine/Resources/ResourceLibrary.cs`, line 751).
- **After a script writes a resource, wait with a limit for its compiled file.**
  `AssetSystem.CreateResource` writes `{}` to the file, registers it, and saves a default
  resource over it (`26.10.13:engine/Sandbox.Tools/Assets/AssetSystem.cs`, lines 343-379).
  Loading an asset as a resource reads its compiled file, and fails while that file isn't
  there (`Asset.cs`, lines 429-480). A native asset such as a material compiles in the
  native asset system, and `HasCompiledFile` asks that system each time it is read
  (`NativeAsset.cs`, lines 277-291 and 375). On `26.10.13a`, a terrain material made with
  `CreateResource` failed to load right after the call. On `26.10.27c`, a material compiled
  with `Compile( true )` already loaded with its shader and textures while
  `HasCompiledFile` was still false, and its compiled file came a moment later. So read a
  new resource's values from its source with `Asset.ReadJson` until it has compiled, and
  before using a compiled file, wait until `HasCompiledFile` is true and the file is on
  disk. When the limit runs out, report `IsCompileFailed`. The next lesson adds that the
  file must be this run's.
- **Ask for a compile with `Compile`, but don't take its result as the verdict.**
  `NativeAsset.Compile` returns false when the asset can't be recompiled, and otherwise
  whatever the native asset system's `RecompileAsset` returns
  (`26.10.27:engine/Sandbox.Tools/Assets/NativeAsset/NativeAsset.cs`, lines 275-289).
  S&box's own `CompileIfNeededAsync` drops that result and waits for `IsCompiled`, failing
  only on `IsCompileFailed` or its time limit (lines 326-363). On `26.10.27c` a build
  stopped on a material whose `Compile( true )` returned false while `IsCompileFailed` was
  false. A compiled file an earlier build left says nothing about this one, and a project
  that keeps compiled files out of Git keeps them on disk between runs, so a wait for
  `HasCompiledFile` alone can pass on an old file. After a script changes a source, call
  `Compile( true )` to ask for the compile. Then wait, with a limit, for `HasCompiledFile`
  and a compiled file on disk written at or after the source the run wrote, or one that
  wasn't there before the request or has changed since. Fail on `IsCompileFailed` or on the
  limit, and say which, with what `Compile` returned and the compiled file's time. Judge
  the file by other file times, never by the clock: Windows stamps a file write with the
  time of the system clock's last tick, so a file written just after a `DateTime.UtcNow`
  reading can read as older than it, and `Compile` runs synchronously (line 337 says so),
  so a compile can finish in the request's own tick. A test of such a wait on Windows
  failed 4 runs in 7 that way; the file times are not read in source. Time the wait itself
  with `RealTimeSince` or a count of its waits.
- **Behind a junction, the Editor doesn't see a file change.** A loaded resource takes a
  recompiled file only when S&box's file watch reports it: the resource loader watches
  `*.<extension>_c` on the mounted file system and reloads the resource when one changes
  (`26.10.13:engine/Sandbox.Engine/Resources/ResourceLoader.cs`, lines 146-160 and
  163-218). A terrain material loads its generated textures only when it loads or reloads
  (`26.10.13:engine/Sandbox.Engine/Resources/Terrain/TerrainMaterial.cs`, lines 64-80). On
  Windows, a folder watch reported nothing written behind a junction: a test outside S&box
  saw no events through the junction, and two for the same writes in a plain folder. So
  where a project sees a folder through a junction, as when a game links content into its
  own `Assets`, a file written there stays as it was in the Editor until something loads it
  again. On `26.10.27c` a build that waited for a terrain material compiled behind a
  junction gave up after 60 seconds, though its compiled files were on disk. Once the files
  are on disk and newer than the compile, reload the resource as the watch would, through
  `GameResource.PostReloadInternal` (internal, so reached by reflection; `GameResource.cs`,
  line 127), then wait with a limit for its values. With that, the same build passed.
- **Give a generated material its world mapping.** S&box's material generator writes a
  `.vmat` with its shader, features and textures, and no world mapping
  (`26.10.13:engine/Sandbox.Tools/Utility/MaterialGenerator.cs`, lines 190-234). At the
  default texture scale, 0.25, a mesh then repeats the material every texture width times
  0.25 units, unless the material sets `WorldMappingWidth` and `WorldMappingHeight`
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/Mesh/PolygonMesh.cs`, lines 3723-3733,
  3785-3818 and 4606-4623), so a 2048-pixel texture repeats every 512 inches, about 13
  metres, whatever size its source gives it. Write both in the `.vmat`'s `SystemAttributes`
  block, as S&box's own materials do
  (`26.10.13:game/core/materials/dev/simple/simple_tile.vmat`, lines 19-23), from the size
  the texture's source gives, and check the built file and what S&box reads back against
  that size. This was read in source before any run.
- **When a script sets an object's tags, keep the ones its components add.** A
  `MeshComponent` adds `world` to its object each time it is enabled
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/Mesh/MeshComponent.cs`, lines 149-151).
  Others add a tag when they wake: a light `light`
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/Light/Light.cs`, lines 228-233) and
  `light_point`, `light_spot` or `light_directional` for its kind, a `SkyBox2D` `skybox`
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/Render/SkyBox2D.cs`, lines 65-67), and
  a `ParticleSystem` `particles`
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/Effects/ParticleSystem.cs`, lines
  45-47). A reopen enables and wakes them again. On `26.10.27c` a build that set some
  objects' tags to exactly what its layout listed, which was none, saved them with none,
  the reopened scene saved them with `world`, and the save check failed. So a script that
  sets tags exactly adds back the tags of the object's own components.
- **In engine tests, add a code library's assembly before loading a scene that uses its
  components.** The test host's type library holds the engine's assemblies and the game
  assembly (`26.10.13:engine/Sandbox.Engine/Game/Game/Game.Local.cs`, lines 17-28). A game
  adds a library's assembly when it loads a package
  (`26.10.13:engine/Sandbox.GameInstance/GameInstanceDll.cs`, lines 212-219), which a test
  host never does, and a saved component whose type isn't in the type library loads as a
  `MissingComponent`
  (`26.10.13:engine/Sandbox.Engine/Scene/GameObject/GameObject.Serialize.cs`, lines 515 and
  534-539). On `26.10.27c` a library's component loaded that way in an engine test, though
  the library's DLL was built beside the test assembly. Add each library's assembly to
  `Game.TypeLibrary` first with `TypeLibrary.AddAssembly( assembly, true )`, as the game
  does. It is internal (`26.10.13:engine/Sandbox.Reflection/TypeLibrary/TypeLibrary.cs`,
  line 85), so reach it by reflection. Find the library's DLL from the test build's
  `.deps.json`, not from what the build's output folder holds, since a library that was
  dropped can leave its old DLL there. That the component then loads as itself is from the
  source, not yet run.
- **Read a store package's licence from its `AssetLicense`, and take a missing one as no
  licence.** `Package.AssetLicense` names the licence covering a package's assets, such as
  `CC0` or `CC_BY`, and is null when the package declares none
  (`26.10.13:engine/Sandbox.Engine/Services/Packages/Package.License.cs`, lines 5-24;
  `26.10.13:engine/Sandbox.Engine/Services/Packages/RemotePackage.cs`, line 118). The
  package service gives it as a `LicenseType` number: 1 for CC0, 2 for CC BY-NC-ND, 3 for
  CC BY and 4 for CC BY-SA (`26.10.13:engine/Sandbox.Services/Api/Models/Licensing.cs`,
  lines 6-21), and on 2026-11-01 it left the field out for a package that declares none.
  Who published a package says where it came from, not what it allows: that day, some of
  Facepunch's own packages declared no licence while others were CC0. Read each package's
  version and size again on the day you pin it too, since a publisher can replace a package
  at any time: that day, several packages read far smaller than they had a few days before.
- **After an S&box update, commit what the Editor re-saves with the new fields.**
  `26.10.27` added fields such as a light's `Intensity` and `Temperature`
  (`26.10.27:engine/Sandbox.Engine/Scene/Components/Light/Light.cs`, lines 160-172 and
  179-194) and a project's `PublishUsedAssetsOnly`
  (`26.10.27:engine/Sandbox.Engine/Systems/Project/ProjectConfig.cs`, line 95), and the
  Editor writes each at its default the first time it saves a scene or project file. On
  `26.10.27c`, checks that compare a run's own saves passed and left every scene and
  `.sbproj` changed, and the next check refused to run on an unclean tree. In the update
  review, put Git's bytes back before each check, and commit the Editor's saves with the
  review once every check has passed.
- **Tell a waiting S&box update by Steam's target build ID, not its update flag.** On
  `26.10.13a` a check that read the "update required" flag, 2, in the `StateFlags` of
  Steam's `appmanifest_590830.acf` reported a waiting update, and launching S&box cleared
  the flag with nothing new installed: `buildid` and `TargetBuildID` were the same. Report
  a waiting update only when `TargetBuildID` is set and differs from `buildid`. Steam's
  manifest format isn't documented; this was seen.
- **Compare rotations read back from S&box as unit quaternions, with atan2, not acos.** A
  `Rotation` is a float32 quaternion (`26.10.27:engine/Sandbox.System/Math/Rotation.cs`,
  lines 16-53), and the ones S&box builds can be only nearly unit:
  `Rotation.From( 0, 90, 0 )` gives `0, 0, 0.70710677, 0.70710677`, whose length squared is
  0.99999997 (lines 162-188). The usual turn between two rotations, `2 acos(|a · b|)`, is
  steep near 1, so it reads two identical such rotations as 0.03 degrees apart. On
  `26.10.27c` a check with a 0.01 degree limit failed that way on a target rotation and the
  same rotation read back from S&box. A 1 degree limit elsewhere had hidden it, and the
  check's self-test, fed exactly unit doubles, never showed it. Scale each quaternion to
  unit length, flip one when their dot product is negative so q and -q count as one
  rotation, and take the turn as `4 atan2(|a - b|, |a + b|)`, which stays exact near 0.
  Feed the self-test float32 values the way S&box hands them over. S&box's own
  `Rotation.Distance` doesn't help at such limits: it takes a float32 acos of the
  difference's `w` (lines 295-318), which by the same arithmetic reads any turn up to about
  0.03 degrees as 0, and the smallest turn it can see as 0.04. That is worked from the
  source, not run.
- **Load a sound with `LoadAsync` before a script reads its length.** `SoundFile.Load`
  returns a handle and loads nothing
  (`26.10.27:engine/Sandbox.Engine/Resources/Sound/SoundFile.cs`, lines 196-222). `IsValid`
  reads the handle, but `Duration`, `Rate`, `Channels` and the other format members read
  the loaded sound (lines 89-129). Only `LoadAsync`, `Preload` or a reload of the file sets
  it, and `IsLoaded` says whether it is there, so a script that only waits for `IsLoaded`
  can wait for ever. `LoadAsync` starts the load and waits until the sound can play, but
  returns false after 3 seconds (lines 432-457). On `26.10.27c` a `run_csharp` script that
  loaded two freshly compiled `.wav` files with `SoundFile.Load` and read `Duration`
  stopped with `NullReferenceException: VSound_t was null when calling Duration`, though
  each handle was valid. Before a script reads anything a sound file holds, call
  `LoadAsync` again until `IsLoaded`, with a limit, and stop with the file's name when the
  handle goes away or the limit runs out.
- **A sound component's `Force2d` works with Sound Override off.** The Inspector shows
  `Force2d` inside the Sound Override group, but `BaseSoundComponent` applies it whether
  that override is on or not, and after the distance override, so it wins: it moves the
  sound to `Vector3.Forward * 10` and turns off its distance attenuation, occlusion and air
  absorption
  (`26.10.27:engine/Sandbox.Engine/Scene/Components/Audio/BaseSoundComponent.cs`, lines
  20-32 and 75-112). Only with Sound Override on does it also set `ListenLocal`, which puts
  the listener at the origin facing forward, so the sound plays just in front of it
  (`26.10.27:engine/Sandbox.Engine/Systems/Audio/SoundHandle.cs`, lines 305-308); with the
  override off, the sound sits at that point in the world, still with no fade over
  distance. A script that builds sound emitters, and means them to fade with distance, sets
  `Force2d` to false and reads it back with the other overrides. Read from the source, not
  run.
- **Set a picture compare's threshold from a planted change and two captures of one
  build.** A check that compares an S&box update's screenshots with approved ones needs a
  share of changed pixels above which a picture trips, and a share picked by hand can be
  loose enough to pass anything. One way that worked on `26.10.27c`: take every shot in
  play mode, since an editor capture can show what the game hides (see [the import
  reference](IMPORTING.md#tools-and-scripting)), at one fixed size, and refuse any other
  size rather than scale it. Convert each pixel from sRGB to CIELAB under D65 and count it
  as moved when it moved by a just-noticeable difference, a CIE76 ΔE of 2.3. Capture the
  scene twice from one build and commit, for the noise, and once with a planted change the
  check must catch, such as one lamp's colour. Set the share at half the share the planted
  change moved, and only when both plain captures stay under it. On `26.10.27c` the two
  plain captures came out byte for byte the same, so the noise between runs of one build
  was 0; the noise between builds first shows in the first real update compare. Record the
  three runs, the commit and the build beside the share, and have the compare's self-test
  check that the share follows from them by the rule, so a share typed by hand fails. Give
  that self-test a thresholds file of its own: one that reads the real file breaks as soon
  as the share is set. No engine source is involved; this was seen.
- **After a build fails part way, put back what it wrote before the run that counts.**
  `Asset.MetaData.Set` writes the `.meta` file each time it is called, not when the build
  ends or the scene saves (`26.10.27:engine/Sandbox.Tools/Assets/MetaData.cs`, lines 88-119
  and 186-200). So a build that sets keys in several `.meta` files and stops between them
  leaves some set and the rest as they were, and nothing in the scene shows it. On
  `26.10.27c` a failed build left one sound's `.wav.meta` with its loop keys and another
  with only its GUID, and a review caught it before the commit. If the build writes only
  what differs, its next run skips the file the failed run set, so the run that passes
  neither writes it nor records it, and the commit can't show which run did. Before
  building again, put back from Git each file the failed run touched: the scene, its
  folder, and the `.meta` files beside its sources. For a new source's `.meta`, which Git
  doesn't have yet, take out the keys the run added and keep the `guid` S&box gave it.
- **Set a decal's `Rotation` to a constant.** A `Decal`'s `Rotation`, its roll about its
  forward axis, defaults to `new ParticleFloat( 0, 360 )`, a range
  (`26.10.27:engine/Sandbox.Engine/Scene/Components/Render/Decal.cs`, line 71). The
  component draws a new seed with `Random.Shared` each time it is enabled and takes the
  roll from it (lines 167-178, 300-303 and 366-371). So a decal a script places without
  setting its roll lands at a new one each time the scene loads or plays, and two captures
  of one build can differ. S&box saves a constant `ParticleFloat` as a plain number, and a
  range as an object with its `Type` and `Constants`
  (`26.10.27:engine/Sandbox.Engine/Scene/Components/Particles/ParticleFloat.cs`, lines
  233-268), so a scene check can tell them apart. Set the roll the layout means as a
  constant, and have the scene check expect that number. Read from the source, not run.
- **Put a map's `Fog` where no camera or post-process volume owns it.** On `26.10.27`,
  `GradientFog` is marked obsolete in favour of `Fog`, a post-process effect
  (`26.10.27:engine/Sandbox.Engine/Scene/Components/Render/GradientFog.cs`, line 6). `Fog`
  is the one post-process effect there that is a camera effect
  (`26.10.27:engine/Sandbox.Engine/Scene/Components/PostProcessing/Fog.Blending.cs`, line
  10), and it reaches cameras by its own rule. Any other effect works only on a camera's
  object or under it, or under a post-process volume the camera stands in
  (`26.10.27:engine/Sandbox.Engine/Scene/Components/PostProcessing/PostProcessSystem.cs`,
  lines 96-120; `PostProcessSystem.BuildScratch.cs` beside it, lines 26-35). A `Fog`
  belongs to the nearest `PostProcessVolume` or `CameraComponent` on its object or above
  it, disabled ones included, and a `Fog` with no owner is added for every camera at full
  weight (`PostProcessSystem.cs`, lines 143-217; `PostProcessSystem.BuildScratch.cs`, lines
  50-77). So a fog on a plain object under the scene's root fogs every camera, the same fog
  under a camera's object fogs only that camera, and under a disabled camera or volume it
  is no longer added for every camera. A camera with `EnablePostProcessing` off gets no fog
  either way; it is on by default
  (`26.10.27:engine/Sandbox.Engine/Scene/Components/Camera/CameraComponent.PostProcess.cs`,
  line 35). A camera with a `PostProcessAnchor` picks its volumes from that object's
  position, not its own (line 41; `CameraComponent.cs` beside it, line 444). Both are a new
  camera's defaults, but a camera a scene already saved keeps what it was saved with, so
  have the build set `EnablePostProcessing` on and the anchor empty on each camera it
  makes, and the scene check expect both. Have the scene check hold the map's fog alone on
  its object, with no camera or volume on it or above it, and plant a camera there to see
  the check fail. Set the fog's other values to the look you want rather than leaving its
  defaults: `Mode` is Exponential, the colour comes from the sky (`ColorSource` is
  `SceneSky`), and `SkyAffect` is 1, so the fog covers the sky too (`Fog.cs`, lines 77, 175
  and 249-253). Leave its height layer off unless the map wants one: `HeightEnabled`, off
  by default, draws fog by height alone, apart from distance, full at `HeightOffset` above
  the fog's object and fading over `HeightGradientLength` (`Fog.cs`, lines 111-127), so
  with it on a room below that height is fogged however near the camera stands, and a scene
  check can fail it. New at `26.10.27`: at `26.10.13` there is no `Fog` and `GradientFog`
  isn't obsolete. Read from the source, not run.
- **Bake envmap probes in the editor, track the compiled bake, and don't capture a probe
  with no bake.** `EnvmapProbe.Bake` runs only in the editor
  (`26.10.27:engine/Sandbox.Engine/Scene/Components/Light/EnvmapProbe.Baking.cs`, lines
  15-20). It writes the bake straight to a compiled texture,
  `<scene>_scene_data/envmap/bake_<Id>.vtex_c`, with no source file, then loads it as the
  probe's `BakedTexture` (lines 41-53), and loading a texture drops the `_c`
  (`26.10.27:engine/Sandbox.Engine/Resources/Textures/Texture.Load.cs`, line 62), so the
  scene names `bake_<Id>.vtex`. A project that keeps compiled `*_c` files out of Git has to
  let these in, since only another bake makes them again. A check that each file a scene
  names is tracked has to read `bake_<Id>.vtex` as `bake_<Id>.vtex_c`, as
  [`tools/scene_refs.py`](tools/scene_refs.py) does. A probe in `Baked` mode with no bake
  hands its scene object a null texture
  (`26.10.27:engine/Sandbox.Engine/Scene/Components/Light/EnvmapProbe.cs`, lines 376-379),
  and on `26.10.27c` a picture check of a scene whose probes had no bake read their boxes
  as black, so it measured the missing bake, not the light. Before capturing a scene, check
  that each probe in `Baked` mode holds its `BakedTexture`, and bake first when one
  doesn't. Seen on `26.10.27c`: the first bake wrote only the `.vtex_c` files, and a scene
  check failed the `.vtex` paths as missing until it read them this way.
- **Check that a picture check's camera sees each thing it reads, before the capture.** A
  reading that counts the pixels that change when a thing is hidden says almost nothing
  about a thing behind another, and a reading of a box's outline in the shot reads whatever
  stands in front of it. On `26.10.27c` a check set three stand-ins on its camera's line,
  500, 5,300 and 8,000 units out. Hiding the far one changed 2 pixels of the shot and
  hiding the near one 23,089, so the far one read as unseen whatever the scene did, and the
  check was blind to the change it was for. Set apart, the middle one still had a slab's
  corner over its foot. A check on the layout catches this without S&box: trace a grid of
  lines, such as 6 by 6, from the camera to each face of the thing that faces it, against
  every solid in the layout, and refuse the reading when a line is blocked or the camera
  sees no face of it. A line that ends on a solid's face, as one to a patch on a wall does,
  isn't blocked. Run it on each planted copy of the scene the check reads too, and place a
  reading past terrain by hand unless the check traces the terrain as well. No engine
  source is involved; this was seen.
- **Read a player's camera once it has stopped turning, and fail it if it never does.** A
  `PlayerController` writes its eye rotation, made from `EyeAngles`, straight into the
  camera's view each time the scene composes the view, once per tick
  (`26.10.27:engine/Sandbox.Engine/Scene/Components/Game/PlayerController/PlayerController.Camera.cs`,
  lines 41-49 and 90;
  `26.10.27:engine/Sandbox.Engine/Scene/Components/Game/PlayerController/Modes/MoveMode.Camera.cs`,
  lines 9-15; `26.10.27:engine/Sandbox.Engine/Scene/Components/Camera/CameraComponent.cs`,
  lines 270 and 298-311). It smooths only the eye's height and the third-person camera's
  distance (`PlayerController.Camera.cs`, lines 51-54 and 72-84). With `UseLookControls`
  on, each update also adds the look input to `EyeAngles`
  (`PlayerController.DefaultControls.cs`, lines 46-49; `PlayerController.Input.cs`, lines
  82-99). Yet on `26.10.27c`, a check that turned a first-person player a quarter turn in
  play mode and read the camera after five waits of 1/60 s got 63 and 0 degrees in 2 of 45
  runs, and about 90 in the rest. The source doesn't say why. So read the camera once it
  has settled: wait frame by frame, past a least wait, until its view has held still for a
  span, for at most a real-time limit, and fail a camera still moving then, so a part-way
  read fails as one, not as a wrong angle. Don't widen the reading's bounds to fit an early
  read. At `26.10.13` the code reads the same, at lines 71-88 of
  `PlayerController.Input.cs` and 310-323 of `CameraComponent.cs`.

## Lessons from importing old content

These moved to the [import reference](IMPORTING.md) in v1.02. It sorts what a project
learned bringing old content into S&box by topic, and each entry names the S&box version
it was checked on.
