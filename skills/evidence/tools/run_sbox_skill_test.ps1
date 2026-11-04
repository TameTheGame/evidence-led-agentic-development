<#
.SYNOPSIS
Builds one fresh S&box-style project per run and runs headless Claude Code sessions for the
S&box domain-skill test.

.DESCRIPTION
Each project is a git repository whose first commit is the starting state:
  - the synthetic game project in skills/evidence/sbox-skill-test/fixture (spec, layout,
    generator code, and test start-up), with line endings normalized to LF;
  - CLAUDE.md containing @AGENTS.md, and a fixed AGENTS.md;
  - the three ELAD skills in .claude/skills/, plus examples/sbox/skills/sbox-engine-reference
    when the run has "domain": true;
  - tools/spec_lint.py.
The prompt is only the owner's message. File edits inside the project are accepted, running
spec_lint is allowed, and any other command that needs approval is denied.

Plan file (JSON): { "runs": [ { "id": "SF-1", "scenario": "F", "domain": true } ] }
Scenarios: F = fall-through report, W = walls without collision, T = write the spawn test.

A plan can also set, for a later test:
  - "fixture": the fixture folder, relative to the repository, in place of the one above;
  - "prompts": { "<scenario>": "<owner's message>" }, in place of the three above;
  - "starterTests": file names in examples/sbox/rung1-starter/UnitTests to copy into the
    project's UnitTests/; and
  - per run, "skillRef": a git ref to take sbox-engine-reference's SKILL.md from, such as a
    release tag, in place of the working tree.
-BuildOnly builds the projects and stops, to check the starting state.

.EXAMPLE
pwsh skills/evidence/tools/run_sbox_skill_test.ps1 -Plan plan.json -Base C:\scratch\sbox-skill-test
Then: py -3 skills/evidence/tools/analyze_transcripts.py --transcripts <Base>/transcripts --runs <Base>/runs --extracts <Base>/extracts
#>
#Requires -Version 7.0
param(
    [Parameter(Mandatory)][string]$Plan,
    [Parameter(Mandatory)][string]$Base,
    [int]$Parallel = 8,
    [string]$Model,
    [switch]$BuildOnly
)
$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
# Full paths, since each session runs from its own folder and would read a relative one from there.
$Plan = (Resolve-Path $Plan).Path
$Base = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Base)
$fixture = "$repo\skills\evidence\sbox-skill-test\fixture"
$utf8 = New-Object System.Text.UTF8Encoding($false)
# Throws when git fails, so a run folder never starts without its starting commit.
function Invoke-Git { & git @args; if ($LASTEXITCODE) { throw "git $($args -join ' ') failed with exit $LASTEXITCODE" } }
function Put($path, $text) { [IO.File]::WriteAllText($path, (($text -replace "`r`n", "`n").TrimEnd() + "`n"), $utf8) }

$prompts = @{
    F = 'A tester says players fall through the floor near the gate.'
    W = 'The generated walls have no collision in game. Players walk straight through them.'
    T = 'Write the engine test for OUT-SPAWN-01.'
}
$agents = @"
# AGENTS.md

## Checks

``tools/spec_lint.py`` checks the spec files. Run it with ``py -3 tools/spec_lint.py``.

The engine tests in ``UnitTests/`` need S&box installed, so only the owner can run them.
Neither the S&box install nor a clone of the engine source is available in this environment.
"@

$planData = Get-Content -Raw $Plan | ConvertFrom-Json
$runs = $planData.runs
if ($planData.fixture) { $fixture = Join-Path $repo $planData.fixture }
if ($planData.prompts) { $prompts = @{}; foreach ($p in $planData.prompts.PSObject.Properties) { $prompts[$p.Name] = $p.Value } }
New-Item -ItemType Directory -Force "$Base\runs", "$Base\transcripts" | Out-Null

