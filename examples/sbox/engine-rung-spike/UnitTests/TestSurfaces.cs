using System;
using System.Collections.Generic;
using System.Reflection;
using Sandbox;

namespace EladSpike.Tests;

/// <summary>
/// Headless project tests mount no base content, so no "default" physics surface is loaded.
/// Building any PolygonMesh then throws a NullReferenceException in ModelBuilder.AddSurface,
/// which falls back to Surface.FindByName( "default" ) (spike run 2, D1). This makes a default
/// surface available, trying the public route first, and records which route worked.
/// </summary>
static class TestSurfaces
{
	public static string Route { get; private set; } = "not attempted";

	public static void EnsureDefault()
	{
		if ( Surface.FindByName( "default" ) is not null )
		{
			Route = "already loaded";
			return;
		}

		// 1. Public: load the engine's own default surface from core content, if it is mounted.
		try
		{
			ResourceLibrary.Get<Surface>( "surfaces/default.surface" );
		}
		catch ( Exception e )
		{
			Console.WriteLine( $"ResourceLibrary route threw: {e.Message}" );
		}

		if ( Surface.FindByName( "default" ) is not null )
		{
			Route = "public: loaded surfaces/default.surface from core content";
			return;
		}

		// 2. Test-only fallback: register a stand-in surface the way Facepunch's own
		//    MeshComponentBuildTests do. This uses engine internals through reflection, so any
		//    S&box update can break it; the route name makes that visible in the results.
		var register = typeof( Resource ).GetMethod( "RegisterWeakResourceId", BindingFlags.Instance | BindingFlags.NonPublic );
		var all = typeof( Surface ).GetProperty( "All", BindingFlags.Static | BindingFlags.NonPublic )?.GetValue( null ) as Dictionary<int, Surface>;

		if ( register is null || all is null )
		{
			Route = $"unavailable: engine internals not found (RegisterWeakResourceId={register is not null}, All={all is not null})";
			return;
		}

		if ( all.TryGetValue( 0, out var existing ) )
		{
			Route = $"unavailable: surface index 0 is already taken by '{existing?.ResourceName}'";
			return;
		}

		var surface = new Surface();
		register.Invoke( surface, new object[] { "surfaces/default.surface", null } );
		all[0] = surface;

		Route = Surface.FindByName( "default" ) is not null
			? "internal fallback: registered a stand-in default surface (mirrors Facepunch's engine tests)"
			: "unavailable: the stand-in surface was registered but is still not found by name";
	}
}
