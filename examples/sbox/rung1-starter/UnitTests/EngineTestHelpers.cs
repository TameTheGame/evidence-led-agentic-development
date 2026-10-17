using System.IO;
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
	/// "Assets/scenes/minimal.scene". Scene.LoadFromFile fails headlessly, because project
	/// resources aren't registered, so this reads the JSON instead. Tested only on scenes whose
	/// objects don't reference prefabs or models.
	/// It loads without a loading screen, as S&box's own scene tests do (SceneLoadSave.cs).
	/// With one, the scene waits for a loading task that nothing runs headlessly, stays
	/// <see cref="Scene.IsLoading"/>, and <see cref="Scene.GameTick"/> skips it, so a player in
	/// it never moves. Without one, load events' tasks aren't awaited and AfterLoad doesn't fire.
	/// </summary>
	public static bool LoadSavedScene( Scene scene, string relativePath )
	{
		var file = new SceneFile();
		file.LoadFromJson( File.ReadAllText( Path.Combine( ProjectRoot(), relativePath ) ) );

		var options = new SceneLoadOptions { ShowLoadingScreen = false };
		options.SetScene( file );
		return scene.Load( options );
	}

	/// <summary>
	/// The project root: the folder above the one holding this file (UnitTests).
	/// </summary>
	public static string ProjectRoot( [CallerFilePath] string source = "" ) =>
		Path.GetDirectoryName( Path.GetDirectoryName( source ) );
}
