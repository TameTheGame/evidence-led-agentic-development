using System.Linq;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using Sandbox;
using Assert = Microsoft.VisualStudio.TestTools.UnitTesting.Assert;

namespace EladSpike.Tests;

/// <summary>
/// ELAD engine-rung spike: can a project's own UnitTests check map claims headlessly?
/// Each test isolates one capability, so the first failure points at the step that broke.
/// See ../README.md for how to read the results.
/// </summary>
[TestClass]
public class EngineRungTests
{
	static PlayerController CreatePlayer( Scene scene, Vector3 position )
	{
		var go = scene.CreateObject();
		go.Name = "Spike Player";
		go.WorldPosition = position;

		var pc = go.Components.Create<PlayerController>();
		pc.UseInputControls = false;     // no input device in a headless test
		pc.EnableFootstepSounds = false; // no audio content mounted

		return pc;
	}

	static void TickUntilGrounded( Scene scene, PlayerController pc, int maxTicks = 60 )
	{
		for ( int i = 0; i < maxTicks && !pc.IsOnGround; i++ )
			scene.GameTick();
	}

	static bool BodyStartsInsideGeometry( PlayerController pc )
	{
		// Lifted 2 units so resting contact with the floor doesn't count as being stuck.
		var start = pc.GameObject.WorldPosition + Vector3.Up * 2;
		return pc.TraceBody( start, start + Vector3.Up ).StartedSolid;
	}

	[TestMethod]
	public void S1_EngineStartsAndCreatesScene()
	{
		var scene = new Scene();
		using var scope = scene.Push();

		Assert.IsTrue( scene.CreateObject().IsValid() );
	}

	[TestMethod]
	public void S2_Diagnostic_DefaultSurfaceIsAvailable()
	{
		// Informational. Facepunch's own tests install a fallback surface through an internal
		// API before tracing. If this fails but S5-S7 pass, the workaround isn't needed here.
		Assert.IsNotNull( Surface.FindByName( "default" ), "no 'default' surface is loaded" );
	}

	[TestMethod]
	public void S3_PlayerLandsOnBoxColliderFloor()
	{
		// Known-good path: a primitive collider, as in Facepunch's PlayerControllerTests.
		var scene = new Scene();
		using var scope = scene.Push();

		var floor = scene.CreateObject();
		floor.WorldPosition = new Vector3( 0, 0, -50 );
		var box = floor.Components.Create<BoxCollider>();
		box.Scale = new Vector3( 4000, 4000, 100 );
		box.Static = true;

		var pc = CreatePlayer( scene, new Vector3( 0, 0, 10 ) );
		TickUntilGrounded( scene, pc );

		Assert.IsTrue( pc.IsOnGround, $"never landed: {pc.GameObject.WorldPosition}" );
	}

	[TestMethod]
	public void S4_PolygonMeshFloorBuildsCollision()
	{
		var scene = new Scene();
		using var scope = scene.Push();

		var floor = SpikeGeometry.CreateFloor( scene );

		Assert.IsNotNull( floor.Model, "no model was built" );
		Assert.IsTrue( floor.Model.MeshCount > 0, "model has no render mesh" );
		var collisionMeshes = floor.Model.Physics?.Parts.Sum( p => p.Meshes.Count ) ?? 0;
		Assert.AreEqual( 1, collisionMeshes, "expected exactly one collision mesh" );
	}

	[TestMethod]
	public void S5_RayTraceHitsPolygonMeshFloor()
	{
		var scene = new Scene();
		using var scope = scene.Push();

		SpikeGeometry.CreateFloor( scene );

		var tr = scene.Trace.Ray( new Vector3( 0, 0, 100 ), new Vector3( 0, 0, -100 ) ).Run();

		Assert.IsTrue( tr.Hit, "ray missed the floor" );
		Assert.AreEqual( 0f, tr.EndPosition.z, 1f, "ray should stop at the floor's top surface" );
	}

	[TestMethod]
	public void S6_PlayerLandsOnPolygonMeshFloorWithRoomToStand()
	{
		// The shape of a real spawn requirement: lands on ground, not inside anything.
		var scene = new Scene();
		using var scope = scene.Push();

		SpikeGeometry.CreateFloor( scene );

		var pc = CreatePlayer( scene, new Vector3( 0, 0, 10 ) );
		TickUntilGrounded( scene, pc );

		var z = pc.GameObject.WorldPosition.z;
		Assert.IsTrue( pc.IsOnGround, $"never landed: z = {z}" );
		Assert.IsTrue( z > -1f && z < 2f, $"landed at the wrong height: z = {z}" );
		Assert.IsFalse( BodyStartsInsideGeometry( pc ), "body is inside geometry after landing" );
	}

	[TestMethod]
	public void S7_Control_PlayerInsideBlockIsDetected()
	{
		// Control for S6: the "inside geometry" check must actually detect a stuck player.
		// If this fails, S6 passing proves nothing about room to stand.
		var scene = new Scene();
		using var scope = scene.Push();

		SpikeGeometry.CreateFloor( scene );
		SpikeGeometry.CreateBlock( scene, "Spike Block", new Vector3( -64, -64, 0 ), new Vector3( 128, 128, 128 ) );

		var pc = CreatePlayer( scene, new Vector3( 0, 0, 16 ) );

		Assert.IsTrue( BodyStartsInsideGeometry( pc ), "a player placed inside a solid block was not detected" );
	}
}
