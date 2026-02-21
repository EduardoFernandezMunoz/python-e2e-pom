from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from POM_Practice.pageObjects.cart import CartPage
from utils.browserutils import BrowserUtils

class EcommercePage(BrowserUtils):
    def __init__(self, driver):
        super().__init__(driver)
        # Cada div dentro de products representa un producto
        self.product_link = (By.XPATH, "//div[contains(@class, 'products')]/div")
        self.product_name_check = (By.XPATH, ".//a[contains(@class, 'font-oswald')]")
        self.checkout_button = (By.XPATH, "//div[contains(@class, 'profile')]//span[@role='button']")

    def safe_click(self, locator, timeout=15):
        """Click seguro: espera, scroll y JS click para evitar overlays"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            self.driver.execute_script("arguments[0].click();", element)
            return element
        except TimeoutException:
            raise Exception(f"Elemento {locator} no clickable después de {timeout} segundos")
        except ElementClickInterceptedException:
            # Intento extra con scroll adicional
            self.driver.execute_script("window.scrollBy(0, -100);")
            self.driver.execute_script("arguments[0].click();", element)
            return element

    def add_product_to_cart(self, product_name):
        # Obtener todos los productos
        products = self.driver.find_elements(*self.product_link)

        for index, product in enumerate(products, start=1):
            name = product.find_element(*self.product_name_check).text
            if name == product_name:
                # XPath absoluto del botón "Add to cart" según la posición del producto
                absolute_xpath = f"/html/body/div[2]/div/div[2]/div[{index}]/div/button"
                add_to_cart_btn = self.safe_click((By.XPATH, absolute_xpath))
                
                # Opcional: espera a que el botón cambie a "Remove from cart" o similar
                WebDriverWait(self.driver, 5).until(
                    lambda d: add_to_cart_btn.text.strip().lower() in ["remove from cart", "added"]
                )
                break

    def go_to_cart(self):
        """Ir al carrito con clic seguro"""
        self.safe_click(self.checkout_button)
        return CartPage(self.driver)