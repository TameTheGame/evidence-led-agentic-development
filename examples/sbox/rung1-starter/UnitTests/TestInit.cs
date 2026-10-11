using Microsoft.VisualStudio.TestTools.UnitTesting;
using Sandbox;

namespace EngineTests;

[TestClass]
public class TestInit
{
	static TestAppSystem _app;

	[AssemblyInitialize]
	public static void AssemblyInitialize( TestContext context )
	{
		// Boots the real engine without a renderer. Needs the FACEPUNCH_ENGINE environment
		// variable set to the S&box install folder (the one containing sbox-dev.exe).
		_app = new TestAppSystem();
		_app.Init();

		// Headless tests load no "default" physics surface, and building any PolygonMesh needs
		// one. This is test-only scaffolding; see TestSurfaces.
		TestSurfaces.EnsureDefault();
	}

	[AssemblyCleanup]
	public static void AssemblyCleanup() => _app?.Shutdown();
}
