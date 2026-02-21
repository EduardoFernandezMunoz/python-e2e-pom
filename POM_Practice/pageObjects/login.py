from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
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

    def login(self, username, password):
        # Enter user email
        self.driver.find_element(*self.email_input).send_keys(username)

        # Enter password
        password_field = self.driver.find_element(*self.password_input)
        password_field.send_keys(password)

        # Click the "show password" button safely
        # Wait until clickable, scroll into view, then use ActionChains to click
        password_button_clickable = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.show_password_button)        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", password_button_clickable)
        ActionChains(self.driver).move_to_element(password_button_clickable).click().perform()

        # Verify the password input is correct
        password_value = password_field.get_attribute("value")
        assert password_value == "Password123", "Password is different from Password123"

        # Click the login/submit button safely
        # Wait until clickable, scroll into view, then use ActionChains to click
        submit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.go_to_ecommerce_page)
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        ActionChains(self.driver).move_to_element(submit_button).click().perform()

        # Return the EcommercePage object
        ecommerce_page = EcommercePage(self.driver)
        return ecommerce_page