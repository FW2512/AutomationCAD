class Messenger:
    """
    Central dispatcher for application messages.
    Routes messages to all registered handlers.
    """
    _handlers = []

    @classmethod
    def register_handler(cls, handler):
        """
        Register a new message handler.
        :param handler: An object with a 'handle_message' method.
        """
        cls._handlers.append(handler)

    @classmethod
    def info(cls, message: str):
        """
        Dispatch an informational message to all handlers.
        :param message: The message string.
        """
        cls._dispatch(message, level="info")

    @classmethod
    def error(cls, message: str):
        """
        Dispatch an error message to all handlers.
        :param message: The message string.
        """
        cls._dispatch(message, level="error")

    @classmethod
    def _dispatch(cls, message: str, level: str):
        """
        Internal method to send a message to all handlers.
        :param message: The message string.
        :param level: The level of the message ('info', 'error', etc.).
        """
        for handler in cls._handlers:
            handler.handle_message(message, level)
