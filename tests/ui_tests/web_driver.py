from selenium import webdriver
import pytest
from selenium.webdriver.chrome.webdriver import WebDriver

@pytest.fixture
def chrome_web_driver() -> WebDriver:
    driver: WebDriver = webdriver.Chrome()
    try:
        yield driver
    finally:
        driver.close()