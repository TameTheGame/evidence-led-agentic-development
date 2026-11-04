<#
.SYNOPSIS
Holds an S&box start while another program is using the GPU, so S&box doesn't compete with it
for video memory or GPU time.

.DESCRIPTION
The engine test runner and the editor check call this before each S&box start; run it before
any other start too, such as sbox-cli --game or a dedicated server. It reads nvidia-smi and
counts the GPU as busy when:
  - any GPU's use is above -MaxUtilization percent (30 by default); or
  - a process that isn't S&box holds -MaxOtherVramMB MiB of video memory or more (1024, so
    1 GB, by default). The processes are those nvidia-smi lists as using the GPU for compute,
    such as a CUDA workflow. A process counts as S&box when its file name starts with sbox.
While the GPU is busy it says why and checks again every -IntervalSeconds (300, so 5 minutes,
by default). After -TimeoutSeconds (3600, so an hour, by default) it ends with NOT RUN;
-TimeoutSeconds 0 checks once. It only reads: it never stops, pauses or changes a process.

Under Windows' WDDM driver model, which a GPU that drives a display uses, nvidia-smi can't
report a process's own video memory and prints [N/A]. The script then reads that process's
dedicated video memory from Windows' GPU Process Memory counters
(Win32_PerfFormattedData_GPUPerformanceCounters_GPUProcessMemory), for the processes nvidia-smi
lists and no others. A process whose memory neither reports counts as busy, since it may hold
any amount. A figure larger than the memory the GPU has in use, or than the GPU has, can't be
one process's own, so the script reports it and doesn't hold on it. NVIDIA's overlay, which
nvidia-smi lists as a compute process, has read as 36163 MiB on a 32607 MiB card.

With no nvidia-smi, such as on a machine without an NVIDIA GPU, or when nvidia-smi fails, it
warns and goes ahead.

Exit code: 0 go ahead, 2 not run (the GPU stayed busy). -SelfTest checks the reading and the
waiting on faked nvidia-smi output, without a GPU, and waits for nothing.

.EXAMPLE
powershell -File tools/wait_for_gpu.ps1
powershell -File tools/wait_for_gpu.ps1 -TimeoutSeconds 0
powershell -File tools/wait_for_gpu.ps1 -MaxUtilization 50 -MaxOtherVramMB 4096 -TimeoutSeconds 7200
powershell -File tools/wait_for_gpu.ps1 -SelfTest
#>
param(
    [int]$MaxOtherVramMB = 1024,
    [int]$MaxUtilization = 30,
    [int]$IntervalSeconds = 300,
    [int]$TimeoutSeconds = 3600,
    [string]$NvidiaSmi = 'nvidia-smi',
    [switch]$SelfTest
)
$ErrorActionPreference = 'Stop'

# A number from nvidia-smi's CSV, or $null for [N/A], [Not Supported] and the like.
function ConvertTo-Number([string]$Text) {
    $value = 0.0
    $styles = [Globalization.NumberStyles]::Float
    if ([double]::TryParse($Text.Trim(), $styles, [Globalization.CultureInfo]::InvariantCulture, [ref]$value)) { return $value }
    return $null
}

# A process's file name from the path nvidia-smi gives.
function Get-Leaf([string]$Name) { return @($Name.Trim() -split '[\\/]')[-1] }

