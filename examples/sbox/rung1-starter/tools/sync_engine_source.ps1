<#
.SYNOPSIS
Keeps a local clone of Facepunch/sbox-public on the S&box release that is installed.

.DESCRIPTION
Agents read engine source from a clone of Facepunch/sbox-public, but the engine they run is
the one Steam installed, and the two drift apart. Facepunch tags each public Steam release in
sbox-public (for example 26.10.02, or 26.07.08b for a hotfix), and the install names its
release on the first line of its .version file. This script:
  1. reads the installed release;
  2. fetches that release's tag into the clone, only if the clone doesn't have it yet;
  3. checks the tag out as a detached HEAD, unless the clone has local changes; and
  4. prints one line: MATCH, SYNCED, NEAREST, UNKNOWN (a staging build, which has no public
     tag), NOT SYNCED with the reason, or NOT CHECKED when the install or clone isn't given.
A hotfix can ship before Facepunch tags it. Until the tag appears, the script checks out the
nearest tagged release before the hotfix and says NEAREST; a later run picks up the tag.
It changes nothing else in the clone: no branches, commits, or pushes. Run
"git switch master" in the clone to go back to the latest source.
It always exits 0, so a session start or test run never stops on it. Read the line.

.EXAMPLE
powershell -File tools\sync_engine_source.ps1 -Source C:\src\sbox-public
#>
param(
    [string]$Engine = $env:FACEPUNCH_ENGINE,
    [string]$Source = $env:SBOX_PUBLIC,
    [int]$FetchSeconds = 120
)
$ErrorActionPreference = 'Stop'
# A shell started before these were set for the user lacks them, so read the user's values too.
if (-not $Engine) { $Engine = [Environment]::GetEnvironmentVariable('FACEPUNCH_ENGINE', 'User') }
if (-not $Source) { $Source = [Environment]::GetEnvironmentVariable('SBOX_PUBLIC', 'User') }
# Windows PowerShell passes -Source "C:\path\" through with its closing quote; no path has one.
$Engine = "$Engine".Trim().Trim('"')
$Source = "$Source".Trim().Trim('"')

function Invoke-Git {
    # Windows PowerShell stops on a native command's stderr when the preference is Stop.
    $ErrorActionPreference = 'Continue'
    $text = @(& git -C $Source @args 2>&1 | ForEach-Object { "$_" })
    [pscustomobject]@{ Code = $LASTEXITCODE; Text = ($text -join "`n").Trim() }
}

function Get-Position {
    $where = (Invoke-Git describe --tags --always HEAD).Text
    $branch = Invoke-Git symbolic-ref --short -q HEAD
    if ($branch.Code -eq 0) { "$where on $($branch.Text)" } else { $where }
}

# git fetch and ls-remote can hang on a bad network, so they run with a time limit. Code is
# git's exit code, or -1 when it ran out of time; Problem is the last error line.
function Invoke-TimedGit([string]$Arguments) {
    $info = New-Object System.Diagnostics.ProcessStartInfo
    $info.FileName = 'git'
    $info.WorkingDirectory = $Source
    $info.Arguments = $Arguments
    $info.UseShellExecute = $false
    $info.RedirectStandardOutput = $true
    $info.RedirectStandardError = $true
    $info.CreateNoWindow = $true
    $process = [System.Diagnostics.Process]::Start($info)
    $errors = $process.StandardError.ReadToEndAsync()
    $null = $process.StandardOutput.ReadToEndAsync()
    if (-not $process.WaitForExit($FetchSeconds * 1000)) {
        # Stop git's helpers too, such as git-remote-https; Kill() alone leaves them running.
        $ErrorActionPreference = 'Continue'
        & taskkill.exe /T /F /PID $process.Id 2>&1 | Out-Null
        try { $process.Kill() } catch { }
        return [pscustomobject]@{ Code = -1; Problem = "the fetch took longer than $FetchSeconds s" }
    }
    $process.WaitForExit()
    # git's first fatal line names the problem; the lines after it are advice.
    $lines = @($errors.Result.Trim() -split "`n" | ForEach-Object { $_.Trim() })
    $problem = @($lines | Where-Object { $_ -match '^(fatal|error):' }) + $lines[-1]
    [pscustomobject]@{ Code = $process.ExitCode; Problem = $problem[0] }
}

# Fetches a tag into the clone. Returns $null once it is there, 'missing' when origin has no
# such tag, or why the fetch failed.
function Get-Tag([string]$Tag) {
    $fetch = Invoke-TimedGit "fetch --no-tags origin refs/tags/${Tag}:refs/tags/${Tag}"
    if ($fetch.Code -eq 0) { return $null }
    if ($fetch.Code -ne -1) {
        # git's fetch error is worded for people; ls-remote exits 2 when the tag isn't there.
        if ((Invoke-TimedGit "ls-remote --exit-code --tags origin refs/tags/$Tag").Code -eq 2) { return 'missing' }
    }
    return $fetch.Problem
}

# The tag's commit, fetching the tag first if the clone lacks it. Problem is 'missing', why the
# fetch failed, or $null.
function Resolve-Tag([string]$Tag) {
    $found = Invoke-Git rev-parse --verify --quiet "refs/tags/$Tag^{commit}"
    if ($found.Code -ne 0) {
        $problem = Get-Tag $Tag
        if ($problem) { return [pscustomobject]@{ Commit = $null; Problem = $problem } }
        $found = Invoke-Git rev-parse --verify --quiet "refs/tags/$Tag^{commit}"
        if ($found.Code -ne 0) { return [pscustomobject]@{ Commit = $null; Problem = 'missing' } }
    }
    [pscustomobject]@{ Commit = $found.Text; Problem = $null }
}

