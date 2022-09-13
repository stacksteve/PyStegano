from libStegano.Stegano import Stegano
from libStegano.SteganoReader import SteganoReader
from libStegano.SteganoWriter import SteganoWriter
from libSecurity.Encryption import import_rsa_key


def main():
    # Place message
    stegano_writing_machine = SteganoWriter("desktop.png", "desktop_secret.png")
    secret_message = str(input("Secret message: "))
    public_key = import_rsa_key("test_public.pem")
    stegano_writing_machine.place_secret_message(secret_message, public_key)

    # Extract message
    stegano_reading_machine = SteganoReader("desktop.png", "desktop_secret.png")
    private_key = import_rsa_key("test_private.pem")
    stegano_reading_machine.extract_secret_message(private_key)
    print("Extracted message:", stegano_reading_machine.get_extracted_message())


if __name__ == "__main__":
    main()
