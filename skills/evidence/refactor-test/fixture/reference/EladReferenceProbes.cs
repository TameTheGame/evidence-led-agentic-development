using System;
using System.IO;
using System.Linq;
using Frontier;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using Sandbox;
using Assert = Microsoft.VisualStudio.TestTools.UnitTesting.Assert;

namespace EladReference;

/// <summary>
/// Reference checks run by the experimenter after each session, on a copy of its final state.
/// Agents never see this file. They pass only when the generator still builds every mesh
/// block of both areas with collision.
/// </summary>
[TestClass]
public class EladReferenceProbes
{
	static AreaLayout Layout( string area, [System.Runtime.CompilerServices.CallerFilePath] string source = "" ) =>
		AreaLayout.Parse( File.ReadAllText( Path.Combine( Path.GetDirectoryName( Path.GetDirectoryName( source ) ), "spec", $"{area}.layout.json" ) ) );

	[TestMethod]
	public void Reference_EveryBlockBuildsAModel()
	{
		var problems = "";
		foreach ( var area in new[] { "outpost", "quarry" } )
		{
			var scene = new Scene();
			using var scope = scene.Push();
			var layout = Layout( area );
			AreaGenerator.Build( scene, layout );

			var meshes = scene.GetAllComponents<MeshComponent>().ToList();
			var built = meshes.Count( m => m.Model is not null );
			Console.WriteLine( $"reference: {area}: {built} of {meshes.Count} mesh blocks built a model" );
			if ( meshes.Count < layout.Blocks.Count || built != meshes.Count )
				problems += $"{area}: {built} of {meshes.Count} mesh blocks built, {layout.Blocks.Count} expected; ";
		}

		Assert.AreEqual( "", problems );
	}

	[TestMethod]
	public void Reference_FloorsAndWallsCollide()
	{
		bool Hit( string area, Vector3 from, Vector3 to )
		{
			var scene = new Scene();
			using var scope = scene.Push();
			AreaGenerator.Build( scene, Layout( area ) );
			var tr = scene.Trace.Ray( from, to ).Run();
			Console.WriteLine( $"reference: {area} ray {from} -> {to}: hit={tr.Hit} ({tr.GameObject?.Name})" );
			return tr.Hit;
		}

		var apron = Hit( "outpost", new Vector3( 0, -900, 100 ), new Vector3( 0, -900, -100 ) );
		var wall = Hit( "outpost", new Vector3( 0, 700, 64 ), new Vector3( 0, 900, 64 ) );
		var dock = Hit( "quarry", new Vector3( 0, -768, 100 ), new Vector3( 0, -768, -100 ) );
		var cliff = Hit( "quarry", new Vector3( 0, 500, 64 ), new Vector3( 0, 700, 64 ) );
		Assert.IsTrue( apron && wall && dock && cliff,
			$"apron hit={apron}, north wall hit={wall}, dock hit={dock}, north cliff hit={cliff}" );
	}
}