# Why the GPU is busy, one line for each reason in Busy, and figures it left out in Notes; Busy
# is empty when the GPU is free. $Gpus holds nvidia-smi's lines of "index, utilization.gpu,
# memory.used, memory.total", and $Apps its lines of "pid, process_name, used_memory", in
# percent and MiB. $Dedicated maps a process ID to the MiB of dedicated video memory Windows
# counts for it, or is $null; only the processes in $Apps are looked up in it.
function Get-GpuBusy([string[]]$Gpus, [string[]]$Apps, $Dedicated, [int]$MaxVram, [int]$MaxUse) {
    $busy = New-Object System.Collections.Generic.List[string]
    $notes = New-Object System.Collections.Generic.List[string]
    $inUse = 0.0; $size = 0.0; $cards = 0; $usedRead = $true; $sizeRead = $true
    foreach ($line in @($Gpus)) {
        $f = @($line -split ',')
        if ($f.Count -lt 2) { continue }
        $use = ConvertTo-Number $f[1]
        if ($null -ne $use -and $use -gt $MaxUse) { $busy.Add("GPU $($f[0].Trim()) is $use% in use, above $MaxUse%") }
        if ($f.Count -ge 4) {
            $cards++
            $used = ConvertTo-Number $f[2]; $total = ConvertTo-Number $f[3]
            if ($null -eq $used) { $usedRead = $false } else { $inUse += $used }
            if ($null -eq $total) { $sizeRead = $false } else { $size += $total }
        }
    }
    # No process can hold more than the GPUs have in use in all or, when that isn't read, more
    # than they have. With neither read, no figure is left out.
    $most = $null; $what = ''; $on = if ($cards -gt 1) { 'on the GPUs' } else { 'on the GPU' }
    if ($cards -and $usedRead -and $inUse -gt 0) { $most = $inUse; $what = "in use $on" } elseif ($cards -and $sizeRead -and $size -gt 0) { $most = $size; $what = $on }
    foreach ($line in @($Apps)) {
        $f = @($line -split ',')
        if ($f.Count -lt 3) { continue }
        $id = $f[0].Trim()
        # A path can hold a comma, so the name is every field between the ID and the memory.
        $leaf = Get-Leaf ($f[1..($f.Count - 2)] -join ',')
        if ($leaf -like 'sbox*') { continue }
        $mib = ConvertTo-Number $f[$f.Count - 1]
        $from = 'nvidia-smi'
        if ($null -eq $mib -and $null -ne $Dedicated -and $Dedicated.ContainsKey($id)) { $mib = [double]$Dedicated[$id]; $from = 'Windows' }
        if ($null -eq $mib) {
            $busy.Add("$leaf (process $id) uses the GPU, and neither nvidia-smi nor Windows reports how much video memory it holds")
        } elseif ($null -ne $most -and $mib -gt $most) {
            $notes.Add("$leaf (process $id) reads as $([math]::Round($mib)) MiB as $from counts it, more than the $([math]::Round($most)) MiB $what, so that figure isn't its own and is left out")
        } elseif ($mib -ge $MaxVram) {
            $busy.Add("$leaf (process $id) holds $([math]::Round($mib)) MiB of video memory as $from counts it, $MaxVram MiB or more")
        }
    }
    return [pscustomobject]@{ Busy = $busy.ToArray(); Notes = $notes.ToArray() }
}

# A short account of each GPU, for the line that says the GPU is free.
function Format-Gpus([string[]]$Gpus) {
    $parts = foreach ($line in @($Gpus)) {
        $f = @($line -split ',' | ForEach-Object { $_.Trim() })
        if ($f.Count -ge 4) { "GPU $($f[0]) at $($f[1])% use, $($f[2]) of $($f[3]) MiB used" }
    }
    return (@($parts) -join '; ')
}

# Each process's dedicated video memory in MiB, by process ID, from Windows' GPU counters, or an
# empty table when Windows doesn't have them. Each instance is named pid_<ID>_luid_..._phys_<n>.
function Get-DedicatedVram {
    $table = @{}
    try {
        foreach ($row in @(Get-CimInstance -ClassName Win32_PerfFormattedData_GPUPerformanceCounters_GPUProcessMemory -ErrorAction Stop)) {
            if ("$($row.Name)" -match '^pid_(\d+)_') {
                $id = $Matches[1]
                $mib = [double]$row.DedicatedUsage / 1MB
                if ($table.ContainsKey($id)) { $table[$id] += $mib } else { $table[$id] = $mib }
            }
        }
    } catch { }
    return $table
}

