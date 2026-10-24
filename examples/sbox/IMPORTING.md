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
- [World geometry](#world-geometry)
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
- **Give `ModelBuilder` bones in model space, not relative to their parents.** The summary
  of `ModelBuilder.Bone` says its position and rotation are relative to the parent
  (`26.10.13:engine/Sandbox.Engine/Resources/Model/Builder/ModelBuilder.Skeleton.cs`, lines
  24-27). But S&box's own Serious Engine mount multiplies each bone by its parents and
  passes the model-space result
  (`26.10.13:engine/Mounting/Sandbox.Mounting.SE3/Model.Skeleton.cs`, lines 43-59). On
  `26.10.13a`, bones given relative to their parents collapsed a skinned mesh into flat
  spikes, and bones in model space drew whole bodies.
  - Checked: source at `26.10.13`; seen on `26.10.13a`. Proof: the ragdolls built this way
    render as whole bodies in a capture.
- **Build a ragdoll from another game at run time with `ModelBuilder`.** Give it bones in
  model space (above), a skinned mesh whose vertices carry `BlendIndices` and
  `BlendWeight`, one `AddBody` per physics bone with that bone's hulls, and a joint for
  each of the ragdoll's joints, as below. Then simulate it with `ModelPhysics`. S&box's
  Serious Engine mount builds skinned, jointed models the same way
  (`26.10.13:engine/Mounting/Sandbox.Mounting.SE3/Model.Mesh.cs`, lines 27-30;
  `26.10.13:engine/Mounting/Sandbox.Mounting.SE3/Model.Physics.cs`, lines 100-280). A
  ragdoll converted to OBJ has no bones, so it compiles only as a statue. Converting to FBX
  or DMX for ModelDoc is the other route; it wasn't tried.
  - Match Source's joint limits. A Source ragdoll limits each of a joint's three axes
    separately. Give a joint with a z range and no y range, such as a knee or an elbow, an
    `AddHingeJoint` with that range (`WithTwistLimit`). A hinge turns about its frames'
    up axis
    (`26.10.13:engine/Sandbox.Engine/Scene/Components/Render/SkinnedModelRenderer.PhysicsBones.cs`,
    lines 283-296), so turn the frames to put that on the joint's z axis. Give every other
    joint an `AddBallJoint`: turn its frames so the swing cone points at the middle of the
    y and z ranges, set its swing limit to half the wider of the two ranges
    (`WithSwingLimit`), and use the x range as its twist (`WithTwistLimit`). With a ball
    joint everywhere, each cone as wide as the joint's largest limit, a ragdoll carried
    with the physics gun folded its knees backwards and sideways.
  - Read Source's limits right-handed, about the child bone's axes in the bind pose.
    Ragdoll poses recorded in Garry's Mod sat inside the limits read that way (6 ragdolls
    checked).
  - Checked: source at `26.10.13`; seen on `26.10.13a`. Proof: a play-mode test that builds
    every ragdoll and counts its bodies (32 ragdolls, 218 bodies), then hangs each from one
    piece: no knee or elbow went past Source's limits, against 11 of 13 with cones.
- **Draw a Source rope at about a third of its `Width` when it's a solid cylinder.** Source
  draws a rope as a flat strip `Width` wide
  (`source-sdk-2013@be57e3d:src/game/client/c_rope.cpp`, line 1812), and the cable
  material's shading leaves only its middle looking solid. Cylinders as wide as `Width`
  looked about three times as thick as in Garry's Mod. The factor, 0.35, was matched by
  eye.
  - Checked: source at `be57e3d`; seen on `26.10.13a` and in Garry's Mod. Proof: nothing
    yet; a side-by-side picture only.

## World geometry

- **Cut an imported 3D skybox out of the playable world.** Source draws the 3D skybox first
  and the world over it, whatever the depth. Rebuilt in S&box, the skybox is ordinary
  geometry drawn in depth with the world, so its ground, scaled up, covered the map's own
  ground near the edges and showed as a floor underground. Cut it out of the playable
  volume, the map's `world_mins` and `world_maxs`, splitting its triangles along those
  bounds. One skybox displacement scaled up can span the whole map, so leaving out pieces
  by their middle can't help.
  - Checked: seen on `26.10.13a`; no source. Proof: captures of the same spots before and
    after.
- **Clean each imported face before `PolygonMesh.AddFace`.** Remove repeated corners and
  spikes, corners the outline runs out to and straight back from. S&box notes a face whose
  triangulation comes back short as bad, and draws nothing for it when fewer than three
  indices come back (`26.10.13:engine/Sandbox.Engine/Scene/Components/Mesh/PolygonMesh.cs`,
  lines 5924-5940). The map compiler writes a few such faces, and clipping brush sides can
  make more: a big door had a hole where four faces weren't drawn. Keep corners that sit on
  a straight edge, since they match the neighbouring face's corners.
  - Checked: source at `26.10.13`; seen on `26.10.13a`. Proof: a test that counts faces
    drawn with part missing: 59 before, 0 of 46,159 after.

## Collision

- **Give a baked ragdoll no collision.** A static copy of a ragdoll, posed where it settled
  in the original game, overlaps what it lies on. With collision on, it pushed the physics
  props under it out of the world on `26.10.13a`. Why it pushes is inferred: S&box
  separates overlapping bodies.
  - Checked: seen on `26.10.13a`; no source. Proof: a play-mode check that no physics
    object falls out of the world.
- **Keep each convex piece of a Source collision model.** A `.phy` solid is a set of convex
  pieces. One hull around the render mesh, ModelDoc's `PhysicsHullFromRender`, fills in
  hollow props, so things sat on top of crates and buckets instead of inside. Write each
  piece as its own OBJ object and import the file with ModelDoc's `PhysicsHullFile`,
  `import_mode` `"HullPerElement"`.
  - The pieces are stored in the physics engine's metres and axes. To get Source inches,
    scale them and swap the axes to (x, z, -y), as read from the files. A prop's pieces are
    in its posed model space; a ragdoll's are in each bone's space.
  - Checked: seen on `26.10.13a`, with the format read from the files; neither ModelDoc's
    importer nor Source's physics engine is in the public source. Proof: the compiled
    models report one hull per Source piece (a bucket 4, a table 6).
- **Take a brush entity's collision and mass from the BSP's physics lump.** The map
  compiler stores each brush model's convex pieces and mass in lump 29
  (`source-sdk-2013@be57e3d:src/public/bspfile.h`, line 310), in the same format as a
  `.phy`. A `func_physbox` reads its solid from there and scales the mass by its
  `massScale` (`src/game/server/physobj.cpp`, lines 509-516). One hull around a brush
  entity made a crate of thin walls solid and hundreds of times too heavy: 5,600 kg instead
  of 26. In S&box, give each piece a `HullCollider` with `Type` `Points`
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/Collider/HullCollider.cs`, lines 15-29
  and 64), and set the mass as the next section says.
  - Checked: source at `be57e3d` and `26.10.13`; seen on `26.10.13a`. Proof: two brush
    signs weigh what Garry's Mod reports for them.
- **Simplify hulls of more than 64 points before `ModelBuilder` gets them.**
  `PhysicsBodyBuilder.AddHull` takes an optional `HullSimplify` and by default uses the
  points as given
  (`26.10.13:engine/Sandbox.Engine/Resources/Model/Builder/PhysicsBodyBuilder.cs`, lines
  172-205;
  `26.10.13:engine/Sandbox.Engine/Resources/Model/Builder/CPhysBodyDescArray.Create.cs`,
  lines 69-74). On `26.10.13a` a 98-point hull came out with no shape at all, which left
  its body massless; with `MaxVerts` 64 every body got its collider. The limit is seen, not
  read: the hull builder is native.
  - Checked: source at `26.10.13`; seen on `26.10.13a`. Proof: a test that every ragdoll
    body has its collider.
- **Split displacement squares in Source's checkerboard.** Source splits each square of a
  displacement's collision surface by the index of its first vertex: an odd index joins the
  next vertex to the one below, an even index joins the first vertex to the one diagonally
  below it (`source-sdk-2013@be57e3d:src/public/builddisp.cpp`, lines 896-962). Splitting
  every square the same way put steep ground up to 22 units from Source's.
  - Checked: source at `be57e3d`; seen on `26.10.13a`. Proof: a test that compares ground
    heights with heights recorded in Garry's Mod (355 of 355 within 1 unit).
- **Make what moves and carries things collide as convex pieces.** A `MeshComponent` with
  `Mesh` collision is concave
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/Mesh/MeshComponent.cs`, line 123), and
  S&box makes every concave collider static, whatever `Static` is set to
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/Collider/Collider.cs`, lines 12-15).
  Moving one doesn't push or carry what's on it: a loose object on a lift's floor stayed
  put and went through the roof as the lift rose, and a player on the lift rose in small
  jumps that shook the view. Give lifts, doors, and trains convex pieces with `Static` off,
  such as a brush entity's pieces from the BSP's physics lump (above).
  - Checked: source at `26.10.13`; seen on `26.10.13a`. Proof: a play-mode test that the
    lift's colliders aren't static, a dropped object rides 3.3 units above its floor, and
    the player's feet stay on it.
- **To make a `MeshComponent` not solid, set its `Collision` to `None`; don't switch it
  off.** `MeshComponent` is a `Collider` that also draws its mesh
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/Mesh/MeshComponent.cs`, line 11), and
  switched off, it deletes what it draws (lines 159-172). A mounted gun's barrels, which
  the map marks not solid, were invisible with their `MeshComponent`s switched off. Setting
  `Collision` rebuilds the model with the new collision (lines 35-47 and 197-200).
  - Checked: source at `26.10.13`; seen on `26.10.13a`. Proof: a play-mode test that the
    gun's two barrels are drawn.
