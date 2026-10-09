using System;
using System.IO;
using System.Linq;
using System.Runtime.CompilerServices;
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
	internal static PlayerController CreatePlayer( Scene scene, Vector3 position )
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

	internal static bool BodyStartsInsideGeometry( PlayerController pc )
	{
		// Lifted 2 units so resting contact with the floor doesn't count as being stuck.
		var start = pc.GameObject.WorldPosition + Vector3.Up * 2;
		if ( pc.TraceBody( start, start + Vector3.Up ).StartedSolid )
			return true;

		// StartedSolid misses a body wholly inside mesh collision: a concave mesh is a surface
		// with no interior, and traces don't see its faces from behind (run 4: S7, D4-D6).
		// So probe upward from the body's centre to the first face it can see, then trace back.
		// Any face hit on the way back faces away from the centre, so the centre is inside a
		// closed solid. Public trace API only.
		var centre = start + Vector3.Up * (pc.CurrentHeight * 0.5f);
		var outward = ProbeRay( pc, centre, centre + Vector3.Up * 16384 );
		var back = ProbeRay( pc, outward.EndPosition - Vector3.Up * 0.5f, centre );
		return back.Hit;
	}

	static SceneTraceResult ProbeRay( PlayerController pc, Vector3 from, Vector3 to ) =>
		pc.Scene.Trace.Ray( from, to )
			.IgnoreGameObjectHierarchy( pc.GameObject )
			.WithCollisionRules( pc.Tags )
			.Run();

	[TestMethod]
	public void S0_DefaultSurfaceSetup()
	{
		// Reports which route TestSurfaces used to provide the default physics surface.
		Console.WriteLine( $"Default surface route: {TestSurfaces.Route}" );

		Assert.IsFalse( TestSurfaces.Route.StartsWith( "unavailable" ), TestSurfaces.Route );
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
		// Informational. Without TestSurfaces this failed in run 1; S0 says how it was provided.
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

	[TestMethod]
	public void S8_ProjectSavedSceneLoadsWithCollision()
	{
		// Open question 3: can a test load the project's own saved scene and query its collision?
		// Uses the startup scene S&box's new-game template creates (scenes/minimal.scene). Its
		// "Plane" has a box collider whose top is at z = 0. Public routes only; prints which worked.
		var scene = new Scene();
		using var scope = scene.Push();

		var route = "unavailable: no route loaded the scene";
		if ( scene.LoadFromFile( "scenes/minimal.scene" ) )
		{
			route = "public: Scene.LoadFromFile by resource path";
		}
		else
		{
			var file = new SceneFile();
			file.LoadFromJson( File.ReadAllText( Path.Combine( ProjectRoot(), "Assets", "scenes", "minimal.scene" ) ) );

			if ( scene.Load( file ) )
				route = "public: SceneFile.LoadFromJson on the saved file, then Scene.Load";
		}

		Console.WriteLine( $"Saved scene route: {route}" );
		Assert.IsFalse( route.StartsWith( "unavailable" ), route );

		var tr = scene.Trace.Ray( new Vector3( -150, -150, 100 ), new Vector3( -150, -150, -100 ) ).Run();

		Assert.IsTrue( tr.Hit, "ray missed the saved scene's floor" );
		Assert.AreEqual( "Plane", tr.GameObject?.Name, "ray hit something other than the saved floor" );
		Assert.AreEqual( 0f, tr.EndPosition.z, 1f, "ray should stop at the saved floor's top surface" );
	}

	static string ProjectRoot( [CallerFilePath] string source = "" ) =>
		Path.GetDirectoryName( Path.GetDirectoryName( source ) );
}
