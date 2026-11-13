import serial
import json


class SerialClient:
    def __init__(self, port="/dev/ttyUSB0", baudrate=115200):
        self.esp32 = serial.Serial(port, baudrate, timeout=0.1)

    def read_sensors(self):
        line = self.esp32.readline().decode(
            "utf-8", errors="replace"
        ).strip()

        if not line:
            return None

        try:
            return json.loads(line)
        except json.JSONDecodeError:
            return None

    def close(self):
        self.esp32.close()
