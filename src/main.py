# from Stegano import Stegano
from src.libStegano.SteganoWriter import SteganoWriter
from src.libStegano.SteganoReader import SteganoReader
from src.libSecurity.Encryption import importAsymmetricKey


def main():
    # Place message
    stegano_writing_machine = SteganoWriter("testImages/test.png", "testImages/test_secret.png")
    secret_message = str(input("Secret message: "))
    public_key = importAsymmetricKey("test_public.pem")
    stegano_writing_machine.placeSecretMessage(secret_message, public_key)

    # Extract message
    stegano_reading_machine = SteganoReader("testImages/test.png", "testImages/test_secret.png")
    private_key = importAsymmetricKey("test_private.pem")
    stegano_reading_machine.extractSecretMessage(private_key)
    print("Extracted message:", stegano_reading_machine.getExtractedMessage())


if __name__ == "__main__":
    main()
