from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage


class CustomersPage(BasePage):
    CUSTOMER_TABLE_ROWS = (By.XPATH, "//table/tbody/tr")
    FIRST_NAME_HEADER = (By.XPATH, "//thead/tr/td[1]/a")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[ng-model='searchCustomer']")
    DELETE_BUTTON_BY_NAME = (
        By.XPATH,
        "//td[text()='{name}']/following-sibling::td/button[text()='Delete']",
    )

    def search_customer(self, query: str) -> None:
        self.fill_field(self.SEARCH_INPUT, query)

    def get_customers_data(self) -> list[dict]:
        try:
            rows = self.find_elements(self.CUSTOMER_TABLE_ROWS, time=2)
        except TimeoutException:
            return []

        customers = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            customers.append(
                {
                    "first_name": cells[0].text,
                    "last_name": cells[1].text,
                    "post_code": cells[2].text,
                }
            )
        return customers

    def sort_by_first_name(self) -> None:
        self.click_element(self.FIRST_NAME_HEADER)

    def delete_customer(self, first_name: str) -> None:
        strategy, path = self.DELETE_BUTTON_BY_NAME
        specific_locator = (strategy, path.format(name=first_name))

        self.click_element(specific_locator)
