#!/bin/bash

# Find project directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR" || exit 1

echo "Starting Plant Irrigation System..."

# Automatically detect ESP32
PORT=""

for device in /dev/serial/by-id/* /dev/ttyUSB* /dev/ttyACM*; do
    if [ -e "$device" ]; then
        PORT="$device"
        break
    fi
done

if [ -z "$PORT" ]; then
    echo "ERROR: ESP32 not detected!"
    read -r -p "Press Enter to close..."
    exit 1
fi

echo "ESP32 found at: $PORT"
echo "Launching dashboard..."

# Start GUI
python3 main.py "$PORT"

STATUS=$?

echo
echo "GUI exited with status: $STATUS"
read -r -p "Press Enter to close..."
