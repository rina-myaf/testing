from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-notifications")

    driver_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chromedriver.exe")

    if not os.path.exists(driver_path):
        driver_path = "chromedriver.exe"

    if not os.path.exists(driver_path):
        raise FileNotFoundError(f"chromedriver.exe не найден по пути: {driver_path}\n"
                                f"Скачайте chromedriver.exe с https://googlechromelabs.github.io/chrome-for-testing/\n"
                                f"и положите в папку: {os.path.dirname(os.path.dirname(__file__))}")

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    return driver