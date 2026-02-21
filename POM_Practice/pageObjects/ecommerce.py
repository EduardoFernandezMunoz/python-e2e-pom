from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from POM_Practice.pageObjects.cart import CartPage
from utils.browserutils import BrowserUtils

class EcommercePage(BrowserUtils):
    def __init__(self, driver):
        super().__init__(driver)
        self.product_link = (By.XPATH, "//div[contains(@class, 'products')]/div")
        self.product_name_check = (By.XPATH, ".//a[contains(@class, 'font-oswald')]")
        self.checkout_button = (By.XPATH, "//div[contains(@class, 'profile')]//span[@role='button']")

    def safe_click(self, locator, timeout=15):
        """Hace clic seguro en cualquier elemento, con espera y scroll"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            # Scroll al centro de la pantalla
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            # Click con JS para evitar overlays
            self.driver.execute_script("arguments[0].click();", element)
            return element
        except TimeoutException:
            raise Exception(f"Elemento {locator} no clickable después de {timeout} segundos")
        except ElementClickInterceptedException:
            # Intento de nuevo con scroll extra
            self.driver.execute_script("window.scrollBy(0, -100);")
            self.driver.execute_script("arguments[0].click();", element)
            return element

    def add_product_to_cart(self, product_name):
        # Obtener todos los productos
        products = self.driver.find_elements(*self.product_link)

        for index, product in enumerate(products, start=1):
            name = product.find_element(*self.product_name_check).text
            if name == product_name:
                # XPath absoluto para este producto
                absolute_xpath = f"/html/body//div[contains(@class,'products')]/div[{index}]/button[normalize-space()='Add to cart']"
                # Clic seguro
                add_to_cart_btn = self.safe_click((By.XPATH, absolute_xpath))
                # Verificación opcional
                WebDriverWait(self.driver, 5).until(
                    lambda d: add_to_cart_btn.text.strip().lower() in ["remove from cart", "added"]
                )
                break

    def go_to_cart(self):
        """Navega al carrito de forma segura"""
        self.safe_click(self.checkout_button)
        return CartPage(self.driver)