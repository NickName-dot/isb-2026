from pathlib import Path

# Русский алфавит (33 буквы)
RUSSIAN_UPPERCASE = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
RUSSIAN_LOWERCASE = RUSSIAN_UPPERCASE.lower()
RUSSIAN_ALPHABET_SIZE = 33

# Пути к файлам
FILE_PATHS = {
    'original': Path('original.txt'),
    'encrypted': Path('encrypted.txt'),
    'decrypted': Path('decrypted.txt')
}

# Параметры шифрования
CAESAR_SHIFT_DEFAULT = 5
ENCODING_UTF8 = 'utf-8'
