import tkinter as tk

from screens.dashboard import Dashboard
from screens.settings import Settings


class IrrigationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Plant Irrigation System")
        self.root.geometry("480x320")
        self.root.configure(bg="#17212B")

        self.create_widgets()
        self.show_dashboard()

    def create_widgets(self):
        # Navigation bar
        self.navbar = tk.Frame(
            self.root,
            bg="#252D3A"
        )
        self.navbar.pack(side="top", fill="x")

        # Application title
        title = tk.Label(
            self.navbar,
            text="Plant Irrigation System",
            font=("Arial", 13, "bold"),
            fg="white",
            bg="#252D3A"
        )
        title.pack(side="left", padx=10, pady=10)

        # Settings button
        settings_btn = tk.Button(
            self.navbar,
            text="Settings",
            command=self.show_settings
        )
        settings_btn.pack(side="right", padx=5)

        # Dashboard button
        dashboard_btn = tk.Button(
            self.navbar,
            text="Dashboard",
            command=self.show_dashboard
        )
        dashboard_btn.pack(side="right", padx=5)

        # Main content container
        self.content = tk.Frame(
            self.root,
            bg="#17212B"
        )
        self.content.pack(fill="both", expand=True)

    def clear_content(self):
        # Remove widgets from the current screen
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_content()
        dashboard = Dashboard(self.content)
        dashboard.pack(fill="both", expand=True)

    def show_settings(self):
        self.clear_content()
        settings = Settings(self.content)
        settings.pack(fill="both", expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = IrrigationGUI(root)
    root.mainloop()

