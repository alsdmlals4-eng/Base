[CmdletBinding()]
param(
    [switch]$Login
)

$ErrorActionPreference = "Stop"

function Require-Command {
    param([Parameter(Mandatory = $true)][string]$Name)
    $command = Get-Command $Name -ErrorAction SilentlyContinue
    if (-not $command) {
        throw "$($Name.ToUpperInvariant())_UNAVAILABLE"
    }
    return $command.Source
}

function Require-MajorVersion {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][int]$MinimumMajor,
        [Parameter(Mandatory = $true)][string]$VersionText
    )
    $clean = $VersionText.Trim().TrimStart('v')
    $majorText = ($clean -split '\.')[0]
    $major = 0
    if (-not [int]::TryParse($majorText, [ref]$major)) {
        throw "${Name}_VERSION_UNREADABLE:$VersionText"
    }
    if ($major -lt $MinimumMajor) {
        throw "${Name}_VERSION_TOO_OLD:$VersionText (need major >= $MinimumMajor)"
    }
}

function Test-Python312 {
    param(
        [Parameter(Mandatory = $true)][string]$Command,
        [string[]]$PrefixArgs = @()
    )
    & $Command @PrefixArgs -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 12) else 1)" *> $null
    return ($LASTEXITCODE -eq 0)
}

$node = Require-Command "node"
$npm = Require-Command "npm"
Require-MajorVersion "NODE" 22 (& $node --version)
Require-MajorVersion "NPM" 10 (& $npm --version)

$ntn = Get-Command "ntn" -ErrorAction SilentlyContinue
if (-not $ntn) {
    Write-Host "Installing official Notion CLI (ntn) with npm..."
    & $npm install --global ntn
    if ($LASTEXITCODE -ne 0) {
        throw "NTN_INSTALL_FAILED:$LASTEXITCODE"
    }
    $ntn = Get-Command "ntn" -ErrorAction SilentlyContinue
    if (-not $ntn) {
        throw "NTN_UNAVAILABLE_AFTER_INSTALL"
    }
}

& $ntn.Source --version
if ($LASTEXITCODE -ne 0) {
    throw "NTN_VERSION_CHECK_FAILED:$LASTEXITCODE"
}

$bridgeRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$py = Get-Command "py" -ErrorAction SilentlyContinue
$python = Get-Command "python" -ErrorAction SilentlyContinue
$pythonCommand = $null
$pythonPrefixArgs = @()

if ($py -and (Test-Python312 -Command $py.Source -PrefixArgs @("-3.12"))) {
    $pythonCommand = $py.Source
    $pythonPrefixArgs = @("-3.12")
}
elif ($python -and (Test-Python312 -Command $python.Source)) {
    $pythonCommand = $python.Source
}
else {
    throw "PYTHON_3_12_UNAVAILABLE"
}

& $pythonCommand @pythonPrefixArgs -m pip install --user $bridgeRoot
if ($LASTEXITCODE -ne 0) {
    throw "BRIDGE_INSTALL_FAILED:$LASTEXITCODE"
}

if ($Login) {
    Write-Host "Starting official Notion CLI login..."
    & $ntn.Source login
    if ($LASTEXITCODE -ne 0) {
        throw "NTN_LOGIN_FAILED:$LASTEXITCODE"
    }
}

# Run through the selected interpreter so installation verification does not
# depend on the Python user Scripts directory already being on PATH.
& $pythonCommand @pythonPrefixArgs -m notion_native_file_bridge.cli preflight
if ($LASTEXITCODE -ne 0) {
    throw "BRIDGE_PREFLIGHT_FAILED:$LASTEXITCODE"
}

Write-Host "Notion Native File Bridge installation completed."
