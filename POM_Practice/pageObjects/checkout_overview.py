
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from POM_Practice.pageObjects.checkout_complete import CheckoutCompletePage
from POM_Practice.utils.browserutils import BrowserUtils


class CheckoutOverviewPage(BrowserUtils):
    def __init__(self, driver):
        super().__init__(driver)
        self.name_of_product = (By.XPATH, "//h3[@class='font-bold font-oswald text-lg']")
        self.finish_button = (By.XPATH, "//button[normalize-space()='Finish']")

    # Verify that the product in the overview matches the expected product
    def checkout_overview(self, product_name):
        product_element = self.driver.find_element(*self.name_of_product)
        assert product_element.text == product_name, "Product mismatch in overview"

    # Click the "Finish" button to complete the order and navigate to the checkout complete page
    def finish_order(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.finish_button))
        self.driver.find_element(*self.finish_button).click()
        checkout_complete = CheckoutCompletePage(self.driver)
        return checkout_complete