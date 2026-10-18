<#
.SYNOPSIS
Runs a project's headless S&box engine tests and keeps the engine's own log with the results.

.DESCRIPTION
S&box catches errors thrown inside components and writes them only to logs\testhost.log in
the install folder, which every run overwrites. This script:
  1. checks the machine: Windows, a .NET 10 SDK, and an S&box install;
  2. if given a clone of Facepunch/sbox-public (SBOX_PUBLIC or -Source), moves it to the
     installed release with sync_engine_source.ps1, so agents read the source they run;
  3. runs `dotnet test` on the project's UnitTests folder, holding a lock so that only one
     run at a time uses the engine log;
  4. saves the test output, the engine log, and the engine version in test-results\<time>\;
  5. prints the test summary, the source check, and any error lines the engine logged, and
     a warning when the source isn't matched to the installed release.
FACEPUNCH_ENGINE and SBOX_PUBLIC are read from the user's settings when the shell lacks them.
Exit code: dotnet test's, or 2 when the machine or project isn't set up.

.EXAMPLE
powershell -File tools\run_engine_tests.ps1
powershell -File tools\run_engine_tests.ps1 -Filter "Name~SPAWN"
#>
param(
    [string]$Project = '.',
    [string]$Engine = $env:FACEPUNCH_ENGINE,
    [string]$Source = $env:SBOX_PUBLIC,
    [string]$Filter,
    [string]$Out
)
$ErrorActionPreference = 'Stop'
function Stop-Setup($message) { Write-Host "NOT RUN: $message"; exit 2 }

if ([Environment]::OSVersion.Platform -ne 'Win32NT') { Stop-Setup 'S&box engine tests run on Windows only.' }
# A shell started before these were set for the user lacks them, so read the user's values too.
if (-not $Engine) { $Engine = [Environment]::GetEnvironmentVariable('FACEPUNCH_ENGINE', 'User') }
if (-not $Source) { $Source = [Environment]::GetEnvironmentVariable('SBOX_PUBLIC', 'User') }
if (-not $Engine -or -not (Test-Path (Join-Path $Engine 'sbox-dev.exe'))) {
    Stop-Setup 'set FACEPUNCH_ENGINE (or pass -Engine) to the S&box install folder, the one containing sbox-dev.exe.'
}
if (-not (@(& dotnet --list-sdks 2>$null) -match '^10\.')) { Stop-Setup 'install the .NET 10 SDK: "dotnet --list-sdks" shows no 10.x SDK.' }
$tests = Join-Path $Project 'UnitTests'
if (-not (Get-ChildItem $tests -Filter *.csproj -ErrorAction SilentlyContinue)) {
    Stop-Setup "no test project in $tests. Open the project once in the S&box Editor so it generates one."
}

# Steam can update the engine at any launch; keep the source agents read on the same release.
$sync = Join-Path $PSScriptRoot 'sync_engine_source.ps1'
$sourceCheck = try {
    if (Test-Path $sync) { "$(& $sync -Engine $Engine -Source $Source)" -replace '^S&box source: ' }
    else { 'NOT CHECKED - sync_engine_source.ps1 is not next to this script.' }
} catch { "NOT SYNCED - the check failed: $($_.Exception.Message)" }

$version = (Get-Content (Join-Path $Engine '.version') -TotalCount 1 -ErrorAction SilentlyContinue)
if (-not $Out) { $Out = Join-Path $Project ('test-results\' + (Get-Date -Format 'yyyyMMdd-HHmmss')) }
New-Item -ItemType Directory -Force $Out | Out-Null
$log = Join-Path $Engine 'logs\testhost.log'

# Every run overwrites the same engine log, so runs must not overlap.
$lock = New-Object System.Threading.Mutex($false, 'sbox-engine-tests-testhost-log')
try {
    if (-not $lock.WaitOne(0)) {
        Write-Host 'Waiting for another engine test run to finish...'
        if (-not $lock.WaitOne([TimeSpan]::FromMinutes(30))) { Stop-Setup 'another engine test run held the lock for 30 minutes.' }
    }
} catch [System.Threading.AbandonedMutexException] { }

try {
    $env:FACEPUNCH_ENGINE = $Engine
    $started = Get-Date
    $arguments = @('test', $tests, '--logger', 'console;verbosity=detailed')
    if ($Filter) { $arguments += @('--filter', $Filter) }
    # dotnet writes failures to stderr; don't let that stop the script before the log is saved.
    $ErrorActionPreference = 'Continue'
    $output = @(& dotnet @arguments 2>&1 | ForEach-Object { "$_" })
    $code = $LASTEXITCODE
    $ErrorActionPreference = 'Stop'
    [IO.File]::WriteAllLines((Join-Path $Out 'results.txt'), [string[]]$output)

    $logLines = $null
    if ((Test-Path $log) -and (Get-Item $log).LastWriteTime -ge $started) {
        Copy-Item $log (Join-Path $Out 'testhost.log')
        $logLines = @(Get-Content (Join-Path $Out 'testhost.log'))
    }
} finally {
    $lock.ReleaseMutex()
}

# Component errors: the engine catches exceptions thrown in component callbacks such as
# OnEnabled and logs them as "OnEnabled on Sandbox.MeshComponent failed ...". Group them by
# message, with the first stack frame that names the cause.
$component = [ordered]@{}
$other = 0
if ($logLines) {
    for ($i = 0; $i -lt $logLines.Count; $i++) {
        $line = $logLines[$i]
        if ($line -match '\]\s+(On\w+ on \S+ failed.*)$') {
            $message = $Matches[1].Trim()
            if (-not $component.Contains($message)) {
                # The entry's first stacks are the engine's dispatcher. The cause is the first
                # frame of the innermost exception, after the last "--->" in the entry.
                $frame = $null; $outer = $null; $pending = $false
                for ($j = $i + 1; $j -lt $logLines.Count -and $logLines[$j] -notmatch '^\d{4}/\d\d/\d\d '; $j++) {
                    if ($logLines[$j] -match '^\s*--->\s') { $pending = $true }
                    elseif ($logLines[$j] -match '^\s+at ') {
                        if ($pending) { $frame = $logLines[$j].Trim(); $pending = $false }
                        if (-not $outer) { $outer = $logLines[$j].Trim() }
                    }
                }
                $component[$message] = @{ Hits = 0; Frame = $(if ($frame) { $frame } else { $outer }) }
            }
            $component[$message].Hits++
        } elseif ($line -match '^\d{4}/\d\d/\d\d .*\b(error|exception|failed)\b') {
            $other++
        }
    }
}

$results = $output
$summary = @($results | Select-String -Pattern '^\s*(Passed!|Failed!)|Test summary:|Test Run (Successful|Failed|Aborted)|^\s*(Total tests|Passed|Failed|Skipped):\s*\d|error CS\d+|Build FAILED' |
    ForEach-Object { $_.Line.Trim() })
$failed = @($results | Select-String -Pattern '^\s*Failed\s+\S' | ForEach-Object { $_.Line.Trim() })

Write-Host "Engine:     S&box $version ($Engine)"
Write-Host "Source:     $sourceCheck"
Write-Host "Tests:      $(if ($summary) { $summary -join ' | ' } else { "no summary line; see results.txt (exit $code)" })"
foreach ($f in $failed) { Write-Host "  $f" }
if ($null -eq $logLines) {
    Write-Host 'Engine log: not updated by this run'
} else {
    Write-Host "Engine log: $(@($component.Keys).Count) distinct component error(s), not shown in the test output"
    foreach ($m in $component.Keys) {
        Write-Host "  $($component[$m].Hits)x $m"
        if ($component[$m].Frame) { Write-Host "      $($component[$m].Frame)" }
    }
    Write-Host "            $other other error line(s); headless start-up logs some, such as missing shaders, even when every test passes"
}
Write-Host "Saved:      $Out"
# An agent may cite engine source for these results, so say plainly when it isn't the release that ran.
if ($sourceCheck -match '^(NOT CHECKED|NOT SYNCED|NEAREST|UNKNOWN)') {
    Write-Host "Warning:    engine source is $($Matches[1]), not matched to S&box $version. Say so before citing sbox-public for this run; the Source line says why."
}
exit $code
