#!/bin/bash
set -e

# Find directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

LAUNCHER="$SCRIPT_DIR/launch-pis.sh"
TEMPLATE="$SCRIPT_DIR/PIS.desktop"
DESKTOP="$HOME/Desktop"
SHORTCUT="$DESKTOP/PIS.desktop"

echo "Installing Plant Irrigation System..."

# Install dependencies
sudo apt update

sudo apt install -y \
    git \
    python3 \
    python3-tk \
    python3-serial \
    lxterminal

# Make launcher executable
chmod +x "$LAUNCHER"

# Create Desktop directory
mkdir -p "$DESKTOP"

# Generate desktop shortcut with correct path
python3 - "$TEMPLATE" "$LAUNCHER" "$SHORTCUT" <<'PY'
import sys
from pathlib import Path

template = Path(sys.argv[1])
launcher = Path(sys.argv[2]).resolve()
shortcut = Path(sys.argv[3])

content = template.read_text()
content = content.replace(
    "@LAUNCHER_PATH@",
    str(launcher)
)

shortcut.write_text(content)
PY

# Make desktop shortcut executable
chmod +x "$SHORTCUT"

# Check serial port permissions
if ! id -nG "$USER" | grep -qw dialout; then
    sudo usermod -aG dialout "$USER"
    echo "Serial access configured."
    echo "Log out and back in before using the ESP32."
fi

echo
echo "Installation complete!"
echo "Desktop shortcut: $SHORTCUT"
echo
echo "Double-click Plant Irrigation System to launch."
