import pytest
from utils.driver_factory import get_driver

@pytest.fixture
def driver():
    driver = get_driver()
    yield driver
    driver.quit()

@pytest.fixture
def base_url():
    from config import Config
    return Config.BASE_URL