# One reading of nvidia-smi: its GPU and process lines, or Why it couldn't be read.
function Read-NvidiaSmi([string]$Exe) {
    function Reading($Gpus, $Apps, $Why) { [pscustomobject]@{ Gpus = @($Gpus); Apps = @($Apps); Dedicated = $null; Why = $Why } }
    $command = Get-Command $Exe -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
    if (-not $command) { return Reading @() @() "there is no $Exe" }
    $ErrorActionPreference = 'Continue'
    try {
        $gpus = @(& $command.Path '--query-gpu=index,utilization.gpu,memory.used,memory.total' '--format=csv,noheader,nounits' 2>$null | ForEach-Object { "$_" } | Where-Object { $_.Trim() })
        $gpuExit = $LASTEXITCODE
        $apps = @(& $command.Path '--query-compute-apps=pid,process_name,used_memory' '--format=csv,noheader,nounits' 2>$null | ForEach-Object { "$_" } | Where-Object { $_.Trim() })
        $appExit = $LASTEXITCODE
    } catch {
        return Reading @() @() "$Exe failed: $($_.Exception.Message)"
    } finally {
        $ErrorActionPreference = 'Stop'
    }
    if ($gpuExit -ne 0) { return Reading @() @() "$Exe exited $gpuExit" }
    if (-not @($gpus | Where-Object { $null -ne (ConvertTo-Number (@($_ -split ',') + '')[1]) }).Count) { return Reading @() @() "$Exe gave no GPU use to read" }
    if ($appExit -ne 0) { return Reading @() @() "$Exe exited $appExit when asked for its processes" }
    return Reading $gpus $apps $null
}

# Reads until the GPU is free or the time is up, and returns 0 to go ahead or 2 when it stayed
# busy. $Read returns a reading, as Read-NvidiaSmi does, and $Sleep waits the seconds it's given.
function Wait-ForGpu($Read, $Sleep, [int]$MaxVram, [int]$MaxUse, [int]$Interval, [int]$Timeout) {
    $waited = 0
    while ($true) {
        $reading = & $Read
        if ($reading.Why) {
            Write-Host "GPU:        not checked - $($reading.Why); going ahead"
            return 0
        }
        $check = Get-GpuBusy $reading.Gpus $reading.Apps $reading.Dedicated $MaxVram $MaxUse
        $busy = @($check.Busy)
        foreach ($note in @($check.Notes)) { Write-Host "GPU note:   $note" }
        if (-not $busy.Count) {
            Write-Host "GPU:        free - $(Format-Gpus $reading.Gpus)"
            return 0
        }
        if ($waited -ge $Timeout) {
            Write-Host "GPU:        NOT RUN - still busy after $waited s of waiting: $($busy -join '; ')"
            return 2
        }
        $next = [math]::Max(1, [math]::Min($Interval, $Timeout - $waited))
        Write-Host "GPU:        busy - $($busy -join '; '). Checking again in $next s; $waited of $Timeout s waited."
        & $Sleep $next
        $waited += $next
    }
}

