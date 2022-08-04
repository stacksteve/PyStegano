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
