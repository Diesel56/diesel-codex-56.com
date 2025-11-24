#!/bin/bash
# Genesis CLI - Unix/Linux/macOS Shell Script
# Supports both 32-bit and 64-bit architectures

# Detect architecture
ARCH=$(uname -m)
if [[ "$ARCH" == "x86_64" ]] || [[ "$ARCH" == "amd64" ]]; then
    ARCH_TYPE="64-bit"
elif [[ "$ARCH" == "i386" ]] || [[ "$ARCH" == "i686" ]]; then
    ARCH_TYPE="32-bit"
else
    ARCH_TYPE="unknown"
fi

echo "Genesis CLI - Diesel Genesis Engine"
echo "Platform: $(uname -s) ($ARCH_TYPE)"
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check for Node.js
if ! command -v node &> /dev/null; then
    echo "Error: Node.js not found. Please install Node.js first."
    exit 1
fi

# Run the JavaScript CLI
node "$SCRIPT_DIR/genesis-cli.js" "$@"
