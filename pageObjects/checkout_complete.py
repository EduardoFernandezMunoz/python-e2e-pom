from POM_Practice.utils.browserutils import BrowserUtils
from selenium.webdriver.common.by import By


class CheckoutCompletePage(BrowserUtils):
    def __init__(self,driver):
        super().__init__(driver)
        self.order_dispatched = (By.XPATH, "//h3[@class='text-lg uppercase font-black font-oswald mb-4']")

    # Verify that the order was successfully completed
    def order_assertion(self):
        thank_you_message = self.driver.find_element(*self.order_dispatched)
        assert "THANK YOU" in thank_you_message.text, "Error in checkout"

        # Close the browser session after verifying the order
        # Since this is the last page in the POM workflow, we can safely quit the driver here
        self.driver.quit()