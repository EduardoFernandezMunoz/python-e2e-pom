from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from POM_Practice.pageObjects.checkout_overview import CheckoutOverviewPage
from utils.browserutils import BrowserUtils
from selenium.webdriver.support import expected_conditions as EC

class CheckoutInfoPage(BrowserUtils):
    def __init__(self, driver):
        super().__init__(driver)
        self.first_name_input = (By.XPATH, "//div[@class='form-group'][2]/input")
        self.last_name_input = (By.XPATH, "//div[@class='form-group'][3]/input")
        self.zip_code_input = (By.XPATH, "//div[@class='form-group'][4]/input")
        self.continue_to_payment_button = (By.XPATH, "//button[normalize-space()='Continue']")

    # Fill out the user information during checkout
    def fill_out_info(self, first_name, last_name, zip_code):
        first_name_field = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.first_name_input))
        first_name_field.send_keys(first_name)

        last_name_field = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.last_name_input))
        last_name_field.send_keys(last_name)

        zip_code_field = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.zip_code_input))
        zip_code_field.send_keys(zip_code)

    # Click "Continue" button to proceed to the checkout overview page
    def continue_to_payment (self):
        self.driver.find_element(*self.continue_to_payment_button).click()
        checkout_overview = CheckoutOverviewPage(self.driver)
        return checkout_overview