<#
.SYNOPSIS
Runs a project's headless S&box engine tests under a time limit, reads each test's outcome, and
keeps the engine's own log with the results.

.DESCRIPTION
S&box catches errors thrown inside components and writes them only to logs\testhost.log in
the install folder, which every run overwrites. This script:
  1. checks the machine: Windows, a .NET 10 SDK, and an S&box install;
  2. if given a clone of Facepunch/sbox-public (SBOX_PUBLIC or -Source), moves it to the
     installed release with sync_engine_source.ps1, so agents read the source they run;
  3. runs `dotnet test` on the project's UnitTests folder, holding a lock so that only one
     run at a time uses the engine log, and stops it at -TimeoutSeconds (30 minutes by
     default) by killing it and every process under it;
  4. reads each test's outcome from the run's TRX file;
  5. saves the test output, the TRX file, the engine log, and the engine version in
     test-results\<time>\;
  6. prints the outcomes, the source check, and any error lines the engine logged, and a
     warning when the source isn't matched to the installed release.
FACEPUNCH_ENGINE and SBOX_PUBLIC are read from the user's settings when the shell lacks them.

dotnet test exits 0 when tests stop with Assert.Inconclusive, because MSTest records them as
not executed, so the result comes from the TRX file instead:
  PASS          at least one test ran, and every test passed;
  FAIL          a test failed, timed out or was aborted, the run hit its time limit, the run
                wrote no TRX file (after a build error, for one), or dotnet test exited
                non-zero with no failed test;
  INCONCLUSIVE  nothing failed, but a test didn't run, such as one that stopped with
                Assert.Inconclusive, or no test ran at all. It is not a pass.
Exit code: 0 pass, 1 fail, 2 inconclusive, or 2 when the machine or project isn't set up.

At the time limit the script lists the process tree before it kills anything, then kills each
process and repeats from every process it has found until none is left. A process killed first
can take others down with it, and their children keep the dead parent's ID, so a kill that
looks for children only as it goes leaves some running.

-SelfTest checks the verdicts on planted TRX files and the tree walk on planted process lists,
and on Windows kills a planted hung tree of two processes. It needs no S&box.

.EXAMPLE
powershell -File tools/run_engine_tests.ps1
powershell -File tools/run_engine_tests.ps1 -Filter "Name~SPAWN"
powershell -File tools/run_engine_tests.ps1 -SelfTest
#>
param(
    [string]$Project = '.',
    [string]$Engine = $env:FACEPUNCH_ENGINE,
    [string]$Source = $env:SBOX_PUBLIC,
    [string]$Filter,
    [string]$Out,
    [int]$TimeoutSeconds = 1800,
    [switch]$SelfTest
)
$ErrorActionPreference = 'Stop'
function Stop-Setup($message) { Write-Host "NOT RUN: $message"; exit 2 }

# Each test's outcome in a TRX file: Found, the counts, and each test's name, outcome, kind
# (passed, failed or inconclusive) and message. A file older than $Since is an earlier run's.
function Read-TrxOutcomes([string]$Path, [datetime]$Since) {
    $read = [pscustomobject]@{ Found = $false; Passed = 0; Failed = 0; Inconclusive = 0; Tests = @() }
    if (-not $Path -or -not (Test-Path -LiteralPath $Path)) { return $read }
    if ($Since -and (Get-Item -LiteralPath $Path).LastWriteTime -lt $Since) { return $read }
    [xml]$trx = Get-Content -Raw -LiteralPath $Path -Encoding UTF8
    $read.Found = $true
    $tests = @()
    foreach ($r in @($trx.TestRun.Results.UnitTestResult)) {
        if (-not $r) { continue }
        $outcome = [string]$r.outcome
        # vstest writes MSTest's Inconclusive as NotExecuted. PassedButRunAborted means the run
        # broke off, so it counts as failed, as do Failed, Error, Timeout and Aborted.
        $kind = if ($outcome -eq 'Passed') { 'passed' }
            elseif (@('NotExecuted', 'Inconclusive', 'Pending', 'Disconnected', 'Warning', 'NotRunnable') -contains $outcome) { 'inconclusive' }
            else { 'failed' }
        if ($kind -eq 'passed') { $read.Passed++ } elseif ($kind -eq 'failed') { $read.Failed++ } else { $read.Inconclusive++ }
        $message = "$($r.Output.ErrorInfo.Message)".Trim()
        if (-not $message) { $message = "$(@("$($r.Output.StdOut)" -split "`r?`n" | Where-Object { $_ -match 'Inconclusive' } | Select-Object -First 1))".Trim() }
        $tests += [pscustomobject]@{ Name = [string]$r.testName; Outcome = $outcome; Kind = $kind; Message = $message }
    }
    $read.Tests = $tests
    return $read
}

