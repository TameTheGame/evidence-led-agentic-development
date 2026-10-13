<#
.SYNOPSIS
Builds one real, compilable S&box project per run and runs headless Claude Code sessions that
may run the project's engine tests, for the rung-1 live test.

.DESCRIPTION
The template is an S&box game project created in the Editor and opened once with a UnitTests
folder, so its generated project files include UnitTests\<ident>.unittest.csproj. Those files
reach the engine through relative paths, so the script rewrites them for each run folder and
checks that the engine is reachable.

Each run folder (<Data>\runs\<id>) is a git repository whose first commit is the starting state:
  - the template, without build output;
  - the rung-1 starter from examples/sbox/rung1-starter (UnitTests\*.cs, and tools\ with
    run_engine_tests.ps1 and sync_engine_source.ps1);
  - the outpost spec and the buggy generator from skills/evidence/sbox-skill-test/fixture,
    and the live README from skills/evidence/live-test/fixture;
  - for scenario G, the refactor overlay: a correct generator and UnitTests\OutpostTests.cs;
  - for scenario G2, the two-area project from skills/evidence/refactor-test/fixture: a
    shared, correct AreaGenerator in place of the outpost generator, a quarry spec and
    layout beside the outpost's, and engine tests for both areas;
  - the three ELAD skills, plus sbox-engine-reference when the run has "domain": true;
  - tools\spec_lint.py, CLAUDE.md, and AGENTS.md.
Sessions may edit files, run the spec lint, and run tools\run_engine_tests.ps1. Every other
command that needs approval is denied. The runner's lock makes engine runs take turns.
Sessions load project settings only (no user-level skills or CLAUDE.md), get no engine
source clone (SBOX_PUBLIC is cleared), and use the pinned -Model.

Phases:
  build+run (default)  build every project, then run every session
  build                build every project and stop, to check the starting state
  reference            after the extracts are written: copy the reference probes into each
                       final state, run the whole test suite once, save the results in
                       <Data>\reference\<id>, and remove the probes again

Plan file (JSON): { "runs": [ { "id": "SF-1", "scenario": "F", "domain": true } ] }
Scenarios: F = fall-through report, W = walls without collision, T = write the spawn test,
G = refactor the generator (refactor overlay), G2 = a named refactor in the two-area project.

.EXAMPLE
pwsh skills/evidence/tools/run_live_test.ps1 -Plan plan.json -Template C:\...\scratch\live-template -Data C:\...\scratch\lt
Then: py -3 skills/evidence/tools/analyze_transcripts.py --transcripts <Data>/transcripts --runs <Data>/runs --extracts <Data>/extracts --context 3 --new-files
Then: pwsh skills/evidence/tools/run_live_test.ps1 -Plan plan.json -Template ... -Data ... -Phase reference
#>
param(
    [Parameter(Mandatory)][string]$Plan,
    [Parameter(Mandatory)][string]$Template,
    [Parameter(Mandatory)][string]$Data,
    [string]$Engine = 'C:\Steam\steamapps\common\sbox',
    [string]$Model = 'claude-opus-5[1m]',
    [int]$Parallel = 3,
    [ValidateSet('build+run', 'build', 'reference')][string]$Phase = 'build+run'
)
$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$Template = (Resolve-Path $Template).Path
$base = Join-Path $Data 'runs'
$utf8 = New-Object System.Text.UTF8Encoding($false)
function Put($path, $text) { [IO.File]::WriteAllText($path, (($text -replace "`r`n", "`n").TrimEnd() + "`n"), $utf8) }
function CopyText($from, $to) { New-Item -ItemType Directory -Force (Split-Path $to) | Out-Null; Put $to ([IO.File]::ReadAllText($from, $utf8)) }

$runs = (Get-Content -Raw $Plan | ConvertFrom-Json).runs
# Sessions get no engine source clone, so the runner reports its source check as NOT CHECKED.
Remove-Item Env:SBOX_PUBLIC -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force "$Data\transcripts", $base | Out-Null

