from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

byte_seperator = bytes([42, 42, 42, 42, 42, 42])


def generate_rsa_key_pair(key_name: str) -> None:
    private_key = RSA.generate(8192)
    public_key = private_key.public_key()
    open(f"{key_name}_private.pem", "wb").write(private_key.export_key(format="PEM"))
    open(f"{key_name}_public.pem", "wb").write(public_key.export_key(format="PEM"))


def import_rsa_key(key_path: str) -> RSA:
    return RSA.import_key(open(key_path, "rb").read())


def encrypt_symmetric_key(public_key_receiver: RSA, key: bytes) -> bytes:
    cipher = PKCS1_OAEP.new(public_key_receiver)
    return cipher.encrypt(key)


def decrypt_symmetric_key(private_key_receiver: RSA, encrypted_key: bytes) -> bytes:
    cipher = PKCS1_OAEP.new(private_key_receiver)
    return cipher.decrypt(encrypted_key)


def encrypt_message(message: bytes, public_key_receiver: RSA) -> bytes:
    key = get_random_bytes(32)
    cipher = AES.new(key, AES.MODE_CFB)
    ciphertext_bytes = cipher.encrypt(message)
    return ciphertext_bytes + byte_seperator + cipher.iv + byte_seperator + encrypt_symmetric_key(public_key_receiver,
                                                                                                  key)


def decrypt_message(encryption_bytes: bytes, private_key_receiver: RSA) -> str:
    ciphertext_bytes, iv, encrypted_key = encryption_bytes.split(byte_seperator)
    cipher = AES.new(decrypt_symmetric_key(private_key_receiver, encrypted_key), AES.MODE_CFB, iv)
    return cipher.decrypt(ciphertext_bytes).decode()
