import time
import pytest
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC, expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from test.test_Registration import generate_email_with_timestamp


@pytest.mark.usefixtures("setup_and_teardown", "log_on_failure")
class TestManagement:
    def test_verify_integration_bridge_all_icons(self):
        # Enter valid credentials
        self.driver.find_element(By.ID, "login_username").send_keys("depenad165@luravel.com")
        self.driver.find_element(By.ID, "login_password").send_keys("Raunak@8390")

        # Select remember me checkbox
        self.driver.find_element(By.ID, "login_checkbox-input").click()

        # Submit login form
        self.driver.find_element(By.ID, "login_submit").click()

        # Click on eZintegration icon
        wait = WebDriverWait(self.driver, 10)
        integration_icon = wait.until(
            expected_conditions.element_to_be_clickable((By.ID, "dashboard_ib_list")))
        self.driver.execute_script("arguments[0].click();", integration_icon)

        # Verify start button
        start_button = wait.until(expected_conditions.element_to_be_clickable((By.ID, "ib_list_start_service")))
        self.driver.execute_script("arguments[0].click();", start_button)
        start_button_message = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, "//div[@class='alert-message sc-ion-alert-md']")))
        assert start_button_message.is_displayed(), "Start button message is not displayed after starting the service"
        # self.driver.find_element(By.XPATH, "//span[@class='alert-button-inner sc-ion-alert-md']").click()
        wait.until(expected_conditions.element_to_be_clickable(self.driver.find_element(By.XPATH, "//span[@class='alert-button-inner sc-ion-alert-md']"))).click()

        # Verify stop button
        stop_button = wait.until(expected_conditions.element_to_be_clickable((By.ID, "ib_list_stop_service")))
        self.driver.execute_script("arguments[0].click();", stop_button)
        stop_button_message = wait.until(expected_conditions.visibility_of_element_located(
            (By.XPATH, "//div[@class='alert-message sc-ion-alert-md']")))
        assert stop_button_message.is_displayed(), "Stop button message is not displayed after stopped the service"

        # wait.until(expected_conditions.element_to_be_clickable(self.driver.find_element(By.XPATH, "//span[@class='alert-button-inner sc-ion-alert-md']"))).click()

        time.sleep(3)
