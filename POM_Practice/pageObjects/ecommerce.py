from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from pageObjects.cart import CartPage  # Asegúrate de tener tu página de carrito definida

class EcommercePage:
    def __init__(self, driver):
        self.driver = driver
        # Selectores principales
        self.add_to_cart_buttons = (By.CSS_SELECTOR, "button:has(span:text('Add to cart'))")
        self.checkout_button = (By.CSS_SELECTOR, "a[href*='cart']")  # Ajusta según tu sitio
        self.toast_selector = (By.CSS_SELECTOR, "li[data-sonner-toast]")

    def wait_for_element_clickable(self, locator, timeout=10):
        """Espera a que un elemento sea clickable, ignorando overlays/toasts"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
        except TimeoutException:
            raise Exception(f"Elemento {locator} no clickable después de {timeout} segundos")

    def wait_for_toasts_to_disappear(self, timeout=5):
        """Espera a que desaparezcan los popups de confirmación"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(self.toast_selector)
            )
        except TimeoutException:
            # Si no desaparecen, no bloquea el flujo
            pass

    def add_product_to_cart(self, product_name):
        """Añade un producto al carrito de forma segura"""
        # Buscamos el botón específico del producto
        button_locator = (
            By.XPATH, f"//h3[text()='{product_name}']/following-sibling::button[span[text()='Add to cart']]"
        )
        attempts = 0
        max_attempts = 5
        while attempts < max_attempts:
            try:
                button = self.wait_for_element_clickable(button_locator)
                button.click()
                # Esperamos que aparezca el toast y luego desaparezca
                self.wait_for_toasts_to_disappear()
                return
            except ElementClickInterceptedException:
                attempts += 1
                self.driver.execute_script("window.scrollBy(0, 50);")
        raise Exception(f"No se pudo añadir {product_name} al carrito después de {max_attempts} intentos")

    def go_to_cart(self):
        """Navega al carrito de forma segura"""
        self.wait_for_toasts_to_disappear()  # Por si hay un toast activo
        cart_btn = self.wait_for_element_clickable(self.checkout_button)
        cart_btn.click()
        return CartPage(self.driver)