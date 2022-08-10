import json
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
# from Crypto.Random import get_random_bytes -> for later use with ECC encryption


def getKey(key: str):
    hashing = SHA256.new(key.encode())
    return hashing.digest()


def generateKeyPair(key_name: str):
    private_key = ECC.generate(curve="ed25519")
    public_key = private_key.public_key()
    open(f"{key_name}_private.pem", "w").write(private_key.export_key(format="PEM"))
    open(f"{key_name}_public.pem", "w").write(public_key.export_key(format="PEM"))


def encryptMessage(message: str, key: str):
    cipher = AES.new(getKey(key), AES.MODE_CFB)
    ciphertext_bytes = cipher.encrypt(message.encode())
    initialization_vector = b64encode(cipher.iv).decode()
    ciphertext = b64encode(ciphertext_bytes).decode()
    return json.dumps({"iv": initialization_vector, "ct": ciphertext})


def decryptMessage(key: str, ciphertext: str, iv: str):
    iv = b64decode(iv)
    ciphertext_bytes = b64decode(ciphertext)
    cipher = AES.new(getKey(key), AES.MODE_CFB, iv)
    return cipher.decrypt(ciphertext_bytes).decode()
