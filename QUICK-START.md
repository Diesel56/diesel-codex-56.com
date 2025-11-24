# Quick Start - Genesis CLI & IDE Configuration

## 🚀 Quick Setup (5 minutes)

### 1. Initialize Genesis CLI
```bash
# Windows
genesis-cli.bat init

# Linux/macOS
./genesis-cli.sh init
```

### 2. Verify Platform Detection
```bash
genesis-cli status
```

### 3. Sync IDE Configurations
```bash
genesis-cli sync
```

### 4. Open in Your IDE
- **VS Code**: Open workspace → Settings auto-loaded
- **Cursor**: Open workspace → Settings auto-loaded  
- **Claude Code**: Open workspace → Settings auto-loaded

## ✅ Verification Checklist

- [ ] Genesis CLI initialized (`genesis-cli init`)
- [ ] Platform detected correctly (`genesis-cli status`)
- [ ] IDE configurations synced (`genesis-cli sync`)
- [ ] VS Code settings loaded (`.vscode/settings.json`)
- [ ] Cursor settings loaded (`.cursor/settings.json`)
- [ ] Claude Code settings loaded (`.claude-code/settings.json`)
- [ ] Python interpreter detected
- [ ] Terminal profiles configured

## 📋 Common Commands

```bash
# Initialize
genesis-cli init

# Run Diesel Agent
genesis-cli agent run

# Deploy
genesis-cli deploy

# Status
genesis-cli status

# Sync IDEs
genesis-cli sync
```

## 🔧 Platform-Specific Notes

### Windows 32-bit
- Uses `cmd.exe` or PowerShell (32-bit)
- Python: `python` command
- Node: `C:\Program Files (x86)\nodejs\`

### Windows 64-bit
- Uses PowerShell (64-bit) or WSL
- Python: `python` command
- Node: `C:\Program Files\nodejs\`

### Linux/macOS
- Uses bash/zsh
- Python: `python3` command
- Node: Standard paths

## 🆘 Troubleshooting

**Issue**: Genesis CLI not found
- **Solution**: Make scripts executable (`chmod +x genesis-cli.sh`)

**Issue**: Python not detected
- **Solution**: Ensure Python is in PATH, check `genesis-cli status`

**Issue**: IDE settings not loading
- **Solution**: Run `genesis-cli sync` to sync configurations

**Issue**: Platform detection incorrect
- **Solution**: Check `.genesis/config.json` and `.genesis/platform-config.json`

## 📚 Full Documentation

See `GENESIS-CLI-SETUP.md` for complete documentation.
