import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        cls.driver.get("http://127.0.0.1:8000")

    def setUp(self):
        self.username = LoginTest.username
        self.password = LoginTest.password

    def test_login(self):
        print("Login işlemi başlatıldı.")
        open_modal_button = self.driver.find_element(By.XPATH, "//button[contains(@class,'action__btn action__btn-login open-login-popup')]")
        open_modal_button.click()

        self.driver.implicitly_wait(15)

        username_input = self.driver.find_element(By.ID, "username")
        password_input = self.driver.find_element(By.ID, "password")
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        login_button = self.driver.find_element(By.XPATH, "//button[@type='submit'][contains(., 'Giriş Yap')]")
        login_button.click()

        # Explicit wait kullanarak bekleme
        WebDriverWait(self.driver, 15).until(EC.url_contains("/admin"))

        self.assertIn("http://127.0.0.1:8000/admin", self.driver.current_url, "Giriş yapılamadı")
        print("Login işlemi başarıyla tamamlandı.")

    def test_login_and_logout(self):
        self.test_login()
        if self._outcome.success:
            self.test_logout()

    def test_logout(self):
        print("Logout işlemi başlatıldı.")
        logout_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@type='submit' and text()='Log out']"))
        )
        logout_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.url_to_be("http://127.0.0.1:8000/")
        )
        self.assertEqual(self.driver.current_url, "http://127.0.0.1:8000/", "Çıkış yapılamadı")
        print("Logout işlemi başarıyla tamamlandı.")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

def run_tests(username, password):
    LoginTest.username = username
    LoginTest.password = password

    suite = unittest.TestSuite()
    suite.addTest(LoginTest('test_login_and_logout'))

    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == "__main__":
    username = input("Kullanıcı adını giriniz: ")
    password = input("Şifreyi giriniz: ")
    run_tests(username, password)
