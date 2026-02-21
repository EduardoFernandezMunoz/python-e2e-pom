from selenium.webdriver.common.by import By
from utils.browserutils import BrowserUtils
from POM_Practice.pageObjects.cart import CartPage
from selenium.webdriver.support.wait import WebDriverWait

# EcommercePage handles interactions with the products listing and cart navigation
class EcommercePage(BrowserUtils):
    def __init__(self, driver):
        super().__init__(driver)
        self.product_link = (By.XPATH, "//div[contains(@class, 'products')]/div")
        self.product_name_check = (By.XPATH, ".//a[contains(@class, 'font-oswald')]")
        self.checkout_button = (By.XPATH, "//div[contains(@class, 'profile')]//span[@role='button']")

    def add_product_to_cart(self, product_name):
        products = self.driver.find_elements(*self.product_link)
        add_to_cart = None  # ensure variable exists

        for product in products:
            productName = product.find_element(*self.product_name_check).text
            if productName == product_name:
                add_to_cart = product.find_element(By.XPATH, ".//button[normalize-space()='Add to cart']")

                # Wait until the button is clickable (and not covered)
                WebDriverWait(self.driver, 10).until(
                    lambda d: add_to_cart.is_displayed() and add_to_cart.is_enabled())

                # Scroll and click safely
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_to_cart)
                self.driver.execute_script("arguments[0].click();", add_to_cart)

                # Wait for the text to update to "Remove from cart"
                WebDriverWait(self.driver, 5).until(lambda d: add_to_cart.text.strip() == "Remove from cart")
                break

        if not add_to_cart:
            raise Exception(f"Product '{product_name}' not found on page")

    # Find and click the cart button in the profile section
    def go_to_cart(self):
        self.driver.find_element(*self.checkout_button).click()
        cart_page = CartPage(self.driver)
        return cart_page