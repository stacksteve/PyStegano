# from Stegano import Stegano
from SteganoWriter import SteganoWriter
from SteganoReader import SteganoReader


def main():
    # Place message
    stegano_writing_machine = SteganoWriter("desktop.png", "desktop_secret.png")
    secret_message = str(input("Secret message: "))
    stegano_writing_machine.placeSecretMessage(secret_message)

    # Extract message
    stegano_reading_machine = SteganoReader("desktop.png", "desktop_secret.png")
    stegano_reading_machine.extractSecretMessage()
    print("Extracted message:", stegano_reading_machine.getExtractedMessage())


if __name__ == "__main__":
    main()
