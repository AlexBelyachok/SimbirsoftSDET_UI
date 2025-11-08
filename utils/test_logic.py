import string


def generate_first_name_from_post_code(post_code: str) -> str:
    """
    Генерирует First Name на основе Post Code по заданной логике.
    """
    first_name = ""
    alphabet = string.ascii_lowercase
    for i in range(0, len(post_code), 2):
        part = post_code[i : i + 2]
        number = int(part)
        char_index = number % 26
        first_name += alphabet[char_index]
    return first_name.capitalize()


def find_customer_to_delete(names: list[str]) -> str:
    """
    Находит имя клиента, длина которого наиболее близка к среднему.
    """
    if not names:
        raise ValueError("Список имен не может быть пустым")

    lengths = [len(name) for name in names]
    avg_length = sum(lengths) / len(lengths)

    return min(names, key=lambda name: abs(len(name) - avg_length))
