import string
from constants import (
    RUSSIAN_UPPERCASE,
    RUSSIAN_LOWERCASE,
    RUSSIAN_ALPHABET_SIZE,
    FILE_PATHS,
    CAESAR_SHIFT_DEFAULT,
    ENCODING_UTF8
)

def read_file(file_path) -> str:
    """Читает файл с проверкой."""
    try:
        with open(file_path, "r", encoding=ENCODING_UTF8) as f:
            print(f"Файл {file_path.name} загружен")
            return f.read()
    except FileNotFoundError:
        print(f"Файл {file_path.name} не найден")
        return ""

def write_file(file_path, text: str) -> None:
    """Записывает текст в файл."""
    file_path.write_text(text, encoding=ENCODING_UTF8)
    print(f"Сохранено в {file_path.name}")

def clean_text(text: str) -> str:
    """Убирает пунктуацию, пробелы, переводит в нижний регистр."""
    text = text.lower()
    translator = str.maketrans('', '', string.punctuation)
    text = text.translate(translator)
    return text.replace(' ', '')

def caesar_cipher(text: str, shift: int = CAESAR_SHIFT_DEFAULT, 
                  output_path = FILE_PATHS['encrypted']) -> str:
    """Шифрование Цезаря."""
    result = []
    for char in text:
        if char in RUSSIAN_UPPERCASE:
            idx = (RUSSIAN_UPPERCASE.index(char) + shift) % RUSSIAN_ALPHABET_SIZE
            result.append(RUSSIAN_UPPERCASE[idx])
        elif char in RUSSIAN_LOWERCASE:
            idx = (RUSSIAN_LOWERCASE.index(char) + shift) % RUSSIAN_ALPHABET_SIZE
            result.append(RUSSIAN_LOWERCASE[idx])
        else:
            result.append(char)
    
    encrypted_text = ''.join(result)
    write_file(output_path, encrypted_text)
    return encrypted_text

def caesar_decipher(text: str, shift: int = CAESAR_SHIFT_DEFAULT,
                    output_path = FILE_PATHS['decrypted']) -> str:
    """Дешифровка Цезаря."""
    result = []
    decrypt_shift = (-shift) % RUSSIAN_ALPHABET_SIZE
    
    for char in text:
        if char in RUSSIAN_UPPERCASE:
            idx = (RUSSIAN_UPPERCASE.index(char) + decrypt_shift) % RUSSIAN_ALPHABET_SIZE
            result.append(RUSSIAN_UPPERCASE[idx])
        elif char in RUSSIAN_LOWERCASE:
            idx = (RUSSIAN_LOWERCASE.index(char) + decrypt_shift) % RUSSIAN_ALPHABET_SIZE
            result.append(RUSSIAN_LOWERCASE[idx])
        else:
            result.append(char)
    
    decrypted_text = ''.join(result)
    write_file(output_path, decrypted_text)
    return decrypted_text

def main():
    """Полный пайплайн: очистка → шифрование → дешифровка."""
    
    # 1. Читаем оригинал
    original_text = read_file(FILE_PATHS['original'])
    if not original_text:
        return
    
    print("1. ОРИГИНАЛЬНЫЙ ТЕКСТ:")
    print(original_text)
    print("=" * 60)
    
    # 2. Очищаем
    cleaned = clean_text(original_text)
    print("2. ОЧИЩЕННЫЙ ТЕКСТ:")
    print(cleaned)
    print("=" * 60)
    
    # 3. Шифруем
    encrypted_text = caesar_cipher(cleaned)
    print("3. ЗАШИФРОВАННЫЙ ТЕКСТ:")
    print(encrypted_text)
    print("=" * 60)
    
    # 4. Дешифруем
    decrypted_text = caesar_decipher(encrypted_text)
    print("4. ДЕШИФРОВАННЫЙ ТЕКСТ:")
    print(decrypted_text)
    print("\n Текст успешно восстановлен!")

if __name__ == "__main__":
    main()
