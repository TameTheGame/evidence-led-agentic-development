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
| [`IMPORTING.md`](IMPORTING.md) | The import reference: what works and what doesn't when bringing Source and other old content into S&box, sorted by topic, each entry with the S&box version it was checked on |
| [`tools/spec_lint.py`](tools/spec_lint.py) | A rung-0 spec lint: format and card checks that fail the run, a lookup that reports checks not found in the test and script folders, and an owner gate that reports any change to an agreed requirement since the last commit. Run `python tools/test_spec_lint.py` to check it against its fixtures. |

## The ladder for a map

| Rung | Example check |
|---|---|
| **0 · static** | The layout data is valid, spawn IDs are unique, and the saved `.scene` JSON has exactly one main camera. The project's code and its `run_csharp` scripts compile against the installed engine. |
| **1 · engine** | A `UnitTests/` project starts the engine through `TestAppSystem` and builds the area with the same generator code. It then checks collision, spawn grounding, and route traces. |
| **2 · editor** | The generated scene survives save, close, and reopen unchanged. A screenshot from a fixed camera. |
| **3 · session** | A remote client sees and collides with the same walls. Same-machine host and client is not clean-client proof. Until the game is published, host from the Editor; see [Lessons from a world build](#lessons-from-a-world-build). |
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
    script that already runs through `run_csharp` may find the setter simpler. On
    `26.10.13a`, a `run_csharp` script that set it at its end, followed by `save_scene`,
    wrote the scene; the file's new timestamp and contents showed it.
- **A project without code works too.** A project with code must report a finished,
  successful compile. A content project, such as a map, has no `Code` or `Editor` folder
  and never compiles, so the check doesn't wait for a compile result.
- **The screenshot is a record.** `-Camera` and `-Angles` fix the view. The script reports
  how much the two captures differ but doesn't score it, because the byte-identical save
  already proves the scene came back unchanged.
- **It leaves no trace.** It puts the scene file and the project's `.sbproj` back as they
  were, and saves results in `test-results\editor-<time>\`: both captures, both saved files,
  the object lists, and the console errors. The Editor can rewrite the `.sbproj` when it
  starts; see [Lessons from a world build](#lessons-from-a-world-build).
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

## Lessons from a world build

The same project's world work on S&box `26.10.13a` turned up thirteen more. Each is read
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
  link fixed it on `26.10.13a`.
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
  loaded from the Editor gave the Editor's clock, not play time. Read times in the first
  update instead, or do the hook's work inside `using ( Scene.Push() )`
  (`Scene.cs`, lines 261-264); that and the same effect on `Game.ActiveScene` are inferred
  from the source.
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

## Lessons from importing old content

These moved to the [import reference](IMPORTING.md) in v1.02. It sorts what a project
learned bringing old content into S&box by topic, and each entry names the S&box version
it was checked on.
