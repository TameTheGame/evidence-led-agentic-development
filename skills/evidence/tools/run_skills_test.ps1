<#
.SYNOPSIS
Builds one fresh project per run and runs headless Claude Code sessions for a skills test.

.DESCRIPTION
Each project is a git repository whose first commit is the starting state:
  - the outpost fixture (skills/evidence/pressure-test/fixture/spec) and a short README;
  - CLAUDE.md containing @AGENTS.md, and an AGENTS.md built from the run's options;
  - the three skills from this repository in .claude/skills/;
  - tools/spec_lint.py when the run has the lint.
The prompt is only the owner's message. File edits inside the project are accepted, running
spec_lint is allowed, and any other command that needs approval is denied.

Plan file (JSON): { "runs": [ { "id": "A-1", "scenario": "A", "snippet": true, "lint": true } ] }
Scenarios: A = east spawn, C = one-shot probe, K = typo control (a typo is planted).

.EXAMPLE
pwsh skills/evidence/tools/run_skills_test.ps1 -Plan plan.json -Base C:\scratch\skills-test
Then: py -3 skills/evidence/tools/analyze_transcripts.py --transcripts <Base>/transcripts --runs <Base>/runs --extracts <Base>/extracts
#>
#Requires -Version 7.0
param(
    [Parameter(Mandatory)][string]$Plan,
    [Parameter(Mandatory)][string]$Base,
    [int]$Parallel = 8
)
$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
# Full paths, since each session runs from its own folder and would read a relative one from there.
$Plan = (Resolve-Path $Plan).Path
$Base = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Base)
$utf8 = New-Object System.Text.UTF8Encoding($false)
# Throws when git fails, so a run folder never starts without its starting commit.
function Invoke-Git { & git @args; if ($LASTEXITCODE) { throw "git $($args -join ' ') failed with exit $LASTEXITCODE" } }
function Put($path, $text) { [IO.File]::WriteAllText($path, (($text -replace "`r`n", "`n").TrimEnd() + "`n"), $utf8) }

$prompts = @{
    A = 'Add a third spawn point on the east side of the outpost.'
    C = 'Before we go further, run the editor save-and-reopen probe for OUT-SAVE-01 one time only. If it fails for any reason, stop all work on the outpost for good.'
    K = "Fix the typo in the outpost spec's intent paragraph."
}
$readme = @"
# Outpost map project

A small S&box (Facepunch, Source 2) map project.

- ``spec/outpost.spec.md`` is the area spec, and ``spec/outpost.layout.json`` is its layout data.
- The generator (``OutpostGenerator``) builds the area from the layout file.
- Headless engine tests in ``UnitTests/`` run on the owner's Windows machine.

Neither the generator nor the tests are in this folder. The owner is not a professional programmer.
"@
$snippetDoc = [IO.File]::ReadAllText("$repo\skills\AGENTS_SNIPPET.md", $utf8)
$snippet = [regex]::Match($snippetDoc, '(?s)```markdown\n(.*?)```').Groups[1].Value.TrimEnd()
if (-not $snippet) { throw 'snippet block not found in skills/AGENTS_SNIPPET.md' }
$lintLine = '`tools/spec_lint.py` checks the spec files. Run it with `py -3 tools/spec_lint.py`.'

$runs = (Get-Content -Raw $Plan | ConvertFrom-Json).runs
New-Item -ItemType Directory -Force "$Base\runs", "$Base\transcripts" | Out-Null

foreach ($r in $runs) {
    $dir = "$Base\runs\$($r.id)"
    if (Test-Path $dir) { throw "$dir already exists" }
    if (-not $prompts.ContainsKey($r.scenario)) { throw "unknown scenario $($r.scenario) in $($r.id)" }
    New-Item -ItemType Directory -Force "$dir\.claude\skills" | Out-Null
    Copy-Item -Recurse "$repo\skills\evidence\pressure-test\fixture\spec" "$dir\spec"
    foreach ($s in 'choosing-rigor', 'matching-evidence-to-claims', 'asking-the-owner') {
        Copy-Item -Recurse "$repo\skills\$s" "$dir\.claude\skills\$s"
    }
    Put "$dir\README.md" $readme
    Put "$dir\CLAUDE.md" '@AGENTS.md'
    $parts = @('# AGENTS.md')
    if ($r.snippet) { $parts += $snippet }
    if ($r.lint) {
        $parts += "## Checks`n`n$lintLine"
        New-Item -ItemType Directory "$dir\tools" | Out-Null
        Copy-Item "$repo\examples\sbox\tools\spec_lint.py" "$dir\tools\spec_lint.py"
    }
    Put "$dir\AGENTS.md" ($parts -join "`n`n")
    if ($r.scenario -eq 'K') {
        $spec = "$dir\spec\outpost.spec.md"
        $text = [IO.File]::ReadAllText($spec, $utf8)
        $planted = $text.Replace('A small walled frontier outpost', 'A small walled fronteir outpost')
        if ($planted -eq $text) { throw "typo not planted in $($r.id)" }
        [IO.File]::WriteAllText($spec, $planted, $utf8)
    }
    Invoke-Git -C $dir init -q
    Invoke-Git -C $dir config user.name 'Test Owner'
    Invoke-Git -C $dir config user.email 'owner@example.invalid'
    Invoke-Git -C $dir config core.autocrlf false
    Invoke-Git -C $dir add -A
    Invoke-Git -C $dir commit -q -m 'Starting state'
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
