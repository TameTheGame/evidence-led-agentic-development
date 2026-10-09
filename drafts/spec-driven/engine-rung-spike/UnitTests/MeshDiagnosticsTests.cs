using System;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using Sandbox;
using Assert = Microsoft.VisualStudio.TestTools.UnitTesting.Assert;

namespace EladSpike.Tests;

/// <summary>
/// Follow-up to S4 (no model was built, and no engine error was logged). Each test runs one
/// step of the mesh build directly, so an error fails the test with its own stack trace
/// instead of being caught and logged by the engine.
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
}
