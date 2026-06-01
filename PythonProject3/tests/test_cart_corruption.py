import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from config import Config


class TestCartCorruption:

    def test_problem_user_item_page_has_invalid_price(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(Config.LOGIN_PROBLEM, Config.PASSWORD)

        driver.get("https://www.saucedemo.com/inventory-item.html?id=6")

        price_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_details_price"))
        )
        price_text = price_element.text

        assert "√-1" not in price_text, f"Цена содержит √-1, а не должна: {price_text}"

    def test_problem_user_remove_button_appears_after_add(self, driver):
        """Проверка, что кнопка Remove появляется и работает после добавления товара"""
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(Config.LOGIN_PROBLEM, Config.PASSWORD)

        driver.get("https://www.saucedemo.com/inventory-item.html?id=6")

        add_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Add to cart']"))
        )
        driver.execute_script("arguments[0].click();", add_button)

        try:
            remove_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//button[text()='Remove']"))
            )
        except:
            pytest.fail("БАГ: кнопка Remove не появилась после добавления товара")

        driver.execute_script("arguments[0].click();", remove_button)

        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//button[text()='Add to cart']"))
            )
        except:
            pytest.fail("БАГ: после клика на Remove кнопка не вернулась в состояние Add to cart")

    def test_problem_user_cart_contains_item_after_add(self, driver):
        """Проверка, что товар отображается в корзине после добавления"""
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(Config.LOGIN_PROBLEM, Config.PASSWORD)

        driver.get("https://www.saucedemo.com/inventory-item.html?id=6")

        add_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Add to cart']"))
        )
        driver.execute_script("arguments[0].click();", add_button)

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
        )

        driver.get("https://www.saucedemo.com/cart.html")

        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "cart_list"))
            )
        except:
            pytest.fail("БАГ: страница корзины не загрузилась (cart_list не найден)")

        cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
        assert len(cart_items) == 1, f"В корзине {len(cart_items)} товаров, ожидается 1"

        item_name = driver.find_element(By.CLASS_NAME, "inventory_item_name").text
        assert item_name == "Sauce Labs Fleece Jacket", f"В корзине {item_name}"

        remove_in_cart = driver.find_element(By.XPATH, "//button[text()='Remove']")
        driver.execute_script("arguments[0].click();", remove_in_cart)

        import time
        time.sleep(1)

        cart_items_after = driver.find_elements(By.CLASS_NAME, "cart_item")
        assert len(cart_items_after) == 0, "Товар не удалился из корзины"
