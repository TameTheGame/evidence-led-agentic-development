using System.IO;
using System.Linq;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using Outpost;
using Sandbox;
using Assert = Microsoft.VisualStudio.TestTools.UnitTesting.Assert;

namespace EngineTests;

/// <summary>
/// Engine checks for the outpost's requirements, built with the game's own generator.
/// </summary>
[TestClass]
public class OutpostTests
{
	static OutpostLayout Layout() =>
		OutpostLayout.Parse( File.ReadAllText( Path.Combine( EngineTestHelpers.ProjectRoot(), "spec", "outpost.layout.json" ) ) );

	static Vector3 V( float[] a ) => new( a[0], a[1], a[2] );

	[TestMethod]
	public void OUT_COLL_01_EveryFloorHasCollision()
	{
		// OUT-COLL-01 — Every walkable floor in the layout has collision. Floors are the ground
		// and every block whose top is level with the ground's top.
		var scene = new Scene();
		using var scope = scene.Push();
		var layout = Layout();
		OutpostGenerator.Build( scene, layout );

		var groundTop = layout.Ground.Max[2];
		var floors = layout.Blocks
			.Where( b => b.Min[2] + b.Size[2] == groundTop )
			.Select( b => (b.Id, Centre: V( b.Min ) + V( b.Size ) / 2) )
			.Prepend( ("ground", (V( layout.Ground.Min ) + V( layout.Ground.Max )) / 2) )
			.ToList();

		foreach ( var (id, centre) in floors )
		{
			var top = new Vector3( centre.x, centre.y, groundTop );
			var tr = scene.Trace.Ray( top + Vector3.Up * 64, top - Vector3.Up * 64 ).Run();
			Assert.IsTrue( tr.Hit, $"floor '{id}' has no collision" );
			Assert.AreEqual( groundTop, tr.EndPosition.z, 1f, $"floor '{id}' collides at the wrong height" );
		}
	}

	[TestMethod]
	public void OUT_SPAWN_01_EverySpawnLandsOnSolidGround()
	{
		// OUT-SPAWN-01 — Every spawn lands on solid ground with room to stand.
		var scene = new Scene();
		using var scope = scene.Push();
		var layout = Layout();
		OutpostGenerator.Build( scene, layout );

		foreach ( var spawn in layout.Spawns )
		{
			var pc = EngineTestHelpers.CreatePlayer( scene, V( spawn.Position ) );
			var landed = EngineTestHelpers.TickUntilGrounded( scene, pc );
			var z = pc.GameObject.WorldPosition.z;

			Assert.IsTrue( landed, $"{spawn.Id} never landed: z = {z}" );
			Assert.AreEqual( layout.Ground.Max[2], z, 2f, $"{spawn.Id} landed at the wrong height" );
			Assert.IsFalse( EngineTestHelpers.BodyStartsInsideGeometry( pc ), $"{spawn.Id} is inside geometry" );
		}
	}

	[TestMethod]
	public void OUT_SPAWN_01_Control_SpawnInsideTheTowerIsDetected()
	{
		// Control: a player placed wholly inside the generated tower must count as stuck.
		var scene = new Scene();
		using var scope = scene.Push();
		var layout = Layout();
		OutpostGenerator.Build( scene, layout );

		var tower = layout.Blocks.Single( b => b.Id == "tower" );
		var inside = V( tower.Min ) + new Vector3( tower.Size[0] / 2, tower.Size[1] / 2, 16 );
		var pc = EngineTestHelpers.CreatePlayer( scene, inside );

		Assert.IsTrue( EngineTestHelpers.BodyStartsInsideGeometry( pc ), "a player inside the tower was not detected" );
	}
}
