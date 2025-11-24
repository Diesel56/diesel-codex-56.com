# Genesis CLI Setup Guide

## Overview

This configuration ensures proper symbiotic dynamic integration between **Cursor**, **Claude Code**, and **VS Code** with the **Genesis CLI** across Windows (32-bit and 64-bit) architectures.

## Architecture Support

- ✅ Windows 32-bit (x86)
- ✅ Windows 64-bit (x64/AMD64)
- ✅ Linux 32-bit (i386/i686)
- ✅ Linux 64-bit (x86_64/amd64)
- ✅ macOS 64-bit (arm64/x64)

## IDE Configuration Files

### VS Code
- `.vscode/settings.json` - Workspace settings
- `.vscode/tasks.json` - Build tasks and Genesis CLI integration
- `.vscode/launch.json` - Debug configurations
- `.vscode/extensions.json` - Recommended extensions

### Cursor
- `.cursor/settings.json` - Cursor-specific settings with Genesis CLI integration

### Claude Code
- `.claude-code/settings.json` - Claude Code-specific settings with Genesis CLI integration

## Genesis CLI Installation

### Windows

#### 32-bit Windows
```cmd
REM Make genesis-cli.bat executable
genesis-cli.bat init
```

#### 64-bit Windows
```powershell
# Make genesis-cli.bat executable
.\genesis-cli.bat init
```

### Linux/macOS
```bash
# Make scripts executable
chmod +x genesis-cli.sh
chmod +x genesis-cli.js
chmod +x .genesis/symbiotic-sync.js

# Initialize
./genesis-cli.sh init
```

## Genesis CLI Commands

```bash
# Initialize Genesis CLI
genesis-cli init

# Run Diesel Agent
genesis-cli agent run

# Deploy Genesis Engine
genesis-cli deploy

# Show status
genesis-cli status

# Sync IDE configurations
genesis-cli sync
```

## Symbiotic Dynamic Sync

The symbiotic sync ensures that configurations are synchronized across all IDEs:

```bash
# Manual sync
node .genesis/symbiotic-sync.js

# Or use Genesis CLI
genesis-cli sync
```

## Platform-Specific Configuration

Platform-specific settings are automatically detected and configured:

- **Windows 32-bit**: Uses `cmd.exe` or `powershell.exe` (32-bit)
- **Windows 64-bit**: Uses PowerShell (64-bit) or WSL
- **Linux**: Uses bash/zsh with appropriate Python/Node paths
- **macOS**: Uses zsh/bash with Homebrew paths

## IDE Integration

### VS Code
1. Open workspace in VS Code
2. Install recommended extensions (prompted automatically)
3. Genesis CLI tasks are available via `Ctrl+Shift+P` → "Tasks: Run Task"

### Cursor
1. Open workspace in Cursor
2. Settings are automatically loaded from `.cursor/settings.json`
3. Genesis CLI integration is enabled via `cursor.genesis.cli.enabled`

### Claude Code
1. Open workspace in Claude Code
2. Settings are automatically loaded from `.claude-code/settings.json`
3. Genesis CLI integration is enabled via `claude.genesis.cli.enabled`

## Cross-IDE Compatibility

All three IDEs share:
- Python interpreter path
- Code formatting settings
- File associations
- Terminal profiles
- YAML schema mappings

## Troubleshooting

### Windows 32-bit Issues
- Ensure Python is installed and in PATH
- Check that `genesis-cli.bat` uses correct Python path
- Verify Node.js is installed (32-bit version)

### Windows 64-bit Issues
- Use PowerShell for best compatibility
- Ensure Python 3.x is installed (64-bit)
- Check Node.js installation (64-bit version)

### Configuration Sync Issues
- Run `genesis-cli sync` manually
- Check `.genesis/config.json` for platform detection
- Verify all IDE config directories exist

## Verification

To verify the setup:

```bash
# Check Genesis CLI status
genesis-cli status

# Verify platform detection
node genesis-cli.js status

# Test IDE configurations
# Open workspace in each IDE and verify settings are loaded
```

## Files Created

- `genesis-cli.js` - Main CLI script (Node.js)
- `genesis-cli.bat` - Windows batch wrapper
- `genesis-cli.sh` - Unix/Linux/macOS shell wrapper
- `.genesis/config.json` - Genesis CLI configuration
- `.genesis/platform-config.json` - Platform-specific paths
- `.genesis/shared-config.json` - Shared IDE configuration
- `.genesis/symbiotic-sync.js` - Configuration sync script
- `.vscode/symbiotic-sync.json` - VS Code sync configuration

## Next Steps

1. Initialize Genesis CLI: `genesis-cli init`
2. Sync configurations: `genesis-cli sync`
3. Open workspace in your preferred IDE(s)
4. Verify settings are loaded correctly
5. Run `genesis-cli status` to confirm platform detection
