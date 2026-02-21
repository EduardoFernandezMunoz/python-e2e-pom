from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from utils.browserutils import BrowserUtils
from POM_Practice.pageObjects.cart import CartPage

class EcommercePage(BrowserUtils):
    def __init__(self, driver):
        super().__init__(driver)
        self.product_link = (By.XPATH, "//div[contains(@class, 'products')]/div")
        self.product_name_check = (By.XPATH, ".//a[contains(@class, 'font-oswald')]")
        self.checkout_button = (By.XPATH, "//div[contains(@class, 'profile')]//span[@role='button']")

    def add_product_to_cart(self, product_name, max_attempts=5):
        products = self.driver.find_elements(*self.product_link)
        add_to_cart = None

        for product in products:
            productName = product.find_element(*self.product_name_check).text
            if productName == product_name:
                add_to_cart = product.find_element(By.XPATH, ".//button[normalize-space()='Add to cart']")
                break

        if not add_to_cart:
            raise Exception(f"Product '{product_name}' not found on page.")

        attempts = 0
        while attempts < max_attempts:
            try:
                # Scroll the button to center + extra offset
                self.driver.execute_script(
                    "const rect = arguments[0].getBoundingClientRect();"
                    "window.scrollBy(0, rect.top - window.innerHeight/2 - 100);",
                    add_to_cart
                )

                # Wait until clickable
                WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, ".//button[normalize-space()='Add to cart']")))

                # Try normal click
                add_to_cart.click()
                
                # Fallback: JS click if text doesn't change
                if add_to_cart.text.strip() != "Remove from cart":
                    self.driver.execute_script("arguments[0].click();", add_to_cart)

                # Confirm
                if add_to_cart.text.strip() == "Remove from cart":
                    return

            except ElementClickInterceptedException:
                attempts += 1
                self.driver.execute_script("window.scrollBy(0, 50);")  # scroll a little and retry
            except Exception:
                attempts += 1

    raise Exception(f"Could not click 'Add to cart' for {product_name} after {max_attempts} attempts")
    def go_to_cart(self):
        # Wait until cart button is clickable
        cart_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.checkout_button))
        # Scroll to center
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", cart_button)
        # Click safely
        self.driver.execute_script("arguments[0].click();", cart_button)
        return CartPage(self.driver)