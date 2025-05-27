class Messenger:
    """
    Messenger interface for routing messages.
    Can later be extended to connect with PyQt5 or other GUI frameworks.
    """

    _instance = None

    @classmethod
    def set_handler(cls, handler):
        cls._instance = handler

    @classmethod
    def send(cls, msg: str, level: str = "info"):
        if cls._instance:
            cls._instance.handle_message(msg, level)
        else:
            print(f"[{level.upper()}] {msg}")


class ConsoleMessenger:
    """
    Default fallback messenger to console.
    """
    def handle_message(self, msg: str, level: str):
        print(f"[{level.upper()}] {msg}")
