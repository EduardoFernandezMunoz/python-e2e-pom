from selenium.webdriver.common.by import By
from POM_Practice.pageObjects.cart import CartPage
from utils.browserutils import BrowserUtils
from selenium.webdriver.support.wait import WebDriverWait

# EcommercePage handles interactions with the products listing and cart navigation
class EcommercePage(BrowserUtils):
    def __init__(self, driver):
        super().__init__(driver)
        self.product_link = (By.XPATH, "//div[contains(@class, 'products')]/div")
        self.product_name_check = (By.XPATH, ".//a[contains(@class, 'font-oswald')]")
        self.checkout_button = (By.XPATH, "//div[contains(@class, 'profile')]//span[@role='button']")

    def add_product_to_cart(self, product_name):
        # Get all product elements on the page
        products = self.driver.find_elements(*self.product_link)

        # Loop through each product to find the one with the desired name
        for product in products:

            # Get the product name text from the product element
            productName = product.find_element(*self.product_name_check).text

            # Check if this is the product we want
            if productName == product_name:

                # Build absolute XPath for the Add to cart button based on product index
                index = products.index(product) + 1  # XPath indices start at 1
                absolute_xpath = f"/html/body//div[contains(@class,'products')]/div[{index}]/button[normalize-space()='Add to cart']"

                # Wait until button is clickable
                add_to_cart = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, absolute_xpath)))

                # Find the "Add to cart" button inside this product
                add_to_cart = product.find_element(By.XPATH, ".//button[contains(normalize-space(.), 'Add to cart')]")

                # Scroll the button into the center of the viewport
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_to_cart)

                # Click the button using JavaScript to avoid click interception
                self.driver.execute_script("arguments[0].click();", add_to_cart)
                break

        # Verify that the product was added to the cart
        assert add_to_cart.text == "Remove from cart", "{product_name} was not added to cart"

    # Find and click the cart button in the profile section
    def go_to_cart(self):
        self.driver.find_element(*self.checkout_button).click()
        cart_page = CartPage(self.driver)
        return cart_page