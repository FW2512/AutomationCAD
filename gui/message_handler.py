
class QtMessenger:
    def __init__(self, callback):
        """
        callback: function to emit message to GUI (like QTextEdit or QLabel)
        """
        self.callback = callback

    def handle_message(self, msg: str, level: str):
        formatted = f"[{level.upper()}] {msg}"
        self.callback(formatted)
        
"""
## In GUI setup:

from utils.messenger import Messenger
from gui.message_handler import QtMessenger

# Inside your PyQt5 GUI class
Messenger.set_handler(QtMessenger(self.display_message_to_ui))

"""
