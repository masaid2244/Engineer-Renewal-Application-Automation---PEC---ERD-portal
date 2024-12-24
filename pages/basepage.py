from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, WebDriverException, ElementClickInterceptedException
import time

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def capture_screenshot(self, filename):
        try:
            if not filename.endswith(".png"):
                filename += ".png"
            self.driver.get_screenshot_as_file(filename)
            print(f"Screenshot saved as {filename}")
        except Exception as e:
            print(f"Error capturing screenshot: {e}")





    def scroll_and_click(self, locator):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(locator)
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator)).click()
            print(f"Successfully clicked element with locator {locator}.")
            self.capture_screenshot(f"clicked_{locator[1]}.png")
        except ElementClickInterceptedException:
            print(f"Element click intercepted for locator {locator}. Trying JavaScript click.")
            self.driver.execute_script("arguments[0].click();", self.driver.find_element(*locator))
            print(f"Successfully clicked element with locator {locator} using JavaScript.")
            self.capture_screenshot(f"clicked_{locator[1]}_js.png")
        except Exception as e:
            print(f"Error clicking element with locator {locator}: {e}")
            self.capture_screenshot(f"click_error_{locator[1]}.png")

    def select_value_by_text(self, element_id, value):
        try:
            for _ in range(3):  # Retry mechanism
                try:
                    dropdown_element = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.ID, element_id))
                    )
                    dropdown_element.click()

                    option_xpath = f"//li[contains(text(), '{value}')]"
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, option_xpath))
                    )

                    option_to_select = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, option_xpath))
                    )
                    option_to_select.click()
                    return  # Exit after successful selection

                except StaleElementReferenceException:
                    print(f"StaleElementReferenceException encountered. Retrying... ({value})")
                    time.sleep(1)  # Wait before retrying
                    continue

            print(f"Error selecting value '{value}' for '{element_id}': Element not interactable after retries.")
            self.capture_screenshot(f"dropdown_error_{element_id}")

        except WebDriverException as e:
            print(f"Error selecting value '{value}' for '{element_id}': {e}")
            self.capture_screenshot(f"dropdown_error_{element_id}")

    def remove_file(self, xpath):
        try:
            remove_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            remove_button.click()
            print(f"Successfully clicked remove button for XPath: {xpath}")
            time.sleep(2)  # Wait for the removal to complete
        except Exception as e:
            print(f"Error removing existing file for XPath {xpath}: {e}")
            self.capture_screenshot(f"remove_file_error_{xpath.replace('/', '_')}")


