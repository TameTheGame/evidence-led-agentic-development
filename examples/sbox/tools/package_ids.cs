// The ID this editor session gives each store package file that the open scene's saved file
// references, for tools/editor_check.ps1, which runs it through sbox-cli's run_csharp with
// `path` after each save. It is a run_csharp method body, not a C# file.
//
// S&box writes no .meta for a file that a store (cloud) package installed, so no file keeps its
// GUID, and each editor session gives the file a new one (26.10.27:engine/Sandbox.Tools/Assets/
// Asset.cs, lines 107 and 173-176). A scene saves a resource as that GUID and the path,
// {"Id": ..., "Path": ...} (26.10.27:engine/Sandbox.Engine/Resources/Resource.Json.cs,
// WriteJsonReference). For each such reference in the saved file whose path is a package's file,
// this loads the file and returns the ID the scene would save for it now, or null when S&box
// would save the path alone. It changes nothing in the scene or on disk.

var session = Editor.SceneEditorSession.Active ?? throw new System.Exception( "No scene is open in the editor." );
var scenePath = session.Scene?.Source?.ResourcePath ?? throw new System.Exception( "The open scene has never been saved, so it has no file." );
var sceneAsset = Editor.AssetSystem.FindByPath( scenePath ) ?? throw new System.Exception( $"The editor has no asset for {scenePath}." );
var text = System.IO.File.ReadAllText( sceneAsset.AbsolutePath );

// The same pattern editor_check.ps1 reads references with.
var pattern = @"""Id"":\s*""[0-9A-Fa-f-]{36}"",\s*""Path"":\s*""([^""\\]*)""";
var ids = new System.Collections.Generic.SortedDictionary<string, string>( System.StringComparer.Ordinal );
var references = 0;
foreach ( System.Text.RegularExpressions.Match match in System.Text.RegularExpressions.Regex.Matches( text, pattern ) )
{
	cancellationToken.ThrowIfCancellationRequested();
	references++;
	var path = match.Groups[1].Value;
	if ( ids.ContainsKey( path ) || Editor.AssetSystem.FindByPath( path ) is not { IsCloud: true } asset )
		continue;

	// Materials and models load the way a scene's reference loads them; any other kind loads as
	// the resource type of its asset.
	Resource resource = path.EndsWith( ".vmat", System.StringComparison.OrdinalIgnoreCase ) ? Material.Load( path )
		: path.EndsWith( ".vmdl", System.StringComparison.OrdinalIgnoreCase ) ? Model.Load( path )
		: asset.LoadResource();
	if ( resource is null || resource.IsError )
		throw new System.Exception( $"{path}, a store package's file, didn't load." );

	ids[path] = Sandbox.Json.ToNode( resource, resource.GetType() ) is System.Text.Json.Nodes.JsonObject reference
		? reference["Id"]?.GetValue<string>()
		: null;
}

return new { Scene = scenePath, References = references, Ids = ids };