if ($SelfTest) {
    $script:cases = 0; $script:wrong = 0
    function Expect([string]$Name, [bool]$Held, [string]$Why) {
        $script:cases++
        if ($Held) { Write-Host "ok     $Name - $Why" } else { $script:wrong++; Write-Host "WRONG  $Name - $Why" }
    }
    function Busy([string[]]$Gpus, [string[]]$Apps, $Dedicated = $null, [int]$MaxVram = 1024, [int]$MaxUse = 30) {
        # The comma keeps one reason an array, so [0] is its first line, not its first letter.
        return , @((Get-GpuBusy $Gpus $Apps $Dedicated $MaxVram $MaxUse).Busy)
    }
    function Notes([string[]]$Gpus, [string[]]$Apps, $Dedicated = $null) {
        return , @((Get-GpuBusy $Gpus $Apps $Dedicated 1024 30).Notes)
    }
    function Said($Reasons) { if ($Reasons.Count) { return "busy: $($Reasons -join '; ')" } else { return 'free' } }
    # nvidia-smi's lines, as its CSV prints them on Windows.
    $idle = '0, 4, 1350, 24576'
    # Enough memory in use for the processes the busy cases plant.
    $loaded = '0, 4, 8000, 24576'
    $job = 'C:\Tools\gpu-job\python.exe'
    $sbox = 'C:\Program Files (x86)\Steam\steamapps\common\sbox\sbox-dev.exe'

    $r = Busy @($idle) @(); Expect 'an idle GPU with no compute process' ($r.Count -eq 0) (Said $r)
    $r = Busy @('0, 45, 9000, 24576') @(); Expect 'planted fault: a GPU at 45% use' ($r.Count -eq 1) (Said $r)
    $r = Busy @('0, 30, 9000, 24576') @(); Expect 'a GPU at exactly 30% use, which is not above it' ($r.Count -eq 0) (Said $r)
    $r = Busy @('0, 4, 1350, 24576', '1, 88, 20000, 24576') @(); Expect 'the second of two GPUs busy' ($r.Count -eq 1 -and $r[0] -like 'GPU 1 *') (Said $r)
    $r = Busy @($loaded) @("4242, $job, 2048"); Expect 'planted fault: a CUDA process holding 2 GB' ($r.Count -eq 1 -and $r[0] -like 'python.exe (process 4242)*') (Said $r)
    $r = Busy @($idle) @("4242, $job, 1023"); Expect 'a process holding 1023 MiB, under 1 GB' ($r.Count -eq 0) (Said $r)
    $r = Busy @($idle) @("4242, $job, 1024"); Expect 'a process holding exactly 1 GB' ($r.Count -eq 1) (Said $r)
    $r = Busy @($idle) @("5150, $sbox, 6000"); Expect "S&box's own process, left out" ($r.Count -eq 0) (Said $r)
    $r = Busy @($idle) @("5150, C:\Games\SBOX.EXE, 6000"); Expect 'S&box by its file name in another case' ($r.Count -eq 0) (Said $r)
    $r = Busy @($loaded) @("4242, C:\AI\a, b\python.exe, 3000"); Expect 'a process whose path holds a comma' ($r.Count -eq 1 -and $r[0] -like 'python.exe (process 4242) holds 3000 MiB*') (Said $r)
    $r = Busy @($loaded) @("4242, $job, [N/A]") @{ '4242' = 3000.0 }; Expect "memory nvidia-smi gives as [N/A], 3000 MiB as Windows counts it" ($r.Count -eq 1 -and $r[0] -like '*as Windows counts it*') (Said $r)
    $r = Busy @($idle) @("4242, $job, [N/A]") @{ '4242' = 200.0 }; Expect 'memory nvidia-smi gives as [N/A], 200 MiB as Windows counts it' ($r.Count -eq 0) (Said $r)
    $r = Busy @($idle) @("4242, $job, [N/A]") @{}; Expect 'memory neither nvidia-smi nor Windows reports' ($r.Count -eq 1 -and $r[0] -like '*neither nvidia-smi nor Windows*') (Said $r)
    $r = Busy @('0, 45, 9000, 24576') @("4242, $job, 2048") -MaxVram 4096 -MaxUse 50; Expect 'both under thresholds raised to 50% and 4096 MiB' ($r.Count -eq 0) (Said $r)
    $r = Busy @('0, 45, 9000, 24576') @("4242, $job, 2048", "4343, $job, 1500"); Expect 'each reason listed' ($r.Count -eq 3) (Said $r)
    # Figures that can't be one process's own: NVIDIA's overlay read as 36163 MiB from one
    # Windows counter instance on a 32607 MiB card with 26203 MiB in use.
    $card = '0, 2, 26203, 32607'
    $overlay = '23840, C:\Program Files\NVIDIA Corporation\NVIDIA App\CEF\NVIDIA Overlay.exe, [N/A]'
    $r = Busy @($card) @($overlay) @{ '23840' = 36163.0 }; $n = Notes @($card) @($overlay) @{ '23840' = 36163.0 }
    Expect "planted fault: a Windows figure above the GPU's memory in use is left out" ($r.Count -eq 0 -and $n.Count -eq 1 -and $n[0] -like 'NVIDIA Overlay.exe (process 23840) reads as 36163 MiB*') "$(Said $r); notes: $($n -join '; ')"
    $r = Busy @('0, 2, [N/A], 32607') @("4242, $job, 40000"); $n = Notes @('0, 2, [N/A], 32607') @("4242, $job, 40000")
    Expect "planted fault: a figure above the card's size, with its use unread, is left out" ($r.Count -eq 0 -and $n.Count -eq 1) "$(Said $r); notes: $($n -join '; ')"
    $r = Busy @($card) @("33016, $job, [N/A]") @{ '33016' = 16316.0 }
    Expect "a Windows figure within the GPU's memory in use still holds" ($r.Count -eq 1 -and $r[0] -like '*16316 MiB*') (Said $r)
    $r = Busy @('0, 2, 10000, 24576', '1, 2, 10000, 24576') @("4242, $job, [N/A]") @{ '4242' = 15000.0 }
    Expect "a figure above one GPU's memory in use but within two GPUs' still holds" ($r.Count -eq 1 -and $r[0] -like '*15000 MiB*') (Said $r)
    $r = Busy @($card) @() @{ '999' = 20000.0 }
    Expect "a large Windows figure for a process nvidia-smi doesn't list is left alone" ($r.Count -eq 0) (Said $r)
    $apps = @($overlay, '80812, C:\Tools\llm\llama-server.exe, [N/A]', "33016, $job, [N/A]")
    $windows = @{ '23840' = 36163.0; '80812' = 8642.0; '33016' = 16316.0 }
    $r = Busy @('0, 93, 26203, 32607') $apps $windows; $n = Notes @('0, 93, 26203, 32607') $apps $windows
    Expect 'a busy reading with the overlay in it holds on the other three reasons only' ($r.Count -eq 3 -and $n.Count -eq 1 -and -not @($r | Where-Object { $_ -like '*Overlay*' }).Count) "$(Said $r); notes: $($n -join '; ')"

    # The waiting, with readings handed out in turn and a sleep that only counts. The two script
    # blocks find $state and $Readings in Run-Wait's scope when Wait-ForGpu runs them.
    function Run-Wait([object[]]$Readings, [int]$Interval = 300, [int]$Timeout = 3600) {
        $state = @{ Turn = 0; Slept = New-Object System.Collections.Generic.List[int] }
        $read = { $at = [math]::Min($state.Turn, $Readings.Count - 1); $state.Turn++; $Readings[$at] }
        $sleep = { param($Seconds) $state.Slept.Add($Seconds) }
        $code = Wait-ForGpu $read $sleep 1024 30 $Interval $Timeout
        return [pscustomobject]@{ Code = $code; Reads = $state.Turn; Slept = @($state.Slept) }
    }
    function Planted([string[]]$Gpus, [string[]]$Apps = @(), $Why = $null) { [pscustomobject]@{ Gpus = $Gpus; Apps = $Apps; Dedicated = $null; Why = $Why } }
    $free = Planted @($idle); $hot = Planted @('0, 97, 20000, 24576')
    $w = Run-Wait @($free); Expect 'a free GPU goes ahead at once' ($w.Code -eq 0 -and $w.Reads -eq 1 -and $w.Slept.Count -eq 0) "exit $($w.Code), $($w.Reads) reading(s), slept $($w.Slept -join ', ')"
    $w = Run-Wait @($hot, $hot, $free); Expect 'busy twice, then free: it waits 5 minutes twice and goes ahead' ($w.Code -eq 0 -and $w.Reads -eq 3 -and ($w.Slept -join ',') -eq '300,300') "exit $($w.Code), $($w.Reads) reading(s), slept $($w.Slept -join ', ')"
    $w = Run-Wait @($hot) -Timeout 900; Expect 'planted fault: busy throughout ends NOT RUN at the timeout' ($w.Code -eq 2 -and ($w.Slept -join ',') -eq '300,300,300') "exit $($w.Code), $($w.Reads) reading(s), slept $($w.Slept -join ', ')"
    $w = Run-Wait @($hot) -Timeout 700; Expect 'a timeout between checks cuts the last wait short' ($w.Code -eq 2 -and ($w.Slept -join ',') -eq '300,300,100') "exit $($w.Code), slept $($w.Slept -join ', ')"
    $w = Run-Wait @($hot) -Timeout 0; Expect '-TimeoutSeconds 0 checks once' ($w.Code -eq 2 -and $w.Reads -eq 1 -and $w.Slept.Count -eq 0) "exit $($w.Code), $($w.Reads) reading(s)"
    $w = Run-Wait @($hot) -Interval 0 -Timeout 3; Expect 'an interval of 0 still waits a second between checks' ($w.Code -eq 2 -and ($w.Slept -join ',') -eq '1,1,1') "exit $($w.Code), slept $($w.Slept -join ', ')"
    $w = Run-Wait @((Planted @() @() 'there is no nvidia-smi')); Expect 'no nvidia-smi: it warns and goes ahead' ($w.Code -eq 0 -and $w.Slept.Count -eq 0) "exit $($w.Code)"

    # Read-NvidiaSmi on a program that isn't there, and on a faked nvidia-smi.
    $none = Read-NvidiaSmi (Join-Path ([IO.Path]::GetTempPath()) ('no-nvidia-smi-' + [Guid]::NewGuid().ToString('N') + '.exe'))
    Expect 'a missing nvidia-smi is read as not there' ([bool]$none.Why) "$($none.Why)"
    if ([Environment]::OSVersion.Platform -eq 'Win32NT') {
        $folder = Join-Path ([IO.Path]::GetTempPath()) ('wait-for-gpu-self-test-' + [Guid]::NewGuid().ToString('N'))
        New-Item -ItemType Directory -Force $folder | Out-Null
        try {
            # echo leaves findstr's exit code standing, so the fake ends with exit /b 0.
            $fake = Join-Path $folder 'nvidia-smi.cmd'
            [IO.File]::WriteAllText($fake, "@echo off`r`necho %* | findstr /c:""query-gpu"" >nul && (echo 0, 45, 9000, 24576& exit /b 0)`r`necho 4242, $job, [N/A]`r`nexit /b 0`r`n")
            $got = Read-NvidiaSmi $fake
            Expect 'a faked nvidia-smi is read' (-not $got.Why -and $got.Gpus.Count -eq 1 -and $got.Apps.Count -eq 1 -and $got.Apps[0] -like '4242,*') "why '$($got.Why)'; GPU lines '$($got.Gpus -join ' | ')'; process lines '$($got.Apps -join ' | ')'"
            $r = Busy $got.Gpus $got.Apps @{}; Expect "the faked reading is busy for both reasons" ($r.Count -eq 2) (Said $r)
            $broken = Join-Path $folder 'broken-smi.cmd'
            [IO.File]::WriteAllText($broken, "@echo off`r`necho NVIDIA-SMI has failed because it couldn't communicate with the NVIDIA driver.`r`nexit /b 9`r`n")
            $got = Read-NvidiaSmi $broken
            Expect 'a failing nvidia-smi is read as not checked' ($got.Why -like '*exited 9*') "$($got.Why)"
        } finally {
            Remove-Item -LiteralPath $folder -Recurse -Force -ErrorAction SilentlyContinue
        }
    } else {
        Write-Host 'skip   a faked nvidia-smi is read (Windows only)'
    }
    Write-Host "Self-test: $($script:cases - $script:wrong) of $($script:cases) cases gave the expected result."
    exit $(if ($script:wrong) { 1 } else { 0 })
}

$read = {
    $reading = Read-NvidiaSmi $NvidiaSmi
    # Windows' counters only when nvidia-smi leaves a process's memory out.
    if (-not $reading.Why -and @($reading.Apps | Where-Object { $null -eq (ConvertTo-Number (@($_ -split ','))[-1]) }).Count) {
        $reading.Dedicated = Get-DedicatedVram
    }
    $reading
}
exit (Wait-ForGpu $read { param($Seconds) Start-Sleep -Seconds $Seconds } $MaxOtherVramMB $MaxUtilization $IntervalSeconds $TimeoutSeconds)
