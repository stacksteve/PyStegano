from libStegano.Stegano import Stegano
from libSecurity import encrypt_message, sign_message
from utils import read_image, write_image


class SteganoWriter(Stegano):
    def __init__(self, original_image_path: str, stegano_image_path: str):
        """
        Read image data and store filename for later use in place_secret_message.

        :param original_image_path: Image that should be used to perform steganography.
        :param stegano_image_path: Secret message will be placed in this image.
        """
        self.__pil_image, self.__image_data = read_image(original_image_path)
        self.__out_file_name = stegano_image_path

    def place_secret_message(self, secret_message: bytes, public_key_receiver=None, private_key_sender=None) -> None:
        """
        Steps to place the secret message:
            1. Convert Plaintext into binary representation and add the binary end flag
            2. Check whether the number of bits of the message exceeds the number of pixels of the selected image
                2.1 If so, raise Exception
            3. Change the color value for red:
                - Color value XOR 1 -> Bit of secret message at position px equals '1'  (change value)
                - Color value XOR 0 -> Bit of secret message at position px equals '0'  (do not change value)
            4. Save/Write the new image

        :param private_key_sender: EdDSA private key to sign the message
        :param secret_message: Plaintext secret message
        :param public_key_receiver: RSA public key to encrypt the symmetric key
        :return: Method does not return anything
        """
        secret_message_bin = self.__convert_to_binary(secret_message, public_key_receiver, private_key_sender)
        full_secret_message = ''.join([secret_message_bin, self.END_FLAG_BIN])
        if not self.__has_correct_length(full_secret_message):
            raise ValueError('The image you selected is too small to store the secret message.')
        for px in range(len(full_secret_message)):
            self.__image_data[px] = self.__bit_flipper(px, int(full_secret_message[px]))
        write_image(self.__image_data, self.__pil_image, self.__out_file_name)

    def __convert_to_binary(self, secret_message: bytes, public_key_receiver, private_key_sender) -> str:
        """
        Generates a binary string from the plaintext message. Depending on whether a public key_path was provided
        the message gets encrypted before the representation is created.

        :param secret_message: Plaintext secret message
        :param public_key_receiver: RSA public key_path to encrypt the symmetric key_path
        :return: Binary representation of the plaintext message
        """
        if public_key_receiver and private_key_sender:
            return self.bytes_to_binary(encrypt_message(secret_message, public_key_receiver, private_key_sender))
        else:
            return self.bytes_to_binary(secret_message)

    def __bit_flipper(self, px: int, flip_bit: int) -> tuple:
        """
        Changes the color value for red depending on the respective bit (flip_bit) of the secret message.

        :param px: Pixel position in __image_data list
        :param flip_bit: A bit of secret message; if 1 -> change color value for red; else color value remains unchanged
        :return: Tuple of RGB color data (color value for red might be changed)
        """
        return self.__image_data[px][0] ^ flip_bit, self.__image_data[px][1], self.__image_data[px][2]

    def __has_correct_length(self, secret_message) -> bool:
        """
        Check if image has enough pixels to store the secret message.

        :param secret_message: Whole secret message including the plaintext message, message length and seperator
        :return: True if message has legal length; False else
        """
        return len(self.__image_data) >= len(secret_message)
