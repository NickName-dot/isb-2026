from constants import FILE_PATHS_SUBSTITUTION, ENCODING_UTF8

def read_file(file_path: str) -> str:
    """Читает содержимое файла с обработкой ошибок."""
    try:
        with open(file_path, encoding=ENCODING_UTF8) as file:
            print(f"Файл {file_path} загружен")
            return file.read()
    except FileNotFoundError:
        print(f"Файл {file_path} не найден")
        return ""

def write_file(file_path: str, content: str) -> None:
    with open(file_path, "w", encoding=ENCODING_UTF8) as f:
        f.write(content)
    print(f"Сохранено: {file_path}")

def statistic(text: str) -> dict:
    char_set = set(text)
    counts = {char: 0 for char in char_set}
    for char in text:
        counts[char] += 1
    frequencies = {char: count / len(text) for char, count in counts.items()}
    return dict(sorted(frequencies.items(), key=lambda item: item[1], reverse=True))

def write_statistics(text: str, stats_path: str) -> None:
    stats = statistic(text)
    with open(stats_path, "w", encoding=ENCODING_UTF8) as f:
        for char, freq in stats.items():
            f.write(f"{char}\t{freq}\n")
    print(f"Статистика записана: {stats_path}")

def str_to_dict(key_str: str) -> dict:
    key_dict = {}
    for line_num, line in enumerate(key_str.strip().split('\n'), 1):
        line = line.rstrip()
        if '\t' in line:
            parts = line.split('\t')
            if len(parts) == 2:
                original = parts[0].rstrip()
                replacement = parts[1].rstrip()
                if not replacement.strip():
                    replacement = ' '  
                elif replacement.strip() == 'ы':
                    replacement = 'ы'
                
                key_dict[original] = replacement
    return key_dict



def decode(text: str, key: dict) -> str:
    if ' ' in text:
        text = text.replace(' ', 'ы')
    if 'М' in text:
        text = text.replace('М', ' ')
    for i, j in key.items():
        text = text.replace(i, j)
    
    return text




def main() -> None:
    cipher_text = read_file(FILE_PATHS_SUBSTITUTION['cipher_text'])
    if not cipher_text:
        return
    
    write_statistics(cipher_text, FILE_PATHS_SUBSTITUTION['etalon_freq'])
    
    key_text = read_file(FILE_PATHS_SUBSTITUTION['key'])
    if not key_text:
        print("Создайте key.txt по частотам из stats.txt!")
        return
    
    key_dict = str_to_dict(key_text)
    decrypted = decode(cipher_text, key_dict)
    
    write_file(FILE_PATHS_SUBSTITUTION['decoded'], decrypted)
    print(f"\nРАСШИФРОВКА СОХРАНЕНА: {FILE_PATHS_SUBSTITUTION['decoded']}")

if __name__ == "__main__":
    main()