foreach ($r in $runs) {
    $dir = "$Base\runs\$($r.id)"
    if (Test-Path $dir) { throw "$dir already exists" }
    if (-not $prompts.ContainsKey($r.scenario)) { throw "unknown scenario $($r.scenario) in $($r.id)" }
    New-Item -ItemType Directory -Force "$dir\.claude\skills", "$dir\tools" | Out-Null
    foreach ($f in Get-ChildItem -Recurse -File $fixture) {
        $dest = Join-Path $dir $f.FullName.Substring($fixture.Length + 1)
        New-Item -ItemType Directory -Force (Split-Path $dest) | Out-Null
        # A scene's _d file is engine-written binary data; copy it byte for byte.
        if ($f.Name -like '*_d') { Copy-Item $f.FullName $dest } else { Put $dest ([IO.File]::ReadAllText($f.FullName, $utf8)) }
    }
    foreach ($t in @($planData.starterTests | Where-Object { $_ })) {
        New-Item -ItemType Directory -Force "$dir\UnitTests" | Out-Null
        Put "$dir\UnitTests\$t" ([IO.File]::ReadAllText("$repo\examples\sbox\rung1-starter\UnitTests\$t", $utf8))
    }
    foreach ($s in 'choosing-rigor', 'matching-evidence-to-claims', 'asking-the-owner') {
        Copy-Item -Recurse "$repo\skills\$s" "$dir\.claude\skills\$s"
    }
    if ($r.domain) {
        Copy-Item -Recurse "$repo\examples\sbox\skills\sbox-engine-reference" "$dir\.claude\skills\sbox-engine-reference"
        if ($r.skillRef) {
            [Console]::OutputEncoding = $utf8  # git writes UTF-8; read it as that, not the console's code page
            $old = & git -C $repo show "$($r.skillRef):examples/sbox/skills/sbox-engine-reference/SKILL.md"
            if ($LASTEXITCODE) { throw "no sbox-engine-reference at $($r.skillRef) for $($r.id)" }
            Put "$dir\.claude\skills\sbox-engine-reference\SKILL.md" ($old -join "`n")
        }
    }
    Copy-Item "$repo\examples\sbox\tools\spec_lint.py" "$dir\tools\spec_lint.py"
    Put "$dir\CLAUDE.md" '@AGENTS.md'
    Put "$dir\AGENTS.md" $agents
    Invoke-Git -C $dir init -q
    Invoke-Git -C $dir config user.name 'Test Owner'
    Invoke-Git -C $dir config user.email 'owner@example.invalid'
    Invoke-Git -C $dir config core.autocrlf false
    Invoke-Git -C $dir add -A
    Invoke-Git -C $dir commit -q -m 'Starting state'
}
"built $($runs.Count) projects in $Base\runs"
if ($BuildOnly) { return }
$modelArgs = if ($Model) { @('--model', $Model) } else { @() }

$runs | ForEach-Object -ThrottleLimit $Parallel -TimeoutSeconds 2400 -Parallel {
    $r = $_
    $base = $using:Base
    $modelArgs = $using:modelArgs
    $prompt = ($using:prompts)[$r.scenario]
    [Console]::OutputEncoding = [Text.UTF8Encoding]::new()
    Set-Location "$base\runs\$($r.id)"
    $started = Get-Date
    # Project settings only, so the machine's user-level skills and CLAUDE.md stay out.
    & claude -p $prompt --output-format stream-json --verbose --permission-mode acceptEdits @modelArgs `
        --setting-sources project,local `
        --allowedTools Skill 'Bash(py -3 tools/spec_lint.py)' 'Bash(py -3 tools/spec_lint.py:*)' `
        'PowerShell(py -3 tools/spec_lint.py)' 'PowerShell(py -3 tools/spec_lint.py:*)' `
        --strict-mcp-config --no-session-persistence `
        > "$base\transcripts\$($r.id).jsonl" 2> "$base\transcripts\$($r.id).err"
    "{0}: exit {1}, {2:N0}s" -f $r.id, $LASTEXITCODE, ((Get-Date) - $started).TotalSeconds
}
"all runs finished"
