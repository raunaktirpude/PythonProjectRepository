import time

import pyautogui
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


@pytest.mark.usefixtures("setup_and_teardown", "log_on_failure")
class TestLogin:
    def test_verify_login_with_valid_credentials(self):
        # Enter valid credentials
        self.driver.find_element(By.ID, "login_username").send_keys("todafeh107@luravell.com")
        self.driver.find_element(By.ID, "login_password").send_keys("Raunak@8390")

        # Select remember me checkbox
        self.driver.find_element(By.ID, "login_checkbox-input").click()

        # Click on login submit button
        self.driver.find_element(By.ID, "login_submit").click()

        # Wait for the "Organization Admin" element to be visible
        organization_admin_element = WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located((By.XPATH, "//span["
                                                                         "@class='profile"
                                                                         "-name']"
                                                               )))

        # Assert that the "Organization Admin" element is displayed
        assert organization_admin_element.is_displayed(), "Organization Admin text is not displayed after login"

    def test_verify_login_with_invalid_username(self):
        # Enter valid credentials
        self.driver.find_element(By.ID, "login_username").send_keys("todafeh107@luravell.co")
        self.driver.find_element(By.ID, "login_password").send_keys("Raunak@8390")

        # Select remember me checkbox
        self.driver.find_element(By.ID, "login_checkbox-input").click()

        # Click on login submit button
        self.driver.find_element(By.ID, "login_submit").click()

        # Assertion to verify the URL after providing wrong username
        assert self.driver.current_url == "https://carbon.bizdata360.com/#/login", (
            "The URL after providing invalid username "
            "is not as expected")

    def test_verify_login_with_invalid_password(self):
        # Enter valid credentials
        self.driver.find_element(By.ID, "login_username").send_keys("todafeh107@luravell.com")
        self.driver.find_element(By.ID, "login_password").send_keys("Raunak@839")

        # Select remember me checkbox
        self.driver.find_element(By.ID, "login_checkbox-input").click()

        # Click on login submit button
        self.driver.find_element(By.ID, "login_submit").click()

        # Wait for the Attempt remaining text element to be visible
        attempt_remaining = WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(
                (By.XPATH, "//div[@class='error-message ng-star-inserted']"
                 )))

        # Assert that the Attempt remaining text element is displayed
        assert attempt_remaining.is_displayed(), "Attempt remaining text is not displayed after click on submit button"

    def test_verify_all_hyperlinks(self):
        # Verify forgot password link
        self.driver.find_element(By.ID, "login_forgot_password").click()

        # Wait for the "forgot password page" element to be visible
        forgot_page_text = WebDriverWait(self.driver, 0).until(
            expected_conditions.visibility_of_element_located(
                (By.XPATH, "//h2[normalize-space()='Reset Your Password']"))
        )

        # Assert that the "Forgot password" element is displayed
        assert forgot_page_text.is_displayed(), (
            "Reset Your Password text is not displayed after click on forgot password "
            "link")

        # Navigate back to login page
        self.driver.back()

        # Verify sign in link
        self.driver.find_element(By.XPATH, "//a[normalize-space()='Try it here']").click()
        signin_page_text = WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(
                (By.XPATH, "//span[normalize-space()='Real Time Cloud Based Integration Platform']"))
        )

        # Assert that the "Sign in page" element is displayed
        assert signin_page_text.is_displayed(), (
            "Real Time Cloud Based Integration Platform text is not displayed after "
            "click on sign in link")
