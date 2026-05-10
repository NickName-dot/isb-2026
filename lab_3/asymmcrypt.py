from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

def encrypt_symmetric_key(sym_key, public_key):
    """
    Зашифрование симметричного ключа
    получает:
        sym_key: Ключ симметричного алгоритма
        public_key: Публичный ключ RSA
    выдаёт:
        Зашифрованный ключ симметричного шифра
    """
    return public_key.encrypt(
        sym_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def decrypt_key(sym_key_encrypted, private_key):
    """
    Расшифрование симметричного ключа
    получает:
        sym_key_encrypted: Зашифрованный ключ симметричного алгоритма
        private_key: Приватный ключ RSA
    выдаёт:
        Исходный симметричный ключ
    """
    return private_key.decrypt(
        sym_key_encrypted,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )