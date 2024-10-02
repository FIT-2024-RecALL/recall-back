import random
import string


def encrypt_text(source_text: str) -> str:
    return source_text + "fakehash"


def decrypt_text(encrypted_text: str) -> str:
    return encrypted_text[:-8]


def generate_secrete_key() -> str:
    length = random.randint(11, 15)
    characters = string.ascii_letters + string.digits + "_-()!"
    random_link = ''.join(random.choice(characters) for _ in range(length))  # Генерация строки
    return random_link
