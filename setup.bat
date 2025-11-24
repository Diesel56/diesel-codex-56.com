@echo off
REM Genesis CLI Setup Script for Windows (32/64-bit)
REM Configures Cursor, VS Code, and Claude integration

setlocal enabledelayedexpansion

echo ============================================
echo Genesis CLI Setup for Windows
echo ============================================
echo.

REM Detect Windows architecture
if "%PROCESSOR_ARCHITECTURE%"=="AMD64" (
    set ARCH=x64
    set BITS=64
) else if "%PROCESSOR_ARCHITECTURE%"=="x86" (
    if defined PROCESSOR_ARCHITEW6432 (
        set ARCH=x64
        set BITS=64
    ) else (
        set ARCH=x86
        set BITS=32
    )
) else (
    set ARCH=%PROCESSOR_ARCHITECTURE%
    set BITS=unknown
)

echo Detected Architecture: %ARCH% (%BITS%-bit)
echo.

REM Set Python command based on what's available
where python >nul 2>&1
if %errorlevel%==0 (
    set PYTHON_CMD=python
) else (
    where python3 >nul 2>&1
    if %errorlevel%==0 (
        set PYTHON_CMD=python3
    ) else (
        echo ERROR: Python not found in PATH
        echo Please install Python 3.8 or higher
        pause
        exit /b 1
    )
)

echo Using Python: %PYTHON_CMD%
%PYTHON_CMD% --version
echo.

REM Check for Node.js
where node >nul 2>&1
if %errorlevel%==0 (
    echo Node.js found:
    node --version
) else (
    echo WARNING: Node.js not found in PATH
    echo Some features may not work properly
)
echo.

REM Check for Git
where git >nul 2>&1
if %errorlevel%==0 (
    echo Git found:
    git --version
) else (
    echo WARNING: Git not found in PATH
    echo Version control features will not work
)
echo.

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo Creating Python virtual environment...
    %PYTHON_CMD% -m venv .venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install Python dependencies
if exist "requirements.txt" (
    echo Installing Python dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo WARNING: Some dependencies failed to install
    )
) else (
    echo Creating requirements.txt...
    (
        echo pyyaml>=6.0
        echo requests>=2.28.0
        echo black>=22.0.0
        echo flake8>=5.0.0
        echo mypy>=0.990
        echo pytest>=7.0.0
        echo python-dotenv>=0.20.0
        echo watchdog>=2.1.0
        echo colorama>=0.4.5
        echo click>=8.0.0
    ) > requirements.txt
    pip install -r requirements.txt
)

REM Create necessary directories
echo.
echo Creating directory structure...
if not exist ".genesis" mkdir .genesis
if not exist ".genesis\cache" mkdir .genesis\cache
if not exist ".genesis\logs" mkdir .genesis\logs
if not exist ".genesis\temp" mkdir .genesis\temp
if not exist ".genesis\artifacts" mkdir .genesis\artifacts
if not exist ".vscode" mkdir .vscode
if not exist ".cursor" mkdir .cursor

REM Set environment variables
echo.
echo Setting environment variables...
set GENESIS_CLI_HOME=%CD%
set DIESEL_ENGINE_CONFIG=%CD%\diesel_engine.yaml
set PYTHONPATH=%CD%
set GENESIS_PLATFORM=win32-%ARCH%

REM Create batch file for Genesis CLI
echo Creating genesis.bat launcher...
(
    echo @echo off
    echo setlocal
    echo set GENESIS_CLI_HOME=%CD%
    echo set DIESEL_ENGINE_CONFIG=%CD%\diesel_engine.yaml
    echo set PYTHONPATH=%CD%
    echo set GENESIS_PLATFORM=win32-%ARCH%
    echo.
    echo if exist ".venv\Scripts\activate.bat" (
    echo     call .venv\Scripts\activate.bat
    echo )
    echo.
    echo python "%CD%\genesis-cli.py" %%*
    echo endlocal
) > genesis.bat

REM Make genesis-cli.py executable
echo Making genesis-cli.py executable...
attrib +x genesis-cli.py 2>nul

REM Initialize Genesis CLI
echo.
echo Initializing Genesis CLI...
python genesis-cli.py init

REM Validate setup
echo.
echo Validating setup...
python genesis-cli.py validate

REM Show status
echo.
python genesis-cli.py status

echo.
echo ============================================
echo Setup completed successfully!
echo ============================================
echo.
echo To use Genesis CLI, run: genesis [command]
echo To activate the virtual environment: .venv\Scripts\activate.bat
echo.
echo Available commands:
echo   genesis init      - Initialize workspace
echo   genesis build     - Build the project
echo   genesis deploy    - Deploy to production
echo   genesis sync      - Sync editor configurations
echo   genesis validate  - Validate configurations
echo   genesis status    - Show current status
echo.

REM Check for VS Code
where code >nul 2>&1
if %errorlevel%==0 (
    echo VS Code detected. Installing recommended extensions...
    call :install_vscode_extensions
)

REM Check for Cursor
where cursor >nul 2>&1
if %errorlevel%==0 (
    echo Cursor detected. Configuration files created.
)

echo.
echo Press any key to exit...
pause >nul
exit /b 0

:install_vscode_extensions
REM Install VS Code extensions
code --install-extension ms-python.python 2>nul
code --install-extension ms-python.vscode-pylance 2>nul
code --install-extension ms-python.black-formatter 2>nul
code --install-extension esbenp.prettier-vscode 2>nul
code --install-extension redhat.vscode-yaml 2>nul
code --install-extension github.copilot 2>nul
code --install-extension continue.continue 2>nul
exit /b 0