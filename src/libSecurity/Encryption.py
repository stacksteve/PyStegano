from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA, ECC
from Crypto.Random import get_random_bytes
from Crypto.Signature import eddsa
from Crypto.Hash import SHA3_512

BYTE_SEP = bytes([42, 42, 42, 42, 42, 42])
DEFAULT_RSA_KEY_SIZE = 8192


def generate_rsa_key_pair(key_name: str) -> None:
    private_key = RSA.generate(DEFAULT_RSA_KEY_SIZE)
    public_key = private_key.public_key()
    open(f'{key_name}_private.pem', 'wb').write(private_key.export_key(format='PEM'))
    open(f'{key_name}_public.pem', 'wb').write(public_key.export_key(format='PEM'))


def generate_signing_key_pair(key_name: str) -> None:
    private_key = ECC.generate(curve='Ed25519')
    public_key = private_key.public_key()
    open(f'{key_name}_private_signer.pem', 'w').write(private_key.export_key(format='PEM'))
    open(f'{key_name}_public_signer.pem', 'w').write(public_key.export_key(format='PEM'))


def import_rsa_key(key_path: str) -> RSA:
    return RSA.import_key(open(key_path, 'rb').read())


def import_edd_key(key_path: str) -> ECC:
    return ECC.import_key(open(key_path, 'r').read())


def encrypt_symmetric_key(public_key_receiver: RSA, key: bytes) -> bytes:
    cipher = PKCS1_OAEP.new(public_key_receiver)
    return cipher.encrypt(key)


def decrypt_symmetric_key(private_key_receiver: RSA, encrypted_key: bytes) -> bytes:
    cipher = PKCS1_OAEP.new(private_key_receiver)
    return cipher.decrypt(encrypted_key)


def sign_message(private_key_sender: ECC, message: bytes) -> bytes:
    signer = eddsa.new(private_key_sender, mode='rfc8032')
    message_hash = SHA3_512.new()
    message_hash.update(message)
    return signer.sign(message_hash.digest())


def verify_signature(public_key_sender: ECC, message: bytes, signature: bytes) -> bool:
    verifier = eddsa.new(public_key_sender, mode='rfc8032')
    message_hash = SHA3_512.new()
    message_hash.update(message)
    try:
        verifier.verify(message_hash.digest(), signature)
    except ValueError:
        return False
    return True


def encrypt_message(message: bytes, public_key_receiver: RSA, private_key_sender: ECC) -> bytes:
    key = get_random_bytes(32)
    cipher = AES.new(key, AES.MODE_CFB)
    ciphertext = cipher.encrypt(message)
    key_encrypted = encrypt_symmetric_key(public_key_receiver, key)
    signature = sign_message(private_key_sender, message)
    return ciphertext + BYTE_SEP + cipher.iv + BYTE_SEP + key_encrypted + BYTE_SEP + signature


def decrypt_message(encryption_bytes: bytes, private_key_receiver: RSA, public_key_sender: ECC) -> str:
    ciphertext_bytes, iv, encrypted_key, signature = encryption_bytes.split(BYTE_SEP)
    cipher = AES.new(decrypt_symmetric_key(private_key_receiver, encrypted_key), AES.MODE_CFB, iv)
    decrypted_message = cipher.decrypt(ciphertext_bytes)
    if verify_signature(public_key_sender, decrypted_message, signature):
        return decrypted_message.decode('utf-8')
    else:
        raise Exception('Signature verification failed. The message you received could be corrupted.')
