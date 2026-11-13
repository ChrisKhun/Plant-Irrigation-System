import tkinter as tk
from theme import style, color
from serial_client import SerialClient

class Dashboard(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=color("background"))
        self.create_widgets()

    def create_widgets(self):
        # Dashboard title
        title = tk.Label(
            self,
            text="Plant Dashboard",
            **style("title")
        )
        title.pack(pady=10)

        # Sensor grid container
        sensor_grid = tk.Frame(
            self,
            bg=color("background")
        )
        sensor_grid.pack(fill="x", padx=15, pady=5)

        # Configure grid columns
        sensor_grid.columnconfigure(0, weight=1)
        sensor_grid.columnconfigure(1, weight=1)

        # Sensor readings (placeholder values)
        sensors = [
            ("Soil Moisture", "42%"),
            ("Temperature", "74°F"),
            ("Humidity", "58%"),
            ("Reservoir", "75%")
        ]

        # Create sensor boxes
        for index, (name, value) in enumerate(sensors):
            row = index // 2
            col = index % 2

            card = tk.Label(
                sensor_grid,
                text=f"{name}\n{value}",
                bg=color("surface"),
                fg=color("text"),
                font=("Arial", 12),
                padx=10,
                pady=12,
                relief="flat"
            )

            card.grid(
                row=row,
                column=col,
                padx=5,
                pady=5,
                sticky="nsew"
            )

        # Water Now button
        water_button = tk.Button(
            self,
            text="Water Now",
            command=self.water_now,
            **style("button")
        )
        water_button.pack(pady=10)

    def water_now(self):
        print("Water Now button clicked!")

    def update_stats(self):
        pass
