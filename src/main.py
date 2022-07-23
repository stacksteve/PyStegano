from Stegano import SteganoWriter, SteganoReader


def main():
    # Place message
    steg = SteganoWriter("steg.png", "stegged.png")
    secret_message = str(input("Secret message: "))
    steg.placeSecretMessage(secret_message)

    # Extract message
    stegged = SteganoReader("steg.png", "stegged.png")
    stegged.extractSecretMessage()
    print("Extracted message:", stegged.extracted_message)


if __name__ == "__main__":
    main()
