from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, WebDriverException
from utils.browserutils import BrowserUtils

class EcommercePage(BrowserUtils):
    def __init__(self, driver):
        self.driver = driver
        self.checkout_button = (By.XPATH, "//button[contains(text(),'Checkout')]")

    def wait_for_element_clickable(self, locator, timeout=15):
        """Espera a que un elemento sea clickable, ignorando overlays/toasts"""
        end_time = WebDriverWait(self.driver, timeout)
        try:
            return end_time.until(EC.element_to_be_clickable(locator))
        except TimeoutException:
            raise Exception(f"Elemento {locator} no clickable después de {timeout} segundos")

    def add_to_cart(self, product_name):
        """Agrega un producto al carrito, esperando que sea clickable"""
        product_button_locator = (
            By.XPATH, f"//h3[text()='{product_name}']/following-sibling::button[span[text()='Add to cart']]"
        )
        attempts = 0
        max_attempts = 5
        while attempts < max_attempts:
            try:
                button = self.wait_for_element_clickable(product_button_locator, timeout=10)
                try:
                    button.click()
                except ElementClickInterceptedException:
                    # Scroll un poco y reintentar
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                    button.click()

                # Verificar que el texto cambió a "Remove from cart"
                if button.text.strip() == "Remove from cart":
                    return
                else:
                    # Fallback con JS
                    self.driver.execute_script("arguments[0].click();", button)
                    if button.text.strip() == "Remove from cart":
                        return
            except (ElementClickInterceptedException, TimeoutException, WebDriverException):
                attempts += 1
                self.driver.execute_script("window.scrollBy(0, 50);")
        raise Exception(f"No se pudo hacer click en 'Add to cart' para {product_name} después de {max_attempts} intentos")

    # Alias para compatibilidad con el test
    add_product_to_cart = add_to_cart

    def go_to_cart(self):
        """Ir a la página de checkout/cart"""
        button = self.wait_for_element_clickable(self.checkout_button, timeout=15)
        try:
            button.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            button.click()
        from POM_Practice.pageObjects.cart import CartPage  # importa aquí para evitar import circular
        return CartPage(self.driver)