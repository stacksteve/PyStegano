from libStegano.Stegano import Stegano
from libSecurity import encrypt_message
from utils import read_image, write_image
from libExceptions import MessageLengthException


class SteganoWriter(Stegano):
    def __init__(self, original_image_path: str, stegano_image_path: str):
        """
        Read image data and store filename for later use in place_secret_message.

        :param original_image_path: Image that should be used to perform steganography.
        :param stegano_image_path: Secret message will be placed in this image.
        """
        self.__pil_image, self.__image_data = read_image(original_image_path)
        self.__out_file_name = stegano_image_path

    def place_secret_message(self, secret_message: str, public_key_receiver=None) -> None:
        """
        Steps to place the secret message:
            1. Convert Plaintext into binary representation
            2. Convert secret message length into binary representation and merge it with the binary seperator
            3. Full binary message = message length + seperator + secret message
            4. Check whether the number of bits of the message exceeds the number of pixels of the selected image
                4.1 If so, raise Exception
            5. Change the color value for red:
                - Color value XOR 1 -> secret message bit at position i equals "1"  (change value)
                - Color value XOR 0 -> secret message bit at position i equals "0"  (do not change value)
            6. Save/Write the new image

        :param secret_message: Plaintext secret message
        :param public_key_receiver: RSA public key to encrypt the symmetric key
        :return: Method does not return anything
        """
        secret_message_bits = self.__get_secret_message_bits(secret_message, public_key_receiver)
        secret_message_length = self.__gen_binary_message_length_string(len(secret_message_bits))
        full_secret_message = secret_message_length + secret_message_bits
        if not self.has_correct_length(full_secret_message):
            raise MessageLengthException("The image you selected has too less pixel to store the secret message.")
        for i in range(len(full_secret_message)):
            self.__image_data[i] = self.__bit_flipper(i, int(full_secret_message[i]))
        write_image(self.__image_data, self.__pil_image, self.__out_file_name)

    def __get_secret_message_bits(self, secret_message: str, public_key_receiver) -> str:
        """
        Generates a binary string from the plaintext message. Depending on whether a public key was provided
        the message gets encrypted before the representation is created.

        :param secret_message: Plaintext secret message
        :param public_key_receiver: RSA public key to encrypt the symmetric key
        :return: Binary representation of the plaintext message
        """
        if public_key_receiver:
            return self.bytes_to_binary(encrypt_message(secret_message.encode(), public_key_receiver))
        else:
            return self.string_to_binary(secret_message)

    def __gen_binary_message_length_string(self, message_length: int) -> str:
        """
        Generates a binary string that will be used in SteganoReader to find the position of the secret message inside
        the stegano image.

        :param message_length: Length of the binary representation of plaintext message
        :return: Binary string including the message length (integer) and the seperator
        """
        return self.string_to_binary(str(message_length)) + self.seperator_binary

    def __bit_flipper(self, i: int, flip_bit: int) -> tuple:
        """
        Changes the color value for red depending on the respective bit (flip_bit) of the secret message.

        :param i: Pixel position in __image_data list
        :param flip_bit: Bit of secret message; if 1 than change color value for red; else color value remains unchanged
        :return: Tuple of RGB color data (color value for red might be changed)
        """
        return self.__image_data[i][0] ^ flip_bit, self.__image_data[i][1], self.__image_data[i][2]

    def has_correct_length(self, secret_message) -> bool:
        """
        Check if image has enough pixels to store the secret message.

        :param secret_message: Whole secret message including the plaintext message, message length and seperator
        :return: True if message has legal length; False else
        """
        return len(self.__image_data) >= len(secret_message)
