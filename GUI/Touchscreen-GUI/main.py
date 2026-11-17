import sys
import time
import tkinter as tk

import serial

from serial_client import SerialClient
from screens.dashboard import Dashboard
from screens.settings import Settings, load_settings, save_settings, theme_color

PORT = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyUSB0"
BG = theme_color("background", fallback="#1C2420")
FG = theme_color("text", "foreground", fallback="white")


class IrrigationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Plant Irrigation System")
        self.root.geometry("480x320")  # Windowed fallback for desktop testing.
        self.root.configure(bg=BG)
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", self.exit_fullscreen)
        self.root.bind("<F11>", self.toggle_fullscreen)

        self.client = None
        self.connected = False
        self.latest_data = {}
        self.current_screen = None
        self.closed = False

        prefs = load_settings()
        self.schedule_enabled = prefs["timed_watering_enabled"]
        self.interval_minutes = prefs["watering_interval_minutes"]
        # Enabling or launching the app starts a *fresh* countdown, rather
        # than immediately watering to make up for time while it was closed.
        self.next_watering_at = (
            time.monotonic() + self.interval_minutes * 60
            if self.schedule_enabled else None
        )

        try:
            self.client = SerialClient(PORT)
            status = "Connecting to ESP32..."
        except (serial.SerialException, OSError) as error:
            status = f"Connection failed: {error}"

        nav = tk.Frame(root, bg="#3E503E")
        nav.pack(fill="x")
        tk.Button(
            nav, text="Dashboard", command=self.show_dashboard,
            bg="#587B52", fg="white", font=("Arial", 11), relief="flat",
        ).pack(side="left", padx=(5, 2), pady=3)
        tk.Button(
            nav, text="Settings", command=self.show_settings,
            bg="#587B52", fg="white", font=("Arial", 11), relief="flat",
        ).pack(side="left", padx=2, pady=3)
        tk.Button(
            nav, text="X", command=self.close,
            bg="#587852", fg="white", font=("Arial", 11), relief="flat",
            width=3,
        ).pack(side="right", padx=5, pady=3)

        self.status_label = tk.Label(root, text=status, bg=BG, fg=FG,
                                     font=("Arial", 9))
        self.status_label.pack(side="bottom", fill="x")
        self.content = tk.Frame(root, bg=BG)
        self.content.pack(fill="both", expand=True)
        self.show_dashboard()

        self.root.after(100, self.poll_serial)
        self.root.after(1000, self.check_schedule)
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def exit_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", False)

    def toggle_fullscreen(self, event=None):
        self.root.attributes(
            "-fullscreen", not bool(self.root.attributes("-fullscreen"))
        )

    def clear_content(self):
        self.current_screen = None
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_content()
        self.current_screen = Dashboard(
            self.content,
            on_water=self.water_now,
            on_stop=self.stop_water,
            on_timed_changed=self.set_timed_watering,
            timed_enabled=self.schedule_enabled,
            interval_minutes=self.interval_minutes,
        )
        self.current_screen.pack(fill="both", expand=True)
        if self.latest_data:
            self.current_screen.update_stats(self.latest_data)
        self.update_schedule_display()

    def show_settings(self):
        self.clear_content()
        self.current_screen = Settings(
            self.content,
            on_duration_changed=self.set_duration,
            on_interval_changed=self.set_interval,
        )
        self.current_screen.pack(fill="both", expand=True)

    def set_timed_watering(self, enabled):
        self.schedule_enabled = bool(enabled)
        self.next_watering_at = (
            time.monotonic() + self.interval_minutes * 60
            if self.schedule_enabled else None
        )
        settings = load_settings()
        settings["timed_watering_enabled"] = self.schedule_enabled
        try:
            save_settings(settings)
        except OSError as error:
            self.set_status(f"Could not save timer setting: {error}")
        self.update_schedule_display()

    def set_interval(self, minutes):
        # The Settings screen has already saved the new interval.
        self.interval_minutes = minutes
        if self.schedule_enabled:
            self.next_watering_at = time.monotonic() + minutes * 60
        self.update_schedule_display()

    def update_schedule_display(self):
        if isinstance(self.current_screen, Dashboard):
            remaining = None
            if self.next_watering_at is not None:
                remaining = max(0, self.next_watering_at - time.monotonic())
            self.current_screen.update_timed_watering(
                self.schedule_enabled, self.interval_minutes, remaining
            )

    def check_schedule(self):
        if self.closed:
            return
        now = time.monotonic()
        if (self.schedule_enabled and self.next_watering_at is not None
                and now >= self.next_watering_at):
            if not self.connected or self.latest_data.get("pump", False):
                # Retry briefly if ESP32 is offline or another watering is running.
                self.next_watering_at = now + 5
            elif self.water_now():
                # Scheduled watering sends the SAME DURATION and WATER commands
                # used by the manual Water Now button.
                self.next_watering_at = now + self.interval_minutes * 60
            else:
                self.next_watering_at = now + 5
        self.update_schedule_display()
        self.root.after(1000, self.check_schedule)

    def set_duration(self, seconds):
        if self.connected and self.client:
            if not self.client.send(f"DURATION:{seconds}"):
                self.connected = False
                self.set_status("Failed to send duration")

    def water_now(self):
        if not self.connected or not self.client:
            self.set_status("ESP32 not connected")
            return False
        duration = load_settings()["pump_duration"]
        if not self.client.send(f"DURATION:{duration}"):
            self.connected = False
            self.set_status("Failed to set duration")
            return False
        if self.client.send("WATER"):
            self.set_status(f"Watering requested: {duration}s")
            return True
        self.connected = False
        self.set_status("Failed to start pump")
        return False

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
                if "_error" in data:
                    self.connected = False
                    self.set_status(f"ESP32 disconnected: {data['_error']}")
                    continue
                if "pump" not in data:
                    continue
                if not self.connected:
                    if not self.client.running:
                        continue
                    self.connected = True
                    duration = load_settings()["pump_duration"]
                    self.client.send(f"DURATION:{duration}")
                self.latest_data = data
                if isinstance(self.current_screen, Dashboard):
                    self.current_screen.update_stats(data)
                self.set_status(
                    "Pump running..." if data.get("pump", False)
                    else "ESP32 connected | Pump OFF"
                )
        self.root.after(100, self.poll_serial)

    def close(self):
        if self.closed:
            return
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
