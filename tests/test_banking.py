import allure
from pages.manager_page import ManagerPage
from utils.helpers import (
    generate_post_code,
    generate_first_name_from_post_code,
    find_customer_to_delete,
    generate_last_name 
)


@allure.feature("Функционал менеджера")
class TestBanking:
    @allure.story("Управление клиентами")
    @allure.title("Тест-кейс 1: Успешное создание нового клиента")
    def test_add_customer(self, manager_page: ManagerPage):
        last_name = generate_last_name()
        post_code = generate_post_code()
        first_name = generate_first_name_from_post_code(post_code)

        manager_page.go_to_add_customer_tab()
        manager_page.add_new_customer(first_name, last_name, post_code)

        customers_page = manager_page.go_to_customers_tab()
        customers_page.search_customer(first_name)
        customers = customers_page.get_customers_data()

        assert len(customers) == 1
        new_customer = customers[0]
        assert new_customer["first_name"] == first_name
        assert new_customer["last_name"] == last_name

    @allure.story("Управление клиентами")
    @allure.title("Тест-кейс 2: Сортировка клиентов по имени")
    def test_sort_customers_by_first_name(self, manager_page_with_customers: ManagerPage):
        # Переходим на страницу клиентов
        customers_page = manager_page_with_customers.go_to_customers_tab()

        initial_names = [c['first_name'] for c in customers_page.get_customers_data()]

        customers_page.sort_by_first_name()
        sorted_desc = [c['first_name'] for c in customers_page.get_customers_data()]
        assert sorted_desc == sorted(initial_names, reverse=True)

        customers_page.sort_by_first_name()
        sorted_asc = [c['first_name'] for c in customers_page.get_customers_data()]
        assert sorted_asc == sorted(initial_names)

    @allure.story("Управление клиентами")
    @allure.title("Тест-кейс 3: Удаление клиента")
    def test_delete_customer(self, manager_page_with_customers: ManagerPage):
        customers_page = manager_page_with_customers.go_to_customers_tab()

        customers_before = customers_page.get_customers_data()
        names_before = [c['first_name'] for c in customers_before]

        name_to_delete = find_customer_to_delete(names_before)

        customers_page.delete_customer(name_to_delete)

        names_after = [c['first_name'] for c in customers_page.get_customers_data()]
        assert name_to_delete not in names_after