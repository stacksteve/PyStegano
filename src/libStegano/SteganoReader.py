from src.libStegano.Stegano import Stegano
from src.libSecurity.Encryption import decryptMessage
from src.utils.PicReader import readImageData


class SteganoReader(Stegano):
    def __init__(self, original_image_path: str, stegano_image_path: str):
        super().__init__()
        self.__original_image_data = readImageData(original_image_path)[1]  # we only need the color data
        self.__stegano_rgb, self.__stegano_image_data = readImageData(stegano_image_path)
        self.__extracted_message = str()

    def getExtractedMessage(self) -> str:
        return self.__extracted_message

    def __setExtractedMessage(self, secret_message: str, private_key_receiver) -> None:
        if private_key_receiver:
            self.__extracted_message = decryptMessage(self.binaryToBytes(secret_message), private_key_receiver)
        else:
            self.__extracted_message = self.binaryToString(secret_message)

    def __findSeperatorPosition(self) -> int:
        temp_string = ""
        i = 0
        while True:
            temp_string += self.__extractBitAt(i)
            if i >= self.seperator_length and i % 136 == 0:  # Reason for % 136 see performanceTest.py
                seperator_position = temp_string.find(self.seperator_binary)
                if seperator_position != -1:
                    return seperator_position
            i += 1

    def __extractSecretMessageLength(self) -> tuple:
        seperator_begin = self.__findSeperatorPosition()
        assert seperator_begin != -1
        secret_message_length = ""
        for i in range(seperator_begin):
            secret_message_length += self.__extractBitAt(i)
        return int(self.binaryToString(secret_message_length)), seperator_begin + self.seperator_length

    def extractSecretMessage(self, private_key_receiver=None) -> None:
        secret_message_length, seperator_end = self.__extractSecretMessageLength()
        secret_message_end = seperator_end + secret_message_length
        secret_message = "".join([self.__extractBitAt(i) for i in range(seperator_end, secret_message_end)])
        self.__setExtractedMessage(secret_message, private_key_receiver)

    def __extractBitAt(self, i: int) -> str:
        return str(self.__original_image_data[i][0] ^ self.__stegano_image_data[i][0])
