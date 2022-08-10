from Stegano import Stegano
from PIL import Image


class SteganoWriter(Stegano):
    def __init__(self, in_file_name: str, out_file_name: str):
        super().__init__()
        self.__rgba = Image.open(in_file_name).convert("RGBA")
        self.__image_data = self.__rgba.getdata()
        self.__out_file_name = out_file_name

    def placeSecretMessage(self, secret_message: str):
        secret_message_bits = self.stringToBinary(secret_message)
        secret_message_length = self.__genMessageLengthBinaryString(len(secret_message_bits))
        full_secret_message = secret_message_length + secret_message_bits
        new_image_data = []
        for i in range(len(self.__image_data)):
            new_image_data.append(self.__getRgbaValues(i, i < len(full_secret_message) and int(full_secret_message[i])))
        self.__writeDataToFile(new_image_data)

    def __genMessageLengthBinaryString(self, message_len: int) -> str:
        message_len_binary = self.stringToBinary(str(message_len))
        return message_len_binary + self.seperator_binary

    def __getRgbaValues(self, i: int, flip_bit: bool) -> tuple:
        return self.__image_data[i][0] ^ (1 and flip_bit), \
               self.__image_data[i][1], \
               self.__image_data[i][2], \
               self.__image_data[i][3]

    def __writeDataToFile(self, new_image_data):
        self.__rgba.putdata(new_image_data)
        self.__rgba.save(self.__out_file_name)