if ($Phase -eq 'reference') {
    $probes = "$repo\skills\evidence\live-test\fixture\reference\EladReferenceProbes.cs"
    $twoAreaProbes = "$repo\skills\evidence\refactor-test\fixture\reference\EladReferenceProbes.cs"
    # The starter's own runner, not the session's copy, which the agent could have changed.
    $engineRunner = "$repo\examples\sbox\rung1-starter\tools\run_engine_tests.ps1"
    foreach ($r in $runs) {
        $dir = Join-Path $base $r.id
        $probe = if ($r.scenario -eq 'G2') { $twoAreaProbes } else { $probes }
        Copy-Item $probe "$dir\UnitTests\EladReferenceProbes.cs"
        Push-Location $dir
        try {
            & powershell -NoProfile -File $engineRunner -Project $dir -Engine $Engine -Out "$Data\reference\$($r.id)" | Out-Null
            "{0}: exit {1}" -f $r.id, $LASTEXITCODE
        } finally {
            Pop-Location
            Remove-Item "$dir\UnitTests\EladReferenceProbes.cs"
        }
    }
    return
}

$prompts = @{
    F = 'A tester says players fall through the floor near the gate.'
    W = 'The generated walls have no collision in game. Players walk straight through them.'
    T = 'Write the engine test for OUT-SPAWN-01.'
    G = 'Refactor the generator every area uses.'
    G2 = 'Refactor the generator every area uses: move the mesh-block code into its own class.'
}
$agents = @"
# AGENTS.md

## Checks

``tools/spec_lint.py`` checks the spec files. Run it with ``py -3 tools/spec_lint.py``.

Run the engine tests with ``tools\run_engine_tests.ps1``: from PowerShell,
``& .\tools\run_engine_tests.ps1``; from Bash, ``powershell -File tools/run_engine_tests.ps1``.
It builds and runs ``UnitTests/`` against the installed S&box, saves the engine's log with the
results, and prints any component errors the engine caught. Add ``-Filter "Name~OUT_SPAWN"``
to run some of them. A run takes about a minute, longer while another run holds the engine;
allow up to ten minutes.

The S&box engine source isn't available in this environment.
"@
$excluded = 'obj', 'bin', '.sbox', '.vs', 'test-results', 'TestResults'
$fixture = "$repo\skills\evidence\sbox-skill-test\fixture"
$live = "$repo\skills\evidence\live-test\fixture"
$starter = "$repo\examples\sbox\rung1-starter"
$twoAreas = "$repo\skills\evidence\refactor-test\fixture"

