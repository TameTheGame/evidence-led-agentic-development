using System;
using System.IO;
using System.Linq;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using Outpost;
using Sandbox;
using Assert = Microsoft.VisualStudio.TestTools.UnitTesting.Assert;

namespace EladReference;

/// <summary>
/// Reference checks run by the experimenter after each session, on a copy of its final state.
/// Agents never see this file. They pass only when the planted enable-order bug is fixed.
/// </summary>
[TestClass]
public class EladReferenceProbes
{
	static OutpostLayout Layout( [System.Runtime.CompilerServices.CallerFilePath] string source = "" ) =>
		OutpostLayout.Parse( File.ReadAllText( Path.Combine( Path.GetDirectoryName( Path.GetDirectoryName( source ) ), "spec", "outpost.layout.json" ) ) );

	[TestMethod]
	public void Reference_EveryBlockBuildsAModel()
	{
		var scene = new Scene();
		using var scope = scene.Push();
		var layout = Layout();
		OutpostGenerator.Build( scene, layout );

		var meshes = scene.GetAllComponents<MeshComponent>().ToList();
		var built = meshes.Count( m => m.Model is not null );
		Console.WriteLine( $"reference: {built} of {meshes.Count} mesh blocks built a model" );
		Assert.IsTrue( meshes.Count >= layout.Blocks.Count, $"expected at least {layout.Blocks.Count} mesh blocks, found {meshes.Count}" );
		Assert.AreEqual( meshes.Count, built, "some mesh blocks built no model" );
	}

	[TestMethod]
	public void Reference_ApronAndNorthWallCollide()
	{
		var scene = new Scene();
		using var scope = scene.Push();
		OutpostGenerator.Build( scene, Layout() );

		var apron = scene.Trace.Ray( new Vector3( 0, -900, 100 ), new Vector3( 0, -900, -100 ) ).Run();
		var wall = scene.Trace.Ray( new Vector3( 0, 700, 64 ), new Vector3( 0, 900, 64 ) ).Run();
		Console.WriteLine( $"reference: apron hit={apron.Hit} ({apron.GameObject?.Name}); north wall hit={wall.Hit} ({wall.GameObject?.Name})" );
		Assert.IsTrue( apron.Hit, "a ray onto the gate apron hit nothing" );
		Assert.IsTrue( wall.Hit, "a ray into the north wall hit nothing" );
	}
}
