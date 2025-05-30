import os
import logging

class ConsoleHandler:
    def handle_message(self, message: str, level: str):
        prefix = f"[{level.upper()}]"
        print(f"{prefix} {message}")

class LogFileHandler:
    def __init__(self, log_file="logs/app.log"):
        
        self.log_file = log_file
        
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        logging.basicConfig(
            filename=self.log_file,
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filemode='a'
        )
        self.logger = logging.getLogger()

    def handle_message(self, message: str, level: str):
        if level == "info":
            self.logger.info(message)
        elif level == "error":
            self.logger.error(message)
        else:
            self.logger.debug(message)
