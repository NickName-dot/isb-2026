import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms

def generating_symmetric_key(size_bytes):
    """
    Генерация случайного симметричного ключа заданного размера
    """
    return os.urandom(size_bytes)

def generating_nonce():
    """
    Генерация случайного одноразового числа nonce (16 байт)
    """
    return os.urandom(16)

def encrypt_text(text, key, nonce):
    """
    Шифрование текста алгоритмом ChaCha20
    """
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None)
    encryptor = cipher.encryptor()
    return encryptor.update(text.encode('utf-8')) + encryptor.finalize()

def decrypt_text(cipher_text, key, nonce):
    """
    Дешифрование текста алгоритмом ChaCha20
    """
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None)
    decryptor = cipher.decryptor()
    return (decryptor.update(cipher_text) + decryptor.finalize()).decode('utf-8')