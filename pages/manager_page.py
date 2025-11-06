from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.customers_page import CustomersPage  # Импортируем новую страницу


class ManagerPage(BasePage):
    # Локаторы для навигации и формы добавления
    ADD_CUSTOMER_TAB_BUTTON = (By.CSS_SELECTOR, "button[ng-click='addCust()']")
    CUSTOMERS_TAB_BUTTON = (By.CSS_SELECTOR, "button[ng-click='showCust()']")

    FIRST_NAME_INPUT = (By.CSS_SELECTOR, "input[ng-model='fName']")
    LAST_NAME_INPUT = (By.CSS_SELECTOR, "input[ng-model='lName']")
    POST_CODE_INPUT = (By.CSS_SELECTOR, "input[ng-model='postCd']")
    ADD_CUSTOMER_SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    def go_to_add_customer_tab(self) -> None:
        """Переходит на вкладку 'Add Customer'."""
        self.find_element(self.ADD_CUSTOMER_TAB_BUTTON).click()

    def add_new_customer(self, first_name: str, last_name: str, post_code: str) -> None:
        """Заполняет форму и создает нового клиента."""
        self.find_element(self.FIRST_NAME_INPUT).send_keys(first_name)
        self.find_element(self.LAST_NAME_INPUT).send_keys(last_name)
        self.find_element(self.POST_CODE_INPUT).send_keys(post_code)
        self.find_element(self.ADD_CUSTOMER_SUBMIT_BUTTON).click()
        try:
            # Принимаем alert после создания
            self.driver.switch_to.alert.accept()
        except:
            pass

    def go_to_customers_tab(self) -> CustomersPage:
        """
        Переходит на вкладку 'Customers' и возвращает экземпляр CustomersPage.
        """
        self.find_element(self.CUSTOMERS_TAB_BUTTON).click()
        # Паттерн "возврат нового Page Object"
        return CustomersPage(self.driver)