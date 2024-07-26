import os
import random
import time
import pyautogui
from configparser import ConfigParser

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

file_path = os.path.join(os.getcwd(), "Configuration", "change password.ini")


def generate_change_password_with_random_int():
    random_int = random.randint(1000, 9999)
    return f"Testing@{random_int}"


def read_config(category, key):
    config = ConfigParser()
    config.read(file_path)
    return config.get(category, key)


def write_new_password(new_password):
    config = ConfigParser()
    config['DEFAULT'] = {'current_password': new_password}
    with open(file_path, 'w') as configfile:
        config.write(configfile)


@pytest.mark.usefixtures("setup_and_teardown", "log_on_failure")
class TestChangePassword:

    def test_verify_change_password_with_mandatory_fields(self):
        current_password = read_config("DEFAULT", "current_password")

        # Enter valid credentials
        self.driver.find_element(By.ID, "login_username").send_keys("naselip166@kinsef.com")
        self.driver.find_element(By.ID, "login_password").send_keys(current_password)

        # Select remember me checkbox
        self.driver.find_element(By.ID, "login_checkbox-input").click()

        # Click on login submit button
        self.driver.find_element(By.ID, "login_submit").click()

        # Click on settings button
        # WebDriverWait(driver, 10).until(
        #     expected_conditions.element_to_be_clickable((By.XPATH, "//mat-icon[normalize-space()='settings']"))).click()
        element = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable((By.XPATH, "//mat-icon[normalize-space()='settings']")))
        self.driver.execute_script("arguments[0].click();", element)

        # Click on change password button
        self.driver.find_element(By.XPATH, "//div[normalize-space()='Change Password']").click()

        # Enter old password
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable((By.XPATH, "//input[@placeholder='Old Password']")))
        self.driver.find_element(By.XPATH, "//input[@placeholder='Old Password']").send_keys(current_password)

        # Generate and enter new password
        new_password_value = generate_change_password_with_random_int()
        self.driver.find_element(By.XPATH, "//input[@formcontrolname='newPassword']").send_keys(new_password_value)

        # Confirm password
        self.driver.find_element(By.XPATH, "//input[@formcontrolname='confirmPassword']").send_keys(new_password_value)

        # Write the new password back to the configuration file
        write_new_password(new_password_value)

        # Click on change password submit button
        self.driver.find_element(By.XPATH,
                                 "//*[@id='main-content']/app-base-app/div/div/app-change-password-new/ion-content/div/div/div"
                                 "/div/mat-card/mat-card-content/div/form/div/button/span[2]").click()

        # Assertion to verify the URL after click on forgot password submit button
        WebDriverWait(self.driver, 10).until(expected_conditions.url_to_be("https://carbon.bizdata360.com/#/login"))

        assert self.driver.current_url == "https://carbon.bizdata360.com/#/login", "The URL after click on change password submit button is not as expected"

    def test_verify_change_password_with_empty_mandatory_fields(self):
        current_password = read_config("DEFAULT", "current_password")

        # Enter valid credentials
        self.driver.find_element(By.ID, "login_username").send_keys("naselip166@kinsef.com")
        self.driver.find_element(By.ID, "login_password").send_keys(current_password)

        # Select remember me checkbox
        self.driver.find_element(By.ID, "login_checkbox-input").click()

        # Click on login submit button
        self.driver.find_element(By.ID, "login_submit").click()

        # Click on settings button
        # WebDriverWait(driver, 10).until(
        #     expected_conditions.element_to_be_clickable((By.XPATH, "//mat-icon[normalize-space()='settings']"))).click()
        element = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable((By.XPATH, "//mat-icon[normalize-space()='settings']")))
        self.driver.execute_script("arguments[0].click();", element)

        # Click on change password button
        self.driver.find_element(By.XPATH, "//div[normalize-space()='Change Password']").click()

        # Click on forgot password submit button
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                (
                    By.XPATH,
                    "//*[@id='main-content']/app-base-app/div/div/app-change-password-new/ion-content/div/div/div"
                    "/div/mat-card/mat-card-content/div/form/div/button/span[2]")
            )
        )
        self.driver.find_element(By.XPATH,
                                 "//*[@id='main-content']/app-base-app/div/div/app-change-password-new/ion-content/div/div/div"
                                 "/div/mat-card/mat-card-content/div/form/div/button/span[2]").click()

        # New password field error message verification
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located((By.XPATH, "//mat-error[@aria-atomic='true']")))
        expectedNewPasswordFieldMessage = ("Password must have atleast 8 Characters, 1 Number, 1 Special Character, "
                                           "1 Lowercase Character, 1 Upper Character.")
        assert self.driver.find_element(By.XPATH, "//mat-error[@aria-atomic='true']").text.__contains__(
            expectedNewPasswordFieldMessage)

        self.driver.quit()

    def test_verify_change_password_with_same_password(self):
        current_password = read_config("DEFAULT", "current_password")

        # Enter valid credentials
        self.driver.find_element(By.ID, "login_username").send_keys("naselip166@kinsef.com")
        self.driver.find_element(By.ID, "login_password").send_keys(current_password)

        # Select remember me checkbox
        self.driver.find_element(By.ID, "login_checkbox-input").click()

        # Click on login submit button
        self.driver.find_element(By.ID, "login_submit").click()

        # Click on settings button
        # WebDriverWait(driver, 10).until(
        #     expected_conditions.element_to_be_clickable((By.XPATH, "//mat-icon[normalize-space()='settings']"))).click()
        element = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable((By.XPATH, "//mat-icon[normalize-space()='settings']")))
        self.driver.execute_script("arguments[0].click();", element)

        # Click on change password button
        self.driver.find_element(By.XPATH, "//div[normalize-space()='Change Password']").click()

        # Enter old password
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable((By.XPATH, "//input[@placeholder='Old Password']")))
        self.driver.find_element(By.XPATH, "//input[@placeholder='Old Password']").send_keys(current_password)

        # Generate and enter new password
        self.driver.find_element(By.XPATH, "//input[@formcontrolname='newPassword']").send_keys(current_password)

        # Confirm password
        self.driver.find_element(By.XPATH, "//input[@formcontrolname='confirmPassword']").send_keys(current_password)

        # Click on forgot password submit button
        self.driver.find_element(By.XPATH,
                                 "//*[@id='main-content']/app-base-app/div/div/app-change-password-new/ion-content/div/div/div"
                                 "/div/mat-card/mat-card-content/div/form/div/button/span[2]").click()

        # Assertion to verify the URL after click on forgot password submit button
        assert self.driver.current_url == "https://carbon.bizdata360.com/#/baseapp/change-password-new", (
            "The URL after click "
            "on change password"
            "submit button is "
            "not as expected")
