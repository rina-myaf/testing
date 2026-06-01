import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from config import Config


class TestCart:

    @pytest.mark.parametrize("username", [
        Config.LOGIN_STANDARD,
        Config.LOGIN_PROBLEM
    ])
    def test_add_to_cart_and_remove_standard(self, driver, username):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(username, Config.PASSWORD)

        inventory_page = InventoryPage(driver)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
        )

        add_buttons = driver.find_elements(*inventory_page.ADD_TO_CART_BTN)
        assert len(add_buttons) > 0, "Нет кнопок Add to cart на странице"

        driver.execute_script("arguments[0].click();", add_buttons[0])

        time.sleep(1)

        driver.get("https://www.saucedemo.com/cart.html")

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cart_list"))
        )

        cart_page = CartPage(driver)

        cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
        assert len(cart_items) == 1, f"В корзине {len(cart_items)} товаров, ожидается 1"

        remove_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(cart_page.REMOVE_BTN)
        )

        driver.execute_script("arguments[0].click();", remove_btn)

        time.sleep(1)

        cart_items_after = driver.find_elements(By.CLASS_NAME, "cart_item")
        assert len(cart_items_after) == 0, f"Товар не удалился, в корзине {len(cart_items_after)} товар(ов)"