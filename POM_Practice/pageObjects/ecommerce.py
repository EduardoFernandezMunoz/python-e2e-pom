from selenium.webdriver.common.by import By
from POM_Practice.pageObjects.cart import CartPage
from utils.browserutils import BrowserUtils
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# EcommercePage handles interactions with the products listing and cart navigation
class EcommercePage(BrowserUtils):
    def __init__(self, driver):
        super().__init__(driver)
        self.product_container = (By.XPATH, "//div[contains(@class, 'products')]/div")
        self.product_name_check = (By.XPATH, ".//a[contains(@class, 'font-oswald')]")
        self.checkout_button = (By.XPATH, "//div[contains(@class, 'profile')]//span[@role='button']")

    def add_product_to_cart(self, product_name):
        """
        Adds the product with the given name to the cart.
        Uses dynamic XPath based on product name, scrolls into view, waits for clickability,
        and clicks using JS to avoid click interception issues.
        """
        # Build dynamic XPath directly to the "Add to cart" button of the product
        add_to_cart_xpath = (
            f"//div[contains(@class,'products')]"
            f"//a[contains(@class,'font-oswald') and normalize-space(text())='{product_name}']"
            f"/ancestor::div[contains(@class,'product')]"
            f"//button[normalize-space()='Add to cart']"
        )

        # Wait until the button is clickable
        add_to_cart_button = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, add_to_cart_xpath))
        )

        # Scroll into center of viewport
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_to_cart_button)

        # Click with JS to avoid interception issues
        self.driver.execute_script("arguments[0].click();", add_to_cart_button)

        # Optional: verify button text changed to "Remove from cart"
        WebDriverWait(self.driver, 5).until(
            lambda d: add_to_cart_button.text.strip() == "Remove from cart"
        )

    def go_to_cart(self):
        """
        Clicks the cart/checkout button in the profile section and returns the CartPage object.
        """
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.checkout_button)
        ).click()
        return CartPage(self.driver)