- **Shut the doors before a check that counts traces that hit nothing.** World mesh
  collision is one-sided: a trace that starts behind a face, or slips past a door into the
  wall round it, goes straight through solid walls. A check of whether rooms were open to
  the sky sent rays out through the door beside each light; they went on through the wall
  below and hit nothing, so every room looked as if it stood outside the map. Don't count a
  ray that could have started behind a face either.
  - Checked: seen on `26.10.13a`; no source, as the collision is native code. Proof: a
    check that counts "nothing hit" only with the doors shut.

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
- **Give props a few seconds after the map starts before impacts can break them.** Props
  placed touching are pushed apart when physics starts, and S&box counted that push as an
  impact: 35 stacked crates broke at once. Turn `EnableImpactDamage` off for the first
  seconds (`26.10.13:engine/Sandbox.Engine/Scene/Components/Collider/Rigidbody.cs`, line
  199). Why the push counts is inferred.
  - Checked: seen on `26.10.13a`. Proof: a test that no prop is broken 15 seconds after
    start.
- **Give Source props their own mass and mass centre.** Set `Rigidbody.MassOverride` to the
  mass the model's `.phy` states, turn on `OverrideMassCenter`, and set
  `MassCenterOverride` to its collision model's mass centre
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/Collider/Rigidbody.cs`, lines 110-158
  and 832-835). Without them, S&box works the mass out from the collision shapes: a hollow
  8 kg bucket weighed 99 kg, with its centre off to one side, and rocked on its rope
  without settling. How S&box works it out is native code, so that part is inferred.
  - Checked: source at `26.10.13`; seen on `26.10.13a`. Proof: a test that shoves the
    hanging bucket and checks it comes to rest (it moved 3.6 units and turned 26 degrees
    before the fix, and not at all after).
- **Put prop data and break pieces in the model, then reimport placed props.** In ModelDoc,
  use `GameDataList` with a `GenericGameData` whose `game_class` is `prop_data`, with keys
  such as `health`, `min_impact_damage_speed`, and `impact_damage`, and list break pieces
  in a `BreakPieceList` of `BreakPieceExternal`. `GenericDataList` and `GenericData`, the
  names other Source 2 tools use, stopped the model compiling on `26.10.13a`: "Failed to
  allocate an instance of class 'GenericDataList'". The keys are `ModelPropData`'s and the
  pieces `ModelBreakPiece`'s
  (`26.10.13:engine/Sandbox.Engine/Resources/Model/ModelNodes.cs`, lines 9-27 and 32-86).
  - A `Prop` takes its health from the model
    (`26.10.13:engine/Sandbox.Engine/Scene/Components/Game/Prop.cs`, lines 196-205), passes
    the impact keys to its `Rigidbody` (lines 297-309), and spawns the break pieces (line
    535).
  - It takes the health only when its model changes, not while the scene loads (line 200).
    Props placed before the model had health kept 0 and never broke, so reimport the scene
    after adding prop data.
  - Checked: source at `26.10.13`; seen on `26.10.13a`. Proof: a compiled bottle model
    reports health 5, break speed 79, and 2 break pieces; after a reimport, the props whose
    models have health are breakable.
- **Give break pieces Source's outward burst.** Source sends each break piece away from the
  prop's origin at 100 units a second, or at the piece's own `burst` from the model's break
  data, on top of the prop's own velocity
  (`source-sdk-2013@be57e3d:src/game/server/props.cpp`, line 1728;
  `src/game/shared/props_shared.cpp`, lines 578-580, 617, and 1104-1118). S&box's `Prop`
  only passes the prop's velocity on, halved after an impact
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/Game/Prop.cs`, lines 596-621). A table
  broken with a crowbar seemed to vanish: its pieces lay still where it had stood. Add the
  burst in `Prop.OnGibsCreated` (line 633).
  - Checked: source at `be57e3d` and `26.10.13`; seen on `26.10.13a`. Proof: a play-mode
    test that breaks a table with the crowbar: it falls into 10 pieces, thrown up to 29
    units.
