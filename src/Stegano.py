from PIL import Image


class Stegano:
    def __init__(self):
        self.seperator = "!#!SepSepSep!#!"
        self.seperator_binary = self.stringToBinary(self.seperator)
        self.seperator_length = len(self.seperator_binary)

    @staticmethod
    def stringToBinary(string: str) -> str:
        return "".join([format(ord(char), "08b") for char in string])

    @staticmethod
    def binaryToString(binary: str) -> str:
        # Evaluate bit string bytewise
        return "".join(chr(int(binary[i * 8:i * 8 + 8], 2)) for i in range(len(binary) // 8))


class SteganoWriter(Stegano):
    def __init__(self, in_file_name: str, out_file_name: str):
        super().__init__()
        self.rgba = Image.open(in_file_name).convert("RGBA")
        self.image_data = self.rgba.getdata()
        self.out_file_name = out_file_name

    def placeSecretMessage(self, secret_message: str):
        secret_message_bits = self.stringToBinary(secret_message)
        secret_message_bits_length = self.__genMessageLengthBinaryString(len(secret_message_bits))
        new_image_data = []
        for i, bit in enumerate(self.image_data):
            if i < len(secret_message_bits_length):
                r, g, b, a = self.__getRGBAValues(i, bool(int(secret_message_bits_length[i])))
            else:
                try:
                    r, g, b, a = self.__getRGBAValues(i, bool(
                        int(secret_message_bits[i - len(secret_message_bits_length)])))  # start with Position 0
                except IndexError:
                    r, g, b, a = self.__getRGBAValues(i, False)
            new_image_data.append((r, g, b, a))
        self.__writeDataToFile(new_image_data)

    def __genMessageLengthBinaryString(self, message_len: int) -> str:
        message_len_binary = self.stringToBinary(str(message_len))
        return message_len_binary + self.seperator_binary

    def __getRGBAValues(self, i: int, flip_bit: bool) -> tuple:
        return self.image_data[i][0] ^ (1 * flip_bit), \
               self.image_data[i][1], \
               self.image_data[i][2], \
               self.image_data[i][3]

    def __writeDataToFile(self, new_image_data):
        self.rgba.putdata(new_image_data)
        self.rgba.save(self.out_file_name)


class SteganoReader(Stegano):
    def __init__(self, original_image_path: str, stegano_image_path: str):
        super().__init__()
        # original image
        original_image = Image.open(original_image_path)
        self.original_rgba = original_image.convert("RGBA")
        self.original_image_data = self.original_rgba.getdata()

        # stegano image
        stegano_image = Image.open(stegano_image_path)
        self.stegano_rgba = stegano_image.convert("RGBA")
        self.stegano_image_data = self.stegano_rgba.getdata()
        self.extracted_message = str()

    def findSeperatorPosition(self) -> tuple:
        seperator_begin = -1
        temp_string = ""
        i = 0
        found_seperator = False
        while not found_seperator:
            temp_string += str(self.bitWasFlipped(i))
            if i >= self.seperator_length:
                seperator_position = temp_string.find(self.seperator_binary)
                if seperator_position != -1:
                    seperator_begin = seperator_position
                    found_seperator = True
            i += 1
        return seperator_begin, seperator_begin + self.seperator_length

    def extractSecretMessageLength(self) -> tuple:
        seperator_begin, seperator_end = self.findSeperatorPosition()
        secret_message_length = ""
        for i in range(seperator_begin):
            secret_message_length += str(self.bitWasFlipped(i))
        return int(self.binaryToString(secret_message_length)), seperator_end

    def extractSecretMessage(self):
        secret_message_bits = ""
        secret_message_length, seperator_end = self.extractSecretMessageLength()
        for i in range(seperator_end, seperator_end + secret_message_length):
            secret_message_bits += str(self.bitWasFlipped(i))
        self.extracted_message = self.binaryToString(secret_message_bits)

    def bitWasFlipped(self, i: int) -> int:
        return int(self.original_image_data[i][0] ^ self.stegano_image_data[i][0])
