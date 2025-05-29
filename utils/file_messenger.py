import os
from datetime import datetime

class FileMessenger:
    def __init__(self, filepath="logs/app.log"):
        self.filepath = filepath
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

    def handle_message(self, msg: str, level: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(f"{timestamp} [{level.upper()}] {msg}\n")
