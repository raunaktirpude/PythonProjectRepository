import time
from datetime import datetime

import pytest
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import pyautogui


def generate_email_with_timestamp():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"testing_{timestamp}@gmail.com"


@pytest.mark.usefixtures("setup_and_teardown", "log_on_failure")
class TestLogin:
    def test_registration_with_valid_data(self):
        # Navigate to the registration page
        wait = WebDriverWait(self.driver, 10)
        wait.until(
            expected_conditions.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Try it here']"))).click()

        # Enter registration data and submit the form
        wait.until(expected_conditions.visibility_of_element_located((By.ID, "signup_firstname"))).send_keys(
            "TestFirstName")
        self.driver.find_element(By.ID, "signup_lastname").send_keys("TestLastName")
        self.driver.find_element(By.XPATH, "//input[@placeholder='Work email Address']").send_keys(
            generate_email_with_timestamp())
        self.driver.find_element(By.ID, "signup_phone").send_keys("9284673452")
        self.driver.find_element(By.ID, "signup_job").click()
        self.driver.find_element(By.XPATH, "//mat-option[@id='mat-option-1']").click()
        self.driver.find_element(By.ID, "signup_employee").click()
        self.driver.find_element(By.XPATH, "//mat-option[@id='mat-option-10']").click()
        self.driver.find_element(By.ID, "signup_company").send_keys("Test Company")
        self.driver.find_element(By.XPATH, "//mat-select[@formcontrolname='country']").click()
        wait.until(
            expected_conditions.element_to_be_clickable((By.XPATH, "//mat-option[@id='mat-option-117']"))).click()

        self.driver.find_element(By.ID, "signup_checkbox-input").click()
        signup_submit_button = self.driver.find_element(By.ID, "signup_submit")
        self.driver.execute_script("arguments[0].scrollIntoView();", signup_submit_button)
        self.driver.execute_script("arguments[0].click();", signup_submit_button)

        # Verify successful registration
        success_message = WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located((By.ID, "alert-2-hdr"))
        )
        assert success_message.is_displayed(), "Success message not displayed after registration"

    def test_registration_with_empty_data(self):
        # Navigate to the registration page
        wait = WebDriverWait(self.driver, 10)
        wait.until(
            expected_conditions.visibility_of_element_located(
                (By.XPATH, "//a[normalize-space()='Try it here']"))).click()

        # Click on sign up submit
        # wait.until(expected_conditions.visibility_of_element_located((By.ID, "signup_submit"))).click()
        time.sleep(2)
        signup_submit_button = self.driver.find_element(By.ID, "signup_submit")
        self.driver.execute_script("arguments[0].scrollIntoView();", signup_submit_button)
        self.driver.execute_script("arguments[0].click();", signup_submit_button)

        # Verify error messages for all mandatory fields
        # First Name error message verification
        expectedFirstNameMessage = "First Name is Required!"
        assert self.driver.find_element(By.ID, "mat-mdc-error-0").text.__contains__(expectedFirstNameMessage)

        # Last Name error message verification
        expectedLastNameMessage = "Last Name is Required!"
        assert self.driver.find_element(By.ID, "mat-mdc-error-1").text.__contains__(expectedLastNameMessage)

        # Phone error message verification
        expectedPhoneMessage = "Phone Number is Required!"
        assert self.driver.find_element(By.ID, "mat-mdc-error-2").text.__contains__(expectedPhoneMessage)

        # Company error message verification
        expectedCompanyMessage = "Company Name is Required!"
        assert self.driver.find_element(By.ID, "mat-mdc-error-3").text.__contains__(expectedCompanyMessage)

        # Checkbox error message verification
        expectedCheckboxMessage = "Please accept Master subscription."
        assert self.driver.find_element(By.ID, "mat-mdc-error-4").text.__contains__(expectedCheckboxMessage)

    def test_registration_with_invalid_data(self):
        # Navigate to the registration page
        wait = WebDriverWait(self.driver, 10)
        wait.until(
            expected_conditions.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Try it here']"))).click()

        # Enter registration data and submit the form
        wait.until(expected_conditions.visibility_of_element_located((By.ID, "signup_firstname"))).send_keys("!@#$")
        self.driver.find_element(By.ID, "signup_lastname").send_keys("!@#$")
        self.driver.find_element(By.ID, "signup_phone").send_keys("!@#$")

        # Press the Tab key
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.TAB).perform()

        # First Name error message verification
        expectedFirstNameMessage = "First Name Allows Alphanumeric Only!"
        assert self.driver.find_element(By.XPATH,
                                        "//mat-error[normalize-space()='First Name Allows Alphanumeric Only!']").text.__contains__(
            expectedFirstNameMessage)

        # Last Name error message verification
        expectedLastNameMessage = "Last Name Allows Alphanumeric Only!"
        assert self.driver.find_element(By.XPATH,
                                        "//mat-error[normalize-space()='Last Name Allows Alphanumeric Only!']").text.__contains__(
            expectedLastNameMessage)

        # Phone error message verification
        expectedPhoneMessage = "Please Enter a Valid 10 digit Phone Number"
        assert self.driver.find_element(By.XPATH,
                                        "//mat-error[normalize-space()='Please Enter a Valid 10 digit Phone Number']").text.__contains__(
            expectedPhoneMessage)

    def test_handle_signin_url(self):
        # Navigate to the registration page
        wait = WebDriverWait(self.driver, 10)
        wait.until(
            expected_conditions.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Try it here']"))).click()

        # Click on sign up submit
        time.sleep(2)
        # signin_url = wait.until(expected_conditions.visibility_of_element_located((By.ID, "signup_signin")))
        signin_url = self.driver.find_element(By.ID, "signup_signin")
        self.driver.execute_script("arguments[0].scrollIntoView();", signin_url)
        self.driver.execute_script("arguments[0].click();", signin_url)

        # Assertion to verify the URL after click on sign in
        assert self.driver.current_url == "https://carbon.bizdata360.com/#/login", (
            "The URL after click on sign in is not as "
            "expected")
