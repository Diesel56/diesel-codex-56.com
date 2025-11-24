@echo off
REM Genesis CLI - Windows Batch Script
REM Supports both 32-bit and 64-bit Windows architectures

setlocal enabledelayedexpansion

REM Detect architecture
if "%PROCESSOR_ARCHITECTURE%"=="AMD64" (
    set ARCH=64-bit
) else if "%PROCESSOR_ARCHITECTURE%"=="x86" (
    set ARCH=32-bit
) else (
    set ARCH=unknown
)

echo Genesis CLI - Diesel Genesis Engine
echo Platform: Windows (%ARCH%)
echo.

REM Check for Node.js
where node >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Node.js not found. Please install Node.js first.
    exit /b 1
)

REM Run the JavaScript CLI
node "%~dp0genesis-cli.js" %*

endlocal
