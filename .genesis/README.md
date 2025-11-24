# Genesis CLI - Cross-Editor Symbiotic Integration

## Overview

This configuration enables seamless symbiotic integration between **Cursor**, **VS Code**, **Claude Code**, and the **Genesis CLI** across multiple platforms and architectures:

- ✅ Windows (32-bit and 64-bit)
- ✅ Linux (x64 and ARM64)
- ✅ Automatic architecture detection
- ✅ Bidirectional settings synchronization
- ✅ Real-time file watching

## Architecture Support

### Windows
- **x86 (32-bit)**: `genesis-x86.exe`
- **x64 (64-bit)**: `genesis-x64.exe`
- Auto-detection via `%PROCESSOR_ARCHITECTURE%`

### Linux
- **x86_64**: `genesis-x64`
- **ARM64/aarch64**: `genesis-arm64`
- Auto-detection via `uname -m`

## Installation

### Windows

```powershell
# Run the setup script
cd /workspace
.\.genesis\setup.ps1

# Or with verbose output
.\.genesis\setup.ps1 -Verbose
```

The script will:
1. Create `%USERPROFILE%\.genesis` directory structure
2. Add Genesis CLI to your PATH
3. Create architecture-aware wrappers
4. Configure editor integration

### Linux

```bash
# Run the setup script
cd /workspace
bash .genesis/setup.sh

# Reload your shell
source ~/.bashrc  # or ~/.zshrc
```

The script will:
1. Create `~/.genesis` directory structure
2. Add Genesis CLI to your PATH
3. Create architecture-aware wrappers
4. Configure editor integration

## Directory Structure

```
.genesis/
├── config.yaml          # Main configuration file
├── setup.ps1           # Windows setup script
├── setup.sh            # Linux setup script
├── sync.py             # One-time synchronization script
├── watch-sync.py       # Continuous sync with file watching
└── README.md           # This file

~/.genesis/              # User-level installation (Windows: %USERPROFILE%\.genesis)
├── bin/
│   ├── genesis.cmd     # Windows batch wrapper
│   ├── genesis.ps1     # PowerShell wrapper
│   ├── genesis         # Linux shell wrapper
│   ├── genesis-x86.exe # Windows 32-bit binary (install separately)
│   ├── genesis-x64.exe # Windows 64-bit binary (install separately)
│   ├── genesis-x64     # Linux x64 binary (install separately)
│   └── genesis-arm64   # Linux ARM64 binary (install separately)
├── config/
│   └── workspace-config.yaml
└── cache/
```

## Editor Configuration

### VS Code (`.vscode/`)
- `settings.json` - Cross-platform Python, terminal, and Genesis integration
- `extensions.json` - Recommended extensions
- `tasks.json` - Build and sync tasks
- `launch.json` - Debug configurations

### Cursor (`.cursor/`)
- `settings.json` - AI model config, cross-editor sync, Genesis integration
- `extensions.json` - Extension recommendations with sync settings

## Synchronization

### One-Time Sync

```bash
# Run manual sync
python .genesis/sync.py

# Or specify workspace
python .genesis/sync.py /path/to/workspace
```

This will:
- ✅ Sync settings between VS Code and Cursor
- ✅ Validate architecture configurations
- ✅ Create sync manifest
- ✅ Report sync status

### Continuous Watch & Sync

```bash
# Start file watcher (requires watchdog: pip install watchdog)
python .genesis/watch-sync.py

# Or use polling mode (no dependencies)
python .genesis/watch-sync.py
```

Features:
- 👁️ Real-time file monitoring
- 🔄 Automatic bidirectional sync
- ⚡ Debounced updates (500ms)
- 📊 Sync status reporting

## Genesis CLI Commands

Once installed, you can use:

```bash
# Sync workspace
genesis sync --workspace /path/to/workspace

# Cross-editor sync
genesis cross-sync --editors vscode,cursor,claude

# Check version
genesis --version

# View configuration
genesis config show
```

## VS Code Tasks

Access via `Ctrl+Shift+P` → "Tasks: Run Task":

1. **Genesis CLI: Sync Workspace** - Sync current workspace
2. **Genesis CLI: Cross-Editor Sync** - Sync all editors
3. **Python: Install Dependencies** - Install requirements.txt
4. **Setup Genesis CLI** - Run initial setup

## Platform-Specific Features

### Windows
- Supports both 32-bit and 64-bit architectures
- PowerShell and CMD wrappers included
- Automatic PROCESSOR_ARCHITECTURE detection
- User PATH configuration

### Linux
- Support for x64 and ARM64
- Shell integration (.bashrc/.zshrc)
- POSIX-compliant scripts
- Automatic architecture detection

## Configuration Files

### `config.yaml`
Main Genesis CLI configuration with:
- Architecture detection settings
- Editor integration settings
- Cross-editor sync configuration
- Platform-specific paths
- File watching rules

### Editor Settings
Both `.vscode/settings.json` and `.cursor/settings.json` include:
- Python configuration
- Terminal profiles (platform-specific)
- Genesis CLI paths
- AI assistant integration
- Cross-editor sync settings

## Troubleshooting

### Genesis CLI Not Found

**Windows:**
```powershell
# Check PATH
$env:PATH -split ';' | Select-String genesis

# Manual run
& "$env:USERPROFILE\.genesis\bin\genesis.cmd" --version
```

**Linux:**
```bash
# Check PATH
echo $PATH | tr ':' '\n' | grep genesis

# Manual run
~/.genesis/bin/genesis --version
```

### Settings Not Syncing

1. Check file permissions
2. Run manual sync: `python .genesis/sync.py`
3. Check sync manifest: `.genesis/sync-manifest.json`
4. Enable verbose logging in `config.yaml`

### Architecture Detection Issues

```bash
# Windows
echo %PROCESSOR_ARCHITECTURE%

# Linux
uname -m
```

## Integration with Existing Workspace

The Genesis CLI configuration is designed to be non-intrusive:

- ✅ Works alongside existing `.vscode` settings
- ✅ Merges with current configurations
- ✅ Preserves custom settings
- ✅ Bidirectional sync prevents data loss

## Next Steps

1. **Install Genesis CLI Binaries**: Download and place in `~/.genesis/bin/`
2. **Configure Editors**: Open workspace in VS Code and Cursor
3. **Start Sync**: Run `python .genesis/watch-sync.py` in background
4. **Verify**: Make changes in one editor, see them sync to others

## Related Files

- `/workspace/.vscode/` - VS Code workspace configuration
- `/workspace/.cursor/` - Cursor workspace configuration
- `/workspace/requirements.txt` - Python dependencies
- `/workspace/.gitignore` - Excludes cache and temp files

## Support

For issues or questions:
1. Check Genesis CLI logs: `~/.genesis/genesis.log`
2. Review sync manifest: `.genesis/sync-manifest.json`
3. Run with verbose mode: `genesis --verbose`

---

**Version**: 1.0  
**Platform**: Windows (x86, x64), Linux (x64, ARM64)  
**Editors**: VS Code, Cursor, Claude Code
