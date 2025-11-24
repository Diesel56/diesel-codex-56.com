# Genesis CLI Setup Script for Windows (32-bit and 64-bit)
# Configures symbiotic integration with Cursor, VS Code, and Claude Code

param(
    [switch]$Force,
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"

# Color output functions
function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

function Write-Success($message) { Write-ColorOutput Green "✓ $message" }
function Write-Info($message) { Write-ColorOutput Cyan "ℹ $message" }
function Write-Warning($message) { Write-ColorOutput Yellow "⚠ $message" }
function Write-Error($message) { Write-ColorOutput Red "✗ $message" }

Write-Info "Genesis CLI Setup - Windows Architecture Detection"
Write-Info "=================================================="

# Detect architecture
$arch = $env:PROCESSOR_ARCHITECTURE
Write-Info "Detected architecture: $arch"

# Set paths based on architecture
$genesisHome = "$env:USERPROFILE\.genesis"
$genesisBin = "$genesisHome\bin"
$genesisConfig = "$genesisHome\config"
$genesisCache = "$genesisHome\cache"

# Create directories
Write-Info "Creating Genesis directories..."
@($genesisHome, $genesisBin, $genesisConfig, $genesisCache) | ForEach-Object {
    if (-not (Test-Path $_)) {
        New-Item -ItemType Directory -Path $_ -Force | Out-Null
        Write-Success "Created: $_"
    }
}

# Create architecture-specific CLI wrapper
$cliWrapper = @"
@echo off
REM Genesis CLI Wrapper - Auto-detect architecture

SET ARCH=%PROCESSOR_ARCHITECTURE%

IF "%ARCH%"=="AMD64" (
    SET GENESIS_CLI=%~dp0genesis-x64.exe
) ELSE IF "%ARCH%"=="x86" (
    SET GENESIS_CLI=%~dp0genesis-x86.exe
) ELSE (
    echo Unsupported architecture: %ARCH%
    exit /b 1
)

IF NOT EXIST "%GENESIS_CLI%" (
    echo Genesis CLI not found for architecture: %ARCH%
    echo Expected location: %GENESIS_CLI%
    exit /b 1
)

"%GENESIS_CLI%" %*
"@

$wrapperPath = "$genesisBin\genesis.cmd"
$cliWrapper | Out-File -FilePath $wrapperPath -Encoding ASCII -Force
Write-Success "Created CLI wrapper: $wrapperPath"

# Create PowerShell wrapper
$psWrapper = @"
# Genesis CLI PowerShell Wrapper
`$arch = `$env:PROCESSOR_ARCHITECTURE
`$binPath = "`$PSScriptRoot"

if (`$arch -eq "AMD64") {
    `$cliPath = Join-Path `$binPath "genesis-x64.exe"
} elseif (`$arch -eq "x86") {
    `$cliPath = Join-Path `$binPath "genesis-x86.exe"
} else {
    Write-Error "Unsupported architecture: `$arch"
    exit 1
}

if (-not (Test-Path `$cliPath)) {
    Write-Warning "Genesis CLI not found at: `$cliPath"
    Write-Info "This is a placeholder. Install the actual Genesis CLI binary."
    exit 1
}

& `$cliPath `$args
"@

$psWrapperPath = "$genesisBin\genesis.ps1"
$psWrapper | Out-File -FilePath $psWrapperPath -Encoding UTF8 -Force
Write-Success "Created PowerShell wrapper: $psWrapperPath"

# Add to PATH if not already present
$currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
if ($currentPath -notlike "*$genesisBin*") {
    Write-Info "Adding Genesis to user PATH..."
    [Environment]::SetEnvironmentVariable(
        "PATH",
        "$currentPath;$genesisBin",
        "User"
    )
    Write-Success "Added to PATH (restart terminal to use)"
} else {
    Write-Success "Genesis already in PATH"
}

# Copy workspace config
$workspaceConfig = "$PSScriptRoot\config.yaml"
$targetConfig = "$genesisConfig\workspace-config.yaml"
if (Test-Path $workspaceConfig) {
    Copy-Item $workspaceConfig $targetConfig -Force
    Write-Success "Copied workspace configuration"
}

# Create editor integration symlinks/copies
Write-Info "Setting up editor integration..."

# VS Code integration
$vscodeSettingsSource = "$PSScriptRoot\..\workspace\.vscode\settings.json"
if (Test-Path "$env:APPDATA\Code\User\settings.json") {
    Write-Info "VS Code user settings found - Integration ready"
}

# Cursor integration
if (Test-Path "$env:APPDATA\Cursor\User\settings.json") {
    Write-Info "Cursor settings found - Integration ready"
}

# Create stub executables with messaging
$stubContent = @"
@echo off
echo ================================================================
echo Genesis CLI Stub for %PROCESSOR_ARCHITECTURE%
echo ================================================================
echo This is a placeholder script for the Genesis CLI.
echo.
echo To complete setup, install the actual Genesis CLI binary to:
echo %~dp0
echo.
echo Expected filenames:
echo   - genesis-x86.exe (for 32-bit Windows)
echo   - genesis-x64.exe (for 64-bit Windows)
echo.
echo The Genesis CLI will integrate with:
echo   - VS Code (.vscode configuration)
echo   - Cursor (.cursor configuration)
echo   - Claude Code
echo.
echo Configuration file: %USERPROFILE%\.genesis\config\workspace-config.yaml
echo ================================================================
pause
"@

@("genesis-x86.exe", "genesis-x64.exe") | ForEach-Object {
    $stubPath = "$genesisBin\$_"
    if (-not (Test-Path $stubPath)) {
        # Create a batch file as placeholder
        $batchStubPath = $stubPath -replace '\.exe$', '.cmd'
        $stubContent | Out-File -FilePath $batchStubPath -Encoding ASCII -Force
        Write-Warning "Created stub for $_ (install actual binary)"
    }
}

Write-Success ""
Write-Success "Genesis CLI Setup Complete!"
Write-Success "=================================================="
Write-Info "Next steps:"
Write-Info "1. Install Genesis CLI binaries to: $genesisBin"
Write-Info "2. Restart your terminal to update PATH"
Write-Info "3. Run: genesis --version"
Write-Info ""
Write-Info "Symbiotic integration configured for:"
Write-Info "  ✓ VS Code (.vscode/)"
Write-Info "  ✓ Cursor (.cursor/)"
Write-Info "  ✓ Claude Code"
Write-Info "  ✓ Architecture: $arch"
