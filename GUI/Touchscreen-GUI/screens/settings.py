import json
import tkinter as tk
from pathlib import Path

from theme import color


SETTINGS_FILE = (
    Path(__file__).resolve().parent.parent / "settings.json"
)

DEFAULT_SETTINGS = {
    "pump_duration": 5
}


def theme_color(*names, fallback):
    for name in names:
        try:
            return color(name)
        except KeyError:
            continue
    return fallback


def load_settings():
    settings = DEFAULT_SETTINGS.copy()

    try:
        with SETTINGS_FILE.open("r") as file:
            saved = json.load(file)

        if isinstance(saved, dict):
            settings.update(saved)

    except (FileNotFoundError, OSError, json.JSONDecodeError):
        pass

    try:
        settings["pump_duration"] = max(
            1,
            min(30, int(settings["pump_duration"]))
        )
    except (ValueError, TypeError):
        settings["pump_duration"] = 5

    return settings


def save_settings(settings):
    with SETTINGS_FILE.open("w") as file:
        json.dump(settings, file, indent=4)


class Settings(tk.Frame):
    def __init__(self, parent, on_duration_changed=None):
        self.bg_color = theme_color(
            "background", fallback="#1C2420"
        )
        self.text_color = theme_color(
            "text", "text_primary", "foreground",
            fallback="#FFFFFF"
        )

        super().__init__(parent, bg=self.bg_color)

        self.on_duration_changed = on_duration_changed
        self.settings = load_settings()

        self.pump_duration = tk.IntVar(
            value=self.settings["pump_duration"]
        )

        self.create_widgets()

    def create_widgets(self):
        tk.Label(
            self,
            text="Settings",
            font=("Arial", 20, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        ).pack(pady=12)

        frame = tk.Frame(self, bg=self.bg_color)
        frame.pack(fill="x", padx=20, pady=5)

        tk.Label(
            frame,
            text="Pump Duration",
            font=("Arial", 14),
            bg=self.bg_color,
            fg=self.text_color
        ).pack(anchor="w")

        self.duration_label = tk.Label(
            frame,
            text=f"{self.pump_duration.get()} seconds",
            font=("Arial", 12),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.duration_label.pack()

        self.slider = tk.Scale(
            frame,
            from_=1,
            to=30,
            orient="horizontal",
            variable=self.pump_duration,
            resolution=1,
            showvalue=False,
            command=self.update_duration,
            bg=self.bg_color,
            fg=self.text_color,
            highlightthickness=0
        )
        self.slider.pack(fill="x", pady=10)

        tk.Label(
            frame,
            text="Duration is saved automatically.",
            font=("Arial", 10),
            bg=self.bg_color,
            fg=self.text_color
        ).pack()

    def update_duration(self, value):
        seconds = int(float(value))

        self.duration_label.config(
            text=f"{seconds} seconds"
        )

        if self.settings["pump_duration"] != seconds:
            self.settings["pump_duration"] = seconds
            save_settings(self.settings)

            if self.on_duration_changed:
                self.on_duration_changed(seconds)