# Checks the tag out unless the clone is already there or has local changes. Returns 'here',
# 'moved', 'changes', or why the checkout failed.
function Set-Clone([string]$Tag, [string]$Commit) {
    if ((Invoke-Git rev-parse HEAD).Text -eq $Commit) { return 'here' }
    if ((Invoke-Git status --porcelain).Text) { return 'changes' }
    $moved = Invoke-Git -c advice.detachedHead=false checkout --quiet --detach "refs/tags/$Tag"
    if ($moved.Code -ne 0) { return "git checkout failed ($(@($moved.Text -split "`n")[-1]))" }
    return 'moved'
}

# A hotfix shipped before its tag: use the nearest tagged release before it, the earlier
# hotfixes of the same release first, then the release itself.
function Sync-Nearest([string]$Release, [string]$Before) {
    $base = $Release.Substring(0, 8)
    $letter = [int][char]$Release[8]
    $earlier = @(for ($c = $letter - 1; $c -ge [int][char]'a'; $c--) { $base + [char]$c }) + $base
    foreach ($candidate in $earlier) {
        $near = Resolve-Tag $candidate
        if ($near.Problem -eq 'missing') { continue }
        if ($near.Problem) { return "NOT SYNCED - origin has no tag $Release yet, and fetching $candidate failed ($($near.Problem)). The clone was left at $Before." }
        $why = "origin has no tag $Release yet, so engine source is approximate; a later run picks up the tag"
        switch (Set-Clone $candidate $near.Commit) {
            'here' { return "NEAREST - sbox-public is at $candidate, the nearest tagged release before $Release; $why." }
            'moved' { return "NEAREST - moved sbox-public from $Before to $candidate, the nearest tagged release before $Release; $why." }
            'changes' { return "NOT SYNCED - origin has no tag $Release yet, and sbox-public has local changes, so it was left at $Before. Read the nearest release with: git show ${candidate}:<path>" }
            default { return "NOT SYNCED - origin has no tag $Release yet, and moving to $candidate failed: $_. The clone was left at $Before." }
        }
    }
    return "NOT SYNCED - origin has no tag $Release yet, nor any earlier tag of $base. The clone was left at $Before."
}

function Sync {
    if (-not $Engine -or -not (Test-Path (Join-Path $Engine '.version'))) {
        return 'NOT CHECKED - no S&box install with a .version file; set FACEPUNCH_ENGINE or pass -Engine.'
    }
    if (-not $Source) { return 'NOT CHECKED - no sbox-public clone given; set SBOX_PUBLIC or pass -Source.' }
    if (-not (Test-Path -LiteralPath (Join-Path $Source '.git'))) { return "NOT CHECKED - $Source is not a git clone." }
    # One absolute path for every git call, without a trailing backslash to break its quoting.
    $script:Source = (Resolve-Path -LiteralPath $Source).ProviderPath -replace '(?<=[^:])\\+$'

    $release = "$(Get-Content (Join-Path $Engine '.version') -TotalCount 1)".Trim()
    $before = Get-Position
    if ($release -notmatch '^\d\d\.\d\d\.\d\d[a-z]?$') {
        return "UNKNOWN - installed S&box $release is not a public release, so sbox-public has no tag for it. The clone was left at $before."
    }

    $found = Resolve-Tag $release
    if ($found.Problem -eq 'missing' -and $release.Length -eq 9) { return Sync-Nearest $release $before }
    if ($found.Problem -eq 'missing') { return "NOT SYNCED - origin has no tag $release yet; a later run picks it up. The clone was left at $before." }
    if ($found.Problem) { return "NOT SYNCED - could not fetch tag $release from origin ($($found.Problem)). The clone was left at $before." }

    switch (Set-Clone $release $found.Commit) {
        'here' { return "MATCH - sbox-public is at $release, the installed S&box release." }
        'moved' { return "SYNCED - moved sbox-public from $before to $release, the installed S&box release." }
        'changes' { return "NOT SYNCED - sbox-public has local changes, so it was left at $before. Read the installed release with: git show ${release}:<path>" }
        default { return "NOT SYNCED - $_. The clone was left at $before." }
    }
}

$saved = @{ SBOX_SKIP_HOOKS = $env:SBOX_SKIP_HOOKS; GIT_TERMINAL_PROMPT = $env:GIT_TERMINAL_PROMPT }
$held = $false
try {
    # Two sessions starting at once must not check out at the same time.
    $lock = New-Object System.Threading.Mutex($false, 'sbox-public-source-sync')
    try { $held = $lock.WaitOne([TimeSpan]::FromSeconds($FetchSeconds + 30)) } catch [System.Threading.AbandonedMutexException] { $held = $true }
    # sbox-public's optional git hooks download engine artifacts after a checkout; skip them.
    $env:SBOX_SKIP_HOOKS = '1'
    $env:GIT_TERMINAL_PROMPT = '0'
    $line = if ($held) { Sync } else { 'NOT SYNCED - another sync held the lock too long.' }
} catch {
    $line = "NOT SYNCED - unexpected error: $($_.Exception.Message)"
} finally {
    $env:SBOX_SKIP_HOOKS = $saved.SBOX_SKIP_HOOKS
    $env:GIT_TERMINAL_PROMPT = $saved.GIT_TERMINAL_PROMPT
    if ($held) { try { $lock.ReleaseMutex() } catch { } }
}
Write-Output "S&box source: $line"
exit 0
