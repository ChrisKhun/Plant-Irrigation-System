import json
from pathlib import Path

theme_path = Path(__file__).resolve().parent / "themes.json"

with open(theme_path, "r") as file:
    theme = json.load(file)

def style(name):
    return theme[name].copy()

def color(name):
    return theme["colors"][name]
