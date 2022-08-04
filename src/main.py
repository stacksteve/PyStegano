from Stegano import SteganoWriter, SteganoReader, Stegano


def main():
    # Place message
    steg = SteganoWriter("desktop.png", "desktop_secret.png")
    secret_message = str(input("Secret message: "))
    steg.placeSecretMessage(secret_message)

    # Extract message
    stegged = SteganoReader("desktop.png", "desktop_secret.png")
    stegged.extractSecretMessage()
    print("Extracted message:", stegged.extracted_message)


if __name__ == "__main__":
    main()
