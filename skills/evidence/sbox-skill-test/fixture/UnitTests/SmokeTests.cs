using Microsoft.VisualStudio.TestTools.UnitTesting;
using Sandbox;
using Assert = Microsoft.VisualStudio.TestTools.UnitTesting.Assert;

namespace Outpost.Tests;

[TestClass]
public class SmokeTests
{
	[TestMethod]
	public void EngineStartsAndCreatesScene()
	{
		var scene = new Scene();
		using var scope = scene.Push();

		Assert.IsTrue( scene.CreateObject().IsValid() );
	}
}
