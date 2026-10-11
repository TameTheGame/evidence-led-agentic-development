<#
.SYNOPSIS
Runs a project's headless S&box engine tests and keeps the engine's own log with the results.

.DESCRIPTION
S&box catches errors thrown inside components and writes them only to logs\testhost.log in
the install folder, which every run overwrites. This script:
  1. checks the machine: Windows, a .NET 10 SDK, and an S&box install;
  2. runs `dotnet test` on the project's UnitTests folder, holding a lock so that only one
     run at a time uses the engine log;
  3. saves the test output, the engine log, and the engine version in test-results\<time>\;
  4. prints the test summary and any error lines the engine logged.
Exit code: dotnet test's, or 2 when the machine or project isn't set up.

.EXAMPLE
powershell -File tools\run_engine_tests.ps1
powershell -File tools\run_engine_tests.ps1 -Filter "Name~SPAWN"
#>
param(
    [string]$Project = '.',
    [string]$Engine = $env:FACEPUNCH_ENGINE,
    [string]$Filter,
    [string]$Out
)
$ErrorActionPreference = 'Stop'
function Stop-Setup($message) { Write-Host "NOT RUN: $message"; exit 2 }

if ([Environment]::OSVersion.Platform -ne 'Win32NT') { Stop-Setup 'S&box engine tests run on Windows only.' }
if (-not $Engine -or -not (Test-Path (Join-Path $Engine 'sbox-dev.exe'))) {
    Stop-Setup 'set FACEPUNCH_ENGINE (or pass -Engine) to the S&box install folder, the one containing sbox-dev.exe.'
}
if (-not (@(& dotnet --list-sdks 2>$null) -match '^10\.')) { Stop-Setup 'install the .NET 10 SDK: "dotnet --list-sdks" shows no 10.x SDK.' }
$tests = Join-Path $Project 'UnitTests'
if (-not (Get-ChildItem $tests -Filter *.csproj -ErrorAction SilentlyContinue)) {
    Stop-Setup "no test project in $tests. Open the project once in the S&box Editor so it generates one."
}

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
    & dotnet @arguments 2>&1 | ForEach-Object { "$_" } | Tee-Object -FilePath (Join-Path $Out 'results.txt') | Out-Null
    $code = $LASTEXITCODE

    $logNote = 'not updated by this run'
    $errors = @()
    if ((Test-Path $log) -and (Get-Item $log).LastWriteTime -ge $started) {
        Copy-Item $log (Join-Path $Out 'testhost.log')
        $errors = @(Select-String -Path (Join-Path $Out 'testhost.log') -Pattern '\b(error|exception|failed)\b' |
            ForEach-Object { $_.Line.Trim() })
        $logNote = "$($errors.Count) error line(s)"
    }
} finally {
    $lock.ReleaseMutex()
}

$results = Get-Content (Join-Path $Out 'results.txt')
$summary = @($results | Select-String -Pattern '^\s*(Passed!|Failed!)|Test summary:|error CS\d+' | ForEach-Object { $_.Line.Trim() })
$failed = @($results | Select-String -Pattern '^\s*Failed\s+\S' | ForEach-Object { $_.Line.Trim() })

Write-Host "Engine:     S&box $version ($Engine)"
Write-Host "Tests:      $(if ($summary) { $summary -join ' | ' } else { "no summary line; see results.txt (exit $code)" })"
foreach ($f in $failed) { Write-Host "  $f" }
Write-Host "Engine log: $logNote"
foreach ($e in ($errors | Select-Object -First 20)) { Write-Host "  $e" }
if ($errors.Count -gt 20) { Write-Host "  ... $($errors.Count - 20) more in testhost.log" }
Write-Host "Saved:      $Out"
exit $code
