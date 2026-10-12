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
  4. prints one line: MATCH, SYNCED, UNKNOWN (a staging build, which has no public tag),
     NOT SYNCED with the reason, or NOT CHECKED when the install or clone isn't given.
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

# git fetch can hang on a bad network, so it runs with a time limit.
function Get-Tag([string]$Tag) {
    $info = New-Object System.Diagnostics.ProcessStartInfo
    $info.FileName = 'git'
    $info.WorkingDirectory = $Source
    $info.Arguments = "fetch --no-tags origin refs/tags/${Tag}:refs/tags/${Tag}"
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
        return "the fetch took longer than $FetchSeconds s"
    }
    if ($process.ExitCode -ne 0) { return @($errors.Result.Trim() -split "`n")[-1].Trim() }
    return $null
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

    $tag = Invoke-Git rev-parse --verify --quiet "refs/tags/$release^{commit}"
    if ($tag.Code -ne 0) {
        $problem = Get-Tag $release
        if ($problem) { return "NOT SYNCED - could not fetch tag $release from origin ($problem). The clone was left at $before." }
        $tag = Invoke-Git rev-parse --verify --quiet "refs/tags/$release^{commit}"
        if ($tag.Code -ne 0) { return "NOT SYNCED - origin has no tag $release. The clone was left at $before." }
    }

    if ((Invoke-Git rev-parse HEAD).Text -eq $tag.Text) { return "MATCH - sbox-public is at $release, the installed S&box release." }
    if ((Invoke-Git status --porcelain).Text) {
        return "NOT SYNCED - sbox-public has local changes, so it was left at $before. Read the installed release with: git show ${release}:<path>"
    }
    $moved = Invoke-Git -c advice.detachedHead=false checkout --quiet --detach "refs/tags/$release"
    if ($moved.Code -ne 0) { return "NOT SYNCED - git checkout failed ($(@($moved.Text -split "`n")[-1])). The clone was left at $before." }
    return "SYNCED - moved sbox-public from $before to $release, the installed S&box release."
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
