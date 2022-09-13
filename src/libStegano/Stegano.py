class Stegano:
    # seperator = #@&%$*+<>=^
    seperator_binary = "0010001101000000001001100010010100100100001010100010101100111100001111100011110101011110"
    seperator_length = len(seperator_binary)

    @staticmethod
    def string_to_binary(message: str) -> str:
        """
        Format string to binary representation.

        :param message: The original message that should be placed inside an image.
        :return: The binary representation of the
        """
        return "".join([format(ord(char), "08b") for char in message])

    @staticmethod
    def binary_to_string(binary_message: str) -> str:
        """
        Evaluate bit string bytewise.

        :param binary_message: Binary message that has been extracted from an image.
        :return: The string representation of the bitstream.
        """
        return "".join(chr(Stegano.binary_to_int(binary_message[i * 8:i * 8 + 8]))
                       for i in range(len(binary_message) // 8))

    @staticmethod
    def int_to_binary(integer: int) -> str:
        if integer > 255:
            raise ValueError("Only values less or equal 255 (1 byte) are allowed")
        return format(integer, "08b")

    @staticmethod
    def binary_to_int(binary: str) -> int:
        return int(binary, 2)

    @staticmethod
    def bytes_to_binary(bytestream: bytes) -> str:
        return "".join(Stegano.int_to_binary(byte) for byte in bytestream)

    @staticmethod
    def binary_to_bytes(bitstream: str) -> bytes:
        return bytes([Stegano.binary_to_int(bitstream[i * 8:i * 8 + 8]) for i in range(len(bitstream) // 8)])
