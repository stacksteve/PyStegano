from src.libStegano.Stegano import Stegano
from src.libSecurity.Encryption import decryptMessage
from src.utils.PicReader import readImageRgb


class SteganoReader(Stegano):
    def __init__(self, original_image_path: str, stegano_image_path: str):
        super().__init__()
        self.__original_image_data = readImageRgb(original_image_path)
        self.__stegano_image_data = readImageRgb(stegano_image_path)
        self.__extracted_message = str()

    def getExtractedMessage(self) -> str:
        return self.__extracted_message

    def __setExtractedMessage(self, secret_message: str, private_key_receiver) -> None:
        if private_key_receiver:
            self.__extracted_message = decryptMessage(self.binaryToBytes(secret_message), private_key_receiver)
        else:
            self.__extracted_message = self.binaryToString(secret_message)

    def __extractSecretMessageLength(self) -> tuple:
        secret_message_length = ""
        for i in range(len(self.__stegano_image_data)):
            secret_message_length += self.__extractBitAt(i)
            if i >= self.seperator_length:
                seperator_begin = secret_message_length.find(self.seperator_binary)
                if seperator_begin != -1:
                    return int(self.binaryToString(secret_message_length[:seperator_begin])), \
                           seperator_begin + self.seperator_length

    def extractSecretMessage(self, private_key_receiver=None) -> None:
        secret_message_length, seperator_end = self.__extractSecretMessageLength()
        secret_message_end = seperator_end + secret_message_length
        secret_message = "".join([self.__extractBitAt(i) for i in range(seperator_end, secret_message_end)])
        self.__setExtractedMessage(secret_message, private_key_receiver)

    def __extractBitAt(self, i: int) -> str:
        return str(self.__original_image_data[i][0] ^ self.__stegano_image_data[i][0])
