from typing import List, Tuple
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver: WebDriver):
        """
        Конструктор базовой страницы.
        :param driver: Экземпляр WebDriver.
        """
        self.driver = driver

    def open(self, url: str) -> None:
        """
        Открывает страницу по заданному URL.
        :param url: URL для открытия.
        """
        self.driver.get(url)

    def find_element(self, locator: Tuple[str, str], time: int = 10) -> WebElement:
        """
        Находит один элемент, ожидая его появления.
        :param locator: Кортеж (стратегия, значение локатора), например (By.CSS_SELECTOR, 'button').
        :param time: Максимальное время ожидания в секундах.
        :return: Найденный WebElement.
        """
        return WebDriverWait(self.driver, time).until(
            EC.presence_of_element_located(locator),
            message=f"Не удалось найти элемент по локатору {locator}"
        )

    def find_elements(self, locator: Tuple[str, str], time: int = 10) -> List[WebElement]:
        """
        Находит все элементы, подходящие под локатор, ожидая их появления.
        :param locator: Кортеж (стратегия, значение локатора).
        :param time: Максимальное время ожидания в секундах.
        :return: Список найденных WebElement'ов.
        """
        return WebDriverWait(self.driver, time).until(
            EC.presence_of_all_elements_located(locator),
            message=f"Не удалось найти элементы по локатору {locator}"
        )