using Sandbox;

namespace Outpost;

/// <summary>
/// Puts the sign over the south gate when the outpost scene starts.
/// </summary>
public sealed class GateDecal : Component
{
	[Property] public DecalDefinition Sign { get; set; }

	protected override void OnStart()
	{
		var go = Scene.CreateObject();
		go.Name = "gate.sign";
		go.WorldPosition = new Vector3( 0, -816, 128 );
		go.WorldRotation = Rotation.LookAt( Vector3.Forward );

		var decal = go.Components.Create<Decal>();
		decal.Decals = [Sign];
		decal.Size = new Vector2( 96, 48 );
	}
}
