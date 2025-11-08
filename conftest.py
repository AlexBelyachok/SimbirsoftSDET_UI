import pytest
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from config import IS_HEADLESS  # Импортируем настройку из конфига


@pytest.fixture(scope="function")
def driver():
    """Фикстура для инициализации и закрытия драйвера браузера."""
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    if IS_HEADLESS:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для добавления скриншота в Allure отчет при падении теста."""
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed and "driver" in item.fixturenames:
        driver = item.funcargs["driver"]
        allure.attach(
            driver.get_screenshot_as_png(),
            name="screenshot_on_failure",
            attachment_type=AttachmentType.PNG,
        )
