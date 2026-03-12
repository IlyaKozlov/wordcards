import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from utils_for_test import fill_db  # noqa
from web_driver import chrome_web_driver as driver


def test_icon_click(driver):
    driver.get("http://localhost:2218/")
    xpath = '//*[@id="main-rat"]'
    element = driver.find_element(By.XPATH, xpath)
    assert element is not None


def test_login(driver):
    driver.get("http://localhost:2218/")
    id = "login-link"
    element = driver.find_element(By.ID, id)
    assert  element is not None
    element.click()
    assert driver.current_url == "http://localhost:2218/static/login.html"

    input_form = driver.find_element(By.ID, "uid")
    input_form.send_keys("test")

    submit = driver.find_element(By.ID, "okBtn")
    submit.click()


def test_training(fill_db: None, driver):
      check_params("http://localhost:2218/static/task_uncover.html", "?uid=test", driver)

def test_training_new_user(driver):
    check_params("http://localhost:2218/static/no_new_words.html", "?uid=dvarf", driver)
    href = "Main Page"
    element = driver.find_element(By.LINK_TEXT, href)
    assert element is not None
    element.click()
    assert driver.current_url == "http://localhost:2218/static/main.html"

def check_params(expected_prefix, uid, driver):
    expected = expected_prefix + uid
    driver.get("http://localhost:2218/" + uid)
    id = "training-link"
    element = driver.find_element(By.ID, id)
    assert element is not None
    element.click()
    time.sleep(1)
    assert driver.current_url == expected


def test_uncover():
    driver: WebDriver = webdriver.Chrome()
    driver.get("http://localhost:2218/?uid=test")
    id = "uncover-link"
    element = driver.find_element(By.ID, id)
    assert element is not None
    element.click()

    driver.close()

def test_book_upload():
    driver: WebDriver = webdriver.Chrome()
    driver.get("http://localhost:2218/?uid=test")
    id = "book-upload-link"
    element = driver.find_element(By.ID, id)
    assert element is not None
    element.click()

    driver.close()

def test_translate():
    driver: WebDriver = webdriver.Chrome()
    driver.get("http://localhost:2218/?uid=test")
    id = "translate-link"
    element = driver.find_element(By.ID, id)
    assert element is not None
    element.click()

    driver.close()



