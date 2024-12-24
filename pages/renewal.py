from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, StaleElementReferenceException
from pages.basepage import BasePage
import time


class RenewalPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def upload_file(self, dropzone_id, file_path):
        try:
            dropzone_form = (By.ID, dropzone_id)
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(dropzone_form)
            )
            dropzone = self.driver.find_element(*dropzone_form)
            dropzone.click()
            self.driver.find_element(By.CSS_SELECTOR, "input[type='file']").send_keys(file_path)
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "dz-message"))
            )
            self.capture_screenshot(f"upload_success_{dropzone_id}.png")
        except TimeoutException:
            self.capture_screenshot(f"upload_error_{dropzone_id}.png")
        except Exception as e:
            self.capture_screenshot(f"upload_error_{dropzone_id}.png")

    def remove_file(self, xpath):
        try:
            remove_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            remove_button.click()
            time.sleep(2)
        except Exception as e:
            self.capture_screenshot(f"remove_file_error_{xpath.replace('/', '_')}.png")

    def select_value_by_text(self, element_id, value):
        try:
            for _ in range(3):  # Retry mechanism
                try:
                    dropdown_element = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.ID, element_id))
                    )
                    dropdown_element.click()
                    option_xpath = f"//li[contains(text(), '{value}')]"
                    option_to_select = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, option_xpath))
                    )
                    option_to_select.click()
                    return
                except StaleElementReferenceException:
                    time.sleep(1)
            self.capture_screenshot(f"dropdown_error_{element_id}.png")
        except Exception as e:
            self.capture_screenshot(f"dropdown_error_{element_id}.png")

    def submit_form(self):
        try:
            self.driver.find_element(By.ID, "btnAddressSubmit").click()
            WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[7]/button[2]"))
            ).click()
            self.driver.find_element(By.XPATH, "//*[@id='demo-bv-tab1']/div[2]/button").click()
            self.driver.implicitly_wait(5)
            self.driver.find_element(By.XPATH, "//*[@id='demo-bv-tab2']/div[4]/div[2]/button").click()
            self.driver.implicitly_wait(5)
            self.driver.find_element(By.ID, "btn-employment").click()
        except Exception as e:
            self.capture_screenshot("form_submit_error.png")
