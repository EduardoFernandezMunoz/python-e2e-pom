# POM_Practice/pageObjects/ecommerce.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (ElementClickInterceptedException,TimeoutException,NoSuchElementException)

class EcommercePage(BrowserUtils):
    def __init__(self, driver):
        self.driver = driver
        # Localizadores generales
        self.cart_button = (By.XPATH, "//button[contains(text(),'Cart')]")
        self.checkout_button = (By.XPATH, "//button[contains(text(),'Checkout')]")

    def wait_for_element_clickable(self, locator, timeout=15):
        """Espera a que un elemento sea clickable, ignorando overlays/toasts"""
        for attempt in range(5):
            try:
                elem = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable(locator)
                )
                # Intento de clic normal
                elem.click()
                return elem
            except ElementClickInterceptedException:
                # Scroll al elemento y reintento
                try:
                    elem = self.driver.find_element(*locator)
                    self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", elem)
                    WebDriverWait(self.driver, 1).until(lambda d: True)  # delay breve
                    elem.click()
                    return elem
                except Exception:
                    pass
            except TimeoutException:
                pass

        # Fallback final: clic con JS
        elem = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].click();", elem)
        return elem

    def add_to_cart(self, product_name):
        """Añade un producto al carrito por nombre"""
        locator = (By.XPATH, f"//h3[text()='{product_name}']/following-sibling::button[span[text()='Add to cart']]")
        return self.wait_for_element_clickable(locator)

    def go_to_cart(self):
        """Navega a la página de carrito"""
        return self.wait_for_element_clickable(self.cart_button)

    def go_to_checkout(self):
        """Clic en el botón de checkout"""
        return self.wait_for_element_clickable(self.checkout_button)

    def get_product_price(self, product_name):
        """Obtiene el precio de un producto"""
        locator = (By.XPATH, f"//h3[text()='{product_name}']/following-sibling::p")
        try:
            elem = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(locator)
            )
            return elem.text
        except TimeoutException:
            return None