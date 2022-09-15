from src.libStegano.Stegano import Stegano
from src.libSecurity.Encryption import decrypt_message
from src.utils.PicReader import read_image_rgb


class SteganoReader(Stegano):
    def __init__(self, original_image_path: str, stegano_image_path: str):
        """
        Read image data and store filename for later use in extract_secret_message.

        :param original_image_path: Image that was used to perform steganography
        :param stegano_image_path: Image that contains the secret message
        """
        self.__original_image_data = read_image_rgb(original_image_path)
        self.__stegano_image_data = read_image_rgb(stegano_image_path)
        self.__extracted_message = str()

    def extract_secret_message(self, private_key_receiver=None) -> None:
        """
        Steps to extract the secret message:
            1. Find message position
            2. Read the secret message bits
            3. Convert string to plaintext (__set_extracted_message does that)

        :param private_key_receiver: RSA private key to decrypt the symmetric key
        :return: Method does not return anything
        """
        secret_message_begin, secret_message_length = self.__extract_secret_message_length()
        secret_message_end = secret_message_begin + secret_message_length
        secret_message = "".join([self.__extract_bit_at(i) for i in range(secret_message_begin, secret_message_end)])
        self.__set_extracted_message(secret_message, private_key_receiver)

    def __extract_secret_message_length(self) -> tuple:
        """
        Steps to extract the message length:
            1. Read the minimum amount of bits that could contain the seperator
            2. As long as the seperator is not found read the next bit and search again

        :return: Tuple contains:
                    - Pixel position where the secret message begins    (Integer)
                    - Length of the secret message bitstream            (Integer)
        """
        secret_message_length = ""
        for i in range(len(self.__stegano_image_data)):
            secret_message_length += self.__extract_bit_at(i)
            if i >= self.seperator_length:
                seperator_begin = secret_message_length.find(self.seperator_binary)
                if seperator_begin != -1:
                    return seperator_begin + self.seperator_length, \
                           int(self.binary_to_string(secret_message_length[:seperator_begin]))

    def __set_extracted_message(self, secret_message: str, private_key_receiver) -> None:
        """
        Setter method for the extracted message. Depending on whether the message was encrypted
        the program decrypts the string before conversion to plaintext.

        :param secret_message: String that contains the secret message in plaintext
        :param private_key_receiver: RSA private key to decrypt the symmetric key
        :return: Method does not return anything
        """
        if private_key_receiver:
            self.__extracted_message = decrypt_message(self.binary_to_bytes(secret_message), private_key_receiver)
        else:
            self.__extracted_message = self.binary_to_string(secret_message)

    def get_extracted_message(self) -> str:
        """
        Getter method for the extracted message.

        :return: Extracted secret message
        """
        return self.__extracted_message

    def __extract_bit_at(self, i: int) -> str:
        """
        Extracts a bit from the secret message at the respective pixel position.

        :param i: Pixel position
        :return: "0" or "1"
        """
        return str(self.__original_image_data[i][0] ^ self.__stegano_image_data[i][0])
