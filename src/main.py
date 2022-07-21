from Stegano import SteganoWriter, SteganoReader, Stegano


def main():
    # steg = SteganoWriter("steg.png", "stegged.png")
    # steg.placeSecretMessage("Hallo")
    # stegged = SteganoReader("steg.png", "stegged.png", steg.getSecretMessageLength())
    # stegged.extractSecretMessage()
    # print(stegged.extracted_message)
    encoded = Stegano().stringToBinary("!#!SepSepSep!#!")
    print(Stegano().binaryToString(encoded))


if __name__ == "__main__":
    main()
