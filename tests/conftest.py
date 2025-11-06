import pytest
from pages.manager_page import ManagerPage
from config import BASE_URL
from utils.helpers import generate_post_code, generate_first_name_from_post_code


@pytest.fixture(scope="function")
def manager_page(driver):
    """Фикстура для инициализации ManagerPage."""
    page = ManagerPage(driver)
    manager_url = f"{BASE_URL}/angularJs-protractor/BankingProject/#/manager"
    page.open(manager_url)
    yield page


@pytest.fixture(scope="function")
def manager_page_with_customers(manager_page: ManagerPage):
    """Фикстура, подготавливающая страницу с тремя клиентами."""
    manager_page.go_to_add_customer_tab()

    # Создаем 3 клиента с именами разной длины
    for i, length in enumerate([3, 5, 4]):
        post_code = generate_post_code(length)
        first_name = generate_first_name_from_post_code(post_code)
        last_name = f"Testovich_{i + 1}"
        manager_page.add_new_customer(first_name, last_name, post_code)

    yield manager_page