- **Turn Source's impact damage into a break speed.** When a prop hits the world, Source
  squares the speed the prop lost and multiplies by its mass, then by one over that same
  mass, so the mass cancels. It scales that by the prop's `physdamagescale`, 0.1 unless
  set, and reads the damage from a table: the NPC table unless the prop names another, such
  as glass (`source-sdk-2013@be57e3d:src/game/server/physics_impact_damage.cpp`, lines
  109-115, 151-158, and 403-458; `src/game/server/props.cpp`, lines 901-904). S&box deals
  `ImpactDamage` times the speed over `MinImpactDamageSpeed`, and only above that speed.
  Its defaults, 500 and a tenth of the mass
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/Collider/Rigidbody.cs`, lines 199-212
  and 454-487), left glass that never broke from drops and throws. So find the slowest
  impact whose damage reaches the prop's health, set `MinImpactDamageSpeed` to it, and set
  `ImpactDamage` to the health.
  - Props bounce, so they hit faster than the speed they lose: in drops in Garry's Mod,
    about 1.4 times as fast. S&box compares `MinImpactDamageSpeed` with the speed at
    impact, so multiply the speed lost that the table needs by about 1.4.
  - Leave the prop's mass out. A first version that kept it broke tables and chairs dropped
    from knee height. Mass counts only when the other body moves too: Source adds the
    energy that body lost, times its own mass, before dividing (lines 413-429).
  - One hit above that speed then breaks the prop. Source can also wear a prop down with
    several smaller hits, and this doesn't (inferred).
  - Checked: source at `be57e3d` and `26.10.13`; seen on `26.10.13a` and in Garry's Mod.
    Proof: a play-mode test that drops a bottle 40 units, which breaks, and a crate 6,
    which doesn't. In Garry's Mod a bottle broke from a 12-unit drop, and no drop up to 384
    units broke a table or chair.
- **Before retuning props that move too little when hit, compare the weapon's push with
  Source's.** Source pushes a melee hit with 300 for each point of damage, enough to move a
  75 kg body 4 inches a second per point, times `phys_pushscale`, which is 1 by default
  (`source-sdk-2013@be57e3d:src/game/shared/takedamageinfo.cpp`, lines 15, 293-296, and
  347-359). So a 10-point crowbar hit pushes with 3,000. Sandbox's crowbar pushes with
  1,000, its `MeleeWeapon.SwingForce`, read from Sandbox's compiled code. Props matched to
  Garry's Mod for the same shove still moved too little when hit with it. Measure the
  props' side as "Ask the original game what it does", under
  [Faster ways of working](#faster-ways-of-working), says.
  - Checked: source at `be57e3d`; seen on `26.10.13a`. Proof: nothing yet.
- **Don't let anything break a prop the player is carrying.** Carrying pulls a prop through
  whatever is beside it, and a melon lifted out of a crate broke at once. Turn the prop's
  own `EnableImpactDamage` off while it's held. That isn't enough: a `Rigidbody` that
  passes its own break speed also deals 1.2 times its impact damage to what it hits
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/Collider/Rigidbody.cs`, lines 467-510),
  and that is how bottles the carried melon knocked broke it. Also cancel impact damage the
  prop takes while held, in `Prop.OnPropTakeDamage`, which runs before the health comes off
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/Game/Prop.cs`, lines 383-386).
  - Source never lets the player damage a held object. Only a body that weighs 2 kg or more
    and moves faster than the damage table's minimum can hurt it, so the world can't
    (`source-sdk-2013@be57e3d:src/game/server/physics_impact_damage.cpp`, lines 310-317 and
    366-376).
  - Checked: source at `be57e3d` and `26.10.13`; seen on `26.10.13a`. Proof: a play-mode
    test that carries a melon and four bottles around whole. With impact damage left on
    while held, two of three broke.
- **Work out a breakable brush's damage from the scene's collisions.** A component beside a
  static `MeshComponent` never heard a body hit it through `ICollisionListener`, and
  S&box's own impact damage reaches it only from a body that passes its own break speed,
  with S&box's numbers
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/Collider/Rigidbody.cs`, lines 467-510).
  Every contact the physics world reports goes to the scene's `ISceneCollisionEvents`
  components (`26.10.13:engine/Sandbox.Engine/Systems/Physics/3d/ScenePhysicsSystem.cs`,
  lines 88 and 129-171;
  `26.10.13:engine/Sandbox.Engine/Scene/Events/ISceneCollisionEvents.cs`, lines 11-27), so
  listen there for hits on the brush.
  - Work the damage out as Source does: the energy the body lost, times its mass, over the
    breakable's mass (`source-sdk-2013@be57e3d:src/game/server/physics_impact_damage.cpp`,
    lines 403-458). Take the brush's mass from the BSP's physics lump, as under
    [Collision](#collision) above. A glass `func_breakable_surf` reads the glass table and
    breaks above 10 damage (`src/game/server/func_breakablesurf.cpp`, lines 1233-1242). A
    `func_breakable` reads the table its prop data names, or the NPC table
    (`src/game/server/func_break.cpp`, lines 798-816).
  - Checked: source at `be57e3d` and `26.10.13`; seen on `26.10.13a`. Proof: a play-mode
    test that throws a 20 kg tool at a glass pane at 700 units a second, which shatters it
    with 75 damage, and at a breakable window at 900, which breaks it with 500.
- **Write Source's radius damage yourself for an imported map.** S&box's `RadiusDamage`
  measures each target's distance from the target's own position, and checks the line to
  its root object against colliders tagged `map`
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/Game/RadiusDamage.cs`, lines 138-152
  and 185-186). An import that puts every entity under one root object breaks that check.
  Source traces from the blast to the target's middle, takes off the damage over the radius
  for each unit to where that trace ends, and lets the world and doors block it
  (`source-sdk-2013@be57e3d:src/game/shared/gamerules.cpp`, lines 298-317, 334, 381-382,
  and 477-478).
  - An `env_explosion`'s radius is 2.5 per point of damage unless it sets one
    (`src/game/server/explode.cpp`, line 310). A `func_breakable` or `func_physbox` takes
    1.25 times explosion damage (`src/game/server/func_break.cpp`, line 259;
    `src/game/server/physobj.cpp`, line 421; `src/game/server/props.cpp`, lines 82 and
    147-158), and a breakable prop starts at 1 times (`props.cpp`, line 838).
  - Checked: source at `be57e3d` and `26.10.13`; seen on `26.10.13a`. Proof: a play-mode
    test that an explosive set on a breakable brush breaks it.
- **Make hinge friction a motor.** On `26.10.13a`, `HingeJoint.Friction` made no difference
  at any value from 0.5 to 100,000, and hanging signs swung on and on. The component passes
  it to the physics joint only while `Motor` is `Disabled`
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/Joint/HingeJoint.cs`, lines 100 and
  290-298), and that joint hands it to native code
  (`26.10.13:engine/Sandbox.Engine/Systems/Physics/Joints/HingeJoint.cs`, lines 45-48). Set
  `Motor` to `TargetVelocity`, `TargetVelocity` to 0, and `MaxTorque` to the friction
  torque, which goes to `SetAngularMotor` (`Joint/HingeJoint.cs`, lines 305-306).
  - Source's hinge friction torque is `hingefriction` times 1000
    (`source-sdk-2013@be57e3d:src/game/server/physconstraint.cpp`, line 721). Twenty S&box
    torque units per unit of Source's torque matched Garry's Mod.
  - Checked: source at `26.10.13` and `be57e3d`; seen on `26.10.13a` and in Garry's Mod.
    Proof: a test that shoves a hinged sign and times it to rest: within a second, as in
    Garry's Mod.
- **Add a little damping for air drag.** Source slows bodies moving through air; its
  `air_density` command sets "the density of air for drag computations"
  (`source-sdk-2013@be57e3d:src/game/server/physics.cpp`, lines 2844-2859), and Garry's Mod
  reports 2. On `26.10.13a` a swinging object never slowed down. A `Rigidbody` has
  `LinearDamping` and `AngularDamping`
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/Collider/Rigidbody.cs`, lines 54-90),
  and 0.05 of each matched Garry's Mod: a swing lost 30% in 15 seconds, against 27%.
  - Checked: source at `be57e3d` and `26.10.13`; seen on `26.10.13a` and in Garry's Mod.
    Proof: a test that times a swing's decay against Garry's Mod's.
- **Pose a ragdoll before `ModelPhysics` makes its bodies.** `ModelPhysics` starts each
  body at the renderer's bone transform, and at the physics bind pose only when the
  renderer has none
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/Collider/ModelPhysics.PhysicsCreate.cs`,
  lines 233-249). So call `SetBoneTransform` on the renderer first, then enable
  `ModelPhysics`. Bodies made in the bind pose and then moved into place shoved what they
  passed through: a table under two ragdolls was knocked over and broke.
  - Checked: source at `26.10.13`; seen on `26.10.13a`. Proof: a play-mode test that the
    table under them stays put.
- **Keep a ragdoll's pieces from colliding with each other when it starts from a pose
  recorded in another engine.** Recorded poses overlap a little, and S&box kept pushing the
  pieces apart, so two ragdolls never came to rest. Pieces joined by `AddHingeJoint` or
  `AddBallJoint` already skip each other, since `collision` defaults to false for both
  (`26.10.13:engine/Sandbox.Engine/Resources/Model/Builder/ModelBuilder.PhysicsJoints.cs`,
  lines 23-25 and 40-42), but other pairs don't. Turn off collision between all of a
  ragdoll's pieces, and between ragdolls. That Source lets small overlaps rest is inferred
  from Garry's Mod.
  - Checked: source at `26.10.13`; seen on `26.10.13a`. Proof: a test that every ragdoll
    comes to rest (32 of 32; with the pieces colliding, two kept moving).

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
  - The cost: a translucent surface then draws over nearer effects drawn before it. A
    physics gun's beam seen through a translucent grating was hidden behind the grating.
  - Checked: seen on `26.10.13a`. Proof: nothing yet. An editor capture of a chain-link
    material at several distances, with each feature, would settle it.
- **Project a decal that has to wrap a corner.** Source's decals wrap round a corner onto
  the next surface. A decal built as a flat quad trimmed to one surface stops at its edge;
  a projected `Decal` component covers what its box touches, so it wraps.
  - Checked: seen on `26.10.13a`; no source read. Proof: nothing yet.
- **Bring Source's `$selfillum` over as `complex.shader`'s self-illumination, with the base
  texture's alpha as its mask.** In Source, `$selfillum` blends a surface from its lit
  colour to its full, unlit colour times `$selfillumtint`, by the base texture's alpha
  (`source-sdk-2013@be57e3d:src/materialsystem/stdshaders/lightmappedgeneric_ps2_3_x.h`,
  lines 515-518). Imported without it, lamps, screens and consoles came over unlit, and
  their light seemed to come from nowhere. In S&box, switch on `F_SELF_ILLUM` and give
  `TextureSelfIllumMask` an image of that alpha. The glow is the mask times the tint, times
  2 to the power of `g_flSelfIllumBrightness`, times `g_flSelfIllumScale` clamped to 1, and
  by default times the base colour too
  (`26.10.13:game/core/shaders/vr_shared_standard_ps_code.fxc`, lines 145-159 and 365-370).
  So the brightness is in stops, and a scale above 1 does nothing, though the editor allows
  up to 16. Some models share a glowing material but map their part to its dark texels,
  such as a light fitting's "off" version. So find what glows on a model from the mask
  under its own texture coordinates, not from the material it uses.
  - Checked: source at `26.10.13` and `be57e3d`; seen on `26.10.13a`, where `F_SELF_ILLUM`
    is in the private `complex.shader`. Proof: screenshots of the lit fittings, and a
    script that finds each model's glow from the mask under its texture coordinates.
- **Turn the green channel over when converting a Source `$bumpmap` to an S&box normal
  map.** Source's normal maps are DirectX-style, with green pointing down the texture, and
  S&box's are OpenGL-style, with green pointing up. Converted without their bump maps,
  Source's rock walls came over flat and blurry beside Garry's Mod's craggy ones. S&box
  decodes a normal map's colour with no channel swap
  (`26.10.13:game/core/shaders/common/utils/normal.hlsl`, lines 77-80), then turns its y
  over to make up for tools that still build tangent space Source's way
  (`26.10.13:game/core/shaders/common/utils/normal.hlsl`, lines 8-18). Which way green
  should point can't be read from that code alone; the result settled it. The material
  editor also has a "Legacy Source1 Inverted Normals" switch for Source's maps; use it or
  turn green over, not both (inferred).
  - Checked: source at `26.10.13`; seen on `26.10.13b`. The switch was seen, not read: it
    isn't in the public shaders. Proof: the same rock walls pictured in both games from the
    same eye, with their cracks shaded the same way.
- **Draw a live in-world screen with a camera that renders to a texture, shown through a
  glowing material.** Give a `CameraComponent` a `RenderTarget` made with
  `Texture.CreateRenderTarget( name, ImageFormat.RGBA8888, size )`. `RenderTarget` throws
  for a texture that isn't a render target, and a camera with one draws to it instead of
  the screen (`26.10.13:engine/Sandbox.Engine/Scene/Components/Camera/CameraComponent.cs`,
  lines 158-182 and 629-636;
  `26.10.13:engine/Sandbox.Engine/Resources/Textures/Builder/Texture.Create.cs`, lines
  89-98). Set its `IsMainCamera` false, so a player controller doesn't take it as the main
  camera, and switch it off while no one can see the screen, since S&box draws every active
  camera (`26.10.13:engine/Sandbox.Engine/Scene/Scene/Scene.cs`, lines 331-341). Show the
  texture through a copy of the screen's material made with `Material.CreateCopy`
  (`26.10.13:engine/Sandbox.Engine/Resources/Material/Material.cs`, lines 65-71), with
  self-illumination on as the `$selfillum` entry above says, and its `g_tColor` set to the
  texture with `Material.Set( "g_tColor", texture )`
  (`26.10.13:engine/Sandbox.Engine/Resources/Material/Material.Parameters.cs`, line 59).
  The copy kept the texture set at run time. In the editor, a Render Texture asset
  (`.rtex`) in the camera's `RenderTexture` property should do the same job, since
  materials can use one
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/Camera/CameraComponent.cs`, lines
  137-142;
  `26.10.13:engine/Sandbox.Engine/Resources/Textures/Assets/RenderTextureAsset.cs`, lines
  11-12); that way wasn't tried.
  - Checked: source at `26.10.13`; seen on `26.10.13b`. Proof: in play, the screens showed
    their camera's live view, drawn only while a player was near one.

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
- **Bring a Source lamp over with `Attenuation` 16 and its colour 16 times as bright.**
  S&box's point and spot lights fall off as
  `saturate( 10000 / (Attenuation × d²) − the same at the radius )`
  (`26.10.13:engine/Sandbox.SceneRenderer/Pipeline/Features/LightBinnerFeature.Lights.cs`,
  lines 100-114; `26.10.13:game/core/shaders/Shadows/Obsolete.hlsl`, lines 4-13). Source
  scales a lamp so that it has its set brightness at 100 units and falls off with the
  square of the distance (`source-sdk-2013@be57e3d:src/utils/vrad/lightmap.cpp`, lines
  1252-1257). With `Attenuation` 1, S&box matches that only beyond 100 units and stays flat
  closer in, so walls next to lamps looked dull and rooms evenly dim, without the bright
  patch round each lamp. With `Attenuation` 16 and a colour of 16 × brightness / 255, it
  matches down to 25 units. `Attenuation` 1 still has a use: flat within 100 units, it
  leaves no pool or edge, which suits soft fill light. Lights a Source mapper hid for the
  lightmaps, with no lamp model or glowing texture near them, looked like spotlights from
  nowhere when lit live; above ground, soft fill in their place worked. With a radius under
  100 units, though, `Attenuation` 1 stays near full almost to the radius and ends in a
  hard circle.
  - Checked: source at `26.10.13` and `be57e3d`; seen on `26.10.13a`. Proof: screenshots of
    the lit rooms, with their brightness measured, and of a room lit by soft fill.
- **For indoor light, switch off the flat ambient light and bake the bounce into
  `IndirectLightVolume`s.** S&box lights a scene live. A `DirectionalLight`'s `SkyColor`
  and any `AmbientLight` component add a flat light to every surface, underground too
  (`26.10.13:engine/Sandbox.Engine/Scene/Scene/Scene.cs`, lines 424-446), and a Source
  map's sun brings its sky colour with it
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/Map/MapInstance.cs`, lines 768-769). So
  enclosed rooms were lit grey and evenly, with no dark corners. With that light off and
  nothing in its place, they were black between lamps. Bake the bounce instead: a coarse
  volume over the whole map and a finer one, with a probe every 160 units or so, round each
  group of lamps. Where volumes overlap, the smallest is used first
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/IndirectLighting/DDGIVolumeSystem.cs`,
  lines 64-67). A bake renders each probe's view with a black background and no ambient
  light
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/IndirectLighting/DDGIVolumeUpdater.cs`,
  lines 47-55), so it counts the sun's light but not the sky's, and shade outdoors and in
  doorways stayed black. For daylight there, put a large glowing box round the map while
  baking, casting no shadow, and remove it afterwards. A probe grid coarser than a passage
  also leaves the passage black in shade, with its probes inside the walls; give small
  volumes a probe every 64 to 80 units. `BakeProbes` is public and can be awaited from
  `run_csharp`, but it does nothing until the scene has been saved to a file
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/IndirectLighting/IndirectLightVolume.cs`,
  lines 332 and 349-352). A bake took about 25 ms a probe. In dark rooms, the camera's
  `Tonemapping.MaximumExposure` limits how far the eye adapts. It is 3 by default
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/PostProcessing/Effects/Tonemapping.cs`,
  line 82), and 5 let it adapt to the rooms.
  - Checked: source at `26.10.13`; seen on `26.10.13a`. Proof: screenshots of the same
    rooms, and of a shaded entrance, before and after.
- **Where the map's logic switches lamps, bake a volume for each state and switch it with
  them.** A bake holds the light as it was when baked. Baked with the lamps on, rooms whose
  lamps were off glowed with their bounce; baked with the lamps off, lit rooms got no
  bounce. Give each switched group two volumes over the same space, one baked with its
  lamps off and one with them on. Whenever the logic switches the lamps, enable the volume
  that matches (`GameObject.Enabled`). Only enabled volumes are used
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/IndirectLighting/DDGIVolumeSystem.cs`,
  lines 51-56 and 72). Don't switch a volume off while it bakes: that cancels the bake
  (`26.10.13:engine/Sandbox.Engine/Scene/GameObject/GameObject.cs`, lines 67-70;
  `26.10.13:engine/Sandbox.Engine/Scene/Components/IndirectLighting/IndirectLightVolume.cs`,
  line 354).
  - Checked: source at `26.10.13`; seen on `26.10.13a`. Proof: screenshots with the lamps
    off and on.

## Sound and water

Sound lost to key spelling is under [Map logic and entities](#map-logic-and-entities).

- **Give each Source surface property its own S&box surface, with sounds.** Collision
  sounds and a prop's break sound come from the surface of the collider's shape:
  `Surface.PlayCollisionSound` plays its hard or soft impact sound
  (`26.10.13:engine/Sandbox.Engine/Resources/Surface.Effects.cs`, lines 34-58), and a
  `Prop` plays each shape surface's break sound
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/Game/Prop.cs`, lines 490-511). The
  built-in surfaces have no break sound and impact sounds of their own, so props broke
  silently or sounded wrong. Make a `.surface` for each Source surface property, with
  impact, scrape, break, and footstep sounds
  (`26.10.13:engine/Sandbox.Engine/Resources/Surface.Sounds.cs`, lines 13-58), and name it
  on the model's physics shapes.
  - Checked: source at `26.10.13`; seen on `26.10.13a`. Proof: a test that lists each
    prop's surface and its break sound.
- **Give `func_breakable` its `Breakable` sounds, not the surfaces' sounds.** A
  `func_breakable` that breaks plays a `Breakable` sound named for its material, such as
  `Breakable.Glass`, `Breakable.Crate` for wood, or `Breakable.Concrete` for rocks and
  cinder blocks. A hit that doesn't break it plays a `Breakable.Mat` sound, such as
  `Breakable.MatGlass` (`source-sdk-2013@be57e3d:src/game/server/func_break.cpp`, lines
  505-573 and 946-988). Breakables given the prop surfaces' sounds, such as `Glass.Break`,
  asked for two that don't exist, `Concrete.Break` and `Tile.Break`. A
  `func_breakable_surf` pane plays a physics break sound instead
  (`src/game/server/func_breakablesurf.cpp`, line 612).
  - Checked: source at `be57e3d`; seen on `26.10.13a`. Proof: the converted sound list
    resolves all 11 `Breakable` sounds.
- **Make water a trigger tagged `water` with a `WaterVolume`, and add its sounds
  yourself.** `MoveModeSwim` swims in triggers tagged `water`
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/Game/PlayerController/Modes/Swim.cs`,
  lines 54-81), and a `WaterVolume` floats the bodies touching its collider
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/Game/WaterVolume.cs`, lines 95-104).
  Neither plays a sound. Water without a trigger let the player sink to the bottom,
  silently. Give the player a `MoveModeSwim`, and play splash and wading sounds yourself.
  - Source water is brushes with `CONTENTS_WATER`, 0x20, or `CONTENTS_SLIME`, 0x10
    (`source-sdk-2013@be57e3d:src/public/bspflags.h`, lines 30-31). The player plays
    `Player.Wade` going in and out (`src/game/shared/baseplayer_shared.cpp`, lines
    2012-2036) and wading footsteps in the water (lines 586-611).
  - Under water, play the underwater loop and switch on a `DspVolume` with a water preset
    yourself. Source plays `Player.AmbientUnderWater` while the eyes are under water
    (`baseplayer_shared.cpp`, lines 1996-2063) and muffles the sound with its `dsp_water`
    room type, 14, an engine setting outside the SDK. S&box's first 28 DSP presets,
    `metallic.small` to `weird.4`, follow Source's room types 2 to 29 in order, which makes
    14 `water.small` (`26.10.13:engine/Sandbox.Engine/Systems/Audio/Dsp/DspFactory.cs`,
    lines 20-179; the match is inferred from the names). A `DspVolume` mixes in its preset
    while the listener is inside it
    (`26.10.13:engine/Sandbox.Engine/Scene/Components/Audio/Dsp/DspVolumeGameSystem.cs`,
    lines 46-96). One whose `SceneVolume` type is `Infinite` holds the listener anywhere
    (`26.10.13:engine/Sandbox.Engine/Scene/Components/Utility/VolumeSystem/VolumeComponent.cs`,
    lines 9-14), so switch it on and off as the ear goes under and comes out.
  - Inside Facepunch's Sandbox, don't stop at the `water` tag. When the map loads, Sandbox
    gives every collider tagged `water` a `WaterVolume` (read from its compiled code), and
    on `26.10.13a` the installed `WaterVolume`, which isn't the tag's, brings a solid
    `BoxCollider` and floats every body that enters it, players included. The player stood
    on an invisible box, then, with the box gone, bobbed waist deep instead of swimming.
    Remove both, and float loose bodies yourself with `Rigidbody.ApplyBuoyancy`
    (`26.10.13:engine/Sandbox.Engine/Scene/Components/Collider/Rigidbody.Buoyancy.cs`,
    lines 8-23).
  - Checked: source at `26.10.13` and `be57e3d`; seen on `26.10.13a`. Proof: a play-mode
    test that the player swims at the surface and a crate floats, one that hears the
    underwater loop and `water.small` with the ear under water and neither above it, and,
    inside Sandbox, one that the player sinks and swims at the water level and a crate
    floats.
- **Bring Source soundscapes over as `Soundscape` resources played by a `SoundscapeTrigger`
  at each `env_soundscape`, and add Source's line-of-sight rule yourself.** Nothing in
  S&box plays an `env_soundscape`, so a map came over with no ambience. Make a `.sndscape`
  for each soundscape, with a `.sound` for each random sound, and give each
  `env_soundscape` a sphere `SoundscapeTrigger` of its radius. An S&box soundscape can't
  include another (`26.10.13:engine/Sandbox.Engine/Resources/Soundscape.cs`, lines 14-24),
  so fold included soundscapes in at their volume.
  - S&box plays the nearest sphere or box trigger that holds the listener, and by default
    keeps the last one playing when none does
    (`26.10.13:engine/Sandbox.Engine/Scene/GameObjectSystems/SceneSoundscapeSystem.cs`,
    lines 29-48;
    `26.10.13:engine/Sandbox.Engine/Scene/Components/Audio/SoundscapeTrigger.cs`, lines
    62-66 and 200-216), as Source does. Source also needs a line from the `env_soundscape`
    to the player that no brush or water blocks
    (`source-sdk-2013@be57e3d:src/game/server/soundscape.cpp`, lines 258-296), and S&box
    has no such check. So make Source's choice yourself: the nearest `env_soundscape` in
    range with a clear line, which keeps playing until another one qualifies (lines
    235-241). Leave only its trigger switched on, so S&box's picker can't choose
    differently.
  - S&box plays looped sounds at the listener (`SoundscapeTrigger.cs`, line 329) and each
    random sound in a random direction, 50 to 100 units away unless its `Distance` says
    otherwise (lines 390-399; `Soundscape.cs`, line 74). Source plays a random sound whose
    position is "random" 36 units from the ear (`src/game/client/c_soundscape.cpp`, lines
    26 and 833-849).
  - Checked: source at `26.10.13` and `be57e3d`; seen on `26.10.13a`. Proof: a play-mode
    test that every `env_soundscape` got a soundscape (52 of 52), that the right one plays
    at 8 spots, including after flying through a wall, and that it keeps playing after
    leaving every radius.
- **Keep a wave's loop when converting sounds.** Source loops a wave from its first cue
  point, or over its `smpl` loop. Waves converted with only their format and data played
  ambient loops once and stopped. For each wave with a `cue ` or `smpl` chunk, set `loop`,
  `start`, and `end` in its `.wav.meta`, the keys S&box's sound compile settings read
  (`26.10.13:game/addons/tools/Code/Inspectors/SoundFileCompileSettings.cs`, lines 138-140
  and 160-162). The public source doesn't give their units; seconds worked.
  - Checked: source at `26.10.13`; seen on `26.10.13a`; how Source loops a wave isn't in
    the SDK. Proof: a play-mode test that three loops still play a second after their
    length.
- **Give imported Source sounds Source's fade with distance and its cut-off.** A
  `SoundHandle` fades over its `Distance`, 15,000 units unless set, along its `Falloff`
  curve, which is down to 0.22 at 5% of that distance and 0.04 at 20%
  (`26.10.13:engine/Sandbox.Engine/Systems/Audio/SoundHandle.cs`, lines 106-111). Most of a
  Source sound's range was close to silent: of the many sounds a big door makes as it
  opens, only one or two could be heard a few hundred units away. Source's gain is about
  `36 / (distance * 10^((60 - soundlevel) / 20))`, at most 1.
  - Source also has a cut-off. A server sends a sound only to players within
    `2 * 1000 / attenuation` units, where the attenuation is `20 / (soundlevel - 50)`, so
    the cut-off is `100 * (soundlevel - 50)` units: 2,500 at 75 dB
    (`source-sdk-2013@be57e3d:src/game/server/recipientfilter.cpp`, lines 367-412;
    `src/public/soundflags.h`, line 106; `src/public/const.h`, line 428). It applies with
    more than one player, and to ambient sounds only by assumption, since their filter is
    in the engine. Once sounds faded as in Source but without the cut-off, faint machinery
    thousands of units away underground could be heard on the surface, where Source never
    sends it.
  - So set each `SoundHandle`'s `Distance` to the cut-off and its `Falloff` to that gain
    over it.
  - Source's gain formula is in its engine, which the SDK doesn't include. The 36 is the
    SDK's reference distance (`source-sdk-2013@be57e3d:src/game/server/sound.cpp`, line
    52); the 60 dB reference level is inferred.
  - Checked: source at `26.10.13` and `be57e3d`, partly inferred; seen on `26.10.13a`.
    Proof: a play-mode test that every sound Garry's Mod plays near the listener plays and
    reaches it, and one that nothing far away reaches the spawn points.
