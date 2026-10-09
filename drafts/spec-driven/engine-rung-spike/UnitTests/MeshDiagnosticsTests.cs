using System;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using Sandbox;
using Assert = Microsoft.VisualStudio.TestTools.UnitTesting.Assert;

namespace EladSpike.Tests;

/// <summary>
/// D1-D3 follow up S4 (no model was built, and no engine error was logged). Each runs one
/// step of the mesh build directly, so an error fails the test with its own stack trace
/// instead of being caught and logged by the engine. D4-D7 follow up S7 (stuck detection).
/// </summary>
[TestClass]
public class MeshDiagnosticsTests
{
	[TestMethod]
	public void D1_PolygonMeshRebuildsIntoModel()
	{
		// The mesh itself, outside any component.
		var scene = new Scene();
		using var scope = scene.Push();

		var model = SpikeGeometry.Box( new Vector3( 128, 128, 32 ) ).Rebuild();

		Assert.IsNotNull( model, "PolygonMesh.Rebuild() returned null" );
		Assert.IsTrue( model.MeshCount > 0, "the rebuilt model has no render mesh" );
	}

	[TestMethod]
	public void D2_ComponentStateAfterEnable()
	{
		// Did the component actually become active, and did it build?
		var scene = new Scene();
		using var scope = scene.Push();

		var block = SpikeGeometry.CreateFloor( scene );
		var state = $"Enabled={block.Enabled} Active={block.Active} ObjectActive={block.GameObject.Active} " +
			$"HasMesh={block.Mesh is not null} HasModel={block.Model is not null}";
		Console.WriteLine( state );

		Assert.IsTrue( block.Active, $"the component never became active: {state}" );
		Assert.IsNotNull( block.Model, $"active, but no model: {state}" );
	}

	[TestMethod]
	public void D3_FloorBuildsInEditorScene()
	{
		// The same floor in an editor scene, where assigning a mesh rebuilds it directly.
		var scene = Scene.CreateEditorScene();
		using var scope = scene.Push();

		var block = SpikeGeometry.CreateFloor( scene );

		Assert.IsNotNull( block.Model, "no model in an editor scene either" );
	}

	// Follow-up to S7 (run 3): a body wholly inside a mesh-collision block was not detected.
	// Mesh collision is a concave triangle surface, not a solid volume, so a body that touches
	// no triangle may not register. D4-D6 isolate that, using the same check as S6 and S7.

	[TestMethod]
	public void D4_BodyInsideHullBlockIsDetected()
	{
		// Same placement as S7, but the block has hull (convex, solid) collision.
		var scene = new Scene();
		using var scope = scene.Push();

		SpikeGeometry.CreateBlock( scene, "Hull Block", new Vector3( -64, -64, 0 ), new Vector3( 128, 128, 128 ),
			MeshComponent.CollisionType.Hull );

		var pc = EngineRungTests.CreatePlayer( scene, new Vector3( 0, 0, 16 ) );

		Assert.IsTrue( EngineRungTests.BodyStartsInsideGeometry( pc ), "a body wholly inside a hull block was not detected" );
	}

	[TestMethod]
	public void D5_BodyCrossingMeshBlockFaceIsDetected()
	{
		// Mesh collision, but the body crosses the block's top face (z = 128) instead of
		// sitting wholly inside it.
		var scene = new Scene();
		using var scope = scene.Push();

		SpikeGeometry.CreateBlock( scene, "Mesh Block", new Vector3( -64, -64, 0 ), new Vector3( 128, 128, 128 ) );

		var pc = EngineRungTests.CreatePlayer( scene, new Vector3( 0, 0, 100 ) );

		Assert.IsTrue( EngineRungTests.BodyStartsInsideGeometry( pc ), "a body crossing a mesh block's face was not detected" );
	}

	[TestMethod]
	public void D6_RayFromInsideMeshBlockSeesFace()
	{
		// From the middle of a mesh-collision block, straight up through its top face (z = 128).
		var scene = new Scene();
		using var scope = scene.Push();

		SpikeGeometry.CreateBlock( scene, "Mesh Block", new Vector3( -64, -64, 0 ), new Vector3( 128, 128, 128 ) );

		var tr = scene.Trace.Ray( new Vector3( 0, 0, 64 ), new Vector3( 0, 0, 256 ) ).Run();
		var state = $"Hit={tr.Hit} StartedSolid={tr.StartedSolid} EndZ={tr.EndPosition.z} Normal={tr.Normal}";
		Console.WriteLine( state );

		Assert.IsTrue( tr.Hit, $"a ray from inside a mesh block saw no face: {state}" );
	}

	[TestMethod]
	public void D7_BodyUnderMeshCeilingIsNotFlagged()
	{
		// Control for the enclosure probe added after run 4: a ceiling above a standing player
		// is a face the probe sees from below, so it must not count as being inside geometry.
		var scene = new Scene();
		using var scope = scene.Push();

		SpikeGeometry.CreateFloor( scene );
		SpikeGeometry.CreateBlock( scene, "Ceiling", new Vector3( -256, -256, 100 ), new Vector3( 512, 512, 32 ) );

		var pc = EngineRungTests.CreatePlayer( scene, Vector3.Zero );

		Assert.IsFalse( EngineRungTests.BodyStartsInsideGeometry( pc ), "a player standing under a ceiling was flagged as stuck" );
	}
}