# The run's result: Status (PASS, FAIL or INCONCLUSIVE), its exit code, and why.
function Get-Verdict($Outcomes, [bool]$TimedOut, $ExitCode) {
    function Verdict([string]$Status, [int]$Exit, [string]$Why) { [pscustomobject]@{ Status = $Status; Exit = $Exit; Why = $Why } }
    if ($TimedOut) { return Verdict 'FAIL' 1 'the run hit its time limit' }
    if (-not $Outcomes.Found) { return Verdict 'FAIL' 1 "the run wrote no TRX file (dotnet test exit $ExitCode); its output says why" }
    if ($Outcomes.Failed) { return Verdict 'FAIL' 1 "$($Outcomes.Failed) test(s) failed" }
    if ($ExitCode -ne 0) { return Verdict 'FAIL' 1 "dotnet test exited $ExitCode with no failed test" }
    $ran = $Outcomes.Passed + $Outcomes.Inconclusive
    if (-not $ran) { return Verdict 'INCONCLUSIVE' 2 'no test ran' }
    if ($Outcomes.Inconclusive) { return Verdict 'INCONCLUSIVE' 2 "$($Outcomes.Inconclusive) of $ran test(s) didn't run, so they prove nothing" }
    return Verdict 'PASS' 0 "all $ran test(s) passed"
}

# One argument for a Windows command line, quoted so that the program reads it back unchanged.
function ConvertTo-Argument([string]$Value) {
    if ($Value -and $Value -notmatch '[\s"]') { return $Value }
    return '"' + ($Value -replace '(\\*)"', '$1$1\"' -replace '(\\+)$', '$1$1') + '"'
}

# Every process now, by ID: its parent's ID and its start time in ticks.
function Get-ProcessSnapshot {
    $all = @{}
    foreach ($p in @(Get-CimInstance Win32_Process -Property ProcessId, ParentProcessId, CreationDate)) {
        $start = if ($p.CreationDate) { ([datetime]$p.CreationDate).ToUniversalTime().Ticks } else { [long]0 }
        $all[[int]$p.ProcessId] = [pscustomobject]@{ Parent = [int]$p.ParentProcessId; Start = [long]$start }
    }
    return $all
}

# A tree's members in a snapshot, the root first: the root, each member already known (by ID,
# with the start time recorded while it ran), and each process whose parent is a member, that
# started no earlier than that parent and, when a later process now holds the parent's ID,
# before that one. Windows never gives a process a new parent, so a child keeps its dead
# parent's ID; the start times rule out an ID used again. Returns Order and Starts.
function Find-ProcessTree([int]$Root, [hashtable]$Snapshot, $Known) {
    $starts = [System.Collections.Generic.Dictionary[int, long]]::new()
    $order = [System.Collections.Generic.List[int]]::new()
    if ($Known) { foreach ($id in $Known.Keys) { $starts[$id] = $Known[$id]; $order.Add($id) } }
    if (-not $starts.ContainsKey($Root)) {
        if (-not $Snapshot.ContainsKey($Root)) { return [pscustomobject]@{ Order = $order.ToArray(); Starts = $starts } }
        $starts[$Root] = $Snapshot[$Root].Start
        $order.Insert(0, $Root)
    }
    for ($i = 0; $i -lt $order.Count; $i++) {
        $parent = $order[$i]
        $parentStart = $starts[$parent]
        $holder = if ($Snapshot.ContainsKey($parent) -and $Snapshot[$parent].Start -ne $parentStart) { $Snapshot[$parent].Start } else { $null }
        foreach ($entry in $Snapshot.GetEnumerator()) {
            $id = [int]$entry.Key
            $p = $entry.Value
            if ($p.Parent -ne $parent -or $id -eq 0 -or $id -eq $parent -or $starts.ContainsKey($id)) { continue }
            if ($p.Start -lt $parentStart -or ($null -ne $holder -and $p.Start -ge $holder)) { continue }
            $starts[$id] = $p.Start
            $order.Add($id)
        }
    }
    return [pscustomobject]@{ Order = $order.ToArray(); Starts = $starts }
}

