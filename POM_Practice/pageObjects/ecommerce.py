from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.browserutils import BrowserUtils
from POM_Practice.pageObjects.cart import CartPage

class EcommercePage(BrowserUtils):
    def __init__(self, driver):
        super().__init__(driver)
        self.product_link = (By.XPATH, "//div[contains(@class, 'products')]/div")
        self.product_name_check = (By.XPATH, ".//a[contains(@class, 'font-oswald')]")
        self.checkout_button = (By.XPATH, "//div[contains(@class, 'profile')]//span[@role='button']")

    def wait_for_toast_to_disappear(self, timeout=10):
        """Espera a que cualquier toast desaparezca antes de intentar click."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element((By.XPATH, "//li[contains(@data-sonner-toast, '')]"))
            )
        except TimeoutException:
            pass

    def add_product_to_cart(self, product_name):
        products = self.driver.find_elements(*self.product_link)

        for product in products:
            productName = product.find_element(*self.product_name_check).text
            if productName == product_name:
                add_to_cart = product.find_element(By.XPATH, ".//button[normalize-space()='Add to cart']")

                # Scroll button into view
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_to_cart)

                attempts = 0
                max_attempts = 5
                while attempts < max_attempts:
                    try:
                        # Espera a que no haya toasts activos
                        WebDriverWait(self.driver, 5).until(
                            EC.invisibility_of_element_located((By.CSS_SELECTOR, "li[data-type='success']"))
                        )
                        add_to_cart.click()
                        
                        # Comprobar si se cambió el texto
                        if add_to_cart.text.strip() == "Remove from cart":
                            return
                    except (ElementClickInterceptedException, TimeoutException):
                        attempts += 1
                raise Exception(f"Could not click 'Add to cart' for {product_name} after {max_attempts} attempts")

    def go_to_cart(self):
        # Esperar a que los toasts desaparezcan
        try:
            toast = (By.CSS_SELECTOR, "li[data-sonner-toast]")  # selector del toast
            WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located(toast))
        except:
            pass  # si no aparece toast, seguir

        # Ahora sí hacer click en el carrito
        checkout_button = self.checkout_button
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(checkout_button))
        self.driver.find_element(*checkout_button).click()
        return CartPage(self.driver)