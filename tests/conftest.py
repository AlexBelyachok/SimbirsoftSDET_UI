import pytest
from pages.manager_page import ManagerPage
from data.urls import Urls

from data.data_generator import data_generator
from utils.test_logic import generate_first_name_from_post_code


@pytest.fixture(scope="function")
def manager_page(driver):
    page = ManagerPage(driver)
    page.open(Urls.MANAGER_PAGE_URL)
    yield page


@pytest.fixture(scope="function")
def manager_page_with_customers(manager_page: ManagerPage):
    manager_page.go_to_add_customer_tab()

    for length in [3, 5, 4]:
        post_code = data_generator.generate_post_code(length)
        first_name = generate_first_name_from_post_code(post_code)
        last_name = data_generator.generate_last_name()
        manager_page.add_new_customer(first_name, last_name, post_code)

    yield manager_page
