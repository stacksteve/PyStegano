from src.libStegano.Stegano import Stegano
from src.libSecurity.Encryption import decrypt_message
from src.utils.PicReader import read_image_rgb


class SteganoReader(Stegano):
    def __init__(self, original_image_path: str, stegano_image_path: str):
        self.__original_image_data = read_image_rgb(original_image_path)
        self.__stegano_image_data = read_image_rgb(stegano_image_path)
        self.__extracted_message = str()

    def get_extracted_message(self) -> str:
        return self.__extracted_message

    def __set_extracted_message(self, secret_message: str, private_key_receiver) -> None:
        if private_key_receiver:
            self.__extracted_message = decrypt_message(self.binary_to_bytes(secret_message), private_key_receiver)
        else:
            self.__extracted_message = self.binary_to_string(secret_message)

    def __extract_secret_message_length(self) -> tuple:
        secret_message_length = ""
        for i in range(len(self.__stegano_image_data)):
            secret_message_length += self.__extract_bit_at(i)
            if i >= self.seperator_length:
                seperator_begin = secret_message_length.find(self.seperator_binary)
                if seperator_begin != -1:
                    return int(self.binary_to_string(secret_message_length[:seperator_begin])), \
                           seperator_begin + self.seperator_length

    def extract_secret_message(self, private_key_receiver=None) -> None:
        secret_message_length, seperator_end = self.__extract_secret_message_length()
        secret_message_end = seperator_end + secret_message_length
        secret_message = "".join([self.__extract_bit_at(i) for i in range(seperator_end, secret_message_end)])
        self.__set_extracted_message(secret_message, private_key_receiver)

    def __extract_bit_at(self, i: int) -> str:
        return str(self.__original_image_data[i][0] ^ self.__stegano_image_data[i][0])
