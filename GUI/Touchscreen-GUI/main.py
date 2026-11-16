import sys
import tkinter as tk
import serial

from serial_client import SerialClient
from screens.dashboard import Dashboard
from screens.settings import (
    Settings,
    load_settings,
    theme_color
)


PORT = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyUSB0"

BG = theme_color("background", fallback="#1C2420")
FG = theme_color("text", "foreground", fallback="white")


class IrrigationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Plant Irrigation System")
        self.root.geometry("480x320")
        self.root.configure(bg=BG)

        self.client = None
        self.connected = False
        self.latest_data = {}
        self.current_screen = None
        self.closed = False

        # Connect to ESP32
        try:
            self.client = SerialClient(PORT)
            status = "Connecting to ESP32..."
        except (serial.SerialException, OSError) as error:
            status = f"Connection failed: {error}"

        # Navigation
        nav = tk.Frame(root, bg="#3E503E")
        nav.pack(fill="x")

        tk.Button(
            nav,
            text="Dashboard",
            command=self.show_dashboard,
            bg="#587B52",
            fg="white",
            font=("Arial", 11)
        ).pack(side="left", padx=5, pady=5)

        tk.Button(
            nav,
            text="Settings",
            command=self.show_settings,
            bg="#587B52",
            fg="white",
            font=("Arial", 11)
        ).pack(side="left", padx=5, pady=5)

        # Connection status
        self.status_label = tk.Label(
            root,
            text=status,
            bg=BG,
            fg=FG,
            font=("Arial", 9)
        )
        self.status_label.pack(side="bottom", fill="x")

        # Main content
        self.content = tk.Frame(root, bg=BG)
        self.content.pack(fill="both", expand=True)

        self.show_dashboard()

        # Poll ESP32 without freezing GUI
        self.root.after(100, self.poll_serial)

        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_content()

        self.current_screen = Dashboard(
            self.content,
            on_water=self.water_now,
            on_stop=self.stop_water
        )
        self.current_screen.pack(fill="both", expand=True)

        if self.latest_data:
            self.current_screen.update_stats(
                self.latest_data
            )

    def show_settings(self):
        self.clear_content()

        self.current_screen = Settings(
            self.content,
            on_duration_changed=self.set_duration
        )
        self.current_screen.pack(fill="both", expand=True)

    def set_duration(self, seconds):
        if self.connected and self.client:
            if not self.client.send(f"DURATION:{seconds}"):
                self.connected = False
                self.set_status("Failed to send duration")

    def water_now(self):
        if not self.connected or not self.client:
            self.set_status("ESP32 not connected")
            return

        duration = load_settings()["pump_duration"]

        # Send duration before activating pump
        if not self.client.send(f"DURATION:{duration}"):
            self.connected = False
            self.set_status("Failed to set duration")
            return

        if self.client.send("WATER"):
            self.set_status(
                f"Watering requested: {duration}s"
            )
        else:
            self.connected = False
            self.set_status("Failed to start pump")

    def stop_water(self):
        if not self.connected or not self.client:
            self.set_status("ESP32 not connected")
            return

        if self.client.send("STOP"):
            self.set_status("Stop requested")
        else:
            self.connected = False
            self.set_status("Failed to send STOP")

    def set_status(self, message):
        self.status_label.config(text=message)

    def poll_serial(self):
        if self.closed:
            return

        if self.client:
            while not self.client.messages.empty():
                data = self.client.messages.get_nowait()

                # Handle serial errors
                if "_error" in data:
                    self.connected = False
                    self.set_status(
                        f"ESP32 disconnected: {data['_error']}"
                    )
                    continue

                if "pump" not in data:
                    continue

                # First valid JSON message
                if not self.connected:
                    if not self.client.running:
                        continue

                    self.connected = True

                    duration = load_settings()["pump_duration"]
                    self.client.send(
                        f"DURATION:{duration}"
                    )

                self.latest_data = data

                # Update dashboard
                if isinstance(self.current_screen, Dashboard):
                    self.current_screen.update_stats(data)

                # Update pump status
                pump = data.get("pump", False)

                if pump:
                    self.set_status("Pump running...")
                else:
                    self.set_status("ESP32 connected | Pump OFF")

        self.root.after(100, self.poll_serial)

    def close(self):
        self.closed = True

        if self.client:
            if self.connected:
                self.client.send("STOP")

            self.client.close()

        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = IrrigationGUI(root)
    root.mainloop()
