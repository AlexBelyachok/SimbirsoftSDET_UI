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

        assert len(customers) == 1, \
            f"Ожидался 1 клиент после поиска по имени '{first_name}', но найдено {len(customers)}"

        new_customer = customers[0]
        assert new_customer["first_name"] == first_name, \
            f"Имя созданного клиента не совпадает. Ожидалось: '{first_name}', Факт: '{new_customer['first_name']}'"

        assert new_customer["last_name"] == last_name, \
            f"Фамилия созданного клиента не совпадает. Ожидалось: '{last_name}', Факт: '{new_customer['last_name']}'"

    @allure.story("Управление клиентами")
    @allure.title("Тест-кейс 2: Сортировка клиентов по имени")
    def test_sort_customers_by_first_name(self, manager_page_with_customers: ManagerPage):
        customers_page = manager_page_with_customers.go_to_customers_tab()

        initial_names = [c['first_name'] for c in customers_page.get_customers_data()]

        customers_page.sort_by_first_name()  # Сортировка Z-A
        sorted_desc = [c['first_name'] for c in customers_page.get_customers_data()]

        assert sorted_desc == sorted(initial_names, reverse=True), \
            "Сортировка по убыванию (Z-A) работает некорректно"

        customers_page.sort_by_first_name()  # Сортировка A-Z
        sorted_asc = [c['first_name'] for c in customers_page.get_customers_data()]

        assert sorted_asc == sorted(initial_names), \
            "Сортировка по возрастанию (A-Z) работает некорректно"

    @allure.story("Управление клиентами")
    @allure.title("Тест-кейс 3: Удаление клиента")
    def test_delete_customer(self, manager_page_with_customers: ManagerPage):
        customers_page = manager_page_with_customers.go_to_customers_tab()

        customers_before = customers_page.get_customers_data()
        names_before = [c['first_name'] for c in customers_before]

        name_to_delete = find_customer_to_delete(names_before)

        customers_page.delete_customer(name_to_delete)

        customers_after = customers_page.get_customers_data()
        names_after = [c['first_name'] for c in customers_after]

        assert len(customers_after) == len(customers_before) - 1, \
            "Количество клиентов в таблице не уменьшилось на 1 после удаления"

        assert name_to_delete not in names_after, \
            f"Клиент с именем '{name_to_delete}' все еще присутствует в таблице после удаления"