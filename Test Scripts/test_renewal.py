import unittest
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.LoginPage import LoginPage
from pages.renewal import RenewalPage
from pages.Datepicker import TimeInputPage


class RenewalTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chrome_service = ChromeService(ChromeDriverManager().install())
        chrome_options = Options()
        cls.driver = WebDriver(service=chrome_service, options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.driver.get("http://10.0.32.90:8012/")
        self.driver.maximize_window()

    def wait_for_overlay_to_disappear(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "sweet-overlay"))
            )
        except Exception as e:
            print(f"Error waiting for overlay to disappear: {e}")
            self.driver.save_screenshot("overlay_wait_error.png")

    def click_element(self, by, value):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((by, value))
            ).click()
        except Exception as e:
            print(f"Error clicking element with locator ({by}, {value}): {e}")
            self.driver.save_screenshot(f"click_error_{value}.png")

    def select_value_by_text(self, container_id, value):
        try:
            # Click the dropdown to open it
            dropdown = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, container_id))
            )
            dropdown.click()

            # Wait for the dropdown options to be visible
            options_container = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "select2-results"))
            )

            # Wait for the option to be clickable and select it
            option = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//li[text()='{value}']"))
            )
            option.click()
        except Exception as e:
            print(f"Error selecting value '{value}' for '{container_id}': {e}")
            self.driver.save_screenshot(f"dropdown_error_{container_id}.png")

    def test_renewal_process(self):
        login_page = LoginPage(self.driver)
        renewal_page = RenewalPage(self.driver)
        date_picker_page = TimeInputPage(self.driver)

        self.click_element(By.LINK_TEXT, "Sign In")

        username_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        username_field.clear()
        username_field.send_keys("abdullahqureshi914@gmail.com")

        password_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        password_field.clear()
        password_field.send_keys("pecreg81202039")

        self.click_element(By.ID, "btn-login")

        # Navigate to the renewal page
        renewal_page.scroll_and_click((By.XPATH, "//*[@id='mainnav-menu']/li[7]/a"))

        self.wait_for_overlay_to_disappear()

        # Handle dropdown selections
        self.select_value_by_text("select2-renewalBranchOffice-container", "PEC HQ ISLAMABAD")
        self.select_value_by_text("select2-ddlMailingProvince-container", "AJK")
        self.select_value_by_text("select2-ddlMailingDistrict-container", "BHIMBER")
        self.select_value_by_text("select2-ddlMCity-container", "BHIMBER")
        self.select_value_by_text("select2-ddlMailingCountry-container", "Pakistan")

        address_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "renewalPostalAddress"))
        )
        address_element.clear()
        address_element.send_keys("Abc test 123")

        xpaths = [
            '//*[@id="dropzoneProfilePic"]/div[2]/a[1]',
            '//*[@id="dropzoneCnicBackPic"]/div[2]/a[1]',
            '//*[@id="dropzoneCnicPic"]/div[2]/a[1]',
            '//*[@id="dropzoneSignaturePic"]/div[2]/a[1]'
        ]

        for xpath in xpaths:
            try:
                self.click_element(By.XPATH, xpath)
            except Exception as e:
                print(f"Error removing file for XPath: {xpath} - {e}")

        file_paths = {
            "dropzoneProfilePic": r"F:\1pec\test data\Test  data pec\erd1.png",
            "dropzoneSignaturePic": r"F:\1pec\test data\Test  data pec\erd1.png",
            "dropzoneCnicPic": r"F:\1pec\test data\Test  data pec\erd1.png",
            "dropzoneCnicBackPic": r"F:\1pec\test data\Test  data pec\erd1.png"
        }

        for dropzone_id, file_path in file_paths.items():
            try:
                renewal_page.upload_file(dropzone_id, file_path)
            except Exception as e:
                print(f"Error uploading file to {dropzone_id}: {e}")
                self.driver.save_screenshot(f"upload_error_{dropzone_id}.png")

        # Submit the form
        renewal_page.submit_form()

        # Handle additional dropdowns
        self.select_value_by_text("select2-ddlEmpType-container", "Employed (Public Sector)")
        self.select_value_by_text("select2-ddlExpertise-container", "Advanced Methods of Structural Analysis")
        self.driver.find_element(By.ID, "txtExpertise").send_keys("PEC 123 123 123 ")
        self.driver.find_element(By.ID, "txtEmployerName").send_keys("PEC")
        self.driver.find_element(By.ID, "txtDesignation").send_keys("TEST")

        # Handle date inputs
        date_picker_page.input_time("20-Jun-2021", "20-Aug-2024")

        # Upload Employment file
        file_paths = {
            "dropzoneEmployment": r"F:\1pec\test data\Test  data pec\erd1.png",
        }

        for dropzone_id, file_path in file_paths.items():
            try:
                renewal_page.upload_file(dropzone_id, file_path)

                # Assert that the file is uploaded
                uploaded_file_indicator = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, f'//div[@id="{dropzone_id}"]//div[contains(@class, "dz-success-mark")]'))
                )
                self.assertTrue(uploaded_file_indicator.is_displayed(),
                                f"File upload indicator not found for {dropzone_id}.")
                print(f"File uploaded successfully to {dropzone_id}.")
            except Exception as e:
                print(f"Error uploading file to {dropzone_id}: {e}")
                self.driver.save_screenshot(f"upload_error_{dropzone_id}.png")
                self.fail(f"File upload failed for {dropzone_id}")

        # Click the submit button
       # self.click_element(By.ID, "btnSubmitEmployment")


if __name__ == "__main__":
    unittest.main()
