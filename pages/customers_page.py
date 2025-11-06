from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage


class CustomersPage(BasePage):
    # Локаторы, относящиеся только к таблице клиентов
    CUSTOMER_TABLE_ROWS = (By.XPATH, "//table/tbody/tr")
    FIRST_NAME_HEADER = (By.XPATH, "//thead/tr/td[1]/a")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[ng-model='searchCustomer']")

    def search_customer(self, query: str) -> None:
        """Вводит поисковый запрос в поле поиска."""
        self.find_element(self.SEARCH_INPUT).send_keys(query)

    def get_customers_data(self) -> list[dict]:
        """Собирает данные всех клиентов из таблицы."""
        try:
            rows = self.find_elements(self.CUSTOMER_TABLE_ROWS, time=2)
        except TimeoutException:
            return []

        customers = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            customers.append({
                "first_name": cells[0].text,
                "last_name": cells[1].text,
                "post_code": cells[2].text,
                "delete_button": cells[4].find_element(By.TAG_NAME, "button")
            })
        return customers

    def sort_by_first_name(self) -> None:
        """Кликает на заголовок 'First Name' для сортировки."""
        self.find_element(self.FIRST_NAME_HEADER).click()

    def delete_customer(self, first_name: str) -> None:
        """Находит клиента по имени и нажимает кнопку 'Delete'."""
        customers = self.get_customers_data()
        customer_to_delete = next((c for c in customers if c['first_name'] == first_name), None)
        if customer_to_delete:
            customer_to_delete['delete_button'].click()