# Kills a process and every process under it. Returns Tree (every member found, the root first)
# and Left (the members still running when $Seconds ran out).
function Stop-ProcessTree([int]$Root, [int]$Seconds = 30) {
    $known = [System.Collections.Generic.Dictionary[int, long]]::new()
    $clock = [Diagnostics.Stopwatch]::StartNew()
    while ($true) {
        $snapshot = Get-ProcessSnapshot
        $found = Find-ProcessTree $Root $snapshot $known
        $new = @($found.Order | Where-Object { -not $known.ContainsKey($_) })
        foreach ($id in $new) { $known[$id] = $found.Starts[$id] }
        $running = @($found.Order | Where-Object { $snapshot.ContainsKey($_) -and $snapshot[$_].Start -eq $known[$_] -and (Get-Process -Id $_ -ErrorAction SilentlyContinue) })
        if (-not $running.Count -and -not $new.Count) { return [pscustomobject]@{ Tree = $found.Order; Left = @() } }
        if ($clock.Elapsed.TotalSeconds -ge $Seconds) { return [pscustomobject]@{ Tree = $found.Order; Left = $running } }
        foreach ($id in $running) { try { [Diagnostics.Process]::GetProcessById($id).Kill() } catch { } }
        Start-Sleep -Milliseconds 250
    }
}

# A process whose output and error lines are kept in order as .NET reads them, on .NET's own
# threads, which can't run PowerShell script blocks. Written for Windows PowerShell 5.1's C# 5.
if (-not ('EngineTestProcess' -as [type])) {
    Add-Type -TypeDefinition @'
using System.Collections.Generic;
using System.Diagnostics;
using System.Text;
using System.Threading;

public sealed class EngineTestProcess
{
    readonly List<string> lines = new List<string>();
    readonly ManualResetEvent closed = new ManualResetEvent(false);
    int open = 2;
    public Process Process { get; private set; }

    public static EngineTestProcess Start(string file, string arguments, string directory, Encoding encoding)
    {
        var info = new ProcessStartInfo(file, arguments);
        info.WorkingDirectory = directory;
        info.UseShellExecute = false;
        info.CreateNoWindow = true;
        info.RedirectStandardInput = true;
        info.RedirectStandardOutput = true;
        info.RedirectStandardError = true;
        info.StandardOutputEncoding = encoding;
        info.StandardErrorEncoding = encoding;
        var run = new EngineTestProcess();
        var process = new Process();
        process.StartInfo = info;
        process.OutputDataReceived += run.Keep;
        process.ErrorDataReceived += run.Keep;
        process.Start();
        process.StandardInput.Close();
        run.Process = process;
        process.BeginOutputReadLine();
        process.BeginErrorReadLine();
        return run;
    }

    void Keep(object sender, DataReceivedEventArgs e)
    {
        if (e.Data != null) { lock (lines) lines.Add(e.Data); }
        else if (Interlocked.Decrement(ref open) == 0) closed.Set();
    }

    public string[] Lines() { lock (lines) return lines.ToArray(); }

    // Whether output and error both closed within the time given. A process left running under
    // this one can hold them open, so no wait here is unbounded.
    public bool WaitOutput(int milliseconds) { return closed.WaitOne(milliseconds); }
}
'@
}

