from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config import Config

class LoginPage(BasePage):
    # Locators
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def open(self):
        self.driver.get(Config.BASE_URL)

    def login(self, username, password):
        self.input_text(self.USERNAME_INPUT, username)
        self.input_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)

class TestLoginNegative:

    def test_login_empty_username(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("", Config.PASSWORD)

        error = login_page.get_error_message()
        assert "Username is required" in error

    def test_login_empty_password(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(Config.LOGIN_STANDARD, "")

        error = login_page.get_error_message()
        assert "Password is required" in error

    def test_login_locked_out_user(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("locked_out_user", Config.PASSWORD)

        error = login_page.get_error_message()
        assert "locked out" in error