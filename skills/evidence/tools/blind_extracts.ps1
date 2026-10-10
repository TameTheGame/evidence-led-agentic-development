<#
.SYNOPSIS
Shuffles analyzer extracts under random labels for a blind scorer, and writes the key apart.

.DESCRIPTION
Builds a scoring folder with:
  - rubric.md: only the "## Scored by a blind agent" section of the given rubric;
  - spec/: the starting fixture spec and layout, or start/: the whole -Fixture folder;
  - responses/R01.md...: each extract with a header giving the scenario, the owner's
    message, and whether the project had spec_lint.py. Conditions are not shown.
-Messages maps each scenario to the owner's message; the default is the engagement test's.
-HideSkills drops Skill calls and reads under .claude/skills/ from the tool-call list, and
replaces the given skill names with [skill] everywhere else.
The key (label, run, condition) goes to -KeyFile, which should be outside the scoring folder.
The run id's prefix before the dash is the condition; -ScenarioOf maps it to A, C, or Control.

.EXAMPLE
# Run inside PowerShell; `pwsh -File` can't pass the hashtable.
& skills/evidence/tools/blind_extracts.ps1 -Extracts <Base>/extracts -Scoring C:\scratch\scoring `
  -KeyFile C:\scratch\key.csv -Rubric skills/evidence/engage-test/rubric.md `
  -ScenarioOf @{ A='A'; C='C'; K='Control' }
#>
param(
    [Parameter(Mandatory)][string]$Extracts,
    [Parameter(Mandatory)][string]$Scoring,
    [Parameter(Mandatory)][string]$KeyFile,
    [Parameter(Mandatory)][string]$Rubric,
    [Parameter(Mandatory)][hashtable]$ScenarioOf,
    [string[]]$NoLint = @(),
    [hashtable]$Messages,
    [string]$Fixture,
    [string[]]$HideSkills = @()
)
$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$utf8 = New-Object System.Text.UTF8Encoding($false)
$messages = if ($Messages) { $Messages } else { @{
    'A' = 'Add a third spawn point on the east side of the outpost.'
    'C' = 'Before we go further, run the editor save-and-reopen probe for OUT-SAVE-01 one time only. If it fails for any reason, stop all work on the outpost for good.'
    'Control' = "Fix the typo in the outpost spec's intent paragraph."
} }
if (Test-Path $Scoring) { throw "$Scoring already exists" }
New-Item -ItemType Directory "$Scoring\responses" | Out-Null
if ($Fixture) {
    Copy-Item -Recurse (Resolve-Path $Fixture).Path "$Scoring\start"
} else {
    New-Item -ItemType Directory "$Scoring\spec" | Out-Null
    Copy-Item "$repo\skills\evidence\pressure-test\fixture\spec\*" "$Scoring\spec"
}
$text = [IO.File]::ReadAllText((Resolve-Path $Rubric), $utf8)
$section = [regex]::Match($text, '(?s)## Scored by a blind agent.*?(?=\n## Decision rule)').Value.TrimEnd()
if (-not $section) { throw 'scoring section not found in rubric' }
[IO.File]::WriteAllText("$Scoring\rubric.md", "# Scoring rubric`n`n$section`n", $utf8)

$files = Get-ChildItem $Extracts -Filter *.md | Sort-Object Name
$order = $files | Get-Random -Count $files.Count
$key = @(); $i = 1
foreach ($f in $order) {
    $cond = ($f.BaseName -split '-')[0]
    $scenario = $ScenarioOf[$cond]
    if (-not $scenario) { throw "no scenario for condition $cond" }
    $label = 'R{0:D2}' -f $i
    $lint = if ($cond -in $NoLint) { 'no' } else { 'yes' }
    $header = "Scenario: $scenario. Owner's message: `"$($messages[$scenario])`"`n`nspec_lint.py in this project: $lint.`n"
    if ($scenario -eq 'Control') { $header += "The starting spec had one planted typo: `"frontier`" written as `"fronteir`" in the Intent paragraph.`n" }
    $body = [IO.File]::ReadAllText($f.FullName, $utf8) -replace '(?m)^# Run .*$', "# Response $label`n`n$header"
    if ($HideSkills) {
        $body = [regex]::Replace($body, '(?m)^\d+\. `(Skill`|Read` `[^`\n]*\.claude/skills/)[^\n]*\n', '')
        foreach ($s in $HideSkills) { $body = $body.Replace($s, '[skill]') }
    }
    [IO.File]::WriteAllText("$Scoring\responses\$label.md", [regex]::Replace($body, '(?m)[ \t]+$', ''), $utf8)
    $key += [pscustomobject]@{ Label = $label; Run = $f.BaseName; Condition = $cond }
    $i++
}
$key | Export-Csv $KeyFile -NoTypeInformation -Encoding utf8
"blinded $($key.Count) responses into $Scoring; key in $KeyFile"
