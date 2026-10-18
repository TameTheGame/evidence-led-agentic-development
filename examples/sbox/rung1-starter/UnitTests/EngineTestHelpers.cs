using System;
using System.IO;
using System.Reflection;
using System.Runtime.CompilerServices;
using Sandbox;

namespace EngineTests;

/// <summary>
/// Helpers for engine-rung tests, from the ELAD engine-rung spike (S&box 26.10.02).
/// </summary>
static class EngineTestHelpers
{
	/// <summary>
	/// A player that can be ticked headlessly: no input device and no footstep audio.
	/// </summary>
	public static PlayerController CreatePlayer( Scene scene, Vector3 position )
	{
		var go = scene.CreateObject();
		go.Name = "Test Player";
		go.WorldPosition = position;

		var pc = go.Components.Create<PlayerController>();
		pc.UseInputControls = false;
		pc.EnableFootstepSounds = false;

		return pc;
	}

	/// <summary>
	/// Ticks the scene until the player stands on the ground, at most <paramref name="maxTicks"/>
	/// times. Returns whether it landed.
	/// </summary>
	public static bool TickUntilGrounded( Scene scene, PlayerController pc, int maxTicks = 60 )
	{
		for ( int i = 0; i < maxTicks && !pc.IsOnGround; i++ )
			scene.GameTick();

		return pc.IsOnGround;
	}

	/// <summary>
	/// True when the player's body starts inside geometry, including wholly inside mesh collision.
	/// </summary>
	public static bool BodyStartsInsideGeometry( PlayerController pc )
	{
		// Lifted 2 units so resting contact with the floor doesn't count as being stuck.
		var start = pc.GameObject.WorldPosition + Vector3.Up * 2;
		if ( pc.TraceBody( start, start + Vector3.Up ).StartedSolid )
			return true;

		// StartedSolid misses a body wholly inside mesh collision: a concave mesh is a surface
		// with no interior, and traces don't see its faces from behind. So probe upward from the
		// body's centre to the first face it can see, then trace back. Any face hit on the way
		// back faces away from the centre, so the centre is inside a closed solid. This assumes
		// closed meshes with outward-facing faces. Public trace API only.
		var centre = start + Vector3.Up * (pc.CurrentHeight * 0.5f);
		var outward = ProbeRay( pc, centre, centre + Vector3.Up * 16384 );
		var back = ProbeRay( pc, outward.EndPosition - Vector3.Up * 0.5f, centre );
		return back.Hit;
	}

	static SceneTraceResult ProbeRay( PlayerController pc, Vector3 from, Vector3 to ) =>
		pc.Scene.Trace.Ray( from, to )
			.IgnoreGameObjectHierarchy( pc.GameObject )
			.WithCollisionRules( pc.Tags )
			.Run();

	/// <summary>
	/// Loads a saved scene from its file, given a path relative to the project root such as
	/// "Assets/scenes/minimal.scene", or an absolute path. Scene.LoadFromFile fails headlessly,
	/// because project resources aren't registered, so this reads the file instead. Tested only
	/// on scenes whose objects don't reference prefabs or models.
	/// It loads without a loading screen, as S&box's own scene tests do (SceneLoadSave.cs).
	/// With one, the scene waits for a loading task that nothing runs headlessly, stays
	/// <see cref="Scene.IsLoading"/>, and <see cref="Scene.GameTick"/> skips it, so a player in
	/// it never moves. Without one, load events' tasks aren't awaited and AfterLoad doesn't fire.
	/// </summary>
	public static bool LoadSavedScene( Scene scene, string relativePath )
	{
		var options = new SceneLoadOptions { ShowLoadingScreen = false };
		options.SetScene( ReadSceneFile( Path.Combine( ProjectRoot(), relativePath ), relativePath ) );
		return scene.Load( options );
	}

	/// <summary>
	/// Reads a saved scene with its binary data. S&box saves mesh and terrain data beside the
	/// scene, in "&lt;file&gt;_d", and the scene's JSON only refers to it. The public
	/// <see cref="GameResource.LoadFromJson"/> drops that data, so meshes would load empty and
	/// traces would pass through them. When a "_d" file exists, this calls the internal
	/// SceneFile.FromSource the editor itself uses (Sandbox.Tools/Scene/SceneSource.cs).
	/// Test-only: it uses reflection, and an engine update may break it.
	/// </summary>
	static SceneFile ReadSceneFile( string path, string relativePath )
	{
		var json = File.ReadAllText( path );
		var data = path + "_d";
		if ( !File.Exists( data ) )
		{
			var file = new SceneFile();
			file.LoadFromJson( json );
			return file;
		}

		var fromSource = typeof( SceneFile ).GetMethod( "FromSource", BindingFlags.Static | BindingFlags.NonPublic,
			null, new[] { typeof( string ), typeof( Guid ), typeof( string ), typeof( byte[] ) }, null )
			?? throw new InvalidOperationException( "SceneFile.FromSource( string, Guid, string, byte[] ) is gone in this engine build, so a scene's _d data can't be loaded; find the editor's new route in Sandbox.Tools/Scene/SceneSource.cs" );

		// The editor passes the asset path, relative to Assets.
		var assetPath = relativePath.Replace( '\\', '/' );
		if ( assetPath.StartsWith( "Assets/", StringComparison.OrdinalIgnoreCase ) )
			assetPath = assetPath["Assets/".Length..];

		return (SceneFile)fromSource.Invoke( null, new object[] { assetPath, Guid.Empty, json, File.ReadAllBytes( data ) } );
	}

	/// <summary>
	/// The project root: the folder above the one holding this file (UnitTests).
	/// </summary>
	public static string ProjectRoot( [CallerFilePath] string source = "" ) =>
		Path.GetDirectoryName( Path.GetDirectoryName( source ) );
}
