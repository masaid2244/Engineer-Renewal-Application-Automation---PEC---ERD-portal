from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.basepage import BasePage
import time

class TimeInputPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def input_time(self, from_date, to_date):
        # Entering the 'From Date'
        try:
            from_date_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "txtFromDate"))
            )
            from_date_element.send_keys(Keys.BACKSPACE * 10)  # Clear existing value
            from_date_element.send_keys("20-June ")  # Enter partial date
            from_date_element.send_keys(Keys.ARROW_LEFT * 4)  # Move cursor to before year section
            from_date_element.send_keys("2022")  # Enter year

            # Verify the date value
            entered_date = from_date_element.get_attribute("value")
            print(f"Date entered in the field: {entered_date}")
            if entered_date != "20-Jun-2022":
                print("Warning: The entered date does not match the expected value '20-June-2021'.")
            print("From date entered successfully.")
        except Exception as e:
            print(f"Error entering from date: {e}")
            self.capture_screenshot("from_date_error.png")

        # Entering the 'To Date'
        try:
            to_date_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "txtToDate"))
            )
            to_date_element.send_keys(Keys.BACKSPACE * 10)  # Clear existing value
            to_date_element.send_keys("20-Aug ")  # Enter partial date
            to_date_element.send_keys(Keys.ARROW_LEFT * 4)  # Move cursor to before year section
            to_date_element.send_keys("2024")  # Enter year

            # Verify the date value
            entered_date = to_date_element.get_attribute("value")
            print(f"Date entered in the field: {entered_date}")
            if entered_date != "20-Aug-2024":
                print("Warning: The entered date does not match the expected value '20-Aug-2024'.")
            print("To date entered successfully.")
        except Exception as e:
            print(f"Error entering to date: {e}")
            self.capture_screenshot("to_date_error.png")

        # Optional: Pause to ensure the dates are set
        time.sleep(1)



    def wait_for_overlay_to_disappear(self):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.invisibility_of_element((By.CLASS_NAME, "sweet-overlay"))
            )
            print("Overlay disappeared.")
        except Exception as e:
            print(f"Error waiting for overlay to disappear: {e}")
            self.driver.save_screenshot("overlay_disappear_error.png")

    def click_element_with_retry(self, by, value, retries=3):
        for attempt in range(retries):
            try:
                self.wait_for_overlay_to_disappear()
                element = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((by, value))
                )
                element.click()
                print(f"Successfully clicked element with locator ({by}, {value}).")
                return
            except Exception as e:
                print(f"Error clicking element with locator ({by}, {value}): {e}")
                self.driver.save_screenshot(f"click_error_{attempt}.png")
                time.sleep(2)  # Wait before retrying
        print(f"Failed to click element with locator ({by}, {value}) after {retries} attempts.")

    def click_element_with_js(self, by, value):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((by, value))
            )
            self.driver.execute_script("arguments[0].click();", element)
            print(f"Successfully clicked element with locator ({by}, {value}) using JavaScript.")
        except Exception as e:
            print(f"Error clicking element with locator ({by}, {value}) using JavaScript: {e}")
            self.driver.save_screenshot("js_click_error.png")

    def capture_screenshot(self, filename):
        self.driver.save_screenshot(filename)
        print(f"Screenshot saved as {filename}.")
