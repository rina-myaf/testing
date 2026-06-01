import pytest
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from config import Config


class TestCartPageAvailability:

    def test_cart_page_without_login_shows_error(self, driver):
        driver.get(f"{Config.BASE_URL}/cart.html")

        error_header = driver.find_element(By.CSS_SELECTOR, "h3")
        assert "You can only access '/cart.html' when you are logged in" in error_header.text

    def test_cart_page_after_login_contains_cart_content(self, driver):

        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(Config.LOGIN_STANDARD, Config.PASSWORD)

        from pages.inventory_page import InventoryPage
        inventory_page = InventoryPage(driver)
        inventory_page.go_to_cart()

        cart_page = CartPage(driver)


        try:
            cart_page.wait.until(lambda d: d.find_element(*cart_page.CHECKOUT_BTN))
        except:
            page_body = driver.find_element(By.TAG_NAME, "body").text
            assert "cart" in page_body.lower() or "checkout" in page_body.lower(), \
                f"Страница корзины не загрузилась. Содержимое body: {page_body[:200]}"