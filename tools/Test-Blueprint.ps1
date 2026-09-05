[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'

$validators = @(
    (Join-Path $PSScriptRoot 'validate_blueprint.py'),
    (Join-Path $PSScriptRoot 'validate_context_authority_v05.py'),
    (Join-Path $PSScriptRoot 'validate_protocol_security_v05.py'),
    (Join-Path $PSScriptRoot 'validate_adoption_v05.py'),
    (Join-Path $PSScriptRoot 'validate_task_rigor_v05.py'),
    (Join-Path $PSScriptRoot 'validate_release_bundle_v05.py'),
    (Join-Path $PSScriptRoot 'validate_release.py')
)

foreach ($validator in $validators) {
    if (-not (Test-Path -LiteralPath $validator -PathType Leaf)) {
        throw "Blueprint validator not found: $validator"
    }
}

$pythonLauncher = Get-Command py -ErrorAction SilentlyContinue
if ($null -ne $pythonLauncher) {
    $pythonReady = $false
    try {
        & $pythonLauncher.Source -3 -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 3)' 2>$null
        $pythonReady = ($LASTEXITCODE -eq 0)
    }
    catch {
        $pythonReady = $false
    }
    if ($pythonReady) {
        foreach ($validator in $validators) {
            & $pythonLauncher.Source -3 $validator
            if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
        }
        exit 0
    }
}

$python3 = Get-Command python3 -ErrorAction SilentlyContinue
if ($null -ne $python3) {
    $pythonReady = $false
    try {
        & $python3.Source -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 3)' 2>$null
        $pythonReady = ($LASTEXITCODE -eq 0)
    }
    catch {
        $pythonReady = $false
    }
    if ($pythonReady) {
        foreach ($validator in $validators) {
            & $python3.Source $validator
            if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
        }
        exit 0
    }
}

$python = Get-Command python -ErrorAction SilentlyContinue
if ($null -ne $python) {
    $pythonReady = $false
    try {
        & $python.Source -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 3)' 2>$null
        $pythonReady = ($LASTEXITCODE -eq 0)
    }
    catch {
        $pythonReady = $false
    }
    if ($pythonReady) {
        foreach ($validator in $validators) {
            & $python.Source $validator
            if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
        }
        exit 0
    }
}

throw 'Python 3.10 or newer is required to run the dependency-free blueprint validator.'
