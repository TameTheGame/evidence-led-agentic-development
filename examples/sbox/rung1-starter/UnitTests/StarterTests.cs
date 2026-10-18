using System;
using System.IO;
using System.Linq;
using System.Reflection;
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

	[TestMethod]
	public void Setup_SavedSceneSimulates()
	{
		// A loaded scene must finish loading before it simulates. If this fails while
		// Setup_SavedSceneLoads passes, traces work but a player test on a saved scene can't.
		const string path = "Assets/scenes/minimal.scene";
		if ( !File.Exists( Path.Combine( EngineTestHelpers.ProjectRoot(), path ) ) )
			Assert.Inconclusive( $"{path} not found; point this test at one of your scenes" );

		var scene = new Scene();
		using var scope = scene.Push();

		Assert.IsTrue( EngineTestHelpers.LoadSavedScene( scene, path ), $"could not load {path}" );
		Assert.IsFalse( scene.IsLoading, "the saved scene is still loading, so GameTick won't simulate it" );

		var pc = EngineTestHelpers.CreatePlayer( scene, new Vector3( -150, -150, 10 ) );
		var landed = EngineTestHelpers.TickUntilGrounded( scene, pc );

		var z = pc.GameObject.WorldPosition.z;
		Assert.IsTrue( landed, $"never landed on the saved floor: z = {z}" );
		Assert.IsTrue( z > -1f && z < 2f, $"landed at the wrong height: z = {z}" );
	}

	[TestMethod]
	public void Setup_SavedSceneKeepsMeshData()
	{
		// A saved scene keeps mesh and terrain data in a "<scene>_d" file beside it. If this
		// fails, saved meshes load empty in tests and traces pass through them.
		var folder = Path.Combine( Path.GetTempPath(), $"starter-scene-{Guid.NewGuid():N}" );
		Directory.CreateDirectory( folder );
		try
		{
			var path = Path.Combine( folder, "block.scene" );
			var saved = new Scene();
			using ( saved.Push() )
			{
				StarterGeometry.CreateBlock( saved, "Saved Block", new Vector3( -64, -64, -32 ), new Vector3( 128, 128, 32 ) );
				SaveLikeTheEditor( saved, path );
			}
			Assert.IsTrue( File.Exists( path + "_d" ), "the save wrote no _d file, so this test checks nothing" );

			var scene = new Scene();
			using var scope = scene.Push();

			Assert.IsTrue( EngineTestHelpers.LoadSavedScene( scene, path ), $"could not load {path}" );

			var tr = scene.Trace.Ray( new Vector3( 0, 0, 100 ), new Vector3( 0, 0, -100 ) ).Run();

			Assert.IsTrue( tr.Hit, "ray missed the saved block: its mesh loaded without its _d data" );
			Assert.AreEqual( "Saved Block", tr.GameObject?.Name, "ray hit something other than the saved block" );
			Assert.AreEqual( 0f, tr.EndPosition.z, 1f, "ray should stop at the saved block's top surface" );
		}
		finally
		{
			Directory.Delete( folder, true );
		}
	}

	/// <summary>
	/// Writes a scene the way the editor's save does: the JSON, and the binary data in "_d".
	/// Only this self-test uses it; the editor saves a project's own scenes. Scene.CreateSceneFile
	/// and GameResource.SaveToDisk are internal, so it uses reflection.
	/// </summary>
	static void SaveLikeTheEditor( Scene scene, string path )
	{
		var create = typeof( Scene ).GetMethod( "CreateSceneFile", BindingFlags.Instance | BindingFlags.NonPublic );
		var save = typeof( GameResource ).GetMethod( "SaveToDisk", BindingFlags.Instance | BindingFlags.NonPublic,
			null, new[] { typeof( string ), typeof( string ) }, null );
		if ( create is null || save is null )
			Assert.Inconclusive( $"engine internals not found (CreateSceneFile={create is not null}, SaveToDisk={save is not null})" );

		var file = (SceneFile)create.Invoke( scene, null );
		save.Invoke( file, new object[] { path, file.Serialize().ToJsonString() } );
	}
}
