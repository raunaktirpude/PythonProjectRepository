import time

import pyautogui
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


@pytest.mark.usefixtures("setup_and_teardown", "log_on_failure")
class TestForgotPassword:
    def test_verify_forgot_password_with_mandatory_fields(self):
        # Click on forgot password link
        self.driver.find_element(By.ID, "login_forgot_password").click()

        # Provide the email address
        self.driver.find_element(By.XPATH, "//input[@placeholder=' Email']").send_keys("todafeh107@luravell.com")

        # Click submit button
        self.driver.find_element(By.XPATH,
                                 "//*[@id=\"main-content\"]/app-forgot-password/ion-content/div/div/div/div/mat-card"
                                 "/mat-card-content/div[2]/div[2]/div[3]/form/div/button/span[2]").click()

        # Wait for password reset text element to be visible
        reset_text = WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located((By.XPATH, "//div[@class='text']")))

        # Assert that the "Password reset" text element is displayed
        assert reset_text.is_displayed(), ("Password reset text is not displayed after click on send button with email "
                                           "address")

    def test_verify_forgot_password_with_empty_fields(self):
        # Click on forgot password link
        self.driver.find_element(By.ID, "login_forgot_password").click()

        # Wait for the submit button to be clickable
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, "//body//app-root//ion-app//ion-router-outlet//app-forgot-password//ion-content"
                           "//div//div//div//div//mat-card//mat-card-content//div//div//div//form//div"
                           "//button[@type='submit']")
            )
        ).click()

        # Verify the URL after clicking the submit button with an empty email address
        assert self.driver.current_url == "https://carbon.bizdata360.com/#/forgot-password", (
            "The URL after clicking on the submit button with an empty email address is not as expected"
        )

    def test_verify_forgot_password_page_sign_in_url(self):
        # Click on forgot password link
        self.driver.find_element(By.ID, "login_forgot_password").click()

        # Wait for the "Sign in" link to be present
        wait = WebDriverWait(self.driver, 10)
        sign_link = wait.until(
            expected_conditions.element_to_be_clickable((By.XPATH, "//a[normalize-space("
                                                                   ")='Sign in']")))

        # Use JavascriptExecutor to click on the "Sign in" link
        self.driver.execute_script("arguments[0].click();", sign_link)

        # Wait for the URL to change to the expected login URL
        wait.until(expected_conditions.url_to_be("https://carbon.bizdata360.com/#/login"))

        # Assertion to verify the URL after clicking on sign-in link
        assert self.driver.current_url == "https://carbon.bizdata360.com/#/login", (
            "The URL after click on sing in button is "
            "not as expected")