# Runs a program for at most $Seconds, keeping its output in $OutputFile. Returns ExitCode,
# TimedOut, Seconds, Tree (the processes killed), Left (any still running after 30 s of
# killing) and Lines. The tree is killed on every way out but the program's own exit, Ctrl+C
# and errors included.
function Invoke-TimeLimited([string]$File, [string[]]$Arguments, [int]$Seconds, [string]$OutputFile, [string]$Directory) {
    $line = (@($Arguments) | ForEach-Object { ConvertTo-Argument $_ }) -join ' '
    $clock = [Diagnostics.Stopwatch]::StartNew()
    $run = [EngineTestProcess]::Start($File, $line, $Directory, [Console]::OutputEncoding)
    $process = $run.Process
    $result = [pscustomobject]@{ ExitCode = $null; TimedOut = $false; Seconds = 0.0; Tree = @(); Left = @(); Lines = @() }
    $stopped = $false
    try {
        while (-not $process.WaitForExit(1000)) {
            if ($clock.Elapsed.TotalSeconds -ge $Seconds) {
                $result.TimedOut = $true
                $kill = Stop-ProcessTree $process.Id
                $result.Tree = @($kill.Tree); $result.Left = @($kill.Left)
                $stopped = $true
                break
            }
        }
        # The last lines, for at most 10 s: a process left running under it can hold the
        # output open.
        if ($process.HasExited) {
            $null = $run.WaitOutput(10000)
            if (-not $result.TimedOut) { $result.ExitCode = $process.ExitCode }
        }
    } finally {
        try {
            if (-not $stopped -and -not $process.HasExited) {
                $kill = Stop-ProcessTree $process.Id
                $result.Tree = @($kill.Tree); $result.Left = @($kill.Left)
            }
        } finally {
            $result.Seconds = [math]::Round($clock.Elapsed.TotalSeconds, 1)
            $result.Lines = $run.Lines()
            [IO.File]::WriteAllLines($OutputFile, [string[]]$result.Lines)
            $process.Dispose()
        }
    }
    return $result
}

