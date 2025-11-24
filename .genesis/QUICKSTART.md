# Genesis CLI - Quick Start Guide

## 🚀 5-Minute Setup

### Step 1: Run Platform Setup

**Windows (PowerShell):**
```powershell
cd C:\path\to\workspace
.\.genesis\setup.ps1
```

**Linux/Mac (Bash):**
```bash
cd /path/to/workspace
bash .genesis/setup.sh
source ~/.bashrc  # or source ~/.zshrc
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `watchdog` - For real-time file monitoring
- `SpeechRecognition` - For voice features
- `openai-whisper` - For AI transcription

### Step 3: Test Configuration

```bash
# Run one-time sync
python .genesis/sync.py

# You should see:
# ✓ Ensured vscode directory
# ✓ Ensured cursor directory
# ✓ Synced settings.json → cursor/
# ✅ Synchronization complete!
```

### Step 4: Start Live Sync (Optional)

```bash
# Terminal 1: Start file watcher
python .genesis/watch-sync.py

# Keep this running in the background
# It will automatically sync changes between editors
```

### Step 5: Open in Your Editors

1. **VS Code**: `code .`
2. **Cursor**: Open the workspace folder
3. Changes made in one will automatically sync to the other!

## 🎯 What You Get

### ✅ Automatic Architecture Detection
- Windows: Detects x86 vs x64
- Linux: Detects x64 vs ARM64
- Runs the correct binaries automatically

### ✅ Cross-Editor Sync
- Edit in VS Code → Auto-syncs to Cursor
- Edit in Cursor → Auto-syncs to VS Code
- Settings, tasks, launch configs all stay in sync

### ✅ AI Integration
- Cursor AI with Claude 4.5 Sonnet
- GitHub Copilot support
- Shared context between editors

### ✅ Platform-Aware Terminals
- Windows: PowerShell, CMD, Git Bash
- Linux: Bash with proper env vars
- All configured with Genesis CLI paths

## 📁 Configuration Locations

### Workspace Config (Shared)
```
/workspace/.vscode/     # VS Code settings
/workspace/.cursor/     # Cursor settings
/workspace/.genesis/    # Genesis CLI config
```

### User Config (Per-machine)

**Windows:**
```
%USERPROFILE%\.genesis\
  ├── bin\genesis.cmd
  ├── bin\genesis-x86.exe  ← Place your 32-bit binary here
  ├── bin\genesis-x64.exe  ← Place your 64-bit binary here
  └── config\
```

**Linux:**
```
~/.genesis/
  ├── bin/genesis
  ├── bin/genesis-x64      ← Place your x64 binary here
  ├── bin/genesis-arm64    ← Place your ARM64 binary here
  └── config/
```

## 🔧 Common Tasks

### Run Genesis CLI
```bash
# Works on any platform - auto-detects architecture
genesis --version
genesis sync --workspace .
genesis cross-sync --editors vscode,cursor
```

### Manual Sync
```bash
# One-time sync
python .genesis/sync.py

# Sync specific workspace
python .genesis/sync.py /path/to/workspace
```

### VS Code Tasks
Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac):
- Type "Tasks: Run Task"
- Select:
  - "Genesis CLI: Sync Workspace"
  - "Genesis CLI: Cross-Editor Sync"
  - "Python: Install Dependencies"

## 🐛 Troubleshooting

### "genesis: command not found"

**Windows:**
```powershell
# Restart your terminal, then:
$env:PATH

# Should include: C:\Users\YourName\.genesis\bin
```

**Linux:**
```bash
# Reload shell config
source ~/.bashrc

# Verify PATH
echo $PATH | grep genesis
```

### Sync Not Working

```bash
# Check sync status
cat .genesis/sync-manifest.json

# Run manual sync with verbose output
python .genesis/sync.py
```

### Wrong Architecture Detected

**Windows:**
```powershell
echo $env:PROCESSOR_ARCHITECTURE
# Should show: AMD64 (for 64-bit) or x86 (for 32-bit)
```

**Linux:**
```bash
uname -m
# Should show: x86_64 or aarch64
```

## 📚 Next Steps

1. ✅ **Install Genesis CLI binaries** (if available)
2. ✅ **Open workspace in both VS Code and Cursor**
3. ✅ **Make a change in one editor** - watch it sync!
4. ✅ **Run watch-sync.py in background** for real-time sync
5. ✅ **Customize settings** - they'll sync everywhere

## 🔗 Key Files

| File | Purpose |
|------|---------|
| `.vscode/settings.json` | VS Code configuration |
| `.cursor/settings.json` | Cursor configuration |
| `.genesis/config.yaml` | Genesis CLI master config |
| `.genesis/sync.py` | One-time sync script |
| `.genesis/watch-sync.py` | Live file watcher |
| `.genesis/README.md` | Full documentation |

## 💡 Pro Tips

1. **Keep watch-sync.py running** in a terminal tab for instant sync
2. **Extensions sync too** - install in one editor, available in both
3. **Tasks and launch configs** are shared - debug configs work everywhere
4. **Platform-specific paths** auto-adjust based on OS
5. **Git ignores temp files** - only config is committed

## ✨ Features Enabled

- [x] Multi-platform support (Windows 32/64, Linux x64/ARM)
- [x] Cursor ↔ VS Code bidirectional sync
- [x] Genesis CLI integration
- [x] AI model configuration (Claude 4.5)
- [x] Python virtual environment support
- [x] Cross-platform terminal profiles
- [x] Shared debug configurations
- [x] Extension synchronization
- [x] Real-time file watching
- [x] Architecture auto-detection

---

**Ready to go!** 🎉

Try editing a file in VS Code, then check Cursor - it should sync automatically.
