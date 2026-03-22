import time
from typing import Any

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from utils_for_test import fill_db, service_running  # noqa
from web_driver import chrome_web_driver as driver  # noqa


@pytest.mark.skipif(not service_running(), reason="service not running")
def test_icon_click(driver: WebDriver) -> None:
    driver.get("http://localhost:2218/")
    xpath: str = '//*[@id="main-rat"]'
    element: WebElement = driver.find_element(By.XPATH, xpath)
    assert element is not None


@pytest.mark.skipif(not service_running(), reason="service not running")
def test_login(driver: WebDriver) -> None:
    driver.get("http://localhost:2218/")
    uid: str = "login-link"
    element: WebElement = driver.find_element(By.ID, uid)
    assert element is not None
    element.click()
    assert driver.current_url == "http://localhost:2218/static/login.html"

    input_form: WebElement = driver.find_element(By.ID, "uid")
    input_form.send_keys("test")

    submit: WebElement = driver.find_element(By.ID, "okBtn")
    submit.click()


@pytest.mark.skipif(not service_running(), reason="service not running")
def test_training(fill_db: Any, driver: WebDriver) -> None:
    check_params("http://localhost:2218/static/task_uncover.html", "?uid=test", driver)


@pytest.mark.skipif(not service_running(), reason="service not running")
def test_training_new_user(driver: WebDriver) -> None:
    check_params("http://localhost:2218/static/no_new_words.html", "?uid=dvarf", driver)
    href: str = "Main Page"
    element: WebElement = driver.find_element(By.LINK_TEXT, href)
    assert element is not None
    element.click()
    assert driver.current_url == "http://localhost:2218/static/main.html"


def check_params(expected_prefix: str, uid: str, driver: WebDriver) -> None:
    expected: str = expected_prefix + uid
    driver.get("http://localhost:2218/" + uid)
    element_id: str = "training-link"
    element: WebElement = driver.find_element(By.ID, element_id)
    assert element is not None
    element.click()
    time.sleep(1)
    assert driver.current_url == expected


@pytest.mark.skipif(not service_running(), reason="service not running")
def test_uncover() -> None:
    driver: WebDriver = webdriver.Chrome()
    driver.get("http://localhost:2218/?uid=test")
    element_id: str = "uncover-link"
    element: WebElement = driver.find_element(By.ID, element_id)
    assert element is not None
    element.click()

    driver.close()


@pytest.mark.skipif(not service_running(), reason="service not running")
def test_book_upload() -> None:
    driver: WebDriver = webdriver.Chrome()
    driver.get("http://localhost:2218/?uid=test")
    element_id: str = "book-upload-link"
    element: WebElement = driver.find_element(By.ID, element_id)
    assert element is not None
    element.click()

    driver.close()


@pytest.mark.skipif(not service_running(), reason="service not running")
def test_translate() -> None:
    driver: WebDriver = webdriver.Chrome()
    driver.get("http://localhost:2218/?uid=test")
    element_id: str = "translate-link"
    element: WebElement = driver.find_element(By.ID, element_id)
    assert element is not None
    element.click()

    driver.close()
