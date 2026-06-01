from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class InventoryPage(BasePage):
    # Локаторы - проверьте, что они правильные
    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")
    ADD_TO_CART_BTN = (By.XPATH, "//button[text()='Add to cart']")
    REMOVE_BTN = (By.XPATH, "//button[text()='Remove']")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    PROBLEM_ITEM_ADD_BTN = (By.XPATH,
                            "//div[contains(text(),'Sauce Labs Fleece Jacket')]/ancestor::div[@class='inventory_item']//button")

    def add_first_item_to_cart(self):
        """Добавляет первый товар в корзину"""
        buttons = self.driver.find_elements(*self.ADD_TO_CART_BTN)
        if buttons:
            buttons[0].click()
        else:
            raise Exception("Нет кнопок Add to cart на странице")

    def go_to_cart(self):
        self.click(self.CART_ICON)