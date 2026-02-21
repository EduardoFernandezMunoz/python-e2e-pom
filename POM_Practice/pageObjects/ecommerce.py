from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.browserutils import BrowserUtils
from POM_Practice.pageObjects.cart import CartPage

class EcommercePage(BrowserUtils):
    def __init__(self, driver):
        super().__init__(driver)
        self.product_link = (By.XPATH, "//div[contains(@class, 'products')]/div")
        self.product_name_check = (By.XPATH, ".//a[contains(@class, 'font-oswald')]")
        self.checkout_button = (By.XPATH, "//div[contains(@class, 'profile')]//span[@role='button']")

    def wait_for_toast_to_disappear(self, timeout=10):
        """Espera a que cualquier toast desaparezca antes de intentar click."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element((By.XPATH, "//li[contains(@data-sonner-toast, '')]"))
            )
        except TimeoutException:
            pass

    def add_product_to_cart(self, product_name, max_attempts=5):
        products = self.driver.find_elements(*self.product_link)
        add_to_cart = None

        for product in products:
            pname = product.find_element(*self.product_name_check).text
            if pname == product_name:
                add_to_cart = product.find_element(By.XPATH, ".//button[normalize-space()='Add to cart']")
                break

        if not add_to_cart:
            raise Exception(f"Product '{product_name}' not found on page")

        attempts = 0
        while attempts < max_attempts:
            try:
                self.wait_for_toast_to_disappear()
                WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(add_to_cart)
                )
                add_to_cart.click()

                if add_to_cart.text.strip() == "Remove from cart":
                    return

                # fallback JS click
                self.driver.execute_script("arguments[0].click();", add_to_cart)
                if add_to_cart.text.strip() == "Remove from cart":
                    return

            except ElementClickInterceptedException:
                attempts += 1
                self.driver.execute_script("window.scrollBy(0, 50);")  # scroll un poco y reintenta

        raise Exception(f"Could not click 'Add to cart' for {product_name} after {max_attempts} attempts")

    def go_to_cart(self):
        self.wait_for_toast_to_disappear()
        self.driver.find_element(*self.checkout_button).click()
        return CartPage(self.driver)