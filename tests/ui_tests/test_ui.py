from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver



def test_icon_click():
    driver: WebDriver = webdriver.Chrome()
    try:
        driver.get("http://localhost:2218/")
        xpath = '//*[@id="main-rat"]'
        element = driver.find_element(By.XPATH, xpath)
    finally:
        driver.close()
    assert element is not None