from Stegano import Stegano
from PIL import Image


class SteganoReader(Stegano):
    def __init__(self, original_image_path: str, stegano_image_path: str):
        super().__init__()
        # original image
        self.__original_rgba = Image.open(original_image_path).convert("RGBA")
        self.__original_image_data = self.__original_rgba.getdata()

        # stegano image
        self.__stegano_rgba = Image.open(stegano_image_path).convert("RGBA")
        self.__stegano_image_data = self.__stegano_rgba.getdata()
        self.__extracted_message = str()

    def getExtractedMessage(self):
        return self.__extracted_message

    def __findSeperatorPosition(self) -> int:
        seperator_begin = -1
        temp_string = ""
        i = 0
        while seperator_begin == -1:
            temp_string += str(self.__bitWasFlipped(i))
            if i % 50 == 0 and i >= self.seperator_length:
                seperator_position = temp_string.find(self.seperator_binary)
                if seperator_position != -1:
                    seperator_begin = seperator_position
            i += 1
        return seperator_begin

    def __extractSecretMessageLength(self) -> tuple:
        seperator_begin = self.__findSeperatorPosition()
        assert seperator_begin != -1
        secret_message_length = ""
        for i in range(seperator_begin):
            secret_message_length += str(self.__bitWasFlipped(i))
        return int(self.binaryToString(secret_message_length)), seperator_begin + self.seperator_length

    def extractSecretMessage(self):
        secret_message_bits = ""
        secret_message_length, seperator_end = self.__extractSecretMessageLength()
        for i in range(seperator_end, seperator_end + secret_message_length):
            secret_message_bits += str(self.__bitWasFlipped(i))
        self.__extracted_message = self.binaryToString(secret_message_bits)

    def __bitWasFlipped(self, i: int) -> int:
        return self.__original_image_data[i][0] ^ self.__stegano_image_data[i][0]
