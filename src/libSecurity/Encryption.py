import json
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes


def getKey(key: str):
    hashing = SHA256.new(key.encode())
    return hashing.digest()


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


def intToBinary(integer: int) -> str:
    digits = []
    while integer > 0:
        digits.insert(0, integer % 10)
        integer //= 10
    return "".join(format(digit + 48, "08b") for digit in digits)  # 48 to get char-value of '5'
