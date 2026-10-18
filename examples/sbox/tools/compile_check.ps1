<#
.SYNOPSIS
Rung-0 (static) check: compiles run_csharp scripts against the installed S&box engine's
assemblies, without starting S&box.

.DESCRIPTION
A run_csharp script is an async method body, not a C# file, so nothing compiles it until the
editor runs it. This script wraps each one the way run_csharp does (sbox-cli's run-csharp.md,
and Sandbox.Engine/Systems/Mcp/ScriptTools.cs): an async method returning Task<object>, with
exchangeDirectory and cancellationToken, and System, System.Linq, System.Threading,
System.Threading.Tasks, Sandbox, and the game's global names such as Log in scope. It then
builds them in a temporary folder against <engine>\bin\managed\*.dll, with any -Include
folders as plain C# files, using run_csharp's compiler settings: no unsafe code, the default
language version. Included files get the game's global names too, as a project's own code
does.

It proves the names and signatures a script uses exist in the installed build. It proves
nothing about what the script does. It needs the .NET 10 SDK, and it starts nothing.
The project's own code and tests compile the same way through the test project S&box
generates: dotnet build UnitTests.

Exit code: 0 compiles, 1 compile errors, 2 not run.

.EXAMPLE
powershell -File tools\compile_check.ps1 -Scripts tools\place_player.cs
powershell -File tools\compile_check.ps1 -Scripts tools\*.cs -Include Code
#>
param(
    [Parameter(Mandatory)][string[]]$Scripts,
    [string[]]$Include = @(),
    [string]$Engine = $env:FACEPUNCH_ENGINE
)
$ErrorActionPreference = 'Stop'
function Stop-Setup($message) { Write-Output "NOT RUN: $message"; exit 2 }

# The S&box launcher sets FACEPUNCH_ENGINE as a user variable, which older shells lack.
if (-not $Engine) { $Engine = [Environment]::GetEnvironmentVariable('FACEPUNCH_ENGINE', 'User') }
$managed = if ($Engine) { Join-Path $Engine 'bin\managed' } else { '' }
if (-not $managed -or -not (Test-Path (Join-Path $managed 'Sandbox.Engine.dll'))) {
    Stop-Setup 'set FACEPUNCH_ENGINE (or pass -Engine) to the S&box install folder; its bin\managed has the engine assemblies.'
}
if (-not (Get-Command dotnet -ErrorAction SilentlyContinue) -or -not (@(& dotnet --list-sdks 2>$null) -match '^10\.')) { Stop-Setup 'install the .NET 10 SDK: "dotnet --list-sdks" shows no 10.x SDK.' }
$files = @($Scripts | ForEach-Object { Get-ChildItem $_ -File -ErrorAction SilentlyContinue })
if (-not $files) { Stop-Setup "no script files match $($Scripts -join ', ')." }
$extra = @()
foreach ($folder in $Include) {
    if (-not (Test-Path $folder -PathType Container)) { Stop-Setup "no folder $folder to include." }
    $extra += @(Get-ChildItem $folder -Recurse -File -Filter *.cs | Where-Object { $_.FullName -notmatch '\\(obj|bin)\\' })
}
$version = Get-Content (Join-Path $Engine '.version') -TotalCount 1 -ErrorAction SilentlyContinue

$work = Join-Path ([IO.Path]::GetTempPath()) ('sbox-compile-' + [guid]::NewGuid().ToString('N'))
$src = Join-Path $work 'src'
New-Item -ItemType Directory -Force $src | Out-Null
try {
    $n = 0
    foreach ($file in $files) {
        $n++
        $body = [IO.File]::ReadAllText($file.FullName)
        # #line maps compile errors back to the script's own lines. The trailing return covers
        # scripts that end without one, as run_csharp allows.
        $wrapped = "using System; using System.Linq; using System.Threading; using System.Threading.Tasks; using Sandbox;`n" +
            "public static class Script$n { public static async Task<object> Run( string exchangeDirectory, CancellationToken cancellationToken ) {`n" +
            "#line 1 `"$($file.Name)`"`n$body`n#line default`nreturn null; } }`n"
        [IO.File]::WriteAllText((Join-Path $src "Script$n.cs"), $wrapped)
    }
    # run_csharp and S&box's own project files both bring in the game's global names, such as Log.
    [IO.File]::WriteAllText((Join-Path $src 'GlobalUsings.cs'), "global using static Sandbox.Internal.GlobalGameNamespace;`n")
    $m = 0
    foreach ($file in $extra) {
        $m++
        $text = "#line 1 `"$($file.Name)`"`n" + [IO.File]::ReadAllText($file.FullName)
        [IO.File]::WriteAllText((Join-Path $src "Include$m.cs"), $text)
    }

    $project = @"
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
    <OutputType>Library</OutputType>
    <ImplicitUsings>disable</ImplicitUsings>
    <Nullable>disable</Nullable>
    <LangVersion>default</LangVersion>
    <AllowUnsafeBlocks>false</AllowUnsafeBlocks>
    <NoWarn>CS0162;CS1998</NoWarn>
    <NuGetAudit>false</NuGetAudit>
    <EnableDefaultCompileItems>false</EnableDefaultCompileItems>
  </PropertyGroup>
  <ItemGroup>
    <Compile Include="src/*.cs" />
    <Reference Include="$($managed.Replace('\', '/'))/*.dll" Private="false" />
  </ItemGroup>
</Project>
"@
    [IO.File]::WriteAllText((Join-Path $work 'compile-check.csproj'), $project)
    $ErrorActionPreference = 'Continue'
    $log = @(& dotnet build (Join-Path $work 'compile-check.csproj') -nologo -v q 2>&1 | ForEach-Object { "$_" })
    $code = $LASTEXITCODE
    $ErrorActionPreference = 'Stop'
    $errors = @($log | ForEach-Object { if ($_ -match '([^\\/\s]+\.cs)\((\d+),(\d+)\): error (CS\d+): ([^\[]+)') { $Matches[0].Trim() } } | Sort-Object -Unique)
    $what = "$($files.Count) script(s)" + $(if ($extra) { " and $($extra.Count) included file(s)" } else { '' })
    if ($code -ne 0) {
        Write-Output "Compile of $what against S&box ${version}: FAIL"
        if ($errors) { $errors | ForEach-Object { Write-Output "  $_" } } else { $log | Select-Object -Last 15 | ForEach-Object { Write-Output "  $_" } }
        exit 1
    }
    Write-Output "Compile of $what against S&box ${version}: PASS"
    exit 0
} finally {
    if ($work -like (Join-Path ([IO.Path]::GetTempPath()) 'sbox-compile-*')) { Remove-Item -LiteralPath $work -Recurse -Force -ErrorAction SilentlyContinue }
}