if ($SelfTest) {
    $script:cases = 0; $script:wrong = 0
    function Expect([string]$Name, [bool]$Ok, [string]$Detail) {
        $script:cases++
        if ($Ok) { Write-Host "ok     $Name" } else { $script:wrong++; Write-Host "WRONG  $Name - $Detail" }
    }
    $folder = Join-Path ([IO.Path]::GetTempPath()) ('engine-tests-selftest-' + [guid]::NewGuid().ToString('N'))
    New-Item -ItemType Directory -Force $folder | Out-Null
    try {
        # A TRX file in the shape vstest writes, with one result per outcome given, or $Results as written.
        function Write-Trx([string]$Name, [string[]]$Outcomes, $Results = $null) {
            if ($null -eq $Results) {
                $n = 0
                $Results = '<Results>' + ((@($Outcomes) | ForEach-Object { $n++; "<UnitTestResult testName=`"T$n`" outcome=`"$_`" />" }) -join '') + '</Results>'
            }
            $path = Join-Path $folder $Name
            [IO.File]::WriteAllText($path, '<?xml version="1.0" encoding="utf-8"?><TestRun xmlns="http://microsoft.com/schemas/VisualStudio/TeamTest/2010">' + $Results + '</TestRun>')
            return $path
        }
        $since = (Get-Date).AddMinutes(-1)
        function Check([string]$Name, [string]$Trx, [bool]$TimedOut, $ExitCode, [string]$Status) {
            $v = Get-Verdict (Read-TrxOutcomes $Trx $since) $TimedOut $ExitCode
            $exit = switch ($Status) { 'PASS' { 0 } 'FAIL' { 1 } default { 2 } }
            Expect "$Name -> $Status" ($v.Status -eq $Status -and $v.Exit -eq $exit) "got $($v.Status) (exit $($v.Exit)): $($v.Why)"
        }
        Check 'every test passed' (Write-Trx 'pass.trx' @('Passed', 'Passed')) $false 0 'PASS'
        Check 'one test failed' (Write-Trx 'fail.trx' @('Passed', 'Failed')) $false 1 'FAIL'
        Check 'every test inconclusive, dotnet test exit 0' (Write-Trx 'none-ran.trx' @('NotExecuted', 'NotExecuted')) $false 0 'INCONCLUSIVE'
        Check 'some tests inconclusive, the rest passed' (Write-Trx 'some-ran.trx' @('Passed', 'NotExecuted')) $false 0 'INCONCLUSIVE'
        Check 'no test, an empty Results element' (Write-Trx 'empty.trx' @() '<Results />') $false 0 'INCONCLUSIVE'
        Check 'no test, no Results element' (Write-Trx 'no-results.trx' @() '') $false 0 'INCONCLUSIVE'
        Check 'no TRX file' (Join-Path $folder 'missing.trx') $false 1 'FAIL'
        $old = Write-Trx 'old.trx' @('Passed')
        (Get-Item -LiteralPath $old).LastWriteTime = (Get-Date).AddHours(-1)
        Check "an earlier run's TRX file" $old $false 0 'FAIL'
        Check 'the time limit, though every test so far passed' (Write-Trx 'timed-out.trx' @('Passed')) $true $null 'FAIL'
        Check 'a non-zero exit with no failed test' (Write-Trx 'exit.trx' @('Passed')) $false 1 'FAIL'
        Check 'a test that passed but the run aborted' (Write-Trx 'aborted.trx' @('Passed', 'PassedButRunAborted')) $false 0 'FAIL'
        Check 'a test that timed out' (Write-Trx 'timeout.trx' @('Passed', 'Timeout')) $false 0 'FAIL'
        $why = Write-Trx 'message.trx' @() '<Results><UnitTestResult testName="Setup_SavedSceneLoads" outcome="NotExecuted"><Output><ErrorInfo><Message>Assert.Inconclusive failed. No saved scene.</Message></ErrorInfo></Output></UnitTestResult></Results>'
        $read = Read-TrxOutcomes $why $since
        Expect "an inconclusive test's name and message are read" ($read.Tests.Count -eq 1 -and $read.Tests[0].Name -eq 'Setup_SavedSceneLoads' -and $read.Tests[0].Message -eq 'Assert.Inconclusive failed. No saved scene.') "read $(@($read.Tests | ForEach-Object { "$($_.Name): $($_.Message)" }) -join '; ')"

        foreach ($pair in @(@('plain', 'plain'), @('with space', '"with space"'), @('quote"inside', '"quote\"inside"'), @('C:\a b\', '"C:\a b\\"'), @('', '""'))) {
            Expect "an argument quoted: $($pair[0])" ((ConvertTo-Argument $pair[0]) -ceq $pair[1]) "got $(ConvertTo-Argument $pair[0])"
        }

        # Planted process lists: 1 is a process outside the tree.
        function Entry([int]$Parent, [long]$Start) { [pscustomobject]@{ Parent = $Parent; Start = $Start } }
        $known = [System.Collections.Generic.Dictionary[int, long]]::new()
        $known[100] = 1000
        $gone = @{ 200 = (Entry 100 1500); 300 = (Entry 200 1600); 400 = (Entry 1 10) }
        $found = (Find-ProcessTree 100 $gone $known).Order -join ','
        Expect 'a tree whose root has gone is walked from the root it had' ($found -eq '100,200,300') "found $found"
        $reused = @{ 100 = (Entry 1 5000); 200 = (Entry 100 1500); 500 = (Entry 100 6000); 600 = (Entry 100 900) }
        $found = (Find-ProcessTree 100 $reused $known).Order -join ','
        Expect "a root's ID used again leaves out the new holder's children" ($found -eq '100,200') "found $found"

        if ([Environment]::OSVersion.Platform -eq 'Win32NT') {
            # A hung tree: a shell that prints its ID, starts a second that prints its own and
            # sleeps, and sleeps itself. The time limit must kill both and keep the output. Each
            # also writes its ID to a file, and flushes its output itself, so a line a killed
            # shell still held can't read as a line the runner lost; the parent passes the
            # child's line on the same way. Both run from script files: on some machines
            # Windows PowerShell 5.1 never returns from -EncodedCommand.
            $shell = (Get-Process -Id $PID).Path
            function Quote([string]$Text) { "'" + $Text.Replace("'", "''") + "'" }
            function Say([string]$Name) { "[IO.File]::WriteAllText($(Quote (Join-Path $folder "$Name.pid")), [string]`$PID)`r`n[Console]::Out.WriteLine('$Name ' + `$PID)`r`n[Console]::Out.Flush()`r`n" }
            function Plant([string]$Name, [string]$Code) {
                $path = Join-Path $folder "$Name.ps1"
                [IO.File]::WriteAllText($path, $Code, [Text.UTF8Encoding]::new($true))
                return $path
            }
            $child = Plant 'child' "$(Say 'child')Start-Sleep -Seconds 600`r`n"
            $parent = Plant 'parent' ("$(Say 'parent')& $(Quote $shell) -NoProfile -NonInteractive -File $(Quote $child) | ForEach-Object { [Console]::Out.WriteLine(`$_); [Console]::Out.Flush() }`r`nStart-Sleep -Seconds 600`r`n")
            $run = Invoke-TimeLimited $shell @('-NoProfile', '-NonInteractive', '-File', $parent) 15 (Join-Path $folder 'hung.txt') $folder
            $ids = @($run.Lines | ForEach-Object { if ($_ -match '^(parent|child) (\d+)$') { [int]$Matches[2] } })
            $filed = @('parent', 'child' | ForEach-Object { $f = Join-Path $folder "$_.pid"; if (Test-Path -LiteralPath $f) { [int](Get-Content -LiteralPath $f -TotalCount 1) } })
            $alive = @(@($run.Tree) + $filed | Where-Object { Get-Process -Id $_ -ErrorAction SilentlyContinue })
            $missed = @(@($ids) + $filed | Where-Object { $run.Tree -notcontains $_ })
            Expect 'the time limit kills a hung tree of two processes and keeps their output' ($run.TimedOut -and $ids.Count -eq 2 -and $filed.Count -eq 2 -and -not $missed.Count -and -not $alive.Count -and -not @($run.Left).Count) "timed out $($run.TimedOut); output '$($run.Lines -join ' | ')'; ID files $($filed -join ', '); killed $($run.Tree -join ', '); still running $($alive -join ', ')"
        } else {
            Write-Host 'skip   the time limit kills a hung tree of two processes (Windows only)'
        }
    } finally {
        Remove-Item -LiteralPath $folder -Recurse -Force -ErrorAction SilentlyContinue
    }
    Write-Host "Self-test: $($script:cases - $script:wrong) of $($script:cases) cases gave the expected result."
    exit $(if ($script:wrong) { 1 } else { 0 })
}

if ([Environment]::OSVersion.Platform -ne 'Win32NT') { Stop-Setup 'S&box engine tests run on Windows only.' }
# A shell started before these were set for the user lacks them, so read the user's values too.
if (-not $Engine) { $Engine = [Environment]::GetEnvironmentVariable('FACEPUNCH_ENGINE', 'User') }
if (-not $Source) { $Source = [Environment]::GetEnvironmentVariable('SBOX_PUBLIC', 'User') }
if (-not $Engine -or -not (Test-Path (Join-Path $Engine 'sbox-dev.exe'))) {
    Stop-Setup 'set FACEPUNCH_ENGINE (or pass -Engine) to the S&box install folder, the one containing sbox-dev.exe.'
}
$dotnet = Get-Command dotnet -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $dotnet -or -not (@(& $dotnet.Path --list-sdks 2>$null) -match '^10\.')) { Stop-Setup 'install the .NET 10 SDK: "dotnet --list-sdks" shows no 10.x SDK.' }
if ($TimeoutSeconds -le 0) { Stop-Setup '-TimeoutSeconds must be more than 0.' }
$tests = Join-Path $Project 'UnitTests'
if (-not (Get-ChildItem $tests -Filter *.csproj -ErrorAction SilentlyContinue)) {
    Stop-Setup "no test project in $tests. Open the project once in the S&box Editor so it generates one."
}
$projectDir = (Resolve-Path $Project).Path
$tests = (Resolve-Path $tests).Path

# Steam can update the engine at any launch; keep the source agents read on the same release.
$sync = Join-Path $PSScriptRoot 'sync_engine_source.ps1'
$sourceCheck = try {
    if (Test-Path $sync) { "$(& $sync -Engine $Engine -Source $Source)" -replace '^S&box source: ' }
    else { 'NOT CHECKED - sync_engine_source.ps1 is not next to this script.' }
} catch { "NOT SYNCED - the check failed: $($_.Exception.Message)" }

$version = (Get-Content (Join-Path $Engine '.version') -TotalCount 1 -ErrorAction SilentlyContinue)
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
    # Named once the lock is held, to the millisecond, so two runs started in the same second
    # don't share a folder and the second doesn't overwrite the first's results.
    if (-not $Out) { $Out = Join-Path $Project ('test-results\' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff')) }
    New-Item -ItemType Directory -Force $Out | Out-Null
    $Out = (Resolve-Path $Out).Path
    $trx = Join-Path $Out 'results.trx'
    $env:FACEPUNCH_ENGINE = $Engine
    $started = Get-Date
    $arguments = @('test', $tests, '--logger', 'console;verbosity=detailed', '--logger', 'trx;LogFileName=results.trx', '--results-directory', $Out)
    if ($Filter) { $arguments += @('--filter', $Filter) }
    $run = Invoke-TimeLimited $dotnet.Path $arguments $TimeoutSeconds (Join-Path $Out 'results.txt') $projectDir
    $output = @($run.Lines)

    $logLines = $null
    if ((Test-Path $log) -and (Get-Item $log).LastWriteTime -ge $started) {
        Copy-Item $log (Join-Path $Out 'testhost.log')
        $logLines = @(Get-Content (Join-Path $Out 'testhost.log'))
    }
} finally {
    $lock.ReleaseMutex()
}
$outcomes = Read-TrxOutcomes $trx $started
$verdict = Get-Verdict $outcomes $run.TimedOut $run.ExitCode

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

Write-Host "Engine:     S&box $version ($Engine)"
Write-Host "Source:     $sourceCheck"
Write-Host "Tests:      $($outcomes.Passed) passed, $($outcomes.Failed) failed, $($outcomes.Inconclusive) inconclusive, in $($run.Seconds) s$(if (-not $outcomes.Found) { ' (no TRX file)' })"
foreach ($t in @($outcomes.Tests | Where-Object { $_.Kind -ne 'passed' })) {
    $words = (@("$($t.Message)" -split "`r?`n" | Where-Object { $_.Trim() }) | Select-Object -First 2) -join ' / '
    Write-Host "  $($t.Kind.ToUpper()) $($t.Name)$(if ($words) { ": $words" })"
}
# With no test failed, a failure or an empty run is in the build or the run: show dotnet's own
# summary lines.
if (-not $outcomes.Failed -and ($verdict.Status -eq 'FAIL' -or -not ($outcomes.Passed + $outcomes.Inconclusive))) {
    $output | Select-String -Pattern '^\s*(Passed!|Failed!)|Test summary:|Test Run (Successful|Failed|Aborted)|No test matches|error CS\d+|Build FAILED' |
        Select-Object -First 10 | ForEach-Object { Write-Host "  $($_.Line.Trim())" }
}
if ($run.TimedOut) {
    Write-Host "  TIME LIMIT: stopped after $TimeoutSeconds s; killed $(@($run.Tree).Count) process(es)$(if (@($run.Left).Count) { "; still running: $(@($run.Left) -join ', ')" })"
}
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
Write-Host "Result:     $($verdict.Status) - $($verdict.Why)$(if ($verdict.Status -eq 'INCONCLUSIVE') { ' (not a pass)' })"
Write-Host "Saved:      $Out"
# An agent may cite engine source for these results, so say plainly when it isn't the release that ran.
if ($sourceCheck -match '^(NOT CHECKED|NOT SYNCED|NEAREST|UNKNOWN)') {
    Write-Host "Warning:    engine source is $($Matches[1]), not matched to S&box $version. Say so before citing sbox-public for this run; the Source line says why."
}
exit $verdict.Exit
