import json
import queue
import threading
import serial

class SerialClient:
    def __init__(self, port="/dev/ttyUSB0"):
        self.serial = serial.Serial(
            port,
            115200,
            timeout=0.2,
            write_timeout=1
        )

        self.messages = queue.Queue()
        self.running = True
        self.write_lock = threading.Lock()

        self.thread = threading.Thread(
            target=self.read_loop,
            daemon=True
        )
        self.thread.start()

    def read_loop(self):
        while self.running:
            try:
                line = self.serial.readline()
                if not line:
                    continue

                text = line.decode(
                    "utf-8", errors="replace"
                ).strip()

                data = json.loads(text)

                if isinstance(data, dict):
                    self.messages.put(data)

            except json.JSONDecodeError:
                # Ignore ESP32 boot messages
                pass

            except (serial.SerialException, OSError) as error:
                self.running = False
                self.messages.put({
                    "_error": str(error)
                })
                break

    def send(self, command):
        if not self.running:
            return False

        try:
            with self.write_lock:
                self.serial.write(
                    (command + "\n").encode("utf-8")
                )
            return True

        except (serial.SerialException, OSError) as error:
            self.running = False
            self.messages.put({
                "_error": str(error)
            })
            return False

    def close(self):
        self.running = False

        if self.serial.is_open:
            self.serial.close()
