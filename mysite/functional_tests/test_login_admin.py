import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginAdminTest(unittest.TestCase):
    def setUp(self):
        # Setup WebDriver
        self.driver = webdriver.Chrome()
        self.base_url = "http://127.0.0.1:8000/login/"  # URL login ke admin

    def tearDown(self):
        # Tutup browser setelah pengujian selesai
        self.driver.quit()

    def test_success_login(self):
        driver = self.driver
        driver.get(self.base_url)

        # GIVEN I am on the Login Page
        self.assertIn("Login", driver.title)

        # WHEN I fill in username and password fields with valid credentials
        # Find the input fields and fill them in
        username_input = driver.find_element(By.NAME, "username")  # Assuming 'username' is the name attribute
        password_input = driver.find_element(By.NAME, "password")  # Assuming 'password' is the name attribute
        login_button = driver.find_element(By.TAG_NAME, "button")  # Locate the submit button

        username_input.send_keys("admin")  # Username valid
        password_input.send_keys("kelompok6")  # Password valid
        login_button.click()

        # THEN I should be on the dashboard
        driver.implicitly_wait(5)
        self.assertEqual(driver.current_url, "http://127.0.0.1:8000/")

    def test_invalid_credentials(self):
        driver = self.driver
        driver.get(self.base_url)

        # GIVEN I am on the Login Page
        self.assertIn("Login", driver.title)

        # WHEN I fill in username and password fields with invalid credentials
        username_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.NAME, "password")
        login_button = driver.find_element(By.TAG_NAME, "button")

        username_input.send_keys("admin")
        password_input.send_keys("wapresmugibran")
        login_button.click()

        # THEN The response should contain an error message
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "form-field")))  # Wait for the form field to be visible
        error_message = driver.find_element(By.CLASS_NAME, "form-field").text  # Look for error message in form fields
        self.assertIn("Please enter a correct username and password. Note that both fields may be case-sensitive.", error_message)

if __name__ == "__main__":
    unittest.main()