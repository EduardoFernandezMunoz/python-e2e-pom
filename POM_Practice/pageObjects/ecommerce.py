from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from POM_Practice.pageObjects.cart import CartPage
from utils.browserutils import BrowserUtils

class EcommercePage(BrowserUtils):
    def __init__(self, driver):
        super().__init__(driver)
        # Each div inside 'products' represents a single product
        self.product_link = (By.XPATH, "//div[contains(@class, 'products')]/div")
        # Locator to get the product name inside each product div
        self.product_name_check = (By.XPATH, ".//a[contains(@class, 'font-oswald')]")
        # Locator for the cart/checkout button in the profile section
        self.checkout_button = (By.XPATH, "//div[contains(@class, 'profile')]//span[@role='button']")

    def safe_click(self, locator, timeout=15):
        """
        Safe click method: waits until element is clickable, scrolls it into view,
        and uses JavaScript click to avoid overlays or intercepted click errors.
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            # Scroll the element to the center of the viewport
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            # Click using JavaScript to avoid interception issues
            self.driver.execute_script("arguments[0].click();", element)
            return element
        except TimeoutException:
            raise Exception(f"Element {locator} not clickable after {timeout} seconds")
        except ElementClickInterceptedException:
            # Extra attempt with additional scroll in case of click interception
            self.driver.execute_script("window.scrollBy(0, -100);")
            self.driver.execute_script("arguments[0].click();", element)
            return element

    def add_product_to_cart(self, product_name):
        """
        Adds a product to the cart based on the product name provided in the data file.
        Uses absolute XPath for the 'Add to cart' button according to the product's index.
        """
        # Get all product elements on the page
        products = self.driver.find_elements(*self.product_link)

        for index, product in enumerate(products, start=1):
            name = product.find_element(*self.product_name_check).text
            if name == product_name:
                # Absolute XPath of the 'Add to cart' button based on product position
                absolute_xpath = f"/html/body/div[2]/div/div[2]/div[{index}]/div/button"
                add_to_cart_btn = self.safe_click((By.XPATH, absolute_xpath))
                
                # Optional: wait until the button text changes to "Remove from cart" or "Added"
                WebDriverWait(self.driver, 5).until(
                    lambda d: add_to_cart_btn.text.strip().lower() in ["remove from cart", "added"]
                )
                break

    def go_to_cart(self):
        """
        Navigate to the cart page using a safe click on the checkout/cart button.
        Returns the CartPage object.
        """
        self.safe_click(self.checkout_button)
        return CartPage(self.driver)