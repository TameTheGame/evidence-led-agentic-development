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

.EXAMPLE
pwsh skills/evidence/tools/run_sbox_skill_test.ps1 -Plan plan.json -Base C:\scratch\sbox-skill-test
Then: py -3 skills/evidence/tools/analyze_transcripts.py --transcripts <Base>/transcripts --runs <Base>/runs --extracts <Base>/extracts
#>
param(
    [Parameter(Mandatory)][string]$Plan,
    [Parameter(Mandatory)][string]$Base,
    [int]$Parallel = 8
)
$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$fixture = "$repo\skills\evidence\sbox-skill-test\fixture"
$utf8 = New-Object System.Text.UTF8Encoding($false)
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

$runs = (Get-Content -Raw $Plan | ConvertFrom-Json).runs
New-Item -ItemType Directory -Force "$Base\runs", "$Base\transcripts" | Out-Null

foreach ($r in $runs) {
    $dir = "$Base\runs\$($r.id)"
    if (Test-Path $dir) { throw "$dir already exists" }
    if (-not $prompts.ContainsKey($r.scenario)) { throw "unknown scenario $($r.scenario) in $($r.id)" }
    New-Item -ItemType Directory -Force "$dir\.claude\skills", "$dir\tools" | Out-Null
    foreach ($f in Get-ChildItem -Recurse -File $fixture) {
        $dest = Join-Path $dir $f.FullName.Substring($fixture.Length + 1)
        New-Item -ItemType Directory -Force (Split-Path $dest) | Out-Null
        Put $dest ([IO.File]::ReadAllText($f.FullName, $utf8))
    }
    foreach ($s in 'choosing-rigor', 'matching-evidence-to-claims', 'asking-the-owner') {
        Copy-Item -Recurse "$repo\skills\$s" "$dir\.claude\skills\$s"
    }
    if ($r.domain) {
        Copy-Item -Recurse "$repo\examples\sbox\skills\sbox-engine-reference" "$dir\.claude\skills\sbox-engine-reference"
    }
    Copy-Item "$repo\examples\sbox\tools\spec_lint.py" "$dir\tools\spec_lint.py"
    Put "$dir\CLAUDE.md" '@AGENTS.md'
    Put "$dir\AGENTS.md" $agents
    git -C $dir init -q
    git -C $dir config user.name 'Test Owner'
    git -C $dir config user.email 'owner@example.invalid'
    git -C $dir config core.autocrlf false
    git -C $dir add -A
    git -C $dir commit -q -m 'Starting state'
}
"built $($runs.Count) projects in $Base\runs"

$runs | ForEach-Object -ThrottleLimit $Parallel -TimeoutSeconds 2400 -Parallel {
    $r = $_
    $base = $using:Base
    $prompt = ($using:prompts)[$r.scenario]
    [Console]::OutputEncoding = [Text.UTF8Encoding]::new()
    Set-Location "$base\runs\$($r.id)"
    $started = Get-Date
    # Project settings only, so the machine's user-level skills and CLAUDE.md stay out.
    & claude -p $prompt --output-format stream-json --verbose --permission-mode acceptEdits `
        --setting-sources project,local `
        --allowedTools Skill 'Bash(py -3 tools/spec_lint.py)' 'Bash(py -3 tools/spec_lint.py:*)' `
        'PowerShell(py -3 tools/spec_lint.py)' 'PowerShell(py -3 tools/spec_lint.py:*)' `
        --strict-mcp-config --no-session-persistence `
        > "$base\transcripts\$($r.id).jsonl" 2> "$base\transcripts\$($r.id).err"
    "{0}: exit {1}, {2:N0}s" -f $r.id, $LASTEXITCODE, ((Get-Date) - $started).TotalSeconds
}
"all runs finished"
