using System;
using System.IO;
using System.Linq;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using Sandbox;
using Assert = Microsoft.VisualStudio.TestTools.UnitTesting.Assert;

namespace EngineTests;

/// <summary>
/// Setup checks, plus one requirement written the way a project's engine tests should be:
/// the test is named after the requirement's check, and its stuck check has a control case
/// that must fail. Rename STARTER-SPAWN-01 to your own requirement, and build the area with
/// your generator instead of StarterGeometry.
/// </summary>
[TestClass]
public class StarterTests
{
	[TestMethod]
	public void Setup_DefaultSurfaceIsAvailable()
	{
		// If this fails, generated meshes can't build in tests on this engine build: stop and
		// report the printed route rather than working around it.
		Console.WriteLine( $"Default surface route: {TestSurfaces.Route}" );

		Assert.IsFalse( TestSurfaces.Route.StartsWith( "unavailable" ), TestSurfaces.Route );
	}

	[TestMethod]
	public void Setup_GeneratedMeshBuildsCollision()
	{
		// A mesh that fails to build doesn't throw here: the engine catches the error and logs
		// it to logs\testhost.log in the install folder. A missing model is the only sign.
		var scene = new Scene();
		using var scope = scene.Push();

		var floor = StarterGeometry.CreateFloor( scene );

		Assert.IsNotNull( floor.Model, "no model was built; read logs\\testhost.log in the S&box install folder" );
		var collisionMeshes = floor.Model.Physics?.Parts.Sum( p => p.Meshes.Count ) ?? 0;
		Assert.AreEqual( 1, collisionMeshes, "expected exactly one collision mesh" );
	}

	[TestMethod]
	public void STARTER_SPAWN_01_SpawnLandsOnSolidGroundWithRoom()
	{
		// STARTER-SPAWN-01 — A spawn lands on solid ground with room to stand.
		var scene = new Scene();
		using var scope = scene.Push();

		StarterGeometry.CreateFloor( scene );

		var pc = EngineTestHelpers.CreatePlayer( scene, new Vector3( 0, 0, 10 ) );
		var landed = EngineTestHelpers.TickUntilGrounded( scene, pc );

		var z = pc.GameObject.WorldPosition.z;
		Assert.IsTrue( landed, $"never landed: z = {z}" );
		Assert.IsTrue( z > -1f && z < 2f, $"landed at the wrong height: z = {z}" );
		Assert.IsFalse( EngineTestHelpers.BodyStartsInsideGeometry( pc ), "body is inside geometry after landing" );
	}

	[TestMethod]
	public void STARTER_SPAWN_01_Control_PlayerInsideBlockIsDetected()
	{
		// Control for the stuck check: a player placed wholly inside a mesh block must be
		// reported. If this fails, the spawn test passing proves nothing about room to stand.
		var scene = new Scene();
		using var scope = scene.Push();

		StarterGeometry.CreateFloor( scene );
		StarterGeometry.CreateBlock( scene, "Starter Block", new Vector3( -64, -64, 0 ), new Vector3( 128, 128, 128 ) );

		var pc = EngineTestHelpers.CreatePlayer( scene, new Vector3( 0, 0, 16 ) );

		Assert.IsTrue( EngineTestHelpers.BodyStartsInsideGeometry( pc ), "a player placed inside a solid block was not detected" );
	}

	[TestMethod]
	public void Setup_SavedSceneLoads()
	{
		// Uses the startup scene S&box's new-game template creates. Its "Plane" has a box
		// collider whose top is at z = 0. Point this at your own scene and floor once you have one.
		const string path = "Assets/scenes/minimal.scene";
		if ( !File.Exists( Path.Combine( EngineTestHelpers.ProjectRoot(), path ) ) )
			Assert.Inconclusive( $"{path} not found; point this test at one of your scenes" );

		var scene = new Scene();
		using var scope = scene.Push();

		Assert.IsTrue( EngineTestHelpers.LoadSavedScene( scene, path ), $"could not load {path}" );

		var tr = scene.Trace.Ray( new Vector3( -150, -150, 100 ), new Vector3( -150, -150, -100 ) ).Run();

		Assert.IsTrue( tr.Hit, "ray missed the saved scene's floor" );
		Assert.AreEqual( "Plane", tr.GameObject?.Name, "ray hit something other than the saved floor" );
		Assert.AreEqual( 0f, tr.EndPosition.z, 1f, "ray should stop at the saved floor's top surface" );
	}
}
