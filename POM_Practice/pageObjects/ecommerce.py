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
        self.toast_selector = (By.CSS_SELECTOR, "li[data-type='success']")

    def wait_for_toast_to_disappear(self, timeout=8):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(self.toast_selector)
            )
        except:
            pass  # ignore if toast never appeared

    def add_product_to_cart(self, product_name, max_attempts=5):
        products = self.driver.find_elements(*self.product_link)
        add_to_cart = None

        for product in products:
            name = product.find_element(*self.product_name_check).text
            if name.strip() == product_name:
                add_to_cart = product.find_element(
                    By.XPATH, ".//button[normalize-space()='Add to cart']"
                )
                break

        if not add_to_cart:
            raise Exception(f"Product '{product_name}' not found on page.")

        for attempt in range(max_attempts):
            # 🎯 Wait for toast to disappear before clicking
            self.wait_for_toast_to_disappear()

            # Scroll the button into view at the centre
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", add_to_cart
            )

            try:
                # Wait until button really is clickable
                WebDriverWait(self.driver, 8).until(
                    EC.element_to_be_clickable((By.XPATH, ".//button[normalize-space()='Add to cart']"))
                )

                # Normal click
                add_to_cart.click()

                # Verify change or fallback JS click
                if add_to_cart.text.strip() != "Remove from cart":
                    self.driver.execute_script("arguments[0].click();", add_to_cart)

                # If successful, stop
                if add_to_cart.text.strip() == "Remove from cart":
                    return

            except ElementClickInterceptedException:
                # scroll a bit more and retry
                self.driver.execute_script("window.scrollBy(0, 80);")

        raise Exception(
            f"Could not click 'Add to cart' for {product_name} after {max_attempts} attempts"
        )

    def go_to_cart(self):
        cart_btn = WebDriverWait(self.driver, 8).until(
            EC.element_to_be_clickable(self.checkout_button)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", cart_btn)
        self.driver.execute_script("arguments[0].click();", cart_btn)
        return CartPage(self.driver)