import math
import tkinter as tk

from .settings import format_interval, theme_color

BG = theme_color("background", fallback="#1C2420")
FG = theme_color("text", "foreground", fallback="white")
CARD = theme_color("surface", "card", fallback="#28332D")


class Dashboard(tk.Frame):
    def __init__(self, parent, on_water, on_stop,
                 on_timed_changed=None, timed_enabled=False,
                 interval_minutes=60):
        super().__init__(parent, bg=BG)
        self.on_water = on_water
        self.on_stop = on_stop
        self.on_timed_changed = on_timed_changed
        self.timed_enabled = timed_enabled
        self.interval_minutes = interval_minutes
        self.labels = {}
        self.create_widgets()

    def create_widgets(self):
        tk.Label(
            self,
            text="System Dashboard",
            font=("Arial", 16, "bold"),
            bg=BG,
            fg=FG
        ).pack(pady=(3, 5))

        grid = tk.Frame(self, bg=BG)
        grid.pack(fill="x", padx=8)
        items = [
            ("temperature", "Temperature"),
            ("humidity", "Humidity"),
            ("soil_moisture", "Soil Moisture"),
            ("pump", "Pump Status"),
        ]
        for i, (key, title) in enumerate(items):
            frame = tk.Frame(grid, bg=CARD, padx=5, pady=3)
            frame.grid(row=i // 2, column=i % 2, padx=4, pady=3, sticky="nsew")
            tk.Label(
                frame,
                text=title,
                bg=CARD,
                fg=FG,
                font=("Arial", 9)
            ).pack()
            label = tk.Label(
                frame,
                text="--",
                bg=CARD,
                fg=FG,
                font=("Arial", 13, "bold")
            )
            label.pack()
            self.labels[key] = label

        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

        buttons = tk.Frame(self, bg=BG)
        buttons.pack(pady=(6, 4))
        self.water_button = tk.Button(
            buttons,
            text="WATER NOW",
            command=self.on_water,
            bg="#587B52",
            fg="white",
            font=("Arial", 11, "bold"),
            width=13
        )
        self.water_button.pack(side="left", padx=5)
        tk.Button(
            buttons,
            text="STOP",
            command=self.on_stop,
            bg="#A34A42",
            fg="white",
            font=("Arial", 11, "bold"),
            width=8
        ).pack(side="left", padx=5)

        timer_bar = tk.Frame(self, bg=CARD)
        timer_bar.pack(side="bottom", fill="x", padx=6, pady=(1, 4))
        timer_info = tk.Frame(timer_bar, bg=CARD)
        timer_info.pack(side="left", fill="x", expand=True, padx=(8, 3), pady=3)
        tk.Label(
            timer_info,
            text="Timed watering",
            bg=CARD,
            fg=FG,
            font=("Arial", 10, "bold"),
            anchor="w"
        ).pack(fill="x")
        self.schedule_description = tk.Label(
            timer_info,
            text="",
            bg=CARD,
            fg=FG,
            font=("Arial", 9),
            anchor="w"
        )
        self.schedule_description.pack(fill="x")
        self.schedule_toggle = tk.Canvas(
            timer_bar,
            width=64,
            height=32,
            bg=CARD,
            highlightthickness=0,
            borderwidth=0,
            takefocus=1,
            cursor="hand2"
        )
        self.schedule_toggle.pack(side="right", padx=(2, 10), pady=5)
        self.schedule_toggle.bind("<Button-1>", self._toggle)
        self.schedule_toggle.bind("<space>", self._toggle)
        self.schedule_toggle.bind("<Return>", self._toggle)
        self.update_timed_watering(self.timed_enabled, self.interval_minutes)

    def _toggle(self, event=None):
        enabled = not self.timed_enabled
        if self.on_timed_changed:
            self.on_timed_changed(enabled)
        else:
            self.update_timed_watering(enabled, self.interval_minutes)

    def update_timed_watering(self, enabled, interval_minutes, remaining_seconds=None):
        self.timed_enabled = bool(enabled)
        self.interval_minutes = interval_minutes
        self._draw_switch()

        if not self.timed_enabled:
            description = f"OFF | Interval: {format_interval(interval_minutes)}"
        elif remaining_seconds is None:
            description = f"Every {format_interval(interval_minutes)} | Starting..."
        else:
            remaining = max(0, int(math.ceil(remaining_seconds)))
            hrs, remainder = divmod(remaining, 3600)
            mins, secs = divmod(remainder, 60)
            countdown = f"{hrs}h {mins:02d}m" if hrs else f"{mins}m {secs:02d}s"
            description = f"Every {format_interval(interval_minutes)} | Next: {countdown}"
        self.schedule_description.config(text=description)

    def _draw_switch(self):
        canvas = self.schedule_toggle
        canvas.delete("all")
        track = "#729A69" if self.timed_enabled else "#606B62"
        canvas.create_oval(1, 1, 31, 31, fill=track, outline=track)
        canvas.create_rectangle(16, 1, 48, 31, fill=track, outline=track)
        canvas.create_oval(33, 1, 63, 31, fill=track, outline=track)
        center = 48 if self.timed_enabled else 16
        canvas.create_oval(
            center - 12, 4, center + 12, 28, fill="white", outline="white"
        )

    def update_stats(self, data):
        temperature = data.get("temperature")
        humidity = data.get("humidity")
        soil = data.get("soil_moisture")
        pump = data.get("pump", False)

        self.labels["temperature"].config(
            text=f"{temperature:.1f} °F" if isinstance(temperature, (int, float)) else "--"
        )
        self.labels["humidity"].config(
            text=f"{humidity:.1f}%" if isinstance(humidity, (int, float)) else "--"
        )
        self.labels["soil_moisture"].config(
            text=f"{soil} RAW" if soil is not None else "--"
        )
        self.labels["pump"].config(
            text="ON" if pump else "OFF", fg="#83CC79" if pump else FG
        )
        self.water_button.config(state="disabled" if pump else "normal")
