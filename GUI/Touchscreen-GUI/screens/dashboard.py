import tkinter as tk

from .settings import theme_color


BG = theme_color("background", fallback="#1C2420")
FG = theme_color("text", "foreground", fallback="white")
CARD = theme_color("surface", "card", fallback="#28332D")


class Dashboard(tk.Frame):
    def __init__(self, parent, on_water, on_stop):
        super().__init__(parent, bg=BG)

        self.on_water = on_water
        self.on_stop = on_stop
        self.labels = {}

        self.create_widgets()

    def create_widgets(self):
        tk.Label(
            self,
            text="System Dashboard",
            font=("Arial", 18, "bold"),
            bg=BG,
            fg=FG
        ).pack(pady=(8, 10))

        grid = tk.Frame(self, bg=BG)
        grid.pack(fill="x", padx=12)

        items = [
            ("temperature", "Temperature"),
            ("humidity", "Humidity"),
            ("soil_moisture", "Soil Moisture"),
            ("pump", "Pump Status")
        ]

        for i, (key, title) in enumerate(items):
            frame = tk.Frame(
                grid, bg=CARD, padx=8, pady=5
            )

            frame.grid(
                row=i // 2,
                column=i % 2,
                padx=5,
                pady=4,
                sticky="nsew"
            )

            tk.Label(
                frame,
                text=title,
                bg=CARD,
                fg=FG,
                font=("Arial", 10)
            ).pack()

            label = tk.Label(
                frame,
                text="--",
                bg=CARD,
                fg=FG,
                font=("Arial", 15, "bold")
            )
            label.pack()

            self.labels[key] = label

        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

        buttons = tk.Frame(self, bg=BG)
        buttons.pack(pady=12)

        self.water_button = tk.Button(
            buttons,
            text="WATER NOW",
            command=self.on_water,
            bg="#587B52",
            fg="white",
            font=("Arial", 12, "bold"),
            width=13
        )
        self.water_button.pack(side="left", padx=6)

        tk.Button(
            buttons,
            text="STOP",
            command=self.on_stop,
            bg="#A34A42",
            fg="white",
            font=("Arial", 12, "bold"),
            width=8
        ).pack(side="left", padx=6)

    def update_stats(self, data):
        temperature = data.get("temperature")
        humidity = data.get("humidity")
        soil = data.get("soil_moisture")
        pump = data.get("pump", False)

        self.labels["temperature"].config(
            text=(
                f"{temperature:.1f} °F"
                if isinstance(temperature, (int, float))
                else "--"
            )
        )

        self.labels["humidity"].config(
            text=(
                f"{humidity:.1f}%"
                if isinstance(humidity, (int, float))
                else "--"
            )
        )

        self.labels["soil_moisture"].config(
            text=f"{soil} RAW" if soil is not None else "--"
        )

        self.labels["pump"].config(
            text="ON" if pump else "OFF",
            fg="#83CC79" if pump else FG
        )

        self.water_button.config(
            state="disabled" if pump else "normal"
        )
