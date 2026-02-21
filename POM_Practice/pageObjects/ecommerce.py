from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.browserutils import BrowserUtils
from POM_Practice.pageObjects.cart import CartPage
import time

class EcommercePage(BrowserUtils):
    def __init__(self, driver):
        super().__init__(driver)
        self.product_link = (By.XPATH, "//div[contains(@class, 'products')]/div")
        self.product_name_check = (By.XPATH, ".//a[contains(@class, 'font-oswald')]")
        self.checkout_button = (By.XPATH, "//div[contains(@class, 'profile')]//span[@role='button']")

    def add_product_to_cart(self, product_name, max_attempts=3):
        # Get all product elements on the page
        products = self.driver.find_elements(*self.product_link)
        add_to_cart = None

        # Loop through each product to find the desired one
        for product in products:
            productName = product.find_element(*self.product_name_check).text
            if productName == product_name:
                add_to_cart = product.find_element(By.XPATH, ".//button[normalize-space()='Add to cart']")
                break

        if not add_to_cart:
            raise Exception(f"Product '{product_name}' not found on the page")

        # Try clicking the button up to max_attempts
        for attempt in range(1, max_attempts + 1):
            try:
                # Scroll to center and wait until clickable
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_to_cart)
                WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(add_to_cart))

                # ActionChains click
                ActionChains(self.driver).move_to_element(add_to_cart).click().perform()
                
                # As fallback, JS click
                self.driver.execute_script("arguments[0].click();", add_to_cart)

                # Verify it changed to "Remove from cart"
                if add_to_cart.text.strip() == "Remove from cart":
                    return
                else:
                    time.sleep(1)  # small wait and retry
            except Exception as e:
                if attempt == max_attempts:
                    raise Exception(f"Could not click 'Add to cart' for {product_name} after {max_attempts} attempts") from e
                time.sleep(1)