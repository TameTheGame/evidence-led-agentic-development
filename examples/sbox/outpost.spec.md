# Example: Outpost (synthetic S&box map spec)

> **Synthetic, target-specific, non-normative.** This example shows the
> [spec format](../../docs/SPEC_FORMAT.md) and [evidence ladder](../../docs/EVIDENCE_LADDER.md) applied to an imaginary
> S&box map area. The outpost, its coordinates, and its owner decisions are invented.
> The C# sketch below uses public APIs checked against `Facepunch/sbox-public` at
> `3915f1a69810026e23d331581266636de89411d5`, but it has not been compiled or run. Confirm
> it against your own pinned engine source before relying on it.

---

The block below is what a project's `spec/outpost.spec.md` would contain.

```markdown
# Outpost

owner: Owner
data: spec/outpost.layout.json

## Intent
A small walled frontier outpost players reach early. One gate, a water tower that works
as a landmark, and two spawn points. It should read clearly at a glance and be easy to
walk without snagging.

## Out of scope
Interiors, lighting mood, ambient audio, NPCs.

## Requirements

### OUT-DATA-01 — The layout file is valid
- state: agreed
- rung: static
- check: lint-layout OUT-DATA-01
- touches: spec/outpost.layout.json
- why: catches duplicate IDs and spawns outside the bounds before anything runs

### OUT-SCENE-01 — The generated scene has exactly one main camera
- state: agreed
- rung: static
- check: lint-scene OUT-SCENE-01
- touches: spec/outpost.layout.json, Code/OutpostGenerator.cs
- why: PlayerController adjusts an existing main camera but does not create one

### OUT-COLL-01 — Every walkable floor in the layout has collision
- state: agreed
- rung: engine
- check: OUT_COLL_01_EveryFloorHasCollision
- touches: spec/outpost.layout.json, Code/OutpostGenerator.cs

### OUT-SPAWN-01 — Every spawn lands on solid ground with room to stand
- state: agreed
- rung: engine
- check: OUT_SPAWN_01_EverySpawnLandsOnSolidGround
- touches: spec/outpost.layout.json, Code/OutpostGenerator.cs

### OUT-ROUTE-01 — A standing player fits along every listed route segment
- state: agreed
- rung: engine
- check: OUT_ROUTE_01_RoutesAreClear
- touches: spec/outpost.layout.json, Code/OutpostGenerator.cs
- why: listed segments are flat; slopes and stairs need a walk test instead

### OUT-SIGHT-01 — The tower top is visible from eye height at both spawns
- state: agreed
- rung: engine
- check: OUT_SIGHT_01_TowerVisibleFromSpawns
- touches: spec/outpost.layout.json, Code/OutpostGenerator.cs

### OUT-SAVE-01 — The generated scene survives save, close, and reopen unchanged
- state: agreed
- rung: editor
- check: editor-check OUT-SAVE-01
- why: runs unattended through tools/editor_check.ps1; it needs S&box 26.10.13 or later

### OUT-NET-01 — A remote client sees and collides with the same walls and gate
- state: agreed
- rung: session
- check: card NET-1

### OUT-FEEL-01 — Walking spawn to gate to tower feels like a frontier outpost
- state: draft
- rung: owner
- check: card FEEL-1
- why: draft until the owner confirms this is the feeling they want

## Cards

### NET-1 (session)
Build: <commit>, filled in when the card is sent.
1. Host the map. Join from a second client.
2. On the client, walk into the north wall, then through the gate.
Pass: the wall blocks you and the gate lets you through, on both machines.
Fail: you pass through the wall, or the gate blocks you.
Stop if: the client can't join.
Reply: GREEN, or RED plus what you saw and on which machine.
Limit: same-machine host and client is fine here; it is not clean-client proof.

### FEEL-1 (owner)
Build: <commit>, filled in when the card is sent.
1. Spawn at the north spawn. Walk to the gate, then to the tower.
2. Judge: does it read as a frontier outpost, and is the path obvious?
Pass: it reads as a frontier outpost, and you find the way without searching.
Fail: it reads as something else, or you had to search for the way.
Stop if: you can't spawn at the north spawn or reach the gate.
Reply: GREEN, or RED plus what felt wrong.
Limit: one person's judgment of one build; it says nothing about collision or online play.
```

---

## Project-owned data (illustrative)

ELAD does not define this schema. The project's generator and tests both read the same
file, so checks follow the data instead of hard-coding positions.

```json
{
  "bounds": { "min": [-1024, -1024, 0], "max": [1024, 1024, 512] },
  "spawns": [
    { "id": "spawn.north", "position": [0, 600, 8] },
    { "id": "spawn.south", "position": [0, -600, 8] }
  ],
  "landmarks": [ { "id": "tower", "top": [400, 0, 480] } ],
  "routes": [
    { "id": "gate-to-tower", "points": [[0, -900, 0], [0, 0, 0], [400, 0, 0]] }
  ]
}
```

## Rung-1 test sketch

This sketch lives in a `UnitTests/` folder of a game or library project. S&box generates
the MSTest project for that folder. `OutpostLayout` and `OutpostGenerator` are
project-owned. The point is that the test builds the area with **the same generator** the
Editor tool uses, then checks the claim with the real engine and no renderer.

```csharp
[TestClass]
public class TestInit
{
	static TestAppSystem _app;

	[AssemblyInitialize]
	public static void Init( TestContext context )
	{
		_app = new TestAppSystem(); // boots the engine headless; needs FACEPUNCH_ENGINE
		_app.Init();
		TestSurfaces.EnsureDefault(); // generated meshes need a default surface; see the rung-1 starter
	}

	[AssemblyCleanup]
	public static void Cleanup() => _app.Shutdown();
}

[TestClass]
public class OutpostTests
{
	[TestMethod]
	public void OUT_SPAWN_01_EverySpawnLandsOnSolidGround()
	{
		var layout = OutpostLayout.Load( Path.Combine( EngineTestHelpers.ProjectRoot(), "spec", "outpost.layout.json" ) );
		var scene = new Scene();
		using var scope = scene.Push();

		OutpostGenerator.Build( scene, layout ); // PolygonMesh + MeshComponent, from data
		// (in a game scene, create each MeshComponent disabled, set Mesh, then enable it;
		// see the rung-1 starter's StarterGeometry)

		foreach ( var spawn in layout.Spawns )
		{
			var go = scene.CreateObject();
			go.WorldPosition = spawn.Position;

			var pc = go.Components.Create<PlayerController>();
			pc.UseInputControls = false;     // no input in a headless test
			pc.EnableFootstepSounds = false; // no audio content mounted

			for ( int i = 0; i < 60 && !pc.IsOnGround; i++ )
				scene.GameTick();

			Assert.IsTrue( pc.IsOnGround, $"{spawn.Id}: never reached ground" );

			var pos = go.WorldPosition;
			Assert.IsFalse( EngineTestHelpers.BodyStartsInsideGeometry( pc ), $"{spawn.Id}: body starts inside geometry" );

			go.Destroy();
		}
	}
}
```

Where the pattern comes from (read these instead of guessing):

- `engine/Tests/Sandbox.Test.Integration/Assembly.cs` for headless engine startup and
  shutdown.
- `engine/Tests/Sandbox.Test.Integration/Scene/Components/PlayerControllerTests.cs` for
  ticking a controller until it is grounded.
- `engine/Tests/Sandbox.Test.Integration/Scene/Components/MeshComponentBuildTests.cs` for
  building a `PolygonMesh` into a `MeshComponent` with collision.
- `engine/Sandbox.Engine/Scene/Components/Game/PlayerController/PlayerController.Trace.cs`
  for `TraceBody`.

The [engine-rung spike](engine-rung-spike/README.md) ran this pattern on S&box `26.10.02`.
It found two things this sketch needs:

- **A default surface.** Building any `PolygonMesh` needs a default physics surface, which
  only test scaffolding can provide.
- **A stronger stuck check.** `StartedSolid` alone misses a body wholly inside mesh
  collision.

The [rung-1 starter](rung1-starter/README.md) has the copyable code for both: its
`TestSurfaces` and `EngineTestHelpers.BodyStartsInsideGeometry`, with `TestInit` and the
`ProjectRoot` the sketch uses. The spike's own kit stays a record and isn't for copying.

## What results look like

Agent report after a task:

```text
OUT-DATA-01   static   pass   a1b2c3d
OUT-SCENE-01  static   pass   a1b2c3d
OUT-COLL-01   engine   pass   a1b2c3d
OUT-SPAWN-01  engine   pass   a1b2c3d
OUT-ROUTE-01  engine   FAIL   a1b2c3d  gate-to-tower blocked at segment 2; diagnosing
OUT-SIGHT-01  engine   pass   a1b2c3d
OUT-SAVE-01   editor   pass   a1b2c3d
OUT-NET-01    session  waiting on OUT-ROUTE-01 before sending card NET-1
OUT-FEEL-01   owner    draft; needs the owner to agree the requirement first
```

`spec/ACCEPTANCE.md` after the owner runs the cards:

```text
2026-10-09 · OUT-NET-01  · GREEN · d4e5f6a · Owner · client blocked by north wall, gate passable
```
