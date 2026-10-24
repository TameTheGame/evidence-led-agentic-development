<#
.SYNOPSIS
Rung-2 (editor) check for an S&box scene: it survives save, close, and reopen unchanged, and a
fixed camera captures it before and after.

.DESCRIPTION
Runs unattended through sbox-cli, which ships with S&box 26.10.13 and later
(<engine>\bin\managed\sbox-cli.exe) and talks to an editor over a local named pipe. The script:
  1. opens the project in an editor that sbox-cli owns, so the editor closes if the script dies;
  2. opens the scene, saves it, records the saved file's hash and its objects, and takes a
     screenshot from the fixed camera;
  3. quits the editor, opens the project in a new one, and opens the scene again;
  4. checks that the scene reopens with no unsaved changes and no error-level console lines,
     that every saved object comes back with the same name, parent, enabled state, and
     components, and that saving again writes a byte-identical file;
  5. takes the same screenshot, and reports how much it differs as a record, not a score;
  6. puts the scene file and the project's .sbproj back as they were, so the check leaves the
     working tree unchanged. The editor writes the .sbproj again when it starts if the file's
     text differs from what S&box writes, such as LF line endings on Windows.
Results go to test-results\editor-<time>\, with each editor's sbox-cli output and editor log.
On a failure it also prints the last lines of both. Exit code: 0 pass, 1 fail, 2 not run.

When S&box can't start the project, it logs the error and then shows an error box that waits for
someone to click OK, so the editor never answers. While the check waits for an editor, it looks
for that box and for the error in the editor log. On either, it saves the box's text to
error-box.txt, closes the editor and the box with it, and stops with NOT RUN and the error's own
words, so a failed start takes seconds, not the whole timeout. If a call fails later while the
editor shows a box, the check records the box the same way.

The editor skips a save when nothing changed, which would make step 4's comparison empty. So
each save first adds a marker object and undoes it: the content is unchanged, but the editor
writes the scene out again from what it loaded.

A project with code must report a finished, successful compile. A project with no Code or
Editor folder, in it or in its libraries, such as a content map, never compiles: editor_status
then reports no compile result, and the check doesn't wait for one.

The project must be closed in every editor first, because the check closes and reopens it.
Steam must be running, because S&box starts through it; the check doesn't start Steam, which
can update S&box. Editors accept sbox-cli unless Project Settings > AI > Enable MCP
Communication is off.

.EXAMPLE
powershell -File tools\editor_check.ps1 -Scene scenes/outpost.scene
powershell -File tools\editor_check.ps1 -Scene scenes/outpost.scene -Camera "0,-900,400" -Angles "20,90,0"
#>
param(
    [Parameter(Mandatory)][string]$Scene,
    [string]$Project = '.',
    [string]$Camera = '-600,-600,400',
    [string]$Angles = '25,45,0',
    [int]$Width = 1280,
    [int]$Height = 720,
    [string]$Engine = $env:FACEPUNCH_ENGINE,
    [string]$Out,
    [int]$TimeoutSeconds = 300
)
$ErrorActionPreference = 'Stop'
function Stop-Setup($message) { Write-Host "NOT RUN: $message"; exit 2 }

if ([Environment]::OSVersion.Platform -ne 'Win32NT') { Stop-Setup 'S&box editor checks run on Windows only.' }
# The S&box launcher sets FACEPUNCH_ENGINE as a user variable, which older shells lack.
if (-not $Engine) { $Engine = [Environment]::GetEnvironmentVariable('FACEPUNCH_ENGINE', 'User') }
if (-not $Engine -or -not (Test-Path (Join-Path $Engine 'sbox-dev.exe'))) {
    Stop-Setup 'set FACEPUNCH_ENGINE (or pass -Engine) to the S&box install folder, the one containing sbox-dev.exe.'
}
$cli = Join-Path $Engine 'bin\managed\sbox-cli.exe'
if (-not (Test-Path $cli)) { Stop-Setup "no sbox-cli in $Engine\bin\managed; it ships with S&box 26.10.13 and later." }
$version = Get-Content (Join-Path $Engine '.version') -TotalCount 1 -ErrorAction SilentlyContinue
# Without Steam the editor never starts, and sbox-cli gives up with little to go on.
if (-not (Get-Process steam -ErrorAction SilentlyContinue)) {
    Stop-Setup 'Steam is not running, and S&box needs it. Start Steam (for example: Start-Process steam://open/main), wait for it to sign in, and rerun.'
}

