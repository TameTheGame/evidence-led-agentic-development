using System.Collections.Generic;
using System.Text.Json;
using Sandbox;

namespace Outpost;

/// <summary>
/// Builds the outpost into a scene from the layout data (spec/outpost.layout.json).
/// The game calls Build when the outpost scene starts.
/// </summary>
public static class OutpostGenerator
{
	public static void Build( Scene scene, OutpostLayout layout )
	{
		AddGround( scene, V( layout.Ground.Min ), V( layout.Ground.Max ) );

		foreach ( var block in layout.Blocks )
			AddMeshBlock( scene, block.Id, V( block.Min ), V( block.Size ) );
	}

	/// <summary>
	/// The yard's ground: a static box collider whose top is at the layout's ground max z.
	/// Collision only; the ground's look is set up separately.
	/// </summary>
	static GameObject AddGround( Scene scene, Vector3 min, Vector3 max )
	{
		var go = scene.CreateObject();
		go.Name = "ground";
		go.WorldPosition = (min + max) / 2;

		var box = go.Components.Create<BoxCollider>();
		box.Scale = max - min;
		box.Static = true;

		return go;
	}

	/// <summary>
	/// A static box of generated mesh geometry with mesh collision. <paramref name="min"/> is
	/// its lowest corner in world space. Walls, the gate apron, and the tower all use this.
	/// </summary>
	static MeshComponent AddMeshBlock( Scene scene, string id, Vector3 min, Vector3 size )
	{
		var go = scene.CreateObject();
		go.Name = id;
		go.WorldPosition = min;

		var block = go.Components.Create<MeshComponent>();
		block.Collision = MeshComponent.CollisionType.Mesh;
		block.Mesh = BoxMesh( size );

		return block;
	}

	/// <summary>
	/// An axis-aligned box mesh with one corner at the local origin.
	/// </summary>
	static PolygonMesh BoxMesh( Vector3 size )
	{
		var mesh = new PolygonMesh();
		var v = mesh.AddVertices(
			new Vector3( 0, 0, 0 ), new Vector3( size.x, 0, 0 ),
			new Vector3( size.x, size.y, 0 ), new Vector3( 0, size.y, 0 ),
			new Vector3( 0, 0, size.z ), new Vector3( size.x, 0, size.z ),
			new Vector3( size.x, size.y, size.z ), new Vector3( 0, size.y, size.z ) );

		mesh.AddFace( v[0], v[3], v[2], v[1] ); // bottom
		mesh.AddFace( v[4], v[5], v[6], v[7] ); // top
		mesh.AddFace( v[0], v[1], v[5], v[4] );
		mesh.AddFace( v[1], v[2], v[6], v[5] );
		mesh.AddFace( v[2], v[3], v[7], v[6] );
		mesh.AddFace( v[3], v[0], v[4], v[7] );

		return mesh;
	}

	static Vector3 V( float[] a ) => new( a[0], a[1], a[2] );
}

/// <summary>
/// The layout data file, as read by the generator and the tests.
/// </summary>
public sealed class OutpostLayout
{
	public sealed class Box { public float[] Min { get; set; } public float[] Max { get; set; } }
	public sealed class Block { public string Id { get; set; } public float[] Min { get; set; } public float[] Size { get; set; } }
	public sealed class Spawn { public string Id { get; set; } public float[] Position { get; set; } }
	public sealed class Landmark { public string Id { get; set; } public float[] Top { get; set; } }
	public sealed class Route { public string Id { get; set; } public List<float[]> Points { get; set; } = new(); }

	public Box Bounds { get; set; }
	public Box Ground { get; set; }
	public List<Block> Blocks { get; set; } = new();
	public List<Spawn> Spawns { get; set; } = new();
	public List<Landmark> Landmarks { get; set; } = new();
	public List<Route> Routes { get; set; } = new();

	public static OutpostLayout Parse( string json ) =>
		JsonSerializer.Deserialize<OutpostLayout>( json, new JsonSerializerOptions { PropertyNameCaseInsensitive = true } );
}
