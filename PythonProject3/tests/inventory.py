from selenium.webdriver.common.by import By


import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from config import Config


class TestInventory:

    def test_add_multiple_items_to_cart_standard(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(Config.LOGIN_STANDARD, Config.PASSWORD)

        inventory_page = InventoryPage(driver)
        add_buttons = driver.find_elements(*inventory_page.ADD_TO_CART_BTN)
        for btn in add_buttons:
            btn.click()

        cart_count = driver.find_element(*inventory_page.CART_BADGE).text
        assert int(cart_count) == len(add_buttons)

    def test_product_details_page(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(Config.LOGIN_STANDARD, Config.PASSWORD)

        driver.find_element(*InventoryPage.ITEM_NAME).click()

        assert "inventory-item.html" in driver.current_url

    def test_sort_by_price_low_to_high(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(Config.LOGIN_STANDARD, Config.PASSWORD)

        from selenium.webdriver.support.ui import Select
        sort_dropdown = Select(driver.find_element(By.CLASS_NAME, "product_sort_container"))
        sort_dropdown.select_by_value("lohi")

        prices = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
        price_values = [float(p.text.replace("$", "")) for p in prices]
        assert price_values == sorted(price_values)