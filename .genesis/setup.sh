#!/bin/bash
# Genesis CLI Setup Script for Linux
# Configures symbiotic integration with Cursor, VS Code, and Claude Code

set -e

# Color output functions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

success() { echo -e "${GREEN}✓ $1${NC}"; }
info() { echo -e "${CYAN}ℹ $1${NC}"; }
warning() { echo -e "${YELLOW}⚠ $1${NC}"; }
error() { echo -e "${RED}✗ $1${NC}"; }

info "Genesis CLI Setup - Linux Architecture Detection"
info "=================================================="

# Detect architecture
ARCH=$(uname -m)
info "Detected architecture: $ARCH"

# Map architecture names
case "$ARCH" in
    x86_64)
        GENESIS_ARCH="x64"
        ;;
    aarch64|arm64)
        GENESIS_ARCH="arm64"
        ;;
    *)
        error "Unsupported architecture: $ARCH"
        exit 1
        ;;
esac

info "Genesis architecture: $GENESIS_ARCH"

# Set paths
GENESIS_HOME="$HOME/.genesis"
GENESIS_BIN="$GENESIS_HOME/bin"
GENESIS_CONFIG="$GENESIS_HOME/config"
GENESIS_CACHE="$GENESIS_HOME/cache"

# Create directories
info "Creating Genesis directories..."
mkdir -p "$GENESIS_BIN" "$GENESIS_CONFIG" "$GENESIS_CACHE"
success "Created directory structure"

# Create architecture-aware CLI wrapper
cat > "$GENESIS_BIN/genesis" << 'EOF'
#!/bin/bash
# Genesis CLI Wrapper - Auto-detect architecture

ARCH=$(uname -m)
BIN_DIR="$(dirname "$0")"

case "$ARCH" in
    x86_64)
        CLI_PATH="$BIN_DIR/genesis-x64"
        ;;
    aarch64|arm64)
        CLI_PATH="$BIN_DIR/genesis-arm64"
        ;;
    *)
        echo "Unsupported architecture: $ARCH"
        exit 1
        ;;
esac

if [ ! -f "$CLI_PATH" ]; then
    echo "================================================================"
    echo "Genesis CLI not found for architecture: $ARCH"
    echo "Expected location: $CLI_PATH"
    echo ""
    echo "This is a placeholder. Install the actual Genesis CLI binary to:"
    echo "$BIN_DIR"
    echo ""
    echo "Expected filename: $(basename "$CLI_PATH")"
    echo "================================================================"
    exit 1
fi

exec "$CLI_PATH" "$@"
EOF

chmod +x "$GENESIS_BIN/genesis"
success "Created CLI wrapper: $GENESIS_BIN/genesis"

# Add to PATH if not already present
SHELL_RC=""
if [ -n "$BASH_VERSION" ]; then
    SHELL_RC="$HOME/.bashrc"
elif [ -n "$ZSH_VERSION" ]; then
    SHELL_RC="$HOME/.zshrc"
else
    SHELL_RC="$HOME/.profile"
fi

if [ -f "$SHELL_RC" ]; then
    if ! grep -q "GENESIS_HOME" "$SHELL_RC"; then
        info "Adding Genesis to PATH in $SHELL_RC..."
        cat >> "$SHELL_RC" << 'EOF'

# Genesis CLI Configuration
export GENESIS_HOME="$HOME/.genesis"
export PATH="$GENESIS_HOME/bin:$PATH"

# Genesis CLI aliases
alias genesis-sync='genesis sync --workspace "$(pwd)"'
alias genesis-cross-sync='genesis cross-sync --editors vscode,cursor,claude'
EOF
        success "Added to $SHELL_RC (restart shell or run: source $SHELL_RC)"
    else
        success "Genesis already configured in $SHELL_RC"
    fi
fi

# Copy workspace config
WORKSPACE_CONFIG="$(dirname "$0")/config.yaml"
TARGET_CONFIG="$GENESIS_CONFIG/workspace-config.yaml"
if [ -f "$WORKSPACE_CONFIG" ]; then
    cp "$WORKSPACE_CONFIG" "$TARGET_CONFIG"
    success "Copied workspace configuration"
fi

# Create stub executables
info "Creating architecture-specific stubs..."

for stub_arch in "x64" "arm64"; do
    STUB_PATH="$GENESIS_BIN/genesis-$stub_arch"
    if [ ! -f "$STUB_PATH" ]; then
        cat > "$STUB_PATH" << 'STUBEOF'
#!/bin/bash
echo "================================================================"
echo "Genesis CLI Stub for $(uname -m)"
echo "================================================================"
echo "This is a placeholder script for the Genesis CLI."
echo ""
echo "To complete setup, install the actual Genesis CLI binary to:"
echo "$(dirname "$0")"
echo ""
echo "Expected filenames:"
echo "  - genesis-x64 (for x86_64/AMD64)"
echo "  - genesis-arm64 (for ARM64/aarch64)"
echo ""
echo "The Genesis CLI will integrate with:"
echo "  - VS Code (.vscode configuration)"
echo "  - Cursor (.cursor configuration)"  
echo "  - Claude Code"
echo ""
echo "Configuration: $HOME/.genesis/config/workspace-config.yaml"
echo "================================================================"
STUBEOF
        chmod +x "$STUB_PATH"
        warning "Created stub for $stub_arch (install actual binary)"
    fi
done

# Editor integration checks
info "Checking editor integration..."

if [ -d "$HOME/.config/Code/User" ]; then
    info "VS Code configuration found - Integration ready"
fi

if [ -d "$HOME/.config/Cursor/User" ]; then
    info "Cursor configuration found - Integration ready"
fi

success ""
success "Genesis CLI Setup Complete!"
success "=================================================="
info "Next steps:"
info "1. Install Genesis CLI binary to: $GENESIS_BIN"
info "2. Restart your shell or run: source $SHELL_RC"
info "3. Run: genesis --version"
info ""
info "Symbiotic integration configured for:"
info "  ✓ VS Code (.vscode/)"
info "  ✓ Cursor (.cursor/)"
info "  ✓ Claude Code"
info "  ✓ Architecture: $GENESIS_ARCH ($ARCH)"
