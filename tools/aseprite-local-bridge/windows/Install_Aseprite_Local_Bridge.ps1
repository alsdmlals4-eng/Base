[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectRoot,

    [Parameter(Mandatory = $false)]
    [string]$AsepritePath,

    [Parameter(Mandatory = $false)]
    [switch]$PersistAsepritePath
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Test-Python311 {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Command,

        [Parameter(Mandatory = $false)]
        [string[]]$PrefixArgs = @()
    )

    try {
        $versionText = & $Command @PrefixArgs -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>$null
        if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($versionText)) {
            return $false
        }
        $parts = $versionText.Trim().Split(".")
        if ($parts.Count -lt 2) {
            return $false
        }
        $major = [int]$parts[0]
        $minor = [int]$parts[1]
        return ($major -gt 3) -or ($major -eq 3 -and $minor -ge 11)
    }
    catch {
        return $false
    }
}

function Find-Python311 {
    if (Get-Command "py" -ErrorAction SilentlyContinue) {
        foreach ($selector in @("-3.13", "-3.12", "-3.11")) {
            if (Test-Python311 -Command "py" -PrefixArgs @($selector)) {
                return [PSCustomObject]@{
                    Command = "py"
                    Args = @($selector)
                }
            }
        }
    }

    if (Get-Command "python" -ErrorAction SilentlyContinue) {
        if (Test-Python311 -Command "python") {
            return [PSCustomObject]@{
                Command = "python"
                Args = @()
            }
        }
    }

    throw "Python 3.11 or newer was not found. Install Python from https://www.python.org/downloads/windows/ and rerun this script."
}

function Resolve-AsepriteExecutable {
    param(
        [Parameter(Mandatory = $false)]
        [string]$ExplicitPath
    )

    if (-not [string]::IsNullOrWhiteSpace($ExplicitPath)) {
        if (-not (Test-Path -LiteralPath $ExplicitPath -PathType Leaf)) {
            throw "AsepritePath does not point to a file: $ExplicitPath"
        }
        return (Resolve-Path -LiteralPath $ExplicitPath).Path
    }

    $candidates = New-Object System.Collections.Generic.List[string]
    if (-not [string]::IsNullOrWhiteSpace($env:ASEPRITE_PATH)) {
        $candidates.Add($env:ASEPRITE_PATH)
    }

    $command = Get-Command "aseprite" -ErrorAction SilentlyContinue
    if ($null -ne $command) {
        $candidates.Add($command.Source)
    }

    foreach ($root in @($env:ProgramFiles, ${env:ProgramFiles(x86)}, $env:LOCALAPPDATA)) {
        if ([string]::IsNullOrWhiteSpace($root)) {
            continue
        }
        if ($root -eq $env:LOCALAPPDATA) {
            $candidates.Add((Join-Path $root "Programs\Aseprite\Aseprite.exe"))
        }
        else {
            $candidates.Add((Join-Path $root "Aseprite\Aseprite.exe"))
            $candidates.Add((Join-Path $root "Steam\steamapps\common\Aseprite\Aseprite.exe"))
        }
    }

    foreach ($candidate in $candidates) {
        if ([string]::IsNullOrWhiteSpace($candidate)) {
            continue
        }
        if (Test-Path -LiteralPath $candidate -PathType Leaf) {
            return (Resolve-Path -LiteralPath $candidate).Path
        }
    }

    throw @"
Aseprite.exe was not found.
- Direct purchase default: C:\Program Files\Aseprite\Aseprite.exe
- Steam default: C:\Program Files (x86)\Steam\steamapps\common\Aseprite\Aseprite.exe
- Steam custom library: Steam > Library > Aseprite > Manage > Browse local files
Rerun with -AsepritePath "<full path to Aseprite.exe>".
"@
}

function ConvertTo-SingleQuotedLiteral {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Value
    )

    return "'" + $Value.Replace("'", "''") + "'"
}

