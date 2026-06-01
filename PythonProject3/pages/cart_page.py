from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config import Config

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config import Config
from selenium.webdriver.support.ui import WebDriverWait

class CartPage(BasePage):
    CART_ITEM = (By.CLASS_NAME, "cart_item")
    REMOVE_BTN = (By.CSS_SELECTOR, "[data-test^='remove-']")  # Ищем по data-test, начинающемуся с remove-
    CHECKOUT_BTN = (By.ID, "checkout")
    CONTINUE_SHOPPING_BTN = (By.XPATH, "//button[text()='Continue Shopping']")

    def get_cart_items_count(self):
        from selenium.webdriver.support import expected_conditions as EC
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "cart_list"))
            )
        except:
            pass
        return len(self.driver.find_elements(*self.CART_ITEM))

    def click_remove(self):
        from selenium.webdriver.support import expected_conditions as EC
        # Ждём, когда кнопка станет кликабельной
        remove_btn = self.wait.until(EC.element_to_be_clickable(self.REMOVE_BTN))
        remove_btn.click()

    def is_item_removed(self):
        import time
        time.sleep(1)
        return len(self.driver.find_elements(*self.CART_ITEM)) == 0

    def click_continue_shopping(self):
        self.click(self.CONTINUE_SHOPPING_BTN)

    def open(self):
        self.driver.get(f"{Config.BASE_URL}/cart.html")