from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.customers_page import CustomersPage

class ManagerPage(BasePage):
    ADD_CUSTOMER_TAB_BUTTON = (By.CSS_SELECTOR, "button[ng-click='addCust()']")
    CUSTOMERS_TAB_BUTTON = (By.CSS_SELECTOR, "button[ng-click='showCust()']")
    FIRST_NAME_INPUT = (By.CSS_SELECTOR, "input[ng-model='fName']")
    LAST_NAME_INPUT = (By.CSS_SELECTOR, "input[ng-model='lName']")
    POST_CODE_INPUT = (By.CSS_SELECTOR, "input[ng-model='postCd']")
    ADD_CUSTOMER_SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    def go_to_add_customer_tab(self) -> None:
        self.click_element(self.ADD_CUSTOMER_TAB_BUTTON)

    def add_new_customer(self, first_name: str, last_name: str, post_code: str) -> None:
        self.fill_field(self.FIRST_NAME_INPUT, first_name)
        self.fill_field(self.LAST_NAME_INPUT, last_name)
        self.fill_field(self.POST_CODE_INPUT, post_code)
        self.click_element(self.ADD_CUSTOMER_SUBMIT_BUTTON)
        self.handle_alert()

    def go_to_customers_tab(self) -> CustomersPage:
        self.click_element(self.CUSTOMERS_TAB_BUTTON)
        return CustomersPage(self.driver)