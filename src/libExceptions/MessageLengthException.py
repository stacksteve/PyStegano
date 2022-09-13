class MessageLengthException(Exception):
    def __init__(self, error_message: str):
        super().__init__(error_message)
