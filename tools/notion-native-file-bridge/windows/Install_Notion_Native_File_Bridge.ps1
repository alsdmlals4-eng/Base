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

if ($py) {
    & $py.Source -3.12 -c "import sys; assert sys.version_info >= (3, 12)"
    if ($LASTEXITCODE -ne 0) {
        throw "PYTHON_3_12_UNAVAILABLE"
    }
    & $py.Source -3.12 -m pip install --user $bridgeRoot
    if ($LASTEXITCODE -ne 0) {
        throw "BRIDGE_INSTALL_FAILED:$LASTEXITCODE"
    }
}
elif ($python) {
    & $python.Source -c "import sys; assert sys.version_info >= (3, 12)"
    if ($LASTEXITCODE -ne 0) {
        throw "PYTHON_3_12_UNAVAILABLE"
    }
    & $python.Source -m pip install --user $bridgeRoot
    if ($LASTEXITCODE -ne 0) {
        throw "BRIDGE_INSTALL_FAILED:$LASTEXITCODE"
    }
}
else {
    throw "PYTHON_UNAVAILABLE"
}

if ($Login) {
    Write-Host "Starting official Notion CLI login..."
    & $ntn.Source login
    if ($LASTEXITCODE -ne 0) {
        throw "NTN_LOGIN_FAILED:$LASTEXITCODE"
    }
}

$bridge = Get-Command "notion-native-file-bridge" -ErrorAction SilentlyContinue
if ($bridge) {
    & $bridge.Source preflight
    if ($LASTEXITCODE -ne 0) {
        throw "BRIDGE_PREFLIGHT_FAILED:$LASTEXITCODE"
    }
}
else {
    Write-Warning "Bridge installed, but the current shell PATH does not yet include the Python user Scripts directory. Open a new PowerShell window and run: notion-native-file-bridge preflight"
}

Write-Host "Notion Native File Bridge installation completed."
