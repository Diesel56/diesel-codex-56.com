# Genesis CLI Setup Script for Windows PowerShell
# Supports both 32-bit and 64-bit Windows architectures

param(
    [switch]$SkipDependencies,
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Genesis CLI Setup for Windows (PowerShell)" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Detect architecture
function Get-Architecture {
    $arch = [System.Environment]::Is64BitOperatingSystem
    if ($arch) {
        $archType = "x64"
        $bits = "64"
    } else {
        $archType = "x86"
        $bits = "32"
    }
    
    return @{
        Type = $archType
        Bits = $bits
        Processor = $env:PROCESSOR_ARCHITECTURE
    }
}

# Check if command exists
function Test-Command {
    param([string]$Command)
    
    $oldPreference = $ErrorActionPreference
    $ErrorActionPreference = 'SilentlyContinue'
    $result = Get-Command $Command
    $ErrorActionPreference = $oldPreference
    
    return $null -ne $result
}

# Create directory if it doesn't exist
function Ensure-Directory {
    param([string]$Path)
    
    if (!(Test-Path $Path)) {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
        Write-Host "  Created: $Path" -ForegroundColor Green
    }
}

# Main setup
try {
    # Get architecture
    $arch = Get-Architecture
    Write-Host "Detected Architecture: $($arch.Type) ($($arch.Bits)-bit)" -ForegroundColor Green
    Write-Host "Processor: $($arch.Processor)" -ForegroundColor Gray
    Write-Host ""
    
    # Check Python
    Write-Host "Checking Python installation..." -ForegroundColor Yellow
    $pythonCmd = $null
    
    if (Test-Command "python") {
        $pythonCmd = "python"
    } elseif (Test-Command "python3") {
        $pythonCmd = "python3"
    } else {
        Write-Host "ERROR: Python not found" -ForegroundColor Red
        Write-Host "Please install Python 3.8 or higher from https://www.python.org" -ForegroundColor Yellow
        exit 1
    }
    
    Write-Host "Using Python: $pythonCmd" -ForegroundColor Green
    & $pythonCmd --version
    Write-Host ""
    
    # Check Node.js
    Write-Host "Checking Node.js installation..." -ForegroundColor Yellow
    if (Test-Command "node") {
        Write-Host "Node.js found:" -ForegroundColor Green
        & node --version
    } else {
        Write-Host "WARNING: Node.js not found" -ForegroundColor Yellow
        Write-Host "Some features may not work properly" -ForegroundColor Yellow
    }
    Write-Host ""
    
    # Check Git
    Write-Host "Checking Git installation..." -ForegroundColor Yellow
    if (Test-Command "git") {
        Write-Host "Git found:" -ForegroundColor Green
        & git --version
    } else {
        Write-Host "WARNING: Git not found" -ForegroundColor Yellow
        Write-Host "Version control features will not work" -ForegroundColor Yellow
    }
    Write-Host ""
    
    # Create directory structure
    Write-Host "Creating directory structure..." -ForegroundColor Yellow
    $directories = @(
        ".genesis",
        ".genesis\cache",
        ".genesis\logs",
        ".genesis\temp",
        ".genesis\artifacts",
        ".vscode",
        ".cursor"
    )
    
    foreach ($dir in $directories) {
        Ensure-Directory -Path $dir
    }
    Write-Host ""
    
    # Create/activate virtual environment
    if (!(Test-Path ".venv")) {
        Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
        & $pythonCmd -m venv .venv
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to create virtual environment"
        }
    }
    
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & ".\.venv\Scripts\Activate.ps1"
    Write-Host ""
    
    # Upgrade pip
    Write-Host "Upgrading pip..." -ForegroundColor Yellow
    & python -m pip install --upgrade pip --quiet
    
    # Install dependencies
    if (!$SkipDependencies) {
        if (Test-Path "requirements.txt") {
            Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
            & pip install -r requirements.txt --quiet
        } else {
            Write-Host "Creating requirements.txt..." -ForegroundColor Yellow
            @"
pyyaml>=6.0
requests>=2.28.0
black>=22.0.0
flake8>=5.0.0
mypy>=0.990
pytest>=7.0.0
python-dotenv>=0.20.0
watchdog>=2.1.0
colorama>=0.4.5
click>=8.0.0
"@ | Out-File -FilePath "requirements.txt" -Encoding UTF8
            & pip install -r requirements.txt --quiet
        }
    }
    Write-Host ""
    
    # Set environment variables
    Write-Host "Setting environment variables..." -ForegroundColor Yellow
    $env:GENESIS_CLI_HOME = $PWD.Path
    $env:DIESEL_ENGINE_CONFIG = "$($PWD.Path)\diesel_engine.yaml"
    $env:PYTHONPATH = $PWD.Path
    $env:GENESIS_PLATFORM = "win32-$($arch.Type)"
    
    # Create PowerShell genesis function
    Write-Host "Creating Genesis PowerShell function..." -ForegroundColor Yellow
    $genesisFunction = @"
function genesis {
    `$env:GENESIS_CLI_HOME = "$($PWD.Path)"
    `$env:DIESEL_ENGINE_CONFIG = "$($PWD.Path)\diesel_engine.yaml"
    `$env:PYTHONPATH = "$($PWD.Path)"
    `$env:GENESIS_PLATFORM = "win32-$($arch.Type)"
    
    if (Test-Path "$($PWD.Path)\.venv\Scripts\Activate.ps1") {
        & "$($PWD.Path)\.venv\Scripts\Activate.ps1"
    }
    
    & python "$($PWD.Path)\genesis-cli.py" `$args
}
"@
    
    $genesisFunction | Out-File -FilePath "genesis.ps1" -Encoding UTF8
    Write-Host ""
    
    # Initialize Genesis CLI
    Write-Host "Initializing Genesis CLI..." -ForegroundColor Yellow
    & python genesis-cli.py init
    Write-Host ""
    
    # Validate setup
    Write-Host "Validating setup..." -ForegroundColor Yellow
    & python genesis-cli.py validate
    Write-Host ""
    
    # Show status
    & python genesis-cli.py status
    Write-Host ""
    
    # Install VS Code extensions if available
    if (Test-Command "code") {
        Write-Host "Installing VS Code extensions..." -ForegroundColor Yellow
        $extensions = @(
            "ms-python.python",
            "ms-python.vscode-pylance",
            "ms-python.black-formatter",
            "esbenp.prettier-vscode",
            "redhat.vscode-yaml",
            "github.copilot",
            "continue.continue"
        )
        
        foreach ($ext in $extensions) {
            & code --install-extension $ext 2>$null
        }
        Write-Host "VS Code extensions installed" -ForegroundColor Green
    }
    
    Write-Host ""
    Write-Host "============================================" -ForegroundColor Green
    Write-Host "Setup completed successfully!" -ForegroundColor Green
    Write-Host "============================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "To use Genesis CLI:" -ForegroundColor Cyan
    Write-Host "  1. Source the function: . .\genesis.ps1" -ForegroundColor White
    Write-Host "  2. Run: genesis [command]" -ForegroundColor White
    Write-Host ""
    Write-Host "Or use directly:" -ForegroundColor Cyan
    Write-Host "  python genesis-cli.py [command]" -ForegroundColor White
    Write-Host ""
    Write-Host "Available commands:" -ForegroundColor Cyan
    Write-Host "  genesis init      - Initialize workspace" -ForegroundColor White
    Write-Host "  genesis build     - Build the project" -ForegroundColor White
    Write-Host "  genesis deploy    - Deploy to production" -ForegroundColor White
    Write-Host "  genesis sync      - Sync editor configurations" -ForegroundColor White
    Write-Host "  genesis validate  - Validate configurations" -ForegroundColor White
    Write-Host "  genesis status    - Show current status" -ForegroundColor White
    Write-Host ""
    
    # Suggest adding to PowerShell profile
    Write-Host "To add Genesis to your PowerShell profile:" -ForegroundColor Cyan
    Write-Host '  Add-Content $PROFILE ". $PWD\genesis.ps1"' -ForegroundColor White
    Write-Host ""
    
} catch {
    Write-Host "ERROR: $_" -ForegroundColor Red
    exit 1
}