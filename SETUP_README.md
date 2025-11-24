# Genesis CLI - Editor Integration Setup Guide

## Overview

This workspace has been configured for seamless integration between **Cursor**, **Claude Code**, **VS Code**, and the **Genesis CLI** across multiple platforms and architectures.

## 🚀 Quick Start

### Windows (PowerShell)
```powershell
# Run the PowerShell setup script
.\setup.ps1

# Or use the batch file
setup.bat
```

### Windows (Command Prompt)
```cmd
setup.bat
```

### Linux/macOS
```bash
# Make the script executable (if not already)
chmod +x setup.sh

# Run the setup script
./setup.sh
```

## 📋 Supported Platforms

| Platform | Architecture | Support Status |
|----------|-------------|----------------|
| Windows | x64 (64-bit) | ✅ Full Support |
| Windows | x86 (32-bit) | ✅ Full Support |
| Linux | x64 (64-bit) | ✅ Full Support |
| Linux | x86 (32-bit) | ✅ Full Support |
| macOS | x64 (Intel) | ✅ Full Support |
| macOS | ARM64 (M1/M2) | ✅ Full Support |

## 🛠️ Configuration Files

### Editor-Specific Configurations

- **VS Code**: `.vscode/`
  - `settings.json` - Editor settings
  - `extensions.json` - Recommended extensions
  - `launch.json` - Debug configurations
  - `tasks.json` - Build tasks

- **Cursor**: `.cursor/`
  - `settings.json` - Cursor-specific AI settings
  - `workspace.json` - Workspace configuration

- **Unified Workspace**: 
  - `workspace.code-workspace` - Multi-root workspace
  - `.editorconfig` - Cross-editor formatting rules

### Genesis CLI Configuration

- `genesis.config.json` - Main Genesis CLI configuration
- `genesis-cli.py` - Cross-platform CLI implementation
- `diesel_engine.yaml` - Diesel Engine module configuration

## 📦 Required Dependencies

### System Requirements
- **Python**: 3.8 or higher
- **Node.js**: 14.0 or higher (optional, for web features)
- **Git**: 2.0 or higher (optional, for version control)

### Python Packages
All required Python packages are listed in `requirements.txt` and will be installed automatically during setup.

## 🎯 Genesis CLI Commands

After setup, you can use the Genesis CLI with the following commands:

### Windows
```powershell
# If you've sourced the PowerShell function
genesis [command]

# Or directly
python genesis-cli.py [command]
```

### Linux/macOS
```bash
./genesis [command]
```

### Available Commands

| Command | Description |
|---------|-------------|
| `genesis init` | Initialize the workspace |
| `genesis build` | Build the project |
| `genesis deploy` | Deploy to production |
| `genesis sync` | Sync editor configurations |
| `genesis validate` | Validate all configurations |
| `genesis status` | Show current status |

### Command Options

- `--config <file>` - Specify custom config file
- `--debug` - Enable debug logging
- `--env <environment>` - Target environment (for deploy)
- `--secure` - Use secure deployment (for deploy)

## 🔧 Editor Features

### VS Code / Cursor Features
- **Auto-formatting** on save
- **Linting** with flake8 and pylint
- **Type checking** with mypy
- **Integrated terminal** with environment variables
- **Debug configurations** for Python and Node.js
- **Task automation** for build and deploy

### AI Integration
- **Cursor AI** enabled with context-aware suggestions
- **Claude integration** with Opus model
- **GitHub Copilot** support
- **Continue** extension for additional AI features

### Cross-Editor Consistency
- Unified formatting rules via `.editorconfig`
- Synchronized settings across all editors
- Shared debug configurations
- Common task definitions

## 🔄 Environment Variables

The following environment variables are automatically configured:

| Variable | Description |
|----------|-------------|
| `GENESIS_CLI_HOME` | Workspace root directory |
| `DIESEL_ENGINE_CONFIG` | Path to diesel_engine.yaml |
| `PYTHONPATH` | Python module search path |
| `GENESIS_PLATFORM` | Current platform identifier |

## 🐛 Debugging

### Python Debugging
1. Open the file you want to debug
2. Set breakpoints by clicking in the gutter
3. Press `F5` or select a debug configuration
4. Choose from available configurations:
   - Python: Current File
   - Python: Diesel Agent
   - Python: Voice Loop
   - Python: Deploy

### JavaScript Debugging
1. Open the JavaScript file
2. Set breakpoints
3. Press `F5` and select:
   - Node.js: Current File
   - Node.js: Resonance Core

### Full Stack Debugging
Use the compound configuration "Full Stack" to debug both Python and JavaScript simultaneously.

## 🚨 Troubleshooting

### Python Not Found
- **Windows**: Install from [python.org](https://www.python.org)
- **Linux**: `sudo apt install python3 python3-pip`
- **macOS**: `brew install python3`

### Virtual Environment Issues
```bash
# Remove existing venv
rm -rf .venv

# Create new venv
python3 -m venv .venv

# Activate
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate      # Windows
```

### Permission Denied (Linux/macOS)
```bash
chmod +x setup.sh genesis-cli.py genesis
```

### Module Import Errors
```bash
# Ensure PYTHONPATH is set
export PYTHONPATH=$PWD

# Reinstall dependencies
pip install -r requirements.txt
```

## 📝 Manual Setup

If the automated setup fails, you can manually configure:

1. **Create virtual environment**:
   ```bash
   python3 -m venv .venv
   ```

2. **Activate virtual environment**:
   - Linux/macOS: `source .venv/bin/activate`
   - Windows: `.venv\Scripts\activate`

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create directories**:
   ```bash
   mkdir -p .genesis/{cache,logs,temp,artifacts}
   mkdir -p .vscode .cursor
   ```

5. **Set environment variables**:
   ```bash
   export GENESIS_CLI_HOME=$PWD
   export DIESEL_ENGINE_CONFIG=$PWD/diesel_engine.yaml
   export PYTHONPATH=$PWD
   ```

## 🔐 Security Notes

- API keys should be stored in environment variables or `.env` files
- Never commit `.env` files to version control
- Use `secure_deploy.py` for production deployments
- Keep dependencies updated regularly

## 📚 Additional Resources

- [VS Code Documentation](https://code.visualstudio.com/docs)
- [Cursor Documentation](https://cursor.sh/docs)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [EditorConfig](https://editorconfig.org/)

## 💡 Tips

1. **Use workspace file**: Open `workspace.code-workspace` for multi-root workspace
2. **Install extensions**: Accept all recommended extensions for best experience
3. **Format on save**: Enable format on save for consistent code style
4. **Use tasks**: Run tasks with `Ctrl+Shift+B` (build) or `Ctrl+Shift+P` > "Tasks: Run Task"
5. **Debug efficiently**: Use compound configurations for full-stack debugging

## 🤝 Contributing

When contributing to this project:

1. Follow the `.editorconfig` rules
2. Run `genesis validate` before committing
3. Use `genesis build` to format and lint code
4. Write tests for new features
5. Update this README if adding new configurations

## 📄 License

See LICENSE file for details.

---

**Setup Complete!** Your development environment is now configured for seamless integration between all editors and the Genesis CLI. Happy coding! 🎉