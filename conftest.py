import pytest
import allure
from utils.helpers import generate_first_name_from_post_code, generate_post_code
from allure_commons.types import AttachmentType
from selenium import webdriver
from pages.manager_page import ManagerPage
from config import BASE_URL, IS_HEADLESS

@pytest.fixture(scope="function")
def driver():
    """Фикстура для инициализации и закрытия драйвера браузера."""
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    if IS_HEADLESS:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def manager_page(driver):
    """
    Фикстура для инициализации ManagerPage на чистой странице.
    """
    page = ManagerPage(driver)
    manager_url = f"{BASE_URL}/angularJs-protractor/BankingProject/#/manager"
    page.open(manager_url)
    yield page

@pytest.fixture(scope="function")
def manager_page_with_customers(manager_page: ManagerPage):
    """
    Фикстура, которая подготавливает страницу с тремя уже созданными клиентами.
    Использует фикстуру manager_page для базовой настройки.
    """
    
    manager_page.go_to_add_customer_tab()
    
    
    post_code_lengths = [3, 4, 5]
    
    for i, length in enumerate(post_code_lengths):
        post_code = generate_post_code(length)
        first_name = generate_first_name_from_post_code(post_code)
        last_name = f"Testovich_{i+1}"
        
        manager_page.add_new_customer(first_name, last_name, post_code)
        
    yield manager_page

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Хук для добавления скриншота в Allure отчет при падении теста.
    """
    outcome = yield
    rep = outcome.get_result()

    setattr(item, "rep_" + rep.when, rep)

    if rep.when == "call" and rep.failed:
        if 'driver' in item.fixturenames:
            driver = item.funcargs['driver']
            allure.attach(
                driver.get_screenshot_as_png(),
                name="screenshot_on_failure",
                attachment_type=AttachmentType.PNG
            )