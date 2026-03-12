import time

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


def test_login():
    driver: WebDriver = webdriver.Chrome()
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


    driver.close()

def test_training():
    driver: WebDriver = webdriver.Chrome()
    driver.get("http://localhost:2218/?uid=test")
    id = "training-link"
    element = driver.find_element(By.ID, id)
    assert element is not None
    element.click()
    #assert  driver.current_url == "http://165.154.213.241:2218/static/task_uncover.html?uid=test"

    # driver: WebDriver = webdriver.Chrome()
    # driver.get("http://localhost:2218/static/no_new_words.html?uid=test")
    # href = "static/main.html"
    # elements = driver.find_elements(By.LINK_TEXT,href )
    # assert element is not None
    # element.click()

    driver.close()


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



