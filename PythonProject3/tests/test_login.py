import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from config import Config

class TestLogin:
    def test_valid_login_standard_user(self, driver, base_url):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(Config.LOGIN_STANDARD, Config.PASSWORD)

        inventory_page = InventoryPage(driver)
        assert inventory_page.is_element_visible(inventory_page.CART_ICON), "Логин не удался"

    def test_valid_login_problem_user(self, driver, base_url):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(Config.LOGIN_PROBLEM, Config.PASSWORD)

        inventory_page = InventoryPage(driver)
        assert inventory_page.is_element_visible(inventory_page.CART_ICON), "Логин не удался"

    def test_invalid_login(self, driver, base_url):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("wrong_user", "wrong_pass")

        error = login_page.get_error_message()
        assert "Username and password do not match" in error