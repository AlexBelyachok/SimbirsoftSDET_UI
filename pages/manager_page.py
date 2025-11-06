from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage


class ManagerPage(BasePage):
    ADD_CUSTOMER_TAB_BUTTON = (By.CSS_SELECTOR, "button[ng-click='addCust()']")
    CUSTOMERS_TAB_BUTTON = (By.CSS_SELECTOR, "button[ng-click='showCust()']")
    FIRST_NAME_INPUT = (By.CSS_SELECTOR, "input[ng-model='fName']")
    LAST_NAME_INPUT = (By.CSS_SELECTOR, "input[ng-model='lName']")
    POST_CODE_INPUT = (By.CSS_SELECTOR, "input[ng-model='postCd']")
    ADD_CUSTOMER_SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    CUSTOMER_TABLE_ROWS = (By.XPATH, "//table/tbody/tr")
    FIRST_NAME_HEADER = (By.XPATH, "//thead/tr/td[1]/a")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[ng-model='searchCustomer']")

    def open(self, url):
        self.driver.get(url)

    def go_to_add_customer_tab(self):
        self.find_element(self.ADD_CUSTOMER_TAB_BUTTON).click()

    def add_new_customer(self, first_name, last_name, post_code):
        self.find_element(self.FIRST_NAME_INPUT).send_keys(first_name)
        self.find_element(self.LAST_NAME_INPUT).send_keys(last_name)
        self.find_element(self.POST_CODE_INPUT).send_keys(post_code)
        self.find_element(self.ADD_CUSTOMER_SUBMIT_BUTTON).click()
        try:
            self.driver.switch_to.alert.accept()
        except:
            pass

    def go_to_customers_tab(self):
        self.find_element(self.CUSTOMERS_TAB_BUTTON).click()

    def search_customer(self, query):
        self.find_element(self.SEARCH_INPUT).send_keys(query)

    def get_customers_data(self):
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

    def sort_by_first_name(self):
        self.find_element(self.FIRST_NAME_HEADER).click()

    def delete_customer(self, first_name):
        customers = self.get_customers_data()
        customer_to_delete = next((c for c in customers if c['first_name'] == first_name), None)
        if customer_to_delete:
            customer_to_delete['delete_button'].click()