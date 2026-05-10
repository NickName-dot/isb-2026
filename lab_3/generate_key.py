import os
from cryptography.hazmat.primitives.asymmetric import rsa

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

def generating_asymmetric_key():
    """
    Генерация пары асимметричных ключей RSA (2048 бит)
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    return private_key, public_key