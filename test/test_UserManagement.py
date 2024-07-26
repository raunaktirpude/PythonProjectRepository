import time
import pytest
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from test.test_Registration import generate_email_with_timestamp


@pytest.mark.usefixtures("setup_and_teardown", "log_on_failure")
class TestManagement:
    def test_verify_create_user_with_mandatory_field(self):
        # Enter valid credentials
        self.driver.find_element(By.ID, "login_username").send_keys("depenad165@luravel.com")
        self.driver.find_element(By.ID, "login_password").send_keys("Raunak@8390")

        # Select remember me checkbox
        self.driver.find_element(By.ID, "login_checkbox-input").click()

        # Submit login form
        self.driver.find_element(By.ID, "login_submit").click()

        # Wait for the element to be clickable
        menu_button = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable((By.XPATH, "//ion-menu-button[@id='head_ham_btn']")))
        self.driver.execute_script("arguments[0].click();", menu_button)

        # Click on management
        management_button = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable((By.XPATH, "//ion-label[normalize-space()='Management']"))
        )
        self.driver.execute_script("arguments[0].click();", management_button)

        # Click on user option
        user_button = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable((By.XPATH, "//ion-label[normalize-space()='User']"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", user_button)
        self.driver.execute_script("arguments[0].click();", user_button)

        # Perform a right-click if the menu does not close
        # WebDriverWait.driverWait(self.driver,10).until(expected_conditions.invisibility_of_element_located(user_button))
        ActionChains(self.driver).move_by_offset(20, 10).context_click().perform()

        # Click on add button to open user add form
        add_button = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Add']")))
        self.driver.execute_script("arguments[0].click();", add_button)

        # Fill up add user form
        # First name
        self.driver.find_element(By.XPATH, "//input[@placeholder='First name']").send_keys("Create")

        # Last name
        self.driver.find_element(By.XPATH, "//input[@placeholder='Last name']").send_keys("User")

        # Email address
        self.driver.find_element(By.XPATH, "//input[@placeholder='Email Address']").send_keys(
            generate_email_with_timestamp())

        # User permission
        self.driver.find_element(By.XPATH, "//mat-select[@formcontrolname='permission']").click()
        self.driver.find_element(By.XPATH,
                                 "//mat-option[@role='option']//span[contains(text(),'List (User)')]").click()

        self.driver.find_element(By.XPATH,
                                 "//mat-option[@role='option']//span[contains(text(),'List (Integration Bridge)')]").click()

        # Perform Tab key press
        ActionChains(self.driver).send_keys(Keys.TAB).perform()

        # Make admin toggle button
        toggle_button = self.driver.find_element(By.XPATH, "//button[@role='switch']")
        toggle_button.click()
        time.sleep(0.5)
        toggle_button.click()

        # Click on add button to create or add user
        user_add_button = self.driver.find_element(By.XPATH, "//span[normalize-space()='Add']")
        user_add_button.click()

        # Wait for the URL to change to the expected URL
        expected_url = "https://carbon.bizdata360.com/#/baseapp/user"
        WebDriverWait(self.driver, 10).until(expected_conditions.url_to_be(expected_url))

        # Assert the URL
        assert self.driver.current_url == expected_url, "The URL after click on add button to create or add user is not as expected"

    def test_verify_create_user_with_empty_field(self):
        self.driver.find_element(By.ID, "login_username").send_keys("depenad165@luravel.com")
        self.driver.find_element(By.ID, "login_password").send_keys("Raunak@8390")

        # Select remember me checkbox
        self.driver.find_element(By.ID, "login_checkbox-input").click()

        # Submit login form
        self.driver.find_element(By.ID, "login_submit").click()

        # Wait for the menu button to be clickable and click it
        menu_button = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable((By.XPATH, "//ion-menu-button[@id='head_ham_btn']"))
        )
        self.driver.execute_script("arguments[0].click();", menu_button)

        # Click on management
        management_button = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable((By.XPATH, "//ion-label[normalize-space()='Management']"))
        )
        self.driver.execute_script("arguments[0].click();", management_button)

        # Click on user option
        user_button = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable((By.XPATH, "//ion-label[normalize-space()='User']"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", user_button)
        self.driver.execute_script("arguments[0].click();", user_button)

        # Perform a right-click if the menu does not close
        ActionChains(self.driver).move_by_offset(20, 10).context_click().perform()

        # Click on add button to open user add form
        add_button = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Add']"))
        )
        self.driver.execute_script("arguments[0].click();", add_button)

        # Click on add button to create or add user
        user_add_button = self.driver.find_element(By.XPATH, "//span[normalize-space()='Add']")
        user_add_button.click()

        # Verify error messages for all mandatory fields
        # First Name error message verification
        expected_first_name_error_message = "First Name Required"
        assert self.driver.find_element(By.XPATH,
                                        "//mat-error[normalize-space()='First Name Required']").text.__contains__(
            expected_first_name_error_message
        )

        # Last Name error message verification
        expected_last_name_error_message = "Last Name Required"
        assert self.driver.find_element(By.XPATH,
                                        "//mat-error[normalize-space()='Last Name Required']").text.__contains__(
            expected_last_name_error_message
        )

        # Email error message verification
        expected_email_error_message = "Work email Required."
        assert self.driver.find_element(By.XPATH,
                                        "//mat-error[normalize-space()='Work email Required.']").text.__contains__(
            expected_email_error_message
        )

        # User permission error message verification
        expected_user_permission_error_message = "Need to select permission"
        assert self.driver.find_element(By.XPATH,
                                        "//mat-error[normalize-space()='Need to select permission']").text.__contains__(
            expected_user_permission_error_message
        )

    def test_verify_user_view_more_icon(self):
        self.driver.find_element(By.ID, "login_username").send_keys("depenad165@luravel.com")
        self.driver.find_element(By.ID, "login_password").send_keys("Raunak@8390")

        # Select remember me checkbox
        self.driver.find_element(By.ID, "login_checkbox-input").click()

        # Submit login form
        self.driver.find_element(By.ID, "login_submit").click()

        # Wait for the element to be clickable
        menu_button = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable((By.XPATH, "//ion-menu-button[@id='head_ham_btn']")))
        self.driver.execute_script("arguments[0].click();", menu_button)

        # Click on management
        management_button = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable((By.XPATH, "//ion-label[normalize-space()='Management']"))
        )
        self.driver.execute_script("arguments[0].click();", management_button)

        # Click on user option
        user_button = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable((By.XPATH, "//ion-label[normalize-space()='User']"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", user_button)
        self.driver.execute_script("arguments[0].click();", user_button)

        # Perform a right-click if the menu does not close
        ActionChains(self.driver).move_by_offset(20, 10).context_click().perform()

        # click on info button
        info_button = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable((By.XPATH, "//mat-icon[normalize-space()='info']")))

        self.driver.execute_script("arguments[0].click();", info_button)

        # Wait for the user details page to be visible
        user_details_page = WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located((By.XPATH, "//a[normalize-space()='Details']")))
        assert user_details_page.is_displayed(), "User details page is not visible"

    def test_verify_user_list_toggle_icons(self):
        self.driver.find_element(By.ID, "login_username").send_keys("depenad165@luravel.com")
        self.driver.find_element(By.ID, "login_password").send_keys("Raunak@8390")

        # Select remember me checkbox
        self.driver.find_element(By.ID, "login_checkbox-input").click()

        # Submit login form
        self.driver.find_element(By.ID, "login_submit").click()

        # Wait for the element to be clickable
        menu_button = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable((By.XPATH, "//ion-menu-button[@id='head_ham_btn']")))
        self.driver.execute_script("arguments[0].click();", menu_button)

        # Click on management
        management_button = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable((By.XPATH, "//ion-label[normalize-space()='Management']"))
        )
        self.driver.execute_script("arguments[0].click();", management_button)

        # Click on user option
        user_button = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable((By.XPATH, "//ion-label[normalize-space()='User']"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", user_button)
        self.driver.execute_script("arguments[0].click();", user_button)

        # Perform a right-click if the menu does not close
        ActionChains(self.driver).move_by_offset(20, 10).context_click().perform()

        # click on toggle button
        toggle_button = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable((By.XPATH, "//button[@role='switch']")))

        self.driver.execute_script("arguments[0].click();", toggle_button)
        time.sleep(0.5)
        self.driver.execute_script("arguments[0].click();", toggle_button)

        # Assert the state of the toggle button
        assert toggle_button.get_attribute(
            "aria-checked") == "false", "Toggle button is not in the expected state after clicking"

    def test_verify_update_user(self):
        self.driver.find_element(By.ID, "login_username").send_keys("depenad165@luravel.com")
        self.driver.find_element(By.ID, "login_password").send_keys("Raunak@8390")

        # Select remember me checkbox
        self.driver.find_element(By.ID, "login_checkbox-input").click()

        # Submit login form
        self.driver.find_element(By.ID, "login_submit").click()

        # Wait for the element to be clickable
        menu_button = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable((By.XPATH, "//ion-menu-button[@id='head_ham_btn']")))
        self.driver.execute_script("arguments[0].click();", menu_button)

        # Click on management
        management_button = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable((By.XPATH, "//ion-label[normalize-space()='Management']"))
        )
        self.driver.execute_script("arguments[0].click();", management_button)

        # Click on user option
        user_button = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable((By.XPATH, "//ion-label[normalize-space()='User']"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", user_button)
        self.driver.execute_script("arguments[0].click();", user_button)

        # Perform a right-click if the menu does not close
        ActionChains(self.driver).move_by_offset(20, 10).context_click().perform()

        # Wait for the "Edit" button to be visible and clickable
        edit_button = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable((By.XPATH, "//mat-icon[normalize-space()='edit']"))
        )
        self.driver.execute_script("arguments[0].click();", edit_button)

        # Scroll to the "Update" button
        update_button_element = self.driver.find_element(By.XPATH, "//span[normalize-space()='Update']")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", update_button_element)

        # Wait for the "Update" button to be clickable
        update_button = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(update_button_element))
        time.sleep(0.5)

        # Click the "Update" button
        self.driver.execute_script("arguments[0].click();", update_button)

        # Wait for the URL to change to the expected URL
        expected_url = "https://carbon.bizdata360.com/#/baseapp/user"
        WebDriverWait(self.driver, 10).until(expected_conditions.url_to_be(expected_url))

        # Assert the URL
        assert self.driver.current_url == expected_url, "The URL after click on add button to create or add user is not as expected"