if (-not (Test-Path -LiteralPath $ProjectRoot -PathType Container)) {
    throw "ProjectRoot is not a directory: $ProjectRoot"
}
$ResolvedProjectRoot = (Resolve-Path -LiteralPath $ProjectRoot).Path
$AssetVaultLibrary = Join-Path $ResolvedProjectRoot ".asset-vault\library"
if (-not (Test-Path -LiteralPath $AssetVaultLibrary -PathType Container)) {
    throw @"
Asset Vault is not initialized: $AssetVaultLibrary
Run this first from the Base checkout:
python tools/project_asset_vault.py init --project-root "$ResolvedProjectRoot"
"@
}

$BridgeRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$RunnerPath = (Resolve-Path -LiteralPath (Join-Path $BridgeRoot "run_bridge.py")).Path
$ConfigTemplate = Join-Path $BridgeRoot "bridge_config.example.json"
$ProjectConfig = Join-Path $ResolvedProjectRoot ".aseprite-bridge.json"
$Python = Find-Python311
$PythonCommand = $Python.Command
$PythonPrefixArgs = @($Python.Args)
$ResolvedAseprite = Resolve-AsepriteExecutable -ExplicitPath $AsepritePath

$env:ASEPRITE_PATH = $ResolvedAseprite
if ($PersistAsepritePath) {
    [Environment]::SetEnvironmentVariable("ASEPRITE_PATH", $ResolvedAseprite, "User")
    Write-Host "ASEPRITE_PATH was persisted for the current Windows user."
}
else {
    Write-Host "ASEPRITE_PATH is set only for this PowerShell process."
}

if (-not (Test-Path -LiteralPath $ProjectConfig -PathType Leaf)) {
    Copy-Item -LiteralPath $ConfigTemplate -Destination $ProjectConfig
    Write-Host "Created project config: $ProjectConfig"
}
else {
    Write-Host "Preserved existing project config: $ProjectConfig"
}

$LauncherRoot = Join-Path $ResolvedProjectRoot ".asset-vault\tools"
New-Item -ItemType Directory -Force -Path $LauncherRoot | Out-Null
$LauncherPath = Join-Path $LauncherRoot "Aseprite_Local_Bridge.ps1"

$PythonCommandLiteral = ConvertTo-SingleQuotedLiteral $Python.Command
$PythonArgLiterals = @($Python.Args | ForEach-Object { ConvertTo-SingleQuotedLiteral $_ })
$PythonArgsText = $PythonArgLiterals -join ", "
$RunnerLiteral = ConvertTo-SingleQuotedLiteral $RunnerPath
$ProjectLiteral = ConvertTo-SingleQuotedLiteral $ResolvedProjectRoot
$AsepriteLiteral = ConvertTo-SingleQuotedLiteral $ResolvedAseprite

$LauncherContent = @"
`$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

`$BridgeArgs = @(`$args)
if (`$BridgeArgs.Count -lt 1) {
    throw "A bridge command is required: doctor, inspect, export-candidate, or validate-candidate."
}
`$AllowedCommands = @("doctor", "inspect", "export-candidate", "validate-candidate")
if (`$BridgeArgs[0] -notin `$AllowedCommands) {
    throw "Unsupported bridge command. Use doctor, inspect, export-candidate, or validate-candidate."
}

`$PythonCommand = $PythonCommandLiteral
`$PythonArgs = @($PythonArgsText)

& `$PythonCommand @PythonArgs $RunnerLiteral @BridgeArgs `
    --project-root $ProjectLiteral `
    --aseprite $AsepriteLiteral
exit `$LASTEXITCODE
"@

$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($LauncherPath, $LauncherContent, $Utf8NoBom)
Write-Host "Created local launcher: $LauncherPath"

Push-Location $ResolvedProjectRoot
try {
    & $PythonCommand @PythonPrefixArgs $RunnerPath "doctor" `
        --project-root $ResolvedProjectRoot `
        --aseprite $ResolvedAseprite
    if ($LASTEXITCODE -ne 0) {
        throw "Aseprite Local Bridge doctor failed with exit code $LASTEXITCODE"
    }
}
finally {
    Pop-Location
}

Write-Host "Aseprite Local Bridge launcher and doctor completed with no pip/network/PATH registration."
Write-Host "Use: & '$LauncherPath' doctor"
Write-Host "Rollback local launcher: $LauncherPath"
Write-Host "Next: copy a disposable .aseprite file under .asset-vault\library and run inspect/export-candidate."