- **Set an `ambient_generic`'s sound level the way Source does.** One that names a wave
  file plays at a level set by its radius, `40 + 20 * log10(radius / 36)`
  (`source-sdk-2013@be57e3d:src/game/server/sound.cpp`, lines 55-69 and 956-957). One that
  names a soundscript plays at the script's own level and ignores the radius
  (`src/game/shared/SoundEmitterSystem.cpp`, lines 815 and 931-951). Cutting every ambient
  sound off at its radius silenced alarms whose soundscripts carry much further.
  - A `func_rotating` plays a plain wave at the level its radius flag gives: small 60 dB,
    medium 66, and large or none 75 (`src/game/server/bmodels.cpp`, lines 645-660 and
    861-868; `src/public/soundflags.h`, lines 44-46 and 105). A soundscript brings its own
    level. Two generators flagged medium played at 75 dB and carried much further than in
    Source.
  - Checked: source at `be57e3d`; seen on `26.10.13a`. Proof: the play-mode sound tests in
    the entry above; the generators reach 1,600 units.

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
- **Draw a brush that moves in `OnFixedUpdate` with a `ModelRenderer`, and hide its
  `MeshComponent` in game.** Give the `ModelRenderer` the `MeshComponent`'s `Model`, and
  set the `MeshComponent`'s `HideInGame`. S&box smooths a transform moved in fixed update
  between physics steps, and `ModelRenderer` draws the smoothed one
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/Render/ModelRenderer.cs`, lines
  318-323). `MeshComponent` takes `WorldTransform` when the transform changes
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/Mesh/MeshComponent.cs`, lines 217-221),
  but the smoothing raises that change inside a callback where `WorldTransform` is the
  stepped one
  (`26.10.13:engine/Sandbox.Engine/Scene/GameObject/GameTransform/GameTransform.Interpolation.cs`,
  line 251;
  `26.10.13:engine/Sandbox.Engine/Scene/GameObject/GameTransform/GameTransform.TransformChanged.cs`,
  line 26;
  `26.10.13:engine/Sandbox.Engine/Scene/GameObject/GameTransform/GameTransform.cs`, line
  50). So the brush judders on screen: at 50 steps a second on a 60 Hz screen, five frames
  move and one doesn't. A lift looked jittery to its rider while the rider and a box in the
  car looked smooth. Positions logged every frame were smooth too, and only a recording of
  the screen showed it.
  - Checked: source at `26.10.13`; seen on `26.10.13a`. Proof: a recording of the game
    window during a ride, measured frame to frame as
    [the guide](README.md#the-ladder-for-a-map) says: the car's wall held still in the view
    to 0.1 pixels a frame, against 3 pixels on five frames and none on the sixth before.
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
- **Inside Sandbox, implement `IPhysgunEvent` to hear about the physics gun.** Sandbox's
  physics gun calls `OnPhysgunGrab`, `OnPhysgunPickup`, and `OnPhysgunDrop` on the object
  it grabs, and Source's `OnPhysGunPickup` and `OnPhysGunDrop` outputs map onto them. A
  part pulled out of its socket with the physics gun left the socket's pickup output
  unfired, because only carrying the part by hand fired it. Sandbox's code isn't in
  `sbox-public`; this was read from its compiled code, where the interface is public.
  - Checked: seen on `26.10.13a`; no source. Proof: nothing yet.
- **Rebuild `trigger_hurt` from Source's rules.** Nothing in S&box hurts or clicks for one.
  A `trigger_hurt` deals its `damage` per second, in half-second steps, and with
  `damagemodel` 1 it doubles the damage each step up to `damagecap`
  (`source-sdk-2013@be57e3d:src/game/server/triggers.cpp`, lines 798-809, 839, and
  860-879).
  - A radiation one also drives the player's Geiger counter with three times the distance
    from its box to the player (lines 720-727). The counter clicks only while that is above
    0 and under 1000 (`src/game/server/player.cpp`, lines 4269-4306 and 5426-5427;
    `src/game/client/geiger.cpp`, lines 95-104), so it goes quiet inside the box. That is
    how the code reads; it wasn't heard in Garry's Mod.
  - Checked: source at `be57e3d`; seen on `26.10.13a`. Proof: a play-mode test of the
    counter (300 at 100 units outside, 748 at 250, 0 inside). Playing inside Facepunch's
    Sandbox, standing in a doubling one took 0.5, 1.1, 2.0, 4.2, 8.3, then 10.4 health per
    half second.
- **When a breakable entity breaks, remove what's parented to it a tenth of a second
  later.** `CBreakable::Die` removes the entity 0.1 seconds later, and removing an entity
  removes whatever is still parented to it
  (`source-sdk-2013@be57e3d:src/game/server/func_break.cpp`, lines 1109-1116;
  `src/game/server/baseentity.cpp`, lines 2504-2514). Inputs fired at the same moment, such
  as an explosion, still run first. When an explosive physbox's `Break` input did nothing,
  only a button parented to it, which the same output removed, disappeared.
  - Checked: source at `be57e3d`; seen on `26.10.13a`. Proof: a play-mode test that, 11
    seconds after a button press, the explosive and the button are gone and the breakable
    it blew up is cleared.
- **Read a power system's state only from its lamps that start dark.** A map can give an
  always-on lamp the same name as the lamps a power system switches. Read from all of
  them, the power looked on from the start: the bounce light baked for "power on" showed
  with the power off, and doors meant to wait for the power opened. The lamps the system
  switches are the ones with the "start off" flag (see [Lighting](#lighting)).
  - Checked: seen on `26.10.13a`; no source, as it comes from the map's data. Proof: a
    play-mode test that the doors stay shut until the system's lamps come on.

## Player movement

To test walking without a keyboard, see
[Lessons from a world build](README.md#lessons-from-a-world-build).

- **Let the player off a ladder at its foot.** `MoveModeLadder` keeps climbing the ladder
  trigger it's on, starts climbing one that reaches at least halfway up the player, and
  moves only up and down
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/Game/PlayerController/Modes/Ladder.cs`,
  lines 118-142 and 176). So a ladder trigger that reaches the floor kept the player
  climbing at its foot. Make a subclass that lets go when the player moves down onto the
  ground or jumps, and ignores that ladder until the player moves clear of it or walks back
  into it.
  - Checked: source at `26.10.13`; seen on `26.10.13a`. Proof: a play-mode test that climbs
    down and checks the player is walking and clear of the ladder.
- **Keep the player's body awake while it stands on anything that moves.**
  `PlayerController` keeps a walking player on the floor by snapping it down each step, but
  skips that while its body sleeps
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/Game/PlayerController/PlayerController.Ground.cs`,
  lines 67-74), and a body standing still falls asleep. Waking it once the floor has moved
  is too late, because the floor is already out of reach. A player at rest on a lift
  setting off down hung in the air for a quarter of a second, then dropped about 10 units
  onto the floor, which looked like the lift juddering. So keep the body awake for as long
  as the collider under it isn't static: each fixed update, set its physics body's
  `Sleeping` to false, as the controller does when it changes mode
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/Game/PlayerController/PlayerController.Mode.cs`,
  lines 18-21), while `GroundComponent` is a `Collider` whose `Static` is false
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/Collider/Collider.cs`, lines 12-16). A
  concave collider always counts as static, but one that moves should collide as convex
  pieces anyway (see [Collision](#collision)).
  - Checked: source at `26.10.13`; seen on `26.10.13a`. Proof: a play-mode test that rides
    a lift down from rest: the feet stayed 0.0 units above the floor from the first step,
    against 9.7 when the body was only woken after the floor moved.

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
- **In a `run_csharp` check, wait for the next frame with a delay, not `GameTask.Yield`.**
  `GameTask.Yield` awaits `Task.Yield`
  (`26.10.13:engine/Sandbox.Engine/Systems/Threads/TaskSource.cs`, lines 15 and 575-579),
  which on `26.10.13a` resumed within the same frame, so whatever the game does each frame
  hadn't run. A check counted 7,920 yields in a second at about 140 frames a second, and
  another read a value the game resets every frame four times after yields and saw it
  unchanged. `TaskSource.Frame` waits for the next frame's update (lines 584-588), but the
  static `GameTask` has no `Frame`. Wait with `GameTask.DelaySeconds` instead: with
  0.2-second delays, the value was reset each time.
  - Checked: source at `26.10.13`; seen on `26.10.13a`. Proof: nothing yet.
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
- **Register files written while the Editor is open, compile the ones you rewrite, and
  leave alone the ones whose bytes haven't changed.** `AssetSystem.FindByPath` looks only
  in the Editor's list of known assets, and `RegisterFile`'s summary says to register an
  asset you just created (`26.10.13:engine/Sandbox.Tools/Assets/AssetSystem.cs`, lines
  196-219 and 266-283). On `26.10.13a`, new models weren't found until they were
  registered, so register each new file before compiling it. The Editor recompiles most
  files it already knows when they're rewritten, but not all: after a pass that rewrote
  several materials, one loaded as `materials/error.vmat` while the others had recompiled.
  So after rewriting files, find each with `AssetSystem.FindByPath`, or register it if it's
  new, and call its `Compile( true )`, which forces a recompile
  (`26.10.13:engine/Sandbox.Tools/Assets/Asset.cs`, lines 303-307). Each rewrite costs a
  recompile even when nothing in the file changed, and a write can hit a file the Editor
  has open. A converter that rewrote all of its several hundred materials and textures on
  every run had the Editor recompile them all, and some of its writes failed with
  "Permission denied". One model file couldn't be written while the Editor was compiling it
  either, though running that step again worked. So a converter that may run while the
  Editor is open should compare each file's new bytes with the old and write only the ones
  that differ.
  - Checked: source at `26.10.13`; seen on `26.10.13a` and `26.10.13b`. Proof: after
    registering, all 245 new surfaces, sounds, and piece models compiled; a script that
    compiles each rewritten material fixed the stale one; a converter that writes only
    changed files rewrote one material when only one had changed.
- **To play a map inside Facepunch's Sandbox, make the map's own project an addon.** Give
  its project `Type` `"addon"` and `ParentPackage` `"facepunch.sandbox"` in its `Metadata`,
  and keep it one project. Sandbox brings the player, camera, physics gun, weapons, and
  health. Switch your own player and camera off when `Game.Ident` isn't your project's, and
  give Sandbox's players any extras of yours from a `GameObjectSystem` as they spawn. A
  second project with its folders linked to the first left two projects to choose between,
  and the map's own player and camera got in Sandbox's way. `ParentPackage` is a key a
  project's metadata can carry
  (`26.10.13:engine/Launcher/StandaloneTest/Widgets/ProjectTemplate.cs`, line 13), an
  addon's editor session loads that package as the running game
  (`26.10.13:engine/Sandbox.Tools/StartupLoadProject.cs`, lines 204-212), and in play
  `Game.Ident`, "the current game's ident", was `facepunch.sandbox`
  (`26.10.13:engine/Sandbox.Engine/Game/Game/Game.cs`, lines 61-63).
  - The game's project settings apply, not the addon's. A game mounts its own package's
    `ProjectSettings` (`26.10.13:engine/Sandbox.GameInstance/GameInstance.cs`, line 326),
    so in play the addon's `Input.config` and `Collision.config` were ignored, and
    `ProjectSettings.Input` and `ProjectSettings.Collision` listed Sandbox's actions and
    tags. Use the game's input actions, and add the collision pairs you need when the scene
    loads, through `Scene.PhysicsWorld.CollisionRules`
    (`26.10.13:engine/Sandbox.Engine/Systems/Physics/PhysicsWorld.cs`, lines 73-77).
    Without that, ragdoll pieces collided with each other again, break pieces blocked the
    player, and noclip had no key.
  - Sandbox's `Player` component turns the controller's `UseInputControls` back on every
    frame (read from its compiled code). A check that steers the player itself with
    `WishVelocity` has to switch that component off first; until then, ladder, lift, and
    use checks didn't move the player at all.
  - Checked: source at `26.10.13`; seen on `26.10.13a`. Proof: in play, `Game.Ident` is
    `facepunch.sandbox` and the project settings are Sandbox's, and every play-mode check
    passes with Sandbox's player (it climbs a ladder 49 units in 2 seconds).
- **Trigger a game's input action from code with `Input.SetAction`.** Call
  `Input.SetAction( action, true )` for one frame from a `GameObjectSystem` at
  `Stage.StartUpdate`, and the game's own code sees `Input.Pressed` for it: `Pressed` means
  down now and not down in the last command, and `SetAction` is public
  (`26.10.13:engine/Sandbox.Engine/Systems/Input/Input.Actions.cs`, lines 118-123 and 140).
  `Input.Clear( action )` at the same point hides an action from the game's code (line
  149). Use them for an action the game binds to no key, or in a check. Sandbox's noclip
  had no key and its toggle is private, so this was the way to give it Garry's Mod's key
  and console command without copying it.
  - Checked: source at `26.10.13`; seen on `26.10.13a`. Proof: a play-mode test that
    toggles noclip this way, and one in which a player working a mounted gun stays put
    while it fires.
- **In play, keep the game's own camera and switch off the cameras the map brings.** A
  player controller, Sandbox's included, drives the scene's main camera instead of bringing
  its own. The main camera is the first with `IsMainCamera`, then by `Priority`
  (`26.10.13:engine/Sandbox.Engine/Scene/Scene/Scene.Camera.cs`, lines 12-16), and S&box
  draws every active camera in `Priority` order
  (`26.10.13:engine/Sandbox.Engine/Scene/Scene/Scene.cs`, lines 331-341). So a still camera
  of equal priority drew over the player's view, and the view stayed on a fixed spot.
  Switching off all the scene's cameras made it worse, since one was the camera Sandbox
  drives. Keeping `Scene.Camera` and switching off the rest fixed that, but `Scene.Camera`
  was the map's plain camera: the player drove it, and Sandbox's own camera, which carries
  its colour grading, bloom, and physics gun highlight, sat switched off. So keep the
  game's camera as the main one, and switch off the map's.
  - Checked: source at `26.10.13`; seen on `26.10.13a`. Proof: nothing yet; in play, the
    main camera was Sandbox's, at the player's eyes, and the map's was off.
- **Trace again when a trace starts inside a collider.** On `26.10.13a`, a trace that
  started inside a collider reported that collider as its hit, with `StartedSolid` set
  (`26.10.13:engine/Sandbox.Engine/Scene/Scene/Scene.Trace.cs`, lines 770-774; which
  collider comes back is decided in native code). An explosion sits inside the explosive,
  so every line from it to the explosives around it stopped at once, and a chain reaction
  never spread. So trace again, ignoring the collider the trace started in. How Source's
  trace treats a solid it starts in is engine code outside the SDK, and the chain wasn't
  measured in Garry's Mod.
  - Checked: source at `26.10.13`; seen on `26.10.13a`. Proof: a play-mode test in which
    one hit sets off a chain of 22 explosives; none spread before the fix.
- **In a check that throws a prop, set its position and velocity but leave its rotation.**
  Resetting a long prop's rotation before throwing it stopped it dead three times in a row,
  most likely because its end started inside a wall. The same throw with the rotation left
  alone worked at once.
  - Checked: seen on `26.10.13a`; no source. Proof: the throw lands in the play-mode test
    that uses it.
- **Give each `sbox-cli` call a timeout longer than its work, and after a timeout, stop and
  look before you retry or save.** `sbox-cli` waits 300 seconds for a call unless
  `--request-timeout` gives another number of seconds, from 1 to 86400
  (`26.10.13:engine/Launcher/SboxCli/Options.cs`, line 40;
  `26.10.13:engine/Launcher/SboxCli/skills/sbox-cli/references/protocol.md`, lines 43-44).
  When a call runs past it, `sbox-cli` says it "exceeded --request-timeout. The outcome of
  an already running tool is unknown" and closes the connection
  (`26.10.13:engine/Launcher/SboxCli/Program.cs`, lines 379 and 472). Closing it cancels
  the script's `cancellationToken`, but only cooperatively: a script that doesn't check the
  token runs on in the editor
  (`26.10.13:engine/Sandbox.Engine/Systems/Mcp/McpPipeServer.cs`, lines 89 and 146-148;
  `26.10.13:engine/Sandbox.Engine/Systems/Mcp/ScriptTools.cs`, line 64;
  `26.10.13:engine/Launcher/SboxCli/skills/sbox-cli/references/protocol.md`, lines
  132-135). A bake script that ran past the timeout had switched lamps off for its bake.
  Its retries did nothing, because `BakeProbes` returns at once while that volume is still
  baking
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/IndirectLighting/IndirectLightVolume.cs`,
  line 351). The scene was then saved with the lamps still off: the first call's `finally`
  block, which switched them back on, ran later. Another time, a loop that sent bake calls
  with the default timeout sent five whose bakes overlapped: one volume was baked twice,
  each call switched the lamps for its own volume, and the whole bake had to be redone. So
  pass `--request-timeout` longer than the call's work, and split long work into calls that
  each fit, such as one volume per call, sized from a measured rate. When a call says it
  exceeded the timeout, don't send it again: check what the editor is doing and what the
  scene holds before another call or a save.
  - Pass the script's `cancellationToken` to long engine calls and check it in loops, so a
    timeout stops the work instead of leaving it running. `BakeProbes` takes one and, when
    it's cancelled, keeps the volume's last bake
    (`26.10.13:engine/Sandbox.Engine/Scene/Components/IndirectLighting/IndirectLightVolume.cs`,
    lines 349-397). That a timeout then stops a bake cleanly is inferred, not seen.
  - Checked: source at `26.10.13`; seen on `26.10.13a` and `26.10.13b`. Proof: a bake
    script, called with a timeout longer than its work, that starts a volume only when its
    estimated time fits and stops when a call times out.
- **To find files a scene no longer uses, compare its references without regard to case,
  and with `_c` removed.** S&box writes baked files into a folder beside the scene, such as
  `outpost_scene_data/` for `outpost.scene`
  (`26.10.13:engine/Sandbox.Tools/Scene/Session/SceneEditorSession.cs`, lines 593-625), in
  the casing it's given. A light bake writes `<object>_Irradiance_<id>_<bake>.vtex_c`
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/IndirectLighting/IndirectLightVolume.cs`,
  lines 376-378 and 484). The path the folder hands back is lower-cased
  (`26.10.13:engine/Sandbox.Tools/Scene/Session/SceneEditorSession.cs`, line 638;
  `26.10.13:engine/Sandbox.System/Extend/StringExtensions.cs`, lines 85 and 120-123), and
  loading the texture drops the `_c`
  (`26.10.13:engine/Sandbox.Engine/Resources/Textures/Texture.Load.cs`, lines 62-68), so
  the scene stores `<object>_irradiance_<id>_<bake>.vtex`. Each bake writes new files and
  leaves the old ones
  (`26.10.13:engine/Sandbox.Engine/Scene/Components/IndirectLighting/IndirectLightVolume.cs`,
  line 374), so the folder grows with every bake. A clean-up that matched names exactly
  found no file in use and deleted the current bake too, which then had to be baked again.
  Compare paths the way S&box does (`26.10.13:engine/Sandbox.Engine/Resources/Resource.cs`,
  lines 70-80): lower case, forward slashes, no leading slash and no `_c`.
  [Clearing out generated files](README.md#clearing-out-generated-files) has the steps and
  a check.
  - Checked: source at `26.10.13`; seen on `26.10.13a`. Proof:
    [`tools/scene_refs.py`](tools/scene_refs.py) passes its test on a throwaway project
    laid out the same way, and fails its controls; it hasn't yet run on a real project.
- **In Python, write files that shell scripts read with `newline='\n'`.** On Windows,
  Python's text mode turns each `\n` it writes into `\r\n` unless `newline` says otherwise
  ([Python's `open`](https://docs.python.org/3/library/functions.html#open)). With its
  default settings, bash's `read` splits a line only on spaces, tabs and newlines, so it
  keeps the `\r` on the line's last field. A list of points written by Python and read in
  bash put `104\r` into a generated `run_csharp` script, which then failed to compile at
  every point, and a run of 108 screenshots all showed the same view. Open such files with
  `newline='\n'`, or pass it to `Path.write_text` (Python 3.10 and newer), or strip the
  `\r` in bash with `tr -d '\r'`.
  - Checked: Python's documentation; seen on Windows. Proof: nothing yet.

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
  - Measure physics instead of tuning it by eye. Have the script shove an object and sample
    it every 0.1 seconds, give the S&box copy the same shove, and match the curves. The
    hinge, air drag, and mass entries above were tuned this way.
  - To record a ragdoll's pose on the server, read each limb from its physics object.
    There, `GetBoneMatrix` gave a ragdoll's feet at the entity's origin with no rotation.
  - Check the map in plain Garry's Mod before copying behaviour someone remembers from an
    old server: a server's gamemode and addons add rules the map doesn't have. Doors and a
    lift remembered as locked until the power came on opened without it in the map itself.
  - Checked: seen in Garry's Mod during a port to S&box `26.10.13a`; the wiki as read on
    2026-10-21. Proof: the physics entries' tests, which compare with Garry's Mod's
    records, and a test that the same doors and buttons start locked as in Garry's Mod.
- **Solve a screenshot's camera instead of hunting for it.** To match an old screenshot's
  viewpoint, trace a few pixels of a rough S&box render to get world points, mark the same
  points in the screenshot, and solve the camera from them with the old game's field of
  view held fixed. The solver's pixel error says how close it got: 2 to 20 pixels on
  `26.10.13a`. A screenshot taken under water carries the old game's underwater tint, and no
  camera matches it.
  - Checked: seen on `26.10.13a`. Proof: the solver's reported pixel error.
- **Run the case with the fix switched off before writing a fix.** When S&box seems to lack
  something, run the case without your fix first. A system to wake props whose table moves
  was written, then a run without it showed S&box already wakes them, so it came out. This
  goes with searching the engine source first, as the multiply decal entry says.
  - Checked: seen on `26.10.13a`. Proof: the run with the fix off, in which none of 72
    props was left hanging.
- **When something of the parent game misbehaves in a map running inside it, try a bare
  addon project first.** Make an `.sbproj` with `ParentPackage` and nothing else, and see
  whether the fault is there too before tracing your own code. A weapon's swing that didn't
  animate inside Facepunch's Sandbox was traced through weapon and view-model code for a
  long time before a bare project showed the same thing: it was Sandbox's own bug. Delete
  the bare project afterwards, as [Throwaway projects](README.md#throwaway-projects) says.
  - Checked: seen on `26.10.13a`. Proof: nothing yet.
- **Check an engine type's members in the running editor before writing code from the
  engine source.** List them by reflection through `run_csharp`. The installed build can
  differ from the nearest `sbox-public` tag: code written from `26.10.13` didn't compile
  against the installed `26.10.13a`. The tag's `WaterVolume` has `FluidDensity` and
  `IgnoreTags` (`26.10.13:engine/Sandbox.Engine/Scene/Components/Game/WaterVolume.cs`,
  lines 16 and 58); the installed one has neither, and requires a `BoxCollider`. No version
  of that file in `sbox-public` had the installed members, so its history didn't help
  either. This adds to the
  [S&box skill](skills/sbox-engine-reference/SKILL.md#the-engine-source-is-ground-truth)'s
  advice to compare dates.
  - Checked: source at `26.10.13`; seen on `26.10.13a`, whose engine is dated four days
    after the tag. Proof: nothing yet.

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