foreach ($r in $runs) {
    $dir = Join-Path $base $r.id
    if (Test-Path $dir) { throw "$dir already exists" }
    if (-not $prompts.ContainsKey($r.scenario)) { throw "unknown scenario $($r.scenario) in $($r.id)" }
    & robocopy $Template $dir /E /XD @excluded /NFL /NDL /NJH /NJS /NP | Out-Null
    if ($LASTEXITCODE -ge 8) { throw "robocopy failed for $($r.id) (exit $LASTEXITCODE)" }
    foreach ($proj in Get-ChildItem $dir -Recurse -Filter *.csproj) {
        $rel = [IO.Path]::GetRelativePath($proj.DirectoryName, $Engine).Replace('\', '/') + '/'
        $text = [IO.File]::ReadAllText($proj.FullName) -replace '(\.\./)+Steam/steamapps/common/sbox/', $rel
        [IO.File]::WriteAllText($proj.FullName, $text)
        $dll = [IO.Path]::GetFullPath((Join-Path $proj.DirectoryName ($rel + 'bin/managed/Sandbox.Engine.dll')))
        if (-not (Test-Path $dll)) { throw "$($proj.FullName) can't reach the engine at $dll" }
    }

    foreach ($f in Get-ChildItem "$starter\UnitTests" -Filter *.cs) { CopyText $f.FullName "$dir\UnitTests\$($f.Name)" }
    foreach ($t in 'run_engine_tests.ps1', 'sync_engine_source.ps1') { CopyText "$starter\tools\$t" "$dir\tools\$t" }
    foreach ($f in Get-ChildItem "$fixture\spec") { CopyText $f.FullName "$dir\spec\$($f.Name)" }
    CopyText "$fixture\Code\OutpostGenerator.cs" "$dir\Code\OutpostGenerator.cs"
    CopyText "$live\README.md" "$dir\README.md"
    if ($r.scenario -eq 'G') {
        CopyText "$live\refactor\README.md" "$dir\README.md"
        CopyText "$live\refactor\Code\OutpostGenerator.cs" "$dir\Code\OutpostGenerator.cs"
        CopyText "$live\refactor\UnitTests\OutpostTests.cs" "$dir\UnitTests\OutpostTests.cs"
    }
    if ($r.scenario -eq 'G2') {
        Remove-Item "$dir\Code\OutpostGenerator.cs"
        foreach ($f in Get-ChildItem -Recurse -File $twoAreas | Where-Object { $_.Directory.Name -ne 'reference' }) {
            CopyText $f.FullName (Join-Path $dir $f.FullName.Substring($twoAreas.Length + 1))
        }
    }
    Add-Content "$dir\.gitignore" "`ntest-results/`nTestResults/"
    New-Item -ItemType Directory -Force "$dir\.claude\skills" | Out-Null
    foreach ($s in 'choosing-rigor', 'matching-evidence-to-claims', 'asking-the-owner') {
        Copy-Item -Recurse "$repo\skills\$s" "$dir\.claude\skills\$s"
    }
    if ($r.domain) {
        Copy-Item -Recurse "$repo\examples\sbox\skills\sbox-engine-reference" "$dir\.claude\skills\sbox-engine-reference"
    }
    CopyText "$repo\examples\sbox\tools\spec_lint.py" "$dir\tools\spec_lint.py"
    Put "$dir\CLAUDE.md" '@AGENTS.md'
    Put "$dir\AGENTS.md" $agents
    git -C $dir init -q
    git -C $dir config user.name 'Test Owner'
    git -C $dir config user.email 'owner@example.invalid'
    git -C $dir config core.autocrlf false
    git -C $dir add -A
    git -C $dir commit -q -m 'Starting state'
}
"built $($runs.Count) projects in $base"
if ($Phase -eq 'build') { return }

# The PowerShell tool refuses a nested powershell process, so PowerShell sessions need the
# in-process forms; Bash sessions need the powershell -File forms.
$runner = @('powershell -File tools\run_engine_tests.ps1', 'powershell -NoProfile -File tools\run_engine_tests.ps1',
    'powershell.exe -File tools\run_engine_tests.ps1', 'pwsh -File tools\run_engine_tests.ps1',
    '.\tools\run_engine_tests.ps1', '& .\tools\run_engine_tests.ps1',
    'tools\run_engine_tests.ps1', '& tools\run_engine_tests.ps1')
$allowed = @('Skill', 'Bash(py -3 tools/spec_lint.py)', 'Bash(py -3 tools/spec_lint.py:*)',
    'PowerShell(py -3 tools/spec_lint.py)', 'PowerShell(py -3 tools/spec_lint.py:*)')
foreach ($c in $runner) {
    $slash = $c.Replace('\', '/')
    $allowed += "PowerShell($c)", "PowerShell(${c}:*)", "PowerShell($slash)", "PowerShell(${slash}:*)"
    $allowed += "Bash($slash)", "Bash(${slash}:*)", "Bash($($c.Replace('\', '\\')):*)"
}

# The timeout covers the whole batch; it only guards against a hung session.
$runs | ForEach-Object -ThrottleLimit $Parallel -TimeoutSeconds 28800 -Parallel {
    $r = $_
    $dir = Join-Path $using:base $r.id
    $allowedTools = $using:allowed
    $data = $using:Data
    $prompt = ($using:prompts)[$r.scenario]
    $env:FACEPUNCH_ENGINE = $using:Engine
    [Console]::OutputEncoding = [Text.UTF8Encoding]::new()
    Set-Location $dir
    $started = Get-Date
    # Project settings only, so the machine's user-level skills and CLAUDE.md stay out.
    & claude -p $prompt --output-format stream-json --verbose --permission-mode acceptEdits `
        --model $using:Model --setting-sources project,local `
        --allowedTools $allowedTools --strict-mcp-config --no-session-persistence `
        > "$data\transcripts\$($r.id).jsonl" 2> "$data\transcripts\$($r.id).err"
    "{0}: exit {1}, {2:N0}s" -f $r.id, $LASTEXITCODE, ((Get-Date) - $started).TotalSeconds
}
"all runs finished"