$dir = (Resolve-Path $Project).Path
if ($dir -like '*.sbproj') { $dir = Split-Path $dir }
if (-not (Get-ChildItem $dir -Filter *.sbproj)) { Stop-Setup "no .sbproj in $dir." }
# S&box compiles the Code and Editor folders of the project and of each library in Libraries\.
$codeRoots = @($dir) + @(Get-ChildItem (Join-Path $dir 'Libraries') -Directory -ErrorAction SilentlyContinue | ForEach-Object FullName)
$hasCode = [bool]($codeRoots | Where-Object { (Test-Path (Join-Path $_ 'Code')) -or (Test-Path (Join-Path $_ 'Editor')) })
$Scene = $Scene.Replace('\', '/').TrimStart('/')
$sceneFile = Join-Path $dir ('Assets\' + $Scene.Replace('/', '\'))
if (-not (Test-Path $sceneFile)) { Stop-Setup "no scene at $sceneFile; pass -Scene as the asset path, such as scenes/outpost.scene." }

if (-not $Out) { $Out = Join-Path $dir ('test-results\editor-' + (Get-Date -Format 'yyyyMMdd-HHmmss')) }
New-Item -ItemType Directory -Force $Out | Out-Null

# Runs sbox-cli and returns { Code; Out; Err }. Exit 0 = success, 2 = the tool reported an error,
# 1 = no editor to connect to, or bad arguments.
function Invoke-SboxCli([string[]]$Arguments) {
    # Windows PowerShell 5.1 strips double quotes from native arguments.
    if ($PSVersionTable.PSVersion.Major -lt 7) { $Arguments = $Arguments | ForEach-Object { $_ -replace '"', '\"' } }
    $errFile = [IO.Path]::GetTempFileName()
    try {
        $ErrorActionPreference = 'Continue'
        $text = & $cli @Arguments 2> $errFile | Out-String
        $code = $LASTEXITCODE
        $ErrorActionPreference = 'Stop'
        [pscustomobject]@{ Code = $code; Out = "$text".Trim(); Err = "$(Get-Content $errFile -Raw)".Trim() }
    } finally { Remove-Item $errFile -ErrorAction SilentlyContinue }
}

# Calls one editor tool on this project's editor; throws if it fails.
function Call([string]$Tool, [hashtable]$Arguments = @{}) {
    $r = Invoke-SboxCli @('--connect', $dir, '--call', $Tool, ($Arguments | ConvertTo-Json -Compress))
    if ($r.Code -ne 0) { throw "$Tool failed: $(if ($r.Err) { $r.Err } else { $r.Out })" }
    return $r.Out
}

# The sbox-cli process that owns an editor prints why it stopped, such as a failed start, and
# nothing else keeps that output. This collects it from .NET's own threads, which can't run
# PowerShell script blocks.
if (-not ('EditorCheckOutput' -as [type])) {
    Add-Type -TypeDefinition @'
using System.Collections.Concurrent;
using System.Diagnostics;
public static class EditorCheckOutput {
    public static ConcurrentQueue<string> Attach(Process process) {
        var lines = new ConcurrentQueue<string>();
        DataReceivedEventHandler keep = (sender, e) => {
            if (e.Data == null) return;
            lines.Enqueue(e.Data);
            string dropped;
            while (lines.Count > 5000) lines.TryDequeue(out dropped);
        };
        process.OutputDataReceived += keep;
        process.ErrorDataReceived += keep;
        return lines;
    }
}
'@
}

# S&box shows a native error box when it can't start, and waits on it until someone clicks OK
# (26.10.13:engine/Sandbox.Engine/Core/Bootstrap.cs, lines 113-127 and 331-348). This reads the
# title and text of each dialog box a process shows. It reads them with WM_GETTEXT, because
# GetWindowText doesn't read the controls of another process.
if (-not ('EditorCheckDialogs' -as [type])) {
    Add-Type -TypeDefinition @'
using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Text;
public static class EditorCheckDialogs {
    delegate bool EnumProc(IntPtr window, IntPtr data);
    [DllImport("user32.dll")] static extern bool EnumWindows(EnumProc callback, IntPtr data);
    [DllImport("user32.dll")] static extern bool EnumChildWindows(IntPtr parent, EnumProc callback, IntPtr data);
    [DllImport("user32.dll")] static extern uint GetWindowThreadProcessId(IntPtr window, out uint processId);
    [DllImport("user32.dll")] static extern bool IsWindowVisible(IntPtr window);
    [DllImport("user32.dll", CharSet = CharSet.Unicode)] static extern int GetClassName(IntPtr window, StringBuilder name, int size);
    [DllImport("user32.dll", CharSet = CharSet.Unicode)]
    static extern IntPtr SendMessageTimeout(IntPtr window, uint message, IntPtr wParam, StringBuilder lParam, uint flags, uint milliseconds, out IntPtr result);
    [DllImport("user32.dll")]
    static extern IntPtr SendMessageTimeout(IntPtr window, uint message, IntPtr wParam, IntPtr lParam, uint flags, uint milliseconds, out IntPtr result);

    static string ClassOf(IntPtr window) {
        var name = new StringBuilder(256);
        GetClassName(window, name, name.Capacity);
        return name.ToString();
    }

    // WM_GETTEXTLENGTH, then WM_GETTEXT, giving up after a second if the window doesn't answer.
    static string TextOf(IntPtr window) {
        IntPtr length, copied;
        if (SendMessageTimeout(window, 0x000E, IntPtr.Zero, IntPtr.Zero, 0x0002, 1000, out length) == IntPtr.Zero) return "";
        var text = new StringBuilder(length.ToInt32() + 1);
        if (SendMessageTimeout(window, 0x000D, (IntPtr)text.Capacity, text, 0x0002, 1000, out copied) == IntPtr.Zero) return "";
        return text.ToString();
    }

    // Each visible dialog box (window class #32770) of the process: its title, then the text of
    // each control other than its buttons, one per line.
    public static string[] Find(int processId) {
        var boxes = new List<string>();
        EnumWindows(delegate (IntPtr window, IntPtr data) {
            uint owner;
            GetWindowThreadProcessId(window, out owner);
            if (owner != processId || !IsWindowVisible(window) || ClassOf(window) != "#32770") return true;
            var lines = new List<string>();
            lines.Add(TextOf(window));
            EnumChildWindows(window, delegate (IntPtr child, IntPtr unused) {
                if (ClassOf(child) != "Button") {
                    var text = TextOf(child);
                    if (text.Length > 0) lines.Add(text);
                }
                return true;
            }, IntPtr.Zero);
            boxes.Add(string.Join(Environment.NewLine, lines.ToArray()));
            return true;
        }, IntPtr.Zero);
        return boxes.ToArray();
    }
}
'@
}
$editorLog = Join-Path $Engine 'logs\sbox-dev.log'
$sessions = New-Object System.Collections.Generic.List[object]

function Test-Open {
    $r = Invoke-SboxCli @('--list')
    if ($r.Code -ne 0 -or -not $r.Out) { return $false }
    # Windows PowerShell's ConvertFrom-Json passes a JSON array on as one object; the
    # parentheses make foreach walk its items in both shells.
    foreach ($i in ($r.Out | ConvertFrom-Json)) {
        $p = "$($i.project)"
        if ($p -like '*.sbproj') { $p = Split-Path $p }
        if ($p -and $p.TrimEnd('\') -eq $dir.TrimEnd('\')) { return $true }
    }
    return $false
}

# The editor process a session's sbox-cli started, once it exists.
function Get-EditorProcess($session) {
    if (-not $session.Editor) {
        $child = Get-CimInstance Win32_Process -Filter "ParentProcessId = $($session.Owner.Id) AND Name = 'sbox-dev.exe'" -ErrorAction SilentlyContinue |
            Select-Object -First 1
        if ($child) { $session.Editor = Get-Process -Id $child.ProcessId -ErrorAction SilentlyContinue }
    }
    return $session.Editor
}

# The text of each error box the editor shows; none once it has exited.
function Get-ErrorBoxes($process) {
    if (-not $process -or $process.HasExited) { return @() }
    try { return @([EditorCheckDialogs]::Find($process.Id)) } catch { return @() }
}

# The editor log's entry for a failed start, if there is one. Bootstrap logs the exception before
# it shows its box, and the exception's stack ends where Bootstrap caught it, in Init or PreInit
# (Bootstrap.cs, lines 123 and 333). Entries from before this start are skipped: the last run's
# log stays in place until the new editor starts logging.
function Get-LoggedStartupError([datetime]$Since) {
    if (-not (Test-Path $editorLog)) { return $null }
    try {
        # The editor keeps its log open, so read it with sharing allowed.
        $stream = [IO.File]::Open($editorLog, 'Open', 'Read', 'ReadWrite, Delete')
        try { $text = (New-Object IO.StreamReader($stream, [Text.Encoding]::UTF8)).ReadToEnd() } finally { $stream.Dispose() }
    } catch { return $null }
    # Each entry starts with its time (26.10.13:engine/Sandbox.System/Logging/Logging.cs, line 60).
    foreach ($entry in [regex]::Split($text, '(?m)^(?=\d{4}/\d\d/\d\d \d\d:\d\d:\d\d)')) {
        if ($entry -notmatch '^(\d{4}/\d\d/\d\d \d\d:\d\d:\d\d)') { continue }
        $time = [datetime]::ParseExact($Matches[1], 'yyyy/MM/dd HH:mm:ss', [Globalization.CultureInfo]::InvariantCulture)
        if ($time -lt $Since.AddSeconds(-2)) { continue }
        if ($entry -match '(?m)^\s*at Sandbox\.Engine\.Bootstrap\.(Pre)?Init\(') { return $entry.Trim() }
    }
    return $null
}

# One line from an error's text: its innermost exception, or else its first line that says more
# than "Failed to bootstrap engine." The box lists compile errors instead when there are any.
function Get-Detail([string]$Text) {
    $lines = @($Text -split "`r?`n|`t" | ForEach-Object { $_.Trim() } | Where-Object { $_ })
    $exception = @($lines | Where-Object { $_ -match '^(--->\s*)?[\w.]+Exception: ' } | Select-Object -Last 1)
    $line = if ($exception.Count) { $exception[0] -replace '^--->\s*' }
        else { @($lines | Where-Object { $_ -ne 'Failed to bootstrap engine.' } | Select-Object -First 1)[0] }
    if ("$line".Length -gt 300) { $line = $line.Substring(0, 300) + '...' }
    return "$line"
}

# Saves the error boxes' text to error-box.txt and returns one line about the first of them.
function Save-ErrorBoxes([string[]]$Boxes) {
    [IO.File]::WriteAllText((Join-Path $Out 'error-box.txt'), ($Boxes -join "`r`n`r`n"))
    $title, $rest = $Boxes[0] -split "`r?`n", 2
    $detail = Get-Detail "$rest"
    return "an error box, '$title'$(if ($detail) { ": $detail" })"
}

# Why the editor failed to start, or nothing while it is still starting. A log entry for a failed
# start waits a few seconds for the box, which comes just after it, because the box's text can
# hold compile errors that the log entry lacks.
function Get-StartupError($session) {
    $logged = Get-LoggedStartupError $session.Started
    $boxes = @(Get-ErrorBoxes (Get-EditorProcess $session))
    for ($i = 0; $logged -and -not $boxes.Count -and $i -lt 5; $i++) {
        Start-Sleep -Seconds 1
        $boxes = @(Get-ErrorBoxes (Get-EditorProcess $session))
    }
    if ($boxes.Count) { return "it showed $(Save-ErrorBoxes $boxes)" }
    if ($logged) {
        [IO.File]::WriteAllText((Join-Path $Out 'error-box.txt'), $logged)
        return "its log says $(Get-Detail $logged)"
    }
    return $null
}

# Closes an editor stuck behind an error box. When its input closes, sbox-cli closes the editor it
# owns, box and all, through the Windows job it started the editor in
# (26.10.13:engine/Launcher/SboxCli/Program.cs, lines 94-97, 111-120 and 169-186; OwnedProcess.cs,
# line 30).
function Close-StuckEditor($session) {
    if (-not $session.Owner.HasExited) {
        try { $session.Owner.StandardInput.Close() } catch { }
        if (-not $session.Owner.WaitForExit(30000)) { $session.Owner.Kill() }
    }
    $editor = $session.Editor
    if ($editor -and -not $editor.WaitForExit(10000)) { try { $editor.Kill() } catch { } }
    Save-SessionLogs
}

# Opens the project in an editor owned by a sbox-cli process, and waits for a finished compile
# if the project has code. Without code, editor_status reports LastCompileSucceeded as null.
function Start-Editor {
    $info = New-Object System.Diagnostics.ProcessStartInfo
    $info.FileName = $cli
    $info.Arguments = "--project `"$dir`" --idle-timeout 7200"
    $info.UseShellExecute = $false
    $info.CreateNoWindow = $true
    $info.RedirectStandardInput = $true
    $info.RedirectStandardOutput = $true
    $info.RedirectStandardError = $true
    $started = Get-Date
    $owner = [Diagnostics.Process]::Start($info)
    $n = $sessions.Count + 1
    $sessions.Add([pscustomobject]@{ Owner = $owner; Started = $started; Lines = [EditorCheckOutput]::Attach($owner)
        Output = Join-Path $Out "sbox-cli-$n.txt"; Log = Join-Path $Out "sbox-dev-$n.log"; Saved = $false; Editor = $null })
    $session = $sessions[$sessions.Count - 1]
    $owner.BeginOutputReadLine(); $owner.BeginErrorReadLine()
    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        $failure = Get-StartupError $session
        if ($failure) {
            Close-StuckEditor $session
            Stop-Setup "S&box couldn't start the project; $failure`nThe check closed the editor and its error box. Full text: $(Join-Path $Out 'error-box.txt'). Editor log: $($session.Log)"
        }
        if ($owner.HasExited) { throw "sbox-cli stopped before the editor was ready (exit $($owner.ExitCode)); see sbox-cli-$n.txt" }
        $r = Invoke-SboxCli @('--connect', $dir, '--call', 'editor_status')
        if ($r.Code -eq 0) {
            $status = $r.Out | ConvertFrom-Json
            if (-not $status.IsCompiling -and ($null -ne $status.LastCompileSucceeded -or -not $hasCode)) {
                return @{ Owner = $owner; Status = $status }
            }
        }
        Start-Sleep -Seconds 3
    }
    throw "the editor wasn't ready after $TimeoutSeconds s; see sbox-cli-$n.txt and sbox-dev-$n.log"
}

# Saves each stopped editor's sbox-cli output, and the editor log it wrote, once.
function Save-SessionLogs {
    foreach ($s in $sessions) {
        if ($s.Saved -or -not $s.Owner.HasExited) { continue }
        $s.Owner.WaitForExit()   # without a time limit, this also waits for the last output lines
        [IO.File]::WriteAllLines($s.Output, [string[]]$s.Lines.ToArray())
        if ((Test-Path $editorLog) -and (Get-Item $editorLog).LastWriteTime -ge $s.Started) { Copy-Item $editorLog $s.Log }
        $s.Saved = $true
    }
}

# Quits the editor the way a person closes it, then makes sure it is gone.
function Stop-Editor($owner) {
    if (-not $owner -or $owner.HasExited) { return }
    Invoke-SboxCli @('--connect', $dir, '--call', 'instance_console_command', '{"command":"quit"}') | Out-Null
    if (-not $owner.WaitForExit(60000)) {
        $owner.StandardInput.Close()   # sbox-cli then closes the editor it owns
        if (-not $owner.WaitForExit(30000)) { $owner.Kill() }
    }
    for ($i = 0; $i -lt 20 -and (Test-Open); $i++) { Start-Sleep -Seconds 1 }
    Save-SessionLogs
}

# One line per saved object: parent, id, name, enabled state, and component types. Editor-only
# objects, such as the editor camera, are left out: their ids aren't in the saved file.
function Get-Objects {
    $text = [IO.File]::ReadAllText($sceneFile)
    $lines = New-Object System.Collections.Generic.List[string]
    function Walk($objects, $parent) {
        foreach ($o in @($objects)) {
            if ($text.Contains("`"$($o.Id)`"")) {
                $lines.Add("$parent/$($o.Id) '$($o.Name)' enabled=$($o.Enabled) [$(@($o.Components) -join ', ')]")
            }
            Walk $o.Children $o.Id
        }
    }
    Walk (Call 'scene_tree' @{ scene = $Scene; maxDepth = 0 } | ConvertFrom-Json).Objects ''
    return @($lines | Sort-Object)
}

function Get-Errors([string]$Name) {
    $text = Call 'read_console' @{ minimumLevel = 'Error'; limit = 200 }
    [IO.File]::WriteAllText((Join-Path $Out $Name), $text)
    return @($text -split "`r?`n" | Where-Object { $_ -match '^\d\d:\d\d:\d\d ' })
}

function Save-Screenshot([string]$Name) {
    Call 'set_editor_camera' @{ position = $Camera; angles = $Angles } | Out-Null
    $path = (Call 'editor_camera_screenshot' @{ width = $Width; height = $Height }) -split "`r?`n" |
        Where-Object { $_ -match '\.(png|jpg)$' } | Select-Object -Last 1
    if (-not $path -or -not (Test-Path $path)) { throw 'editor_camera_screenshot returned no image' }
    $target = Join-Path $Out $Name
    Copy-Item $path $target
    return $target
}

# Mean per-channel difference between two captures, as a percentage, on a 160x90 thumbnail.
function Get-Difference($a, $b) {
    Add-Type -AssemblyName System.Drawing
    $x = $null; $y = $null
    function Thumb($path) {
        $image = [System.Drawing.Image]::FromFile($path)
        try { New-Object System.Drawing.Bitmap $image, 160, 90 } finally { $image.Dispose() }
    }
    try {
        $x = Thumb $a; $y = Thumb $b
        $sum = 0
        for ($i = 0; $i -lt 160; $i++) {
            for ($j = 0; $j -lt 90; $j++) {
                $p = $x.GetPixel($i, $j); $q = $y.GetPixel($i, $j)
                $sum += [Math]::Abs($p.R - $q.R) + [Math]::Abs($p.G - $q.G) + [Math]::Abs($p.B - $q.B)
            }
        }
        return [Math]::Round(100 * $sum / (160 * 90 * 3 * 255), 2)
    } catch { return $null } finally { if ($x) { $x.Dispose() }; if ($y) { $y.Dispose() } }
}

function Get-Hash { (Get-FileHash $sceneFile -Algorithm SHA256).Hash.ToLower() }

# Saves the scene for real and returns the file's hash. An undone edit counts as a change, so
# the editor writes the whole scene out instead of skipping the save.
function Save-Scene([string]$Name) {
    Call 'create_game_object' @{ name = 'editor_check_marker' } | Out-Null
    Call 'undo' | Out-Null
    $result = Call 'save_scene' | ConvertFrom-Json
    if ($result.HasUnsavedChanges) { throw 'save_scene left unsaved changes' }
    if ([IO.File]::ReadAllText($sceneFile).Contains('editor_check_marker')) { throw 'the marker object was saved; undo did not remove it' }
    Copy-Item $sceneFile (Join-Path $Out $Name)
    return Get-Hash
}

if (Test-Open) { Stop-Setup "an editor has $dir open. Close it first; this check closes and reopens the editor." }

$original = [IO.File]::ReadAllBytes($sceneFile)
# The editor may rewrite the .sbproj when it starts (26.10.13:engine/Sandbox.Tools/Utility/Utility.Projects.cs).
$projectFiles = @{}
foreach ($f in Get-ChildItem $dir -Filter *.sbproj) { $projectFiles[$f.FullName] = [IO.File]::ReadAllBytes($f.FullName) }
$checks = [ordered]@{}
$notes = New-Object System.Collections.Generic.List[string]
$editor = $null
try {
    # First session: open, save, record.
    $editor = Start-Editor
    if ($editor.Status.LastCompileSucceeded -eq $false) { Stop-Setup "the project has $($editor.Status.LastCompileErrors) compile error(s); fix them first." }
    Call 'open_scene' @{ path = $Scene } | Out-Null
    $saved = Save-Scene 'saved-first.scene'
    if ($saved -ne (Get-FileHash -InputStream ([IO.MemoryStream]::new($original)) -Algorithm SHA256).Hash.ToLower()) {
        $notes.Add('the first save rewrote the scene file; the original is restored at the end')
    }
    $before = Get-Objects
    [IO.File]::WriteAllLines((Join-Path $Out 'objects-before.txt'), [string[]]$before)
    $beforeErrors = Get-Errors 'console-before.txt'
    if ($beforeErrors.Count) { $notes.Add("$($beforeErrors.Count) error line(s) in the first session; see console-before.txt") }
    $shotBefore = Save-Screenshot 'before.png'
    Stop-Editor $editor.Owner

    # Second session: reopen and compare.
    $editor = Start-Editor
    Call 'open_scene' @{ path = $Scene } | Out-Null
    $status = Call 'editor_status' | ConvertFrom-Json
    $afterErrors = Get-Errors 'console-after.txt'
    $checks['Reopen'] = if ($status.SceneHasUnsavedChanges) { 'FAIL - the scene has unsaved changes as soon as it opens' }
        elseif ($afterErrors.Count) { "FAIL - $($afterErrors.Count) error line(s) on reopen; see console-after.txt" }
        else { 'pass - no unsaved changes, no error lines' }
    $after = Get-Objects
    [IO.File]::WriteAllLines((Join-Path $Out 'objects-after.txt'), [string[]]$after)
    $diff = @(Compare-Object $before $after)
    $checks['Objects'] = if ($diff.Count) { "FAIL - $($diff.Count) line(s) differ; compare objects-before.txt and objects-after.txt" }
        else { "pass - $($before.Count) saved objects back unchanged" }
    $shotAfter = Save-Screenshot 'after.png'
    $resaved = Save-Scene 'saved-second.scene'
    $checks['Resave'] = if ($resaved -eq $saved) { "pass - byte-identical ($($saved.Substring(0, 12)))" }
        else { 'FAIL - the second save wrote a different file; compare saved-first.scene and saved-second.scene' }
    Stop-Editor $editor.Owner
    $editor = $null
} catch {
    $checks['Run'] = "FAIL - $($_.Exception.Message)"
    # A call can fail because the editor is stuck behind an error box: record it, and close it.
    foreach ($s in $sessions) {
        $boxes = @(Get-ErrorBoxes (Get-EditorProcess $s))
        if (-not $boxes.Count) { continue }
        $notes.Add("the editor showed $(Save-ErrorBoxes $boxes) (full text in error-box.txt)")
        Close-StuckEditor $s
    }
} finally {
    if ($editor) { try { Stop-Editor $editor.Owner } catch { if (-not $editor.Owner.HasExited) { $editor.Owner.Kill() } } }
    # An editor that failed to start never reached $editor; make sure its sbox-cli is gone too.
    foreach ($s in $sessions) { if (-not $s.Owner.HasExited) { try { Stop-Editor $s.Owner } catch { $s.Owner.Kill() } } }
    try { Save-SessionLogs } catch { $notes.Add("couldn't save the sbox-cli output: $($_.Exception.Message)") }
    if (-not (Test-Open)) {
        if ($null -ne $original) { [IO.File]::WriteAllBytes($sceneFile, $original) }
        foreach ($f in $projectFiles.Keys) {
            if ([Convert]::ToBase64String([IO.File]::ReadAllBytes($f)) -ne [Convert]::ToBase64String($projectFiles[$f])) {
                [IO.File]::WriteAllBytes($f, $projectFiles[$f])
                $notes.Add("the editor rewrote $(Split-Path $f -Leaf); the original is restored")
            }
        }
    }
}

$failed = @($checks.Values | Where-Object { $_ -like 'FAIL*' }).Count
Write-Host "Engine:     S&box $version ($Engine)"
Write-Host "Scene:      $Scene in $dir"
foreach ($k in $checks.Keys) { Write-Host ('{0,-11} {1}' -f "${k}:", $checks[$k]) }
if ($shotBefore -and $shotAfter) {
    $d = Get-Difference $shotBefore $shotAfter
    Write-Host "Screenshot: before.png and after.png from $Camera at $Angles; mean difference $(if ($null -ne $d) { "$d%" } else { 'not measured' }) (a record, not scored)"
}
foreach ($n in $notes) { Write-Host "Note:       $n" }
# On a failure, show the last editor's own account of it.
if (($failed -or -not $checks.Count) -and $sessions.Count) {
    $last = $sessions[$sessions.Count - 1]
    foreach ($file in @($last.Output, $last.Log)) {
        if (-not (Test-Path $file)) { continue }
        Write-Host "Last lines: $(Split-Path $file -Leaf)"
        # Both files are UTF-8 without a byte order mark, which Windows PowerShell reads as ANSI.
        Get-Content $file -Tail 15 -Encoding UTF8 | ForEach-Object { Write-Host "  $_" }
    }
}
Write-Host "Result:     $(if ($failed -or -not $checks.Count) { 'FAIL' } else { 'PASS' })"
Write-Host "Saved:      $Out"
exit $(if ($failed -or -not $checks.Count) { 1 } else { 0 })
