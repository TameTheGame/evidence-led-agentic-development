using Microsoft.VisualStudio.TestTools.UnitTesting;
using Sandbox;

namespace EladSpike.Tests;

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
	}

	[AssemblyCleanup]
	public static void AssemblyCleanup() => _app?.Shutdown();
}
