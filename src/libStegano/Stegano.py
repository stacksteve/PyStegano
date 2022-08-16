class Stegano:
    def __init__(self):
        # TODO: Static
        self.seperator_binary = self.stringToBinary("#@&%$*+<>=^")
        self.seperator_length = len(self.seperator_binary)

    @staticmethod
    def stringToBinary(message: str) -> str:
        """
        Get bytes from message string.

        :param message: The original message, than should be placed inside an image.
        :return: The binary representation of the
        """
        return "".join([format(ord(char), "08b") for char in message])

    @staticmethod
    def binaryToString(binary_message: str) -> str:
        """
        Evaluate bit string bytewise.

        :param binary_message: Binary message that has been extracted from an image.
        :return: The string representation of the bitstream.
        """
        return "".join(chr(Stegano.binaryToInt(binary_message[i * 8:i * 8 + 8])) for i in range(len(binary_message) // 8))

    @staticmethod
    def intToBinary(integer: int) -> str:
        if integer > 255:
            raise ValueError("Only values less or equal 255 (1 byte) are allowed")
        return format(integer, "08b")

    @staticmethod
    def binaryToInt(binary: str) -> int:
        return int(binary, 2)

    @staticmethod
    def bytesToBinary(bytestream: bytes) -> str:
        return "".join(Stegano.intToBinary(byte) for byte in bytestream)

    @staticmethod
    def binaryToBytes(bitstream: str) -> bytes:
        return bytes([Stegano.binaryToInt(bitstream[i * 8:i * 8 + 8]) for i in range(len(bitstream) // 8)])
