from libStegano import Stegano
from libStegano import SteganoReader
from libStegano import SteganoWriter
from libSecurity import import_rsa_key
from libSocket import transmit_data
from libSocket import receive_data


def main():
    # Place message (Client)
    stegano_writing_machine = SteganoWriter("desktop.png", "desktop_secret.png")
    secret_message = str(input("Secret message: "))
    public_key = import_rsa_key("test_public.pem")
    stegano_writing_machine.place_secret_message(secret_message, public_key)
    # image_data = open("desktop_secret.png", "rb").read()
    # transmit_data(image_data, "192.168.178.28", 1337)

    # Extract message (Server)
    # port = 1337
    # image_data = receive_data(port)
    # open("desktop_secret.png", "wb").write(image_data)

    stegano_reading_machine = SteganoReader("desktop.png", "desktop_secret.png")
    private_key = import_rsa_key("test_private.pem")
    stegano_reading_machine.extract_secret_message(private_key)
    print("Extracted message:", stegano_reading_machine.get_extracted_message())


if __name__ == "__main__":
    main()
