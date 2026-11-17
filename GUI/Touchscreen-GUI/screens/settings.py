import json
import tkinter as tk
from pathlib import Path

from theme import color

SETTINGS_FILE = Path(__file__).resolve().parent.parent / "settings.json"
OLD_SCHEDULE_FILE = SETTINGS_FILE.with_name("schedule_settings.json")
DEFAULT_SETTINGS = {
    "pump_duration": 5,
    "timed_watering_enabled": False,
    "watering_interval_minutes": 60,
}
MAX_INTERVAL_STEP = 106


def theme_color(*names, fallback):
    for name in names:
        try:
            return color(name)
        except KeyError:
            continue
    return fallback


def step_to_minutes(step):
    step = max(1, min(MAX_INTERVAL_STEP, int(round(float(step)))))
    return step if step <= 60 else 60 + (step - 60) * 30


def minutes_to_step(minutes):
    minutes = max(1, min(1440, int(float(minutes))))
    if minutes <= 60:
        return minutes
    return max(61, min(MAX_INTERVAL_STEP, 60 + round((minutes - 60) / 30)))


def format_interval(minutes):
    if minutes < 60:
        return f"{minutes} min"
    hours = minutes / 60
    return f"{hours:g} hr" + ("" if hours == 1 else "s")


def load_settings():
    settings = DEFAULT_SETTINGS.copy()
    saved = {}
    try:
        with SETTINGS_FILE.open("r", encoding="utf-8") as file:
            loaded = json.load(file)
        if isinstance(loaded, dict):
            saved = loaded
            settings.update(saved)
    except (FileNotFoundError, OSError, json.JSONDecodeError):
        pass

    # Import an existing timer configuration made by the earlier main.py,
    # but never override a value already stored in settings.json.
    if ("timed_watering_enabled" not in saved or
            "watering_interval_minutes" not in saved):
        try:
            with OLD_SCHEDULE_FILE.open("r", encoding="utf-8") as file:
                legacy = json.load(file)
            if isinstance(legacy, dict):
                if "timed_watering_enabled" not in saved:
                    settings["timed_watering_enabled"] = legacy.get("enabled", False)
                if "watering_interval_minutes" not in saved:
                    settings["watering_interval_minutes"] = legacy.get("interval_minutes", 60)
        except (FileNotFoundError, OSError, json.JSONDecodeError):
            pass

    try:
        settings["pump_duration"] = max(1, min(30, int(settings["pump_duration"])))
    except (ValueError, TypeError, OverflowError):
        settings["pump_duration"] = 5

    settings["timed_watering_enabled"] = settings["timed_watering_enabled"] is True
    try:
        step = minutes_to_step(settings["watering_interval_minutes"])
        settings["watering_interval_minutes"] = step_to_minutes(step)
    except (ValueError, TypeError, OverflowError):
        settings["watering_interval_minutes"] = 60
    return settings


def save_settings(settings):
    with SETTINGS_FILE.open("w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)


class Settings(tk.Frame):
    def __init__(self, parent, on_duration_changed=None, on_interval_changed=None):
        self.bg_color = theme_color("background", fallback="#1C2420")
        self.text_color = theme_color(
            "text", "text_primary", "foreground", fallback="#FFFFFF"
        )
        super().__init__(parent, bg=self.bg_color)

        self.on_duration_changed = on_duration_changed
        self.on_interval_changed = on_interval_changed
        self.settings = load_settings()
        self.pump_duration = tk.IntVar(value=self.settings["pump_duration"])
        self.interval_step = tk.IntVar(
            value=minutes_to_step(self.settings["watering_interval_minutes"])
        )
        self.create_widgets()

    def create_widgets(self):
        tk.Label(
            self,
            text="Settings",
            font=("Arial", 17, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        ).pack(pady=(5, 4))

        panel = tk.Frame(self, bg=self.bg_color)
        panel.pack(fill="both", expand=True, padx=16)

        duration_row = tk.Frame(panel, bg=self.bg_color)
        duration_row.pack(fill="x")
        tk.Label(
            duration_row,
            text="Pump duration",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        ).pack(side="left")
        self.duration_label = tk.Label(
            duration_row,
            text=f"{self.pump_duration.get()} seconds",
            font=("Arial", 11),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.duration_label.pack(side="right")

        self.duration_slider = tk.Scale(
            panel,
            from_=1,
            to=30,
            orient="horizontal",
            variable=self.pump_duration,
            resolution=1,
            showvalue=False,
            command=self.update_duration,
            bg=self.bg_color,
            fg=self.text_color,
            troughcolor="#657B62",
            activebackground="#82A276",
            highlightthickness=0,
            borderwidth=0,
            sliderlength=22
        )
        self.duration_slider.pack(fill="x", pady=(0, 7))

        interval_row = tk.Frame(panel, bg=self.bg_color)
        interval_row.pack(fill="x")
        tk.Label(
            interval_row,
            text="Timed watering interval",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        ).pack(side="left")
        self.interval_label = tk.Label(
            interval_row,
            text=format_interval(self.settings["watering_interval_minutes"]),
            font=("Arial", 11),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.interval_label.pack(side="right")

        self.interval_slider = tk.Scale(
            panel,
            from_=1,
            to=MAX_INTERVAL_STEP,
            orient="horizontal",
            variable=self.interval_step,
            resolution=1,
            showvalue=False,
            command=self.update_interval,
            bg=self.bg_color,
            fg=self.text_color,
            troughcolor="#657B62",
            activebackground="#82A276",
            highlightthickness=0,
            borderwidth=0,
            sliderlength=22
        )
        self.interval_slider.pack(fill="x", pady=(0, 3))

        tk.Label(
            panel,
            text="1-60 min, then 30-min steps up to 24 hrs",
            font=("Arial", 9),
            bg=self.bg_color,
            fg=self.text_color
        ).pack(anchor="w")
        tk.Label(
            panel,
            text="Both settings save automatically.",
            font=("Arial", 9),
            bg=self.bg_color,
            fg=self.text_color
        ).pack(anchor="w", pady=(2, 0))

    def _save(self):
        try:
            save_settings(self.settings)
        except OSError as error:
            print(f"Could not save settings: {error}")

    def update_duration(self, value):
        seconds = int(float(value))
        self.duration_label.config(text=f"{seconds} seconds")
        if self.settings["pump_duration"] != seconds:
            self.settings["pump_duration"] = seconds
            self._save()
            if self.on_duration_changed:
                self.on_duration_changed(seconds)

    def update_interval(self, value):
        minutes = step_to_minutes(value)
        self.interval_label.config(text=format_interval(minutes))
        if self.settings["watering_interval_minutes"] != minutes:
            self.settings["watering_interval_minutes"] = minutes
            self._save()
            if self.on_interval_changed:
                self.on_interval_changed(minutes)
