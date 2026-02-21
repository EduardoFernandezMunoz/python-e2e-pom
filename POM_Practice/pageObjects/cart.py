from selenium.webdriver.common.by import By
from POM_Practice.pageObjects.checkout_info import CheckoutInfoPage
from POM_Practice.utils.browserutils import BrowserUtils

class CartPage(BrowserUtils):
    def __init__(self, driver):
        super().__init__(driver)
        self.button_to_checkout = (By.XPATH, "//button[normalize-space()='Checkout']")

    # Click the checkout button to navigate to the checkout info page
    def go_to_checkout(self):
        self.driver.find_element(*self.button_to_checkout).click()
        checkout_info_page = CheckoutInfoPage(self.driver)
        return checkout_info_page