from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from POM_Practice.pageObjects.ecommerce import EcommercePage
from utils.browserutils import BrowserUtils

class LoginPage(BrowserUtils):
    def __init__(self, driver):
        super().__init__(driver)
        self.email_input = (By.ID, "email")
        self.password_input = (By.ID, "password")
        self.show_password_button = (By.XPATH, "//button[@type='button']")
        self.go_to_ecommerce_page = (By.XPATH, "//button[@type='submit']")

    def safe_click(self, locator):
        """Wait for element to be clickable, scroll to center, and click via JavaScript"""
        element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self.driver.execute_script("arguments[0].click();", element)

    def login(self, username, password):
        # Enter user email
        self.driver.find_element(*self.email_input).send_keys(username)

        # Enter password
        password_field = self.driver.find_element(*self.password_input)
        password_field.send_keys(password)

        # Click the "show password" button safely
        self.safe_click(self.show_password_button)

        # Verify password field
        password_value = password_field.get_attribute("value")
        assert password_value == "Password123", "Password is different from Password123"

        # Click the login/submit button safely
        self.safe_click(self.go_to_ecommerce_page)

        # Return the EcommercePage object
        return EcommercePage(self.driver)