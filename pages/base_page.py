from typing import List, Tuple
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def open(self, url: str) -> None:
        self.driver.get(url)

    def find_element(self, locator: Tuple[str, str], time: int = 10) -> WebElement:
        return WebDriverWait(self.driver, time).until(
            EC.presence_of_element_located(locator),
            message=f"Не удалось найти элемент по локатору {locator}"
        )

    def find_elements(self, locator: Tuple[str, str], time: int = 10) -> List[WebElement]:

        return WebDriverWait(self.driver, time).until(
            EC.presence_of_all_elements_located(locator),
            message=f"Не удалось найти элементы по локатору {locator}"
        )

    def click_element(self, locator: Tuple[str, str], time: int = 10) -> None:
        element = WebDriverWait(self.driver, time).until(
            EC.element_to_be_clickable(locator),
            message=f"Элемент {locator} не кликабелен"
        )
        element.click()

    def fill_field(self, locator: Tuple[str, str], text: str, time: int = 10) -> None:
        element = self.find_element(locator, time)
        element.clear()
        element.send_keys(text)

    def handle_alert(self, accept: bool = True, time: int = 10) -> str | None:
        try:
            alert = WebDriverWait(self.driver, time).until(
                EC.alert_is_present(),
                message="Alert не появился в течение указанного времени"
            )
            alert_text = alert.text
            if accept:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        except TimeoutException:
            print("Alert не был найден.")
            return None