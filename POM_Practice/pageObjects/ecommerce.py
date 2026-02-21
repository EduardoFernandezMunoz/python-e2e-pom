from selenium.webdriver.common.by import By
from utils.browserutils import BrowserUtils
from POM_Practice.pageObjects.cart import CartPage
from selenium.webdriver.support.wait import WebDriverWait
import time
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException


# EcommercePage handles interactions with the products listing and cart navigation
class EcommercePage(BrowserUtils):
    def __init__(self, driver):
        super().__init__(driver)
        self.product_link = (By.XPATH, "//div[contains(@class, 'products')]/div")
        self.product_name_check = (By.XPATH, ".//a[contains(@class, 'font-oswald')]")
        self.checkout_button = (By.XPATH, "//div[contains(@class, 'profile')]//span[@role='button']")

    def add_product_to_cart(self, product_name, retries=3):
    # Get all products
        products = self.driver.find_elements(*self.product_link)

        for product in products:
            # Get product name
            productName = product.find_element(*self.product_name_check).text
            if productName == product_name:
                add_to_cart = product.find_element(By.XPATH, ".//button[normalize-space()='Add to cart']")

                # Retry loop in case click is intercepted
                for attempt in range(retries):
                    try:
                        # Scroll into view and click
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_to_cart)
                        add_to_cart.click()  # normal Selenium click first
                        break  # success, exit retry loop
                    except (ElementClickInterceptedException, StaleElementReferenceException):
                        # Wait a little and retry
                        time.sleep(0.5)
                        # If normal click fails, try JavaScript click as fallback
                        self.driver.execute_script("arguments[0].click();", add_to_cart)
                else:
                    raise Exception(f"Could not click 'Add to cart' for {product_name} after {retries} attempts")

                # Optional: small wait to ensure UI updates
                time.sleep(0.5)

                # Verify that product was added
                new_text = add_to_cart.text
                assert new_text == "Remove from cart", f"{product_name} was not added to cart"
                break

        if not add_to_cart:
            raise Exception(f"Product '{product_name}' not found on page")

    # Find and click the cart button in the profile section
    def go_to_cart(self):
        self.driver.find_element(*self.checkout_button).click()
        cart_page = CartPage(self.driver)
        return cart_page