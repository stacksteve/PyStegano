from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

byte_seperator = bytes([35, 35, 35, 35, 35, 35])


def generateKeyPair(key_name: str) -> None:
    private_key = RSA.generate(8192)
    public_key = private_key.public_key()
    open(f"{key_name}_private.pem", "wb").write(private_key.export_key(format="PEM"))
    open(f"{key_name}_public.pem", "wb").write(public_key.export_key(format="PEM"))


def importAsymmetricKey(key_path: str) -> RSA:
    return RSA.import_key(open(key_path, "rb").read())


def encryptKey(public_key_receiver: RSA, key: bytes) -> bytes:
    cipher = PKCS1_OAEP.new(public_key_receiver)
    return cipher.encrypt(key)


def decryptKey(private_key_receiver: RSA, encrypted_key: bytes) -> bytes:
    cipher = PKCS1_OAEP.new(private_key_receiver)
    return cipher.decrypt(encrypted_key)


def getNewSymmetricEncryptionKey() -> bytes:
    return get_random_bytes(32)


def encryptMessage(message: bytes, public_key_receiver: RSA) -> bytes:
    key = getNewSymmetricEncryptionKey()
    cipher = AES.new(key, AES.MODE_CFB)
    ciphertext_bytes = cipher.encrypt(message)
    return ciphertext_bytes + byte_seperator + cipher.iv + byte_seperator + encryptKey(public_key_receiver, key)


def decryptMessage(encryption_bytes: bytes, private_key_receiver: RSA) -> str:
    ciphertext_bytes, iv, encrypted_key = encryption_bytes.split(byte_seperator)
    cipher = AES.new(decryptKey(private_key_receiver, encrypted_key), AES.MODE_CFB, iv)
    return cipher.decrypt(ciphertext_bytes).decode()
