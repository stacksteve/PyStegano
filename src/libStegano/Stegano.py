from abc import ABC


class Stegano(ABC):
    # END_FLAG = #@&%$*+<>=^
    END_FLAG_BIN = '0010001101000000001001100010010100100100001010100010101100111100001111100011110101011110'
    END_FLAG_LEN = len(END_FLAG_BIN)

    @staticmethod
    def int_to_binary(integer: int) -> str:
        """
        Method used to transform an integer into its binary representation.

        :param integer: Natural number <= 255 (1 byte)
        :return: Binary representation on 1 byte (8 bits)
        """
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
        return ''.join(Stegano.int_to_binary(byte) for byte in bytestream)

    @staticmethod
    def binary_to_bytes(bitstream: str) -> bytes:
        """
        Inverse function of bytes_to_binary.

        :param bitstream: Bit representation of the bytestream (list of integers)
        :return: Bytestream
        """
        return bytes([Stegano.binary_to_int(bitstream[i * 8:i * 8 + 8]) for i in range(len(bitstream) // 8)])
