from PIL import Image


class Stegano:
    @staticmethod
    def stringToBinary(string: str):
        return "".join([format(ord(char), "08b") for char in string])

    @staticmethod
    def binaryToString(binary: str):
        # len(binary) // 8 -> divide into blocks of size 8
        return "".join(chr(int(binary[i * 8:i * 8 + 8], 2)) for i in range(len(binary) // 8))


class SteganoWriter(Stegano):
    def __init__(self, in_file_name: str, out_file_name: str):
        image = Image.open(in_file_name)
        self.rgba = image.convert("RGBA")
        self.image_data = self.rgba.getdata()
        self.out_file_name = out_file_name
        self.secret_message_length = int()

    def placeMessageLength(self):
        pass

    def placeSecretMessage(self, secret_message: str):
        secret_message_bits = self.stringToBinary(secret_message)
        self.secret_message_length = len(secret_message_bits)
        new_image_data = []
        for i, bit in enumerate(self.image_data):
            try:
                r, g, b, a = self.__getRGBAValues(i, bool(int(secret_message_bits[i])))
            except IndexError:
                r, g, b, a = self.__getRGBAValues(i, False)
            new_image_data.append((r, g, b, a))
        self.__writeDataToFile(new_image_data)

    # TODO: Implementieren
    def __genMessageLengthBinaryString(self, message_len: int) -> str:
        message_len_binary = str(message_len)
        seperator = self.stringToBinary("!#!SepSepSep!#!")
        return message_len_binary + seperator

    def __getRGBAValues(self, i: int, flip_bit: bool) -> tuple:
        return self.image_data[i][0] ^ (1 * flip_bit), \
               self.image_data[i][1], \
               self.image_data[i][2], \
               self.image_data[i][3]

    def __writeDataToFile(self, new_image_data):
        self.rgba.putdata(new_image_data)
        self.rgba.save(self.out_file_name)

    def getSecretMessageLength(self) -> int:
        return self.secret_message_length


class SteganoReader(Stegano):
    def __init__(self, original_image_path: str, stegano_image_path: str, secret_message_length: int):
        # original image
        original_image = Image.open(original_image_path)
        self.original_rgba = original_image.convert("RGBA")
        self.original_image_data = self.original_rgba.getdata()

        # stegano image
        stegano_image = Image.open(stegano_image_path)
        self.stegano_rgba = stegano_image.convert("RGBA")
        self.stegano_image_data = self.stegano_rgba.getdata()
        self.secret_message_length = secret_message_length
        self.extracted_message = str()

    def extractSecretMessage(self):
        secret_message_bits = ""
        for i in range(self.secret_message_length):
            if self.bitWasFlipped(i):
                secret_message_bits += "1"
            else:
                secret_message_bits += "0"
        self.extracted_message = self.__reformatSecretMessageBits(secret_message_bits)

    def __reformatSecretMessageBits(self, secret_message_bits: str) -> str:
        temp = self.binaryToString(secret_message_bits)
        return temp

    def bitWasFlipped(self, i: int) -> bool:
        orig = self.original_image_data[i][0]
        steg = self.stegano_image_data[i][0]
        toReturn = bool(self.original_image_data[i][0] ^ self.stegano_image_data[i][0])
        return toReturn
