import time

import allure
import pyautogui
import pytest
from _pytest import config
from allure_commons.types import AttachmentType
from selenium import webdriver

from utilities import ReadConfiguration


@pytest.fixture()
def log_on_failure(request):
    yield
    item = request.node
    if item.rep_call.failed:
        allure.attach(driver.get_screenshot_as_png(), name = "failed_test", attachment_type=AttachmentType.PNG)


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture()
def setup_and_teardown(request):
    browser = ReadConfiguration.read_configuration("basic info", "browser")
    global driver
    # Initialize the WebDriver based on the browser name
    if browser.__eq__("chrome"):
        driver = webdriver.Chrome()
    elif browser.__eq__("firefox"):
        driver = webdriver.Firefox()
    elif browser.__eq__("edge"):
        driver = webdriver.Edge()
    else:
        raise ValueError("Provide a valid browser name from this list chrome/firefox/edge")

    driver.maximize_window()
    login_url = ReadConfiguration.read_configuration("basic info", "loginUrl")
    driver.get(login_url)
    request.cls.driver = driver

    # Perform zoom out using keyboard
    for _ in range(2):
        pyautogui.hotkey('ctrl', '-')
        time.sleep(0.5)
    yield
    driver.quit()
