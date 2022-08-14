from src.libStegano.Stegano import Stegano
from src.libSecurity.Encryption import encryptMessage
from src.utils.PicReader import readImage, writeImage
from src.libExceptions.MessageLengthException import MessageLengthException


class SteganoWriter(Stegano):
    def __init__(self, in_file_name: str, out_file_name: str):
        super().__init__()
        self.__rgb, self.__image_data = readImage(in_file_name)
        self.__out_file_name = out_file_name

    def placeSecretMessage(self, secret_message: str, public_key_receiver=None):
        secret_message_bits = self.__getSecretMessageBits(secret_message, public_key_receiver)
        secret_message_length = self.__genMessageLengthBinaryString(len(secret_message_bits))
        full_secret_message = secret_message_length + secret_message_bits
        if not self.hasCorrectLength(full_secret_message):
            raise MessageLengthException("The message is too long for the image you selected.")
        new_image_data = []
        for i in range(len(self.__image_data)):
            new_image_data.append(self.__getRgbaValues(i, i < len(full_secret_message) and int(full_secret_message[i])))
        writeImage(new_image_data, self.__rgb, self.__out_file_name)

    def __getSecretMessageBits(self, secret_message: str, public_key_receiver):
        if public_key_receiver:
            return self.bytesToBinary(encryptMessage(secret_message, public_key_receiver))
        else:
            return self.stringToBinary(secret_message)

    def __genMessageLengthBinaryString(self, message_len: int) -> str:
        secret_message_len_binary = self.stringToBinary(str(message_len))
        return secret_message_len_binary + self.seperator_binary

    def __getRgbaValues(self, i: int, flip_bit: bool) -> tuple:
        return self.__image_data[i][0] ^ (1 and flip_bit), \
               self.__image_data[i][1], \
               self.__image_data[i][2]

    def hasCorrectLength(self, secret_message) -> bool:
        maximum_bits = len(self.__image_data)
        message_length = len(secret_message)
        return maximum_bits >= message_length
