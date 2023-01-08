from libStegano.Stegano import Stegano
from libSecurity import decrypt_message
from utils import read_image_rgb


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

    def extract_secret_message(self, private_key_receiver=None, public_key_sender=None) -> None:
        """
        Steps to extract the secret message:
            1. As long as the end flag is not found read keep reading new bits
            1.1 Read the minimum amount of bits that could contain the end flag
            1.2 Find the begin of the end flag
            2. All bits before the end flag are the secret message
            3. Convert string/encrypted bytes to plaintext (__set_extracted_message does that)

        :param public_key_sender: Sender's public signing the sender
        :param private_key_receiver: RSA private key to decrypt the symmetric key
        :return: Method does not return anything
        """
        secret_message_bin = ''
        secret_message = ''
        for px in range(len(self.__stegano_image_data)):
            secret_message_bin += self.__check_bit_flip_at(px)
            if px >= self.END_FLAG_LEN:
                end_flag_begin = secret_message_bin.find(self.END_FLAG_BIN)
                if end_flag_begin != -1:
                    secret_message = secret_message_bin[:end_flag_begin]
        self.__set_extracted_message(secret_message, private_key_receiver, public_key_sender)

    def __set_extracted_message(self, secret_message: str, private_key_receiver, public_key_sender) -> None:
        """
        Setter method for the extracted message. Depending on whether the message was encrypted
        the program decrypts the string before conversion to plaintext.

        :param secret_message: String that contains the secret message in plaintext
        :param private_key_receiver: RSA private key_path to decrypt the symmetric key_path
        :return: Method does not return anything
        """
        if private_key_receiver and public_key_sender:
            self.__extracted_message = decrypt_message(self.binary_to_bytes(secret_message), private_key_receiver,
                                                       public_key_sender)
        else:
            self.__extracted_message = self.binary_to_bytes(secret_message).decode('utf-8')

    def get_extracted_message(self) -> str:
        """
        Getter method for the extracted message.

        :return: Extracted secret message
        """
        return self.__extracted_message

    def __check_bit_flip_at(self, i: int) -> str:
        """
        Extracts a bit from the secret message at the respective pixel position.

        :param i: Pixel position
        :return: "0" or "1"
        """
        return str(self.__original_image_data[i][0] ^ self.__stegano_image_data[i][0])
