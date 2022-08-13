from base64 import b64encode, b64decode
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import SHA3_256
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes


def generateKeyPair(key_name: str) -> None:
    private_key = RSA.generate(8192)
    public_key = private_key.public_key()
    open(f"{key_name}_private.pem", "wb").write(private_key.export_key(format="PEM"))
    open(f"{key_name}_public.pem", "wb").write(public_key.export_key(format="PEM"))


def importAsymmetricKey(path: str) -> RSA:
    return RSA.import_key(open(path, "rb").read())


def encryptKey(public_key_receiver: RSA, key: bytes) -> bytes:
    cipher = PKCS1_OAEP.new(public_key_receiver)
    return cipher.encrypt(key)


def decryptKey(private_key_receiver: RSA, encrypted_key: bytes) -> bytes:
    cipher = PKCS1_OAEP.new(private_key_receiver)
    return cipher.decrypt(encrypted_key)


def getNewSymmetricEncryptionKey() -> bytes:
    key = get_random_bytes(32)
    return SHA3_256.new(key).digest()


def encryptMessage(message: str, public_key_receiver: RSA) -> dict:
    key = getNewSymmetricEncryptionKey()
    cipher = AES.new(key, AES.MODE_CFB)
    ciphertext_bytes = cipher.encrypt(message.encode())
    return {
        "ct": b64encode(ciphertext_bytes),
        "iv": b64encode(cipher.iv),
        "key": encryptKey(public_key_receiver, key)
    }


def decryptMessage(ciphertext, iv, encrypted_key: bytes, private_key_receiver) -> str:
    iv = b64decode(iv)
    ciphertext_bytes = b64decode(ciphertext)
    cipher = AES.new(decryptKey(private_key_receiver, encrypted_key), AES.MODE_CFB, iv)
    return cipher.decrypt(ciphertext_bytes).decode()
