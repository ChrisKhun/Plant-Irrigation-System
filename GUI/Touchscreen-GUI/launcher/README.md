# Plant Irrigation System — GUI Installation

Installation guide for the Plant Irrigation System (PIS) touchscreen interface running on a Raspberry Pi.

The GUI is built using Python and Tkinter. It communicates with an ESP32 over USB serial to display sensor readings and control the water pump.

## Requirements

### Hardware
- Raspberry Pi with Raspberry Pi OS Desktop
- Touchscreen or connected display
- ESP32 microcontroller with compatible PIS firmware
- USB data cable
- Water pump and MOSFET switching module
- Power supply appropriate for the water pump

### Software
- Python 3
- Tkinter
- PySerial
- Git
- LXTerminal

The provided installation script installs the required software dependencies automatically.

## Installation

### 1. Connect to the Raspberry Pi

Open a terminal on your computer and connect to the Raspberry Pi through SSH:

```bash
ssh root1@raspberrypi.local
```

Replace `root1` with your Raspberry Pi username if different.

### 2. Clone the Repository

Navigate to your home directory:

```bash
cd ~
```

Clone the project from GitHub:

```bash
git clone https://github.com/ChrisKhun/Plant-Irrigation-System.git
```

### 3. Navigate to the Launcher

```bash
cd ~/Plant-Irrigation-System/GUI/Touchscreen-GUI/launcher
```

The launcher directory contains three files:

| File | Description |
|---|---|
| `install.sh` | Installs dependencies and creates the desktop shortcut |
| `launch-pis.sh` | Detects the serial device and launches the Python GUI |
| `PIS.desktop` | Template for the desktop application shortcut |

### 4. Run the Installer

Execute the installation script:

```bash
bash install.sh
```

The script will:

1. Update the Raspberry Pi's package index.
2. Install the required Python and system packages.
3. Make the launch script executable.
4. Create the desktop launcher.
5. Configure serial port access through the `dialout` group if needed.

After installation, the shortcut will be located at:

```text
~/Desktop/PIS.desktop
```

**Note:** If the installer adds your user to the `dialout` group, log out and back in before launching the application.

## Launching the GUI

1. Connect the ESP32 to the Raspberry Pi using a USB data cable.
2. Open the Raspberry Pi's graphical desktop.
3. Double-click **Plant Irrigation System**.
4. Select **Execute** or **Execute in Terminal** if prompted.

The launcher will search for an available USB serial device and start the Tkinter application.

The dashboard is configured for a 480 × 320 display.

### Manual Launch

Alternatively, open a terminal directly on the Raspberry Pi's graphical desktop:

```bash
cd ~/Plant-Irrigation-System/GUI/Touchscreen-GUI
python3 main.py /dev/ttyUSB0
```

Replace `/dev/ttyUSB0` with the appropriate serial device if necessary.

## Using the Dashboard

Once connected, the GUI provides the following functionality:

| Feature | Description |
|---|---|
| Dashboard | Displays temperature, humidity, soil moisture, and pump status |
| Water Now | Sends a command to activate the pump |
| Stop | Sends a command to stop the pump |
| Settings | Adjusts the pump watering duration |
| Serial Communication | Exchanges commands and sensor data with the ESP32 |

The ESP32 controls the pump duration and automatically turns the pump off when the configured time expires.

## Updating the Application

To download the latest changes from GitHub:

```bash
cd ~/Plant-Irrigation-System
git pull origin main
```

Restart the GUI after updating.

If the repository or launcher location changes, reinstall the desktop shortcut:

```bash
cd ~/Plant-Irrigation-System/GUI/Touchscreen-GUI/launcher
bash install.sh
```

## Troubleshooting

### ESP32 Not Detected

Verify that the ESP32 is connected and check the available serial devices:

```bash
ls /dev/ttyUSB* /dev/ttyACM*
```

You may see `/dev/ttyUSB0`, `/dev/ttyUSB1`, or `/dev/ttyACM0`.

Check serial permissions:

```bash
groups
```

If `dialout` is missing, run:

```bash
sudo usermod -aG dialout "$USER"
```

Log out and back in afterward.

### Serial Port Busy

If the GUI reports that the serial device is busy, close Arduino IDE's Serial Monitor and any other application using the ESP32.

To identify which process is using the device:

```bash
fuser -v /dev/ttyUSB0
```

### GUI Does Not Open

Run the launcher directly from a terminal on the Raspberry Pi's graphical desktop:

```bash
bash ~/Plant-Irrigation-System/GUI/Touchscreen-GUI/launcher/launch-pis.sh
```

Any Python errors should appear in the terminal.
