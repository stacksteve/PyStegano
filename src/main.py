from Stegano import SteganoWriter, SteganoReader, Stegano


def main():
    steg = SteganoWriter("steg.png", "stegged.png")
    steg.placeSecretMessage("Hallo Welt")
    stegged = SteganoReader("steg.png", "stegged.png")
    stegged.extractSecretMessage()
    print(stegged.extracted_message)


if __name__ == "__main__":
    main()
