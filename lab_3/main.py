import argparse
import generate_key
import asymmcrypt
import symmcrypt
import serialization


def parse_cli():
    """
    Разбор аргументов командной строки
    """
    parser = argparse.ArgumentParser(description="Гибридная криптосистема на основе RSA и ChaCha20")

    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('-gen', '--generation', action='store_true', help='Создание ключей и параметров')
    mode.add_argument('-enc', '--encryption', action='store_true', help='Шифрование исходного файла')
    mode.add_argument('-dec', '--decryption', action='store_true', help='Дешифрование зашифрованного файла')

    parser.add_argument('--init', type=str, help='Путь к исходному текстовому файлу')
    parser.add_argument('--enc_file', type=str, help='Путь к зашифрованному файлу')
    parser.add_argument('--dec_file', type=str, help='Путь к расшифрованному выходному файлу')
    parser.add_argument('--sym', type=str, help='Путь к зашифрованному симметричному ключу')
    parser.add_argument('--nonce', type=str, help='Путь к nonce для ChaCha20')
    parser.add_argument('--pub', type=str, help='Путь к открытому ключу RSA')
    parser.add_argument('--priv', type=str, help='Путь к закрытому ключу RSA')
    parser.add_argument('--settings', type=str, default='settings.json', help='Путь к файлу конфигурации')
    parser.add_argument('--key_len', type=int, choices=[256], default=256, help='Размер ключа ChaCha20 в битах')

    return parser.parse_args()


def build_config():
    """
    Формирование конфигурации из аргументов и settings.json
    """
    args = parse_cli()
    base = serialization.load_json(args.settings)

    return {
        "mode": "gen" if args.generation else "enc" if args.encryption else "dec",
        "source_file": args.init or base.get("initial_file", "input.txt"),
        "cipher_file": args.enc_file or base.get("encrypted_file", "encrypted.bin"),
        "plain_file": args.dec_file or base.get("decrypted_file", "decrypted.txt"),
        "wrapped_key": args.sym or base.get("symmetric_key", "sym_key.enc"),
        "nonce_file": args.nonce or base.get("nonce", "nonce.bin"),
        "public_key": args.pub or base.get("public_key", "public.pem"),
        "private_key": args.priv or base.get("private_key", "private.pem"),
        "key_len": args.key_len
    }


def main():
    """
    Главная функция - точка входа в программу
    """
    cfg = build_config()

    match cfg["mode"]:
        case "gen":
            priv, pub = generate_key.generating_asymmetric_key()
            serialization.save_asym_keys(priv, pub, cfg["private_key"], cfg["public_key"])

            secret = generate_key.generating_symmetric_key(cfg["key_len"] // 8)
            nonce = generate_key.generating_nonce()

            serialization.save_symmetric_key(secret, cfg["wrapped_key"])
            serialization.save_nonce(nonce, cfg["nonce_file"])

            print("Генерация ключей завершена.")

        case "enc":
            pub = serialization.load_public_key(cfg["public_key"])
            secret = serialization.load_encrypt_symmetric_key(cfg["wrapped_key"])
            nonce = serialization.load_nonce(cfg["nonce_file"])
            source_text = serialization.read_text_file(cfg["source_file"])

            cipher_text = symmcrypt.encrypt_text(source_text, secret, nonce)
            sealed_key = asymmcrypt.encrypt_symmetric_key(secret, pub)

            serialization.save_symmetric_key(sealed_key, cfg["wrapped_key"])
            serialization.write_binary_file(cipher_text, cfg["cipher_file"])

            print("Шифрование завершено.")

        case "dec":
            priv = serialization.load_private_key(cfg["private_key"])
            sealed_key = serialization.load_encrypt_symmetric_key(cfg["wrapped_key"])
            secret = asymmcrypt.decrypt_key(sealed_key, priv)
            nonce = serialization.load_nonce(cfg["nonce_file"])
            cipher_text = serialization.read_binary_file(cfg["cipher_file"])

            recovered_text = symmcrypt.decrypt_text(cipher_text, secret, nonce)
            serialization.write_text_file(recovered_text, cfg["plain_file"])

            print("Дешифрование завершено.")

        case _:
            print("Неизвестный режим работы.")


if __name__ == "__main__":
    main()