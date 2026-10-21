# Importing old content into S&box

> **Target-specific and non-normative.** What works and what doesn't when bringing content
> from other games into S&box: Source 1 maps and models from Garry's Mod and Half-Life 2,
> and anything general to other games and asset packs. It also lists faster ways of
> working.

> **S&box is still in development.** Every entry names the S&box version it was checked
> on, and any entry can go stale. After an S&box update, recheck the entries as
> [Rechecking after an update](#rechecking-after-an-update) says. When S&box gains an
> easier or more native way to do something here, rewrite the entry or drop it.

A first real project found these while importing an old Source 1 map into S&box `26.10.13a`.
They're sorted by topic, not by when they were found.

## Reading an entry

Each entry opens with what to do. Then it says what fails when you don't, and why. A
`Checked:` line ends it, with:

- **the evidence:**
  - *source*: read in engine source. `26.10.13:<path>` is `Facepunch/sbox-public` at
    tag `26.10.13`, which is approximate for the installed `26.10.13a`.
    `source-sdk-2013@be57e3d:<path>` is Valve's Source SDK 2013
    (`ValveSoftware/source-sdk-2013`) at commit `be57e3d`.
  - *seen*: observed on the S&box build it names.
  - *inferred*: reasoned from the source or the observation, not run.
- **the proof:** the check that showed the fix works, or "nothing yet".

Garry's Mod runs its own fork of Source that isn't public. Where an entry cites the Source
SDK for Garry's Mod behavior, the match is inferred unless the entry says it was seen.

## Contents

- [Models](#models)
- [Collision](#collision)
- [Physics and breakables](#physics-and-breakables)
- [Materials and decals](#materials-and-decals)
- [Lighting](#lighting)
- [Sound and water](#sound-and-water)
- [Map logic and entities](#map-logic-and-entities)
- [Player movement](#player-movement)
- [Tools and scripting](#tools-and-scripting)
- [Faster ways of working](#faster-ways-of-working)
- [Adding an entry](#adding-an-entry)
- [Rechecking after an update](#rechecking-after-an-update)

## Models

- **Convert SMD models before importing them.** The editor treats only FBX, OBJ, and DMX
  files as meshes: the asset browser offers Create Model for those three
  (`26.10.13:game/addons/tools/Code/Editor/AssetList/AssetList.ContextMenu.cs`, lines
  329-349), and the mesh preview covers the same three
  (`26.10.13:game/addons/tools/Code/Assets/PreviewMesh.cs`, lines 4-6). No C# in the engine
  source reads SMD, and on `26.10.13a` ModelDoc wouldn't import one. So convert old Source
  models to FBX, OBJ, or DMX first. ModelDoc's importer itself is native code that isn't in
  `sbox-public`; on `26.10.13a` it also listed VOX.
  - Checked: source at `26.10.13`; seen on `26.10.13a`. Proof: nothing yet.
- **Write OBJ files Y-up.** ModelDoc reads OBJ as Y-up and maps a point (a, b, c) to
  (c, a, b). So write a Source point (X, Y, Z) as (Y, Z, X), or the model comes in lying
  down and turned 90 degrees. ModelDoc's importer is native and not in `sbox-public`. The
  only related C# is the Create Model dialog, which offers an import scale but no axis
  setting (`26.10.13:engine/Sandbox.Tools/Utility/CreateModelFromMeshDialog.cs`, lines
  34-68). The mapping fits a Y-up file landing in S&box's Z-up, X-forward space.
  - Checked: seen on `26.10.13a`, by comparing a prop's facing with its map angles from
    above; no source. Proof: nothing yet. A test that imports a known OBJ and reads back its
    bounds would settle it.
- **Pose a Source prop the way Source draws it.** The Source client builds a model's pose
  from each bone's default position and rotation, then lays the current sequence at its
  current cycle over them at full weight
  (`source-sdk-2013@be57e3d:src/game/client/c_baseanimating.cpp`, lines 1953-1986;
  `src/public/bone_setup.cpp`, lines 1782-1813). Setting an entity's model sets its
  sequence to 0 (`src/game/server/baseanimating.cpp`, lines 2656-2687), and a
  `prop_dynamic` changes that only for a default or random animation
  (`src/game/server/props.cpp`, lines 1907-1921). So such a prop is drawn at frame 0 of
  sequence 0, which can differ from the bind pose its VVD vertices are stored in. Half-Life
  2's door model turns its root bone 90 degrees in that frame, so doors converted in the
  bind pose stood out of their frames on `26.10.13a`.
  - To match, bake that frame into the converted mesh, as the project did, or play the
    sequence, stopped, on a `SkinnedModelRenderer` with `UseAnimGraph` off
    (`26.10.13:engine/Sandbox.Engine/Scene/Components/Render/SkinnedModelRenderer.cs`,
    lines 92-104 and 112; `SkinnedModelRenderer.Sequence.cs`, lines 59-70). The second way
    is inferred and untested.
  - Also inferred: the start cycle of 0, since the engine allocates entities outside the
    SDK. `prop_static` is drawn by engine code outside the SDK, so this entry says nothing
    about it.
  - Checked: source at `be57e3d`; seen on `26.10.13a`. Proof: a test that every
    converted door model sits closed in its frame.

## Collision

- **Give a baked ragdoll no collision.** A static copy of a ragdoll, posed where it settled
  in the original game, overlaps what it lies on. With collision on, it pushed the physics
  props under it out of the world on `26.10.13a`. Why it pushes is inferred: S&box
  separates overlapping bodies.
  - Checked: seen on `26.10.13a`; no source. Proof: a play-mode check that no physics
    object falls out of the world.

## Physics and breakables

- **Let physics props fall from the start unless Source starts them asleep.** Source
  starts a `prop_physics` asleep only when spawn flag 1 is set
  (`source-sdk-2013@be57e3d:src/game/shared/props_shared.h`, line 17;
  `src/game/server/props.cpp`, line 2547); otherwise it falls and settles when the map
  starts. A `Rigidbody` has `StartAsleep` for the flag
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/Collider/Rigidbody.cs`, lines 179-180
  and 558-561). Importing every prop asleep left a heavy prop hanging where the mapper
  placed it.
  - Checked: source at `be57e3d` and `26.10.13`; seen on `26.10.13a`. Proof: a play-mode
    check that the prop rests on the ground.

## Materials and decals

- **Use a Multiply decal for Source's modulate decals.** A `DecalDefinition`'s
  `BlendMode` can be `Multiply`, which multiplies the surface's color by the decal's, and
  white leaves it unchanged
  (`26.10.13:engine/Sandbox.Engine/Systems/Render/DecalBlendMode.cs`, lines 14-18;
  `26.10.13:engine/Sandbox.Engine/Resources/DecalDefinition.cs`, lines 77-80). A `Decal`
  passes it on (`26.10.13:engine/Sandbox.Engine/Scene/Components/Render/Decal.cs`, line
  299), and the shader multiplies the surface's albedo by it
  (`26.10.13:game/core/shaders/common/classes/Decals.hlsl`, lines 266-267). Source's
  `DecalModulate` doubles that product in gamma space, so mid-grey leaves the surface
  unchanged
  (`source-sdk-2013@be57e3d:src/materialsystem/stdshaders/DecalModulate_dx9.cpp`, lines
  73-78). So write the texture at twice its color.
  - Doubling clamps texels brighter than mid-grey at white, where Source would brighten
    the surface (inferred). S&box multiplies the albedo before lighting and Source the lit
    frame, so specular and fog can differ (inferred).
  - A port that assumed S&box had no multiply blend drew these decals as translucent
    quads. Before working around a feature S&box seems to lack, search the engine source
    for it, as the
    [S&box skill](skills/sbox-engine-reference/SKILL.md#the-engine-source-is-ground-truth)
    says.
  - Checked: source at `26.10.13` and `be57e3d`; seen on `26.10.13a`. Proof: a play-mode
    test that each imported modulate decal is a `Multiply` decal.
- **Use translucency, not alpha test, for thin-wire textures.** With `F_ALPHA_TEST`,
  `complex.shader` drew chain-link fences as solid panels a few metres away;
  `F_TRANSLUCENT` drew them right. `complex.shader` itself is private: `sbox-public` leaves
  it out on purpose (`26.10.13:engine/Tools/SboxBuild/Steps/SyncPublicRepo.cs`, line 74).
  - A likely cause, inferred: the public shaders' alpha-test step raises opacity by a
    quarter per mip level, so distant surfaces keep their coverage
    (`26.10.13:game/core/shaders/vr_common.fxc`, lines 294-326; called from
    `26.10.13:game/core/shaders/common/shadingmodel.hlsl`, lines 56-77). A sparse wire
    pattern averages to low alpha in small mips, and that boost can lift it past the
    cutoff, filling the holes. Whether `complex.shader` uses this step can't be read.
  - Checked: seen on `26.10.13a`. Proof: nothing yet. An editor capture of a chain-link
    material at several distances, with each feature, would settle it.
- **Project a decal that has to wrap a corner.** Source's decals wrap round a corner onto
  the next surface. A decal built as a flat quad trimmed to one surface stops at its edge;
  a projected `Decal` component covers what its box touches, so it wraps.
  - Checked: seen on `26.10.13a`; no source read. Proof: nothing yet.

## Lighting

- **Start each light as its "start off" flag says, and let the map's logic switch it.** A
  Source light with spawn flag 1 starts dark
  (`source-sdk-2013@be57e3d:src/game/server/util.h`, line 533;
  `src/game/server/lights.cpp`, lines 76-77), and the map's logic turns it on. Lights
  imported all off left lit rooms black; lights imported all on break logic that switches
  them. In play mode, start each light as its flag says. An editor view can show them all
  on, to compare with screenshots taken with the lights on.
  - Checked: source at `be57e3d`; seen on `26.10.13a`. Proof: a play-mode check that
    counts the lights lit at start.
- **Expect live lighting, not Source's baked lighting.** S&box lights a scene live, so
  enclosed rooms got sky light they don't get in Source and looked brighter and flatter.
  An `IndirectLightVolume` (DDGI) per room is the likely fix
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/IndirectLighting/IndirectLightVolume.cs`,
  lines 14-19); that is inferred and untested.
  - Checked: seen on `26.10.13a`. Proof: nothing yet.

## Sound and water

No entries yet. Sound lost to key spelling is under
[Map logic and entities](#map-logic-and-entities).

## Map logic and entities

- **Match Source entity keys without regard to case.** Source compares keyvalue names
  case-insensitively
  (`source-sdk-2013@be57e3d:src/game/server/saverestore_gamedll.cpp`, line 46;
  `src/game/server/util.h`, lines 188-191), so a map may spell a key `MoveSound` or
  `movesound`. A tool that compared the exact spelling silently dropped every door and lift
  sound.
  - Checked: source at `be57e3d`; seen on `26.10.13a`. Proof: the list of sounds found,
    which gained the missing ones.
- **Put a track train on its first path node, facing along the path.** One frame after it
  spawns, Source moves a `func_tracktrain` to its first `path_track`, raised by its
  `height`, and turns it to face the point its `wheels` distance further along the path,
  unless its fixed-orientation flag is set
  (`source-sdk-2013@be57e3d:src/game/server/trains.cpp`, lines 2549-2599 and 2735). With
  `wheels` at 0 it looks at its own point, and Source turns that into a 90-degree pitch
  (`src/mathlib/mathlib_base.cpp`, lines 1000-1012). Then it fires that node's `OnPass`
  (`trains.cpp`, line 2455; `src/game/server/pathtrack.cpp`, lines 566-568). So a train sits
  somewhere other than where it was built: lifts sat higher, and a platform built standing
  up lay flat. Place and turn trains the same way on import, then fire the first node's
  `OnPass` at start, which sets the starting state.
  - Checked: source at `be57e3d`; seen on `26.10.13a`. Proof: a play-mode test of each
    lift's starting position and state.
- **Read a sliding door's old "starts open" flag the Source way.** A `func_door` with spawn
  flag 1 spawns at its open position, marked open, so Close brings it back to where it was
  built (`source-sdk-2013@be57e3d:src/game/server/doors.cpp`, lines 273-279; the flag is
  `src/game/server/doors.h`, line 22). Reading it as a swap of the two positions, as
  `func_door_rotating` still does (`doors.cpp`, lines 1374-1389), left lift doors open for
  the ride and shut on arrival.
  - Checked: source at `be57e3d`; seen on `26.10.13a`. Proof: a play-mode test that a
    lift's doors are shut while it moves.
- **Swing a rotating door by Source's rule, not always away from the player.** Source
  picks a sign from the cross product of two directions, from the player to the door's
  hinge and from the player to the nearest point of the door. It multiplies the door's open
  angles by that sign, so the sign of the mapper's distance setting still decides the
  direction
  (`source-sdk-2013@be57e3d:src/game/server/doors.cpp`, lines 966-998; the open angles are
  line 1367). "Always away from the player" swung a hatch into its wall. One-way doors and
  doors that don't turn about the vertical axis skip the rule (line 974).
  - Checked: source at `be57e3d`; seen on `26.10.13a`, and in Garry's Mod, which swung
    that hatch the same way. Proof: a test that every rotating door opens without going
    into a wall.
- **Let the player use things that sit inside other solids.** S&box's use trace stops at
  the first solid collider that has nothing to press
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/Game/PlayerController/PlayerController.Pressing.cs`,
  lines 205-261). Source's use also searches a sphere for usable things roughly in front
  (`source-sdk-2013@be57e3d:src/game/shared/baseplayer_shared.cpp`, lines 1067-1269; the
  sphere search starts at line 1182), and
  buttons that act on use and doors are flagged for it (`src/game/server/buttons.cpp`,
  line 696; `src/game/server/doors.h`, line 71). So a button built overlapping a door
  works in Source but not in S&box. Give the player a component that answers the
  controller's `GetUsableComponent` event, which it asks before anything else
  (`Pressing.cs`, line 231; `PlayerController.Events.cs`, line 36).
  - Checked: source at `26.10.13` and `be57e3d`; seen on `26.10.13a`. Proof: a play-mode
    test that presses every usable thing from where a player would stand.

## Player movement

No entries yet. To test walking without a keyboard, see
[Lessons from a world build](README.md#lessons-from-a-world-build).

## Tools and scripting

The guide's [Lessons from a world build](README.md#lessons-from-a-world-build) has more
on scripting the Editor: the clock in a SceneLoaded hook, saving after `run_csharp`, and
the read-only `Editor.FileSystem.Content`.

- **Write full type names in `run_csharp` scripts.** `run_csharp` puts the script inside a
  method, after a fixed set of `using` lines: `System`, `System.Linq`, `System.Threading`,
  `System.Threading.Tasks`, `Sandbox`, and a `using static` for the game namespace
  (`26.10.13:engine/Sandbox.Engine/Systems/Mcp/ScriptTools.cs`, lines 74-86). So a `using`
  line in the script doesn't compile, and an extension method from any other namespace
  doesn't resolve. Write full type names, and call such an extension method as a static
  method of its class. The [compile check](README.md#the-compile-check) wraps scripts the
  same way, so it catches both.
  - Checked: source at `26.10.13`; seen on `26.10.13a`. Proof: the compile check.
- **Inside a component, `Transform` is the component's own property.** `Component`
  has a `Transform` property of type `GameTransform`
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/Component.cs`, line 42), so
  `Transform.Zero` looks for `Zero` on that property and doesn't compile. The `Transform`
  struct is in the global namespace
  (`26.10.13:engine/Sandbox.System/Math/Transform.cs`, lines 13-18), so write
  `global::Transform.Zero` (inferred), or set `LocalPosition` and `LocalRotation`.
  - Checked: source at `26.10.13`; seen on `26.10.13a`. Proof: the project's compile.
- **Set some properties in a constructor, not an initializer.** For an auto-property of a
  simple type, such as an enum, `int`, `bool`, or `float`, the code generator copies the
  initializer into a `[DefaultValue( ... )]` attribute
  (`26.10.13:engine/Sandbox.Generator/Units/DefaultValue.cs`, lines 12-26 and 43-84), and it
  does this for every property in the project
  (`26.10.13:engine/Sandbox.Generator/Worker.cs`, line 302). An attribute argument must be a
  constant, so an initializer that reads a primary-constructor parameter, such as
  `public float Width { get; } = width;`, fails to compile with CS0182, in a struct or a
  class. On `26.10.13a` the Editor then wouldn't open the project. Assigning the property in
  an ordinary constructor compiles.
  - Checked: source at `26.10.13`; seen on `26.10.13a`. Proof: the project's compile.
- **A mesh marked HideInGame still renders in the editor scene.** `MeshComponent` removes
  its scene object for `HideInGame` only outside the editor
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/Mesh/MeshComponent.cs`, lines 77-100
  and 125), so every render of the editor scene draws it. `editor_camera_screenshot`
  renders the editor viewport's own camera, not a `CameraComponent`
  (`26.10.13:game/addons/tools/Code/Mcp/Scene.cs`, lines 227-238), and on `26.10.13a` its
  screenshots showed such meshes even with the camera set to skip their tags. A capture
  meant to show what players see belongs in play mode (inferred from the source).
  - Checked: source at `26.10.13`; seen on `26.10.13a`. Proof: nothing yet.
- **`Material.Load` doesn't return null for a missing file.** Its comment says it returns
  the material or null
  (`26.10.13:engine/Sandbox.Engine/Resources/Material/Material.Load.cs`, line 17), but it
  returns null only when the engine gives it no handle (line 70). The engine gives an error
  material instead, which the load names after the path (lines 30 and 41); on `26.10.13a`
  a missing file came back that way. `Model` and `Texture` override `IsError`
  (`26.10.13:engine/Sandbox.Engine/Resources/Model/Model.cs`, line 105;
  `26.10.13:engine/Sandbox.Engine/Resources/Textures/Texture.cs`, line 33), but `Material`
  keeps the default, which is always false
  (`26.10.13:engine/Sandbox.Engine/Resources/Resource.cs`, line 46). So neither a null check
  nor `IsError` finds a missing material. In editor code, check `AssetSystem.FindByPath`,
  which returns null when no asset has that path
  (`26.10.13:engine/Sandbox.Tools/Assets/AssetSystem.cs`, lines 196-218).
  - Checked: source at `26.10.13`; seen on `26.10.13a`. Proof: nothing yet.

## Faster ways of working

- **Ask the original game what it does.** To learn exactly what an old Garry's Mod map does
  at a spot (where props, doors, and ragdolls end up, what a button does), run the map in
  Garry's Mod with a temporary server Lua script that records it, and compare the port
  with that record. Scripts in `lua/autorun/server` run on the server
  ([Lua Folder Structure](https://wiki.facepunch.com/gmod/Lua_Folder_Structure)), after
  the base gamemode loads and before the active one
  ([Lua Loading Order](https://wiki.facepunch.com/gmod/Lua_Loading_Order)). So the script
  waits for the map's entities in an `InitPostEntity` hook, "Called after all the entities
  are initialized" ([GM:InitPostEntity](https://wiki.facepunch.com/gmod/GM:InitPostEntity)).
  - A Workshop map wouldn't start from the command line with `+map` on a client launch.
    A temporary copy of its BSP in `garrysmod/maps` worked. That rests on one try. A
    dedicated server that mounts a Workshop collection at startup can load a Workshop map
    with `+map`
    ([Workshop for Dedicated Servers](https://wiki.facepunch.com/gmod/Workshop_for_Dedicated_Servers)).
  - Both write into the owner's game folder, so ask the owner first, and delete the
    script and the copy afterwards.
  - Checked: seen in Garry's Mod during a port to S&box `26.10.13a`; the wiki as read on
    2026-10-21. Proof: nothing yet.
- **Solve a screenshot's camera instead of hunting for it.** To match an old screenshot's
  viewpoint, trace a few pixels of a rough S&box render to get world points, mark the same
  points in the screenshot, and solve the camera from them with the old game's field of
  view held fixed. The solver's pixel error says how close it got: 2 to 20 pixels on
  `26.10.13a`. A screenshot taken under water carries the old game's underwater tint, and no
  camera matches it.
  - Checked: seen on `26.10.13a`. Proof: the solver's reported pixel error.

## Adding an entry

Any S&box thread that learns something while importing logs it as it goes, in its own
project's lessons list, in this shape:

```text
**<What to do, as one instruction>**
- Kind: general (any S&box project would hit it) or project-only
- Topic: one of this file's sections
- Fails: what went wrong done the obvious way
- Why: the cause, with the line that shows it (`26.10.13:<path>`, lines N-M, or
  `source-sdk-2013@<commit>:<path>`), or "no source"
- Seen on: the S&box version and the date
- Proof: the check that shows the fix works, and what it reported, or "nothing yet"
- Evidence: source, seen, source and seen, or inferred
```

General entries name no project, map, place, coordinate, or project file. Project-only
entries stay in the project. To add a general one here, re-read each cited line at the
current tag, put it under its topic, and fold it into an entry already there when it
covers the same thing.

## Rechecking after an update

1. List the S&box files this reference cites, and which of them changed in the project's
   local `sbox-public` clone between the tag the entries name and the new one:

   ```sh
   grep -oE '26\.10\.13:[^`<]+' examples/sbox/IMPORTING.md | cut -d: -f2 | sort -u > cited.txt
   git -C <sbox-public> diff --stat 26.10.13 <new tag> -- $(cat cited.txt)
   ```

2. For each entry that cites a changed file, re-read its lines at the new tag. Then
   update its citations and `Checked:` line, rewrite it, or drop it.
3. Rerun the proof of any entry the update could affect, and of every seen-only entry
   when that area is next worked on.
4. Drop or rewrite any entry that S&box now handles in an easier or more native way, such
   as a new import format in ModelDoc.

Entries that cite only the Source SDK or Garry's Mod don't change with S&box; recheck
their S&box side.
