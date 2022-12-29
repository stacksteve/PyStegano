class Stegano:
    # END_FLAG = #@&%$*+<>=^
    END_FLAG_BIN = '0010001101000000001001100010010100100100001010100010101100111100001111100011110101011110'
    END_FLAG_LEN = len(END_FLAG_BIN)

    @staticmethod
    def string_to_binary(message: str) -> str:
        """
        Format string to binary representation.

        :param message: The plaintext message that will be placed inside an image.
        :return: The binary representation of the
        """
        return "".join([Stegano.int_to_binary(ord(char)) for char in message])

    @staticmethod
    def binary_to_string(binary_message: str) -> str:
        """
        Inverse function of string_to_binary

        :param binary_message: Binary message that has been extracted from an image.
        :return: The string representation of the bitstream.
        """
        return "".join(chr(Stegano.binary_to_int(binary_message[i * 8:i * 8 + 8]))
                       for i in range(len(binary_message) // 8))

    @staticmethod
    def int_to_binary(integer: int) -> str:
        """
        Method used to transform an integer into its binary representation.

        :param integer: Natural number <= 255 (1 byte)
        :return: Binary representation on 1 byte (8 bits)
        """
        if integer > 255:
            raise ValueError("Only values less or equal 255 (1 byte) are allowed")
        return format(integer, '08b')

    @staticmethod
    def binary_to_int(binary: str) -> int:
        """
        Inverse method of int_to_binary.

        :param binary: Binary representation of an integer
        :return: Integer value
        """
        return int(binary, 2)

    @staticmethod
    def bytes_to_binary(bytestream: bytes) -> str:
        """
        Method used to transform bytestream (list of integers) into bitstream.

        :param bytestream: Sequence of bytes (0 <= Integer <= 255)
        :return: Binary string representation of the bytestream
        """
        return "".join(Stegano.int_to_binary(byte) for byte in bytestream)

    @staticmethod
    def binary_to_bytes(bitstream: str) -> bytes:
        """
        Inverse function of bytes_to_binary.

        :param bitstream: Bit representation of the bytestream (list of integers)
        :return: Bytestream
        """
        return bytes([Stegano.binary_to_int(bitstream[i * 8:i * 8 + 8]) for i in range(len(bitstream) // 8)])
