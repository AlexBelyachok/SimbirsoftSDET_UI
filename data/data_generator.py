import random
import string
from faker import Faker


class DataGenerator:
    """
    Класс для генерации различных тестовых данных.
    """

    def __init__(self, locale: str = "ru_RU"):
        self.fake = Faker(locale)

    def generate_last_name(self) -> str:
        """Генерирует случайную фамилию."""
        return self.fake.last_name()

    def generate_post_code(self, length: int = 5) -> str:
        """Генерирует случайный Post Code из (length * 2) цифр."""
        return "".join(random.choices(string.digits, k=length * 2))


data_generator = DataGenerator()
