import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class LoginTest(unittest.TestCase):
    # Parametreleri sınıf değişkeni olarak ayarlamak için yeni bir başlatıcı metod
    def setUp(self):
        # Parametreler yerine sınıf değişkenlerini kullan
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.driver.get("http://127.0.0.1:8000")

    def test_login(self):
        open_modal_button = self.driver.find_element(By.XPATH, "//button[contains(@class,'action__btn action__btn-login open-login-popup')]")  # 'loginButton' ID'li buton varsayımı
        open_modal_button.click()

        # Kısa bir bekleme süresi ekleyin
        self.driver.implicitly_wait(15)  # 55 saniye bekleyin, modal yüklenmesi için

        username_input = self.driver.find_element(By.ID, "username")
        password_input = self.driver.find_element(By.ID, "password")
        username_input.send_keys(self.username)  # self.username kullan
        password_input.send_keys(self.password)  # self.password kullan
        login_button = self.driver.find_element(By.XPATH, "//button[@type='submit'][contains(span, 'Giriş Yap')]")
        login_button.click()
        self.assertIn(self.driver.current_url, "http://127.0.0.1:8000/admin","Giriş yapılamadı")

    def tearDown(self):
        self.driver.quit()

# Parametreleri testlerden önce ayarlayacak olan yardımcı fonksiyon
def run_tests(username, password):
    # Sınıf değişkenlerine değer atama
    LoginTest.username = username
    LoginTest.password = password

    # Test süiti oluşturma ve test eklemek
    suite = unittest.TestSuite()
    suite.addTest(LoginTest('test_login'))  # test_login metodunu ekler

    # Test runner ile testleri çalıştırma
    runner = unittest.TextTestRunner()
    runner.run(suite)