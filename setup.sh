#!/bin/bash
# Genesis CLI Setup Script for Linux/macOS (32/64-bit)
# Configures Cursor, VS Code, and Claude integration

set -e

echo "============================================"
echo "Genesis CLI Setup for Unix/Linux"
echo "============================================"
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Detect OS and architecture
detect_platform() {
    OS=$(uname -s | tr '[:upper:]' '[:lower:]')
    ARCH=$(uname -m)
    
    case "$OS" in
        linux*)
            PLATFORM="linux"
            ;;
        darwin*)
            PLATFORM="darwin"
            ;;
        *)
            PLATFORM="unknown"
            ;;
    esac
    
    case "$ARCH" in
        x86_64|amd64)
            ARCH_TYPE="x64"
            BITS="64"
            ;;
        i386|i686)
            ARCH_TYPE="x86"
            BITS="32"
            ;;
        arm64|aarch64)
            ARCH_TYPE="arm64"
            BITS="64"
            ;;
        *)
            ARCH_TYPE="$ARCH"
            BITS="unknown"
            ;;
    esac
    
    echo -e "${GREEN}Detected Platform: $PLATFORM-$ARCH_TYPE ($BITS-bit)${NC}"
}

# Check for required commands
check_command() {
    if command -v "$1" &> /dev/null; then
        echo -e "${GREEN}✓ $1 found: $(command -v $1)${NC}"
        if [ "$2" = "version" ]; then
            $1 --version 2>&1 | head -n 1
        fi
        return 0
    else
        echo -e "${YELLOW}✗ $1 not found${NC}"
        return 1
    fi
}

# Create directory structure
create_directories() {
    echo
    echo "Creating directory structure..."
    
    directories=(
        ".genesis"
        ".genesis/cache"
        ".genesis/logs"
        ".genesis/temp"
        ".genesis/artifacts"
        ".vscode"
        ".cursor"
    )
    
    for dir in "${directories[@]}"; do
        mkdir -p "$dir"
        echo "  Created: $dir"
    done
}

# Setup Python environment
setup_python() {
    echo
    echo "Setting up Python environment..."
    
    # Find Python command
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        echo -e "${RED}ERROR: Python not found${NC}"
        echo "Please install Python 3.8 or higher"
        exit 1
    fi
    
    echo "Using Python: $PYTHON_CMD"
    $PYTHON_CMD --version
    
    # Create virtual environment if it doesn't exist
    if [ ! -d ".venv" ]; then
        echo "Creating Python virtual environment..."
        $PYTHON_CMD -m venv .venv
        if [ $? -ne 0 ]; then
            echo -e "${RED}ERROR: Failed to create virtual environment${NC}"
            exit 1
        fi
    fi
    
    # Activate virtual environment
    echo "Activating virtual environment..."
    source .venv/bin/activate
    
    # Upgrade pip
    echo "Upgrading pip..."
    pip install --upgrade pip
    
    # Install dependencies
    if [ -f "requirements.txt" ]; then
        echo "Installing Python dependencies..."
        pip install -r requirements.txt
    else
        echo "Creating requirements.txt..."
        cat > requirements.txt << EOF
pyyaml>=6.0
requests>=2.28.0
black>=22.0.0
flake8>=5.0.0
mypy>=0.990
pytest>=7.0.0
python-dotenv>=0.20.0
watchdog>=2.1.0
click>=8.0.0
EOF
        pip install -r requirements.txt
    fi
}

# Create genesis launcher script
create_launcher() {
    echo
    echo "Creating genesis launcher..."
    
    cat > genesis << 'EOF'
#!/bin/bash
# Genesis CLI Launcher

# Set environment variables
export GENESIS_CLI_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export DIESEL_ENGINE_CONFIG="$GENESIS_CLI_HOME/diesel_engine.yaml"
export PYTHONPATH="$GENESIS_CLI_HOME"
export GENESIS_PLATFORM="$(uname -s | tr '[:upper:]' '[:lower:]')-$(uname -m)"

# Activate virtual environment if it exists
if [ -f "$GENESIS_CLI_HOME/.venv/bin/activate" ]; then
    source "$GENESIS_CLI_HOME/.venv/bin/activate"
fi

# Run Genesis CLI
python "$GENESIS_CLI_HOME/genesis-cli.py" "$@"
EOF
    
    chmod +x genesis
    chmod +x genesis-cli.py
    
    echo -e "${GREEN}Genesis launcher created${NC}"
}

# Install VS Code extensions
install_vscode_extensions() {
    if command -v code &> /dev/null; then
        echo
        echo "Installing VS Code extensions..."
        
        extensions=(
            "ms-python.python"
            "ms-python.vscode-pylance"
            "ms-python.black-formatter"
            "esbenp.prettier-vscode"
            "redhat.vscode-yaml"
            "github.copilot"
            "continue.continue"
        )
        
        for ext in "${extensions[@]}"; do
            code --install-extension "$ext" 2>/dev/null || true
        done
        
        echo -e "${GREEN}VS Code extensions installed${NC}"
    fi
}

# Main setup function
main() {
    echo "Starting setup..."
    echo
    
    # Detect platform
    detect_platform
    echo
    
    # Check required commands
    echo "Checking required commands..."
    check_command "git" "version"
    check_command "node" "version" || echo "  Some features may not work without Node.js"
    check_command "code" "" || echo "  VS Code not found"
    check_command "cursor" "" || echo "  Cursor not found"
    echo
    
    # Create directories
    create_directories
    
    # Setup Python
    setup_python
    
    # Create launcher
    create_launcher
    
    # Initialize Genesis CLI
    echo
    echo "Initializing Genesis CLI..."
    python genesis-cli.py init
    
    # Validate setup
    echo
    echo "Validating setup..."
    python genesis-cli.py validate || true
    
    # Show status
    echo
    python genesis-cli.py status
    
    # Install VS Code extensions if available
    install_vscode_extensions
    
    echo
    echo "============================================"
    echo -e "${GREEN}Setup completed successfully!${NC}"
    echo "============================================"
    echo
    echo "To use Genesis CLI, run: ./genesis [command]"
    echo "To activate the virtual environment: source .venv/bin/activate"
    echo
    echo "Available commands:"
    echo "  ./genesis init      - Initialize workspace"
    echo "  ./genesis build     - Build the project"
    echo "  ./genesis deploy    - Deploy to production"
    echo "  ./genesis sync      - Sync editor configurations"
    echo "  ./genesis validate  - Validate configurations"
    echo "  ./genesis status    - Show current status"
    echo
    
    # Add to PATH suggestion
    echo "To add Genesis to your PATH, run:"
    echo "  echo 'export PATH=\"$PWD:\$PATH\"' >> ~/.bashrc"
    echo "  source ~/.bashrc"
    echo
}

# Run main function
main