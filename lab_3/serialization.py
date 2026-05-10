import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key

def load_json(path):
    """
    Чтение настроек из json файла
    """
    with open(path, 'r', encoding='utf-8') as fp:
        return json.load(fp)

def save_asym_keys(private_key, public_key, private_path, public_path):
    """
    Сохранение пары RSA ключей в PEM формате
    """
    with open(public_path, 'wb') as public_out:
        public_out.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))
    with open(private_path, 'wb') as private_out:
        private_out.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

def load_public_key(path):
    """
    Загрузка публичного ключа RSA из файла
    """
    with open(path, 'rb') as pem_in:
        return load_pem_public_key(pem_in.read())

def load_private_key(path):
    """
    Загрузка приватного ключа из PEM файла
    """
    with open(path, 'rb') as pem_in:
        return load_pem_private_key(pem_in.read(), password=None)

def save_symmetric_key(data, path):
    """
    Сохранение симметричного ключа в файл
    """
    with open(path, 'wb') as f:
        f.write(data)

def load_encrypt_symmetric_key(path):
    """
    Чтение зашифрованного симметричного ключа
    """
    with open(path, 'rb') as f:
        return f.read()

def save_nonce(nonce, path):
    """
    Сохранение одноразового числа nonce
    """
    with open(path, 'wb') as f:
        f.write(nonce)

def load_nonce(path):
    """
    Загрузка одноразового числа nonce
    """
    with open(path, 'rb') as f:
        return f.read()

def read_text_file(path):
    """
    Чтение исходного сообщения из файла
    """
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_text_file(text, path):
    """
    Сохранение расшифрованного текста в файл
    """
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)

def write_binary_file(data, path):
    """
    Запись бинарных данных в файл
    """
    with open(path, 'wb') as f:
        f.write(data)

def read_binary_file(path):
    """
    Чтение бинарных данных из файла
    """
    with open(path, 'rb') as f:
        return f.read()