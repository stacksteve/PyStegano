from src.libStegano.Stegano import Stegano
from src.libSecurity.Encryption import encrypt_message
from src.utils.PicReader import read_image, write_image
from src.libExceptions.MessageLengthException import MessageLengthException


class SteganoWriter(Stegano):
    def __init__(self, in_file_name: str, out_file_name: str):
        self.__rgb, self.__image_data = read_image(in_file_name)
        self.__out_file_name = out_file_name

    def place_secret_message(self, secret_message: str, public_key_receiver=None):
        secret_message_bits = self.__get_secret_message_bits(secret_message, public_key_receiver)
        secret_message_length = self.__gen_message_length_binary_string(len(secret_message_bits))
        full_secret_message = secret_message_length + secret_message_bits
        if not self.has_correct_length(full_secret_message):
            raise MessageLengthException("The message is too long for the image you selected.")
        for i in range(len(full_secret_message)):
            self.__image_data[i] = (self.__get_rgb_values(i, int(full_secret_message[i])))
        write_image(self.__image_data, self.__rgb, self.__out_file_name)

    def __get_secret_message_bits(self, secret_message: str, public_key_receiver) -> str:
        if public_key_receiver:
            return self.bytes_to_binary(encrypt_message(secret_message.encode(), public_key_receiver))
        else:
            return self.string_to_binary(secret_message)

    def __gen_message_length_binary_string(self, message_len: int) -> str:
        return self.string_to_binary(str(message_len)) + self.seperator_binary

    def __get_rgb_values(self, i: int, flip_bit: int) -> tuple:
        return self.__image_data[i][0] ^ flip_bit, \
               self.__image_data[i][1], \
               self.__image_data[i][2]

    def has_correct_length(self, secret_message) -> bool:
        return len(self.__image_data) >= len(secret_message)
