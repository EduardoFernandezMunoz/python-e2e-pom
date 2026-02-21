from selenium.webdriver.common.by import By
from POM_Practice.pageObjects.ecommerce import EcommercePage
from utils.browserutils import BrowserUtils
from selenium.webdriver.support import expected_conditions as EC

# LoginPage handles login screen interactions
class LoginPage(BrowserUtils):
    def __init__(self, driver):
        super().__init__(driver)
        self.email_input = (By.ID, "email")
        self.password_input = (By.ID, "password")
        self.show_password_button = (By.XPATH, "//button[@type='button']")
        self.go_to_ecommerce_page = (By.XPATH, "//button[@type='submit']")

    def login(self,username,password):
        # Enter user email
        self.driver.find_element(*self.email_input).send_keys(username)

        # Enter password
        password_field = self.driver.find_element(*self.password_input)
        password_field.send_keys(password)

        # Validate password input is correct
        show_password_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.show_password_button)
        self.driver.find_element(*self.show_password_button).click()
        password_value = password_field.get_attribute("value")
        assert password_value == "Password123", "Password is different from Password123"

        # Submit login and navigate to EcommercePage
        self.driver.find_element(*self.go_to_ecommerce_page).click()
        ecommerce_page = EcommercePage(self.driver)
        return ecommerce_page