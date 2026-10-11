using Sandbox;

namespace EngineTests;

/// <summary>
/// Stand-in geometry for the starter tests. In a real project, build the area with the
/// project's own generator instead, so the tests check the code the game runs.
/// </summary>
static class StarterGeometry
{
	/// <summary>
	/// An axis-aligned box mesh with one corner at the local origin.
	/// </summary>
	public static PolygonMesh Box( Vector3 size )
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

	/// <summary>
	/// A static block with mesh collision. <paramref name="min"/> is its lowest corner in world
	/// space.
	/// </summary>
	public static MeshComponent CreateBlock( Scene scene, string name, Vector3 min, Vector3 size )
	{
		var go = scene.CreateObject();
		go.Name = name;
		go.WorldPosition = min;

		// Outside an editor scene, MeshComponent builds only when it is enabled; setting Mesh
		// afterwards does nothing. Create it disabled, assign the mesh, then enable it.
		var block = go.Components.Create<MeshComponent>( false );
		block.Collision = MeshComponent.CollisionType.Mesh;
		block.Mesh = Box( size );
		block.Enabled = true;

		return block;
	}

	/// <summary>
	/// A 1024-unit-square floor slab centred on the origin, with its top surface at z = 0.
	/// </summary>
	public static MeshComponent CreateFloor( Scene scene ) =>
		CreateBlock( scene, "Starter Floor", new Vector3( -512, -512, -32 ), new Vector3( 1024, 1024, 32 ) );
}
