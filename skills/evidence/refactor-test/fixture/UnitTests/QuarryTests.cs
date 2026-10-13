using System.IO;
using System.Linq;
using Frontier;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using Sandbox;
using Assert = Microsoft.VisualStudio.TestTools.UnitTesting.Assert;

namespace EngineTests;

/// <summary>
/// Engine checks for the quarry's requirements, built with the game's own generator.
/// </summary>
[TestClass]
public class QuarryTests
{
	static AreaLayout Layout() =>
		AreaLayout.Parse( File.ReadAllText( Path.Combine( EngineTestHelpers.ProjectRoot(), "spec", "quarry.layout.json" ) ) );

	static Vector3 V( float[] a ) => new( a[0], a[1], a[2] );

	[TestMethod]
	public void QRY_COLL_01_EveryFloorHasCollision()
	{
		// QRY-COLL-01 — Every walkable floor in the layout has collision. Floors are the ground
		// and every block whose top is level with the ground's top.
		var scene = new Scene();
		using var scope = scene.Push();
		var layout = Layout();
		AreaGenerator.Build( scene, layout );

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
	public void QRY_SPAWN_01_EverySpawnLandsOnSolidGround()
	{
		// QRY-SPAWN-01 — Every spawn lands on solid ground with room to stand.
		var scene = new Scene();
		using var scope = scene.Push();
		var layout = Layout();
		AreaGenerator.Build( scene, layout );

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
	public void QRY_SPAWN_01_Control_SpawnInsideTheCrusherIsDetected()
	{
		// Control: a player placed wholly inside the generated crusher must count as stuck.
		var scene = new Scene();
		using var scope = scene.Push();
		var layout = Layout();
		AreaGenerator.Build( scene, layout );

		var crusher = layout.Blocks.Single( b => b.Id == "crusher" );
		var inside = V( crusher.Min ) + new Vector3( crusher.Size[0] / 2, crusher.Size[1] / 2, 16 );
		var pc = EngineTestHelpers.CreatePlayer( scene, inside );

		Assert.IsTrue( EngineTestHelpers.BodyStartsInsideGeometry( pc ), "a player inside the crusher was not detected" );
	}
}
