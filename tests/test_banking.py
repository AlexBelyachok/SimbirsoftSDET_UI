import allure
from pages.manager_page import ManagerPage
from data.data_generator import data_generator
from utils.test_logic import (
    generate_first_name_from_post_code,
    find_customer_to_delete
)


@allure.feature("Функционал менеджера")
class TestBanking:
    @allure.story("Управление клиентами")
    @allure.title("Тест-кейс 1: Успешное создание нового клиента")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_add_customer(self, manager_page: ManagerPage):
        with allure.step("Шаг 1: Генерация тестовых данных"):
            last_name = data_generator.generate_last_name()
            post_code = data_generator.generate_post_code()
            first_name = generate_first_name_from_post_code(post_code)

        with allure.step("Шаг 2: Создание клиента через UI"):
            manager_page.go_to_add_customer_tab()
            manager_page.add_new_customer(first_name, last_name, post_code)

        with allure.step("Шаг 3: Проверка успешного создания клиента"):
            customers_page = manager_page.go_to_customers_tab()
            customers_page.search_customer(first_name)
            customers = customers_page.get_customers_data()

            assert len(customers) == 1, f"Ожидался 1 клиент, но найдено {len(customers)}"
            new_customer = customers[0]
            assert new_customer["first_name"] == first_name, "Имя созданного клиента не совпадает"
            assert new_customer["last_name"] == last_name, "Фамилия созданного клиента не совпадает"

    @allure.story("Управление клиентами")
    @allure.title("Тест-кейс 2: Сортировка клиентов по имени")
    @allure.severity(allure.severity_level.NORMAL)
    def test_sort_customers_by_first_name(self, manager_page_with_customers: ManagerPage):
        customers_page = manager_page_with_customers.go_to_customers_tab()

        with allure.step("Шаг 1: Получение исходного списка имен"):
            initial_names = [c['first_name'] for c in customers_page.get_customers_data()]

        with allure.step("Шаг 2: Проверка сортировки по убыванию (Z-A)"):
            customers_page.sort_by_first_name()
            sorted_desc = [c['first_name'] for c in customers_page.get_customers_data()]
            assert sorted_desc == sorted(initial_names, reverse=True), "Сортировка по убыванию неверна"

        with allure.step("Шаг 3: Проверка сортировки по возрастанию (A-Z)"):
            customers_page.sort_by_first_name()
            sorted_asc = [c['first_name'] for c in customers_page.get_customers_data()]
            assert sorted_asc == sorted(initial_names), "Сортировка по возрастанию неверна"

    @allure.story("Управление клиентами")
    @allure.title("Тест-кейс 3: Удаление клиента")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_customer(self, manager_page_with_customers: ManagerPage):
        customers_page = manager_page_with_customers.go_to_customers_tab()

        with allure.step("Шаг 1: Получение списка клиентов до удаления"):
            customers_before = customers_page.get_customers_data()
            names_before = [c['first_name'] for c in customers_before]

        with allure.step("Шаг 2: Определение клиента для удаления"):
            name_to_delete = find_customer_to_delete(names_before)
            allure.attach(f"Выбрано имя для удаления: {name_to_delete}", name="Info")

        with allure.step("Шаг 3: Удаление клиента из таблицы"):
            customers_page.delete_customer(name_to_delete)

        with allure.step("Шаг 4: Проверка, что клиент был удален"):
            names_after = [c['first_name'] for c in customers_page.get_customers_data()]
            assert name_to_delete not in names_after, f"Клиент '{name_to_delete}' не был удален"