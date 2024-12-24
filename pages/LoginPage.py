from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def wait_for_element(self, by, value):
        return self.wait.until(EC.presence_of_element_located((by, value)))

    def enter_username(self, username):
        username_field = self.wait_for_element(By.ID, "username")
        username_field.clear()
        username_field.send_keys(username)

    def enter_password(self, password):
        password_field = self.wait_for_element(By.ID, "password")
        password_field.clear()
        password_field.send_keys(password)

    def click_signin(self):
        signin_button = self.wait_for_element(By.ID, "signin")
        signin_button.click()
