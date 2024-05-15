import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class HomePageTest(unittest.TestCase):
    def setUp(self):
        # Chrome için ayarlar
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Tarayıcı arayüzünü açmadan çalıştır
        # chrome_options.add_argument("--no-sandbox")  # Sandbox modunu devre dışı bırak
        # chrome_options.add_argument("--disable-dev-shm-usage")  # Paylaşılan bellek kullanımını kısıtla
        print('calismadi')
        # Chrome WebDriver'ını başlat
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.driver.get("http://localhost:8000")  # Django sunucunuzun URL'si

    def test_home_page_load(self):
        # Ana sayfanın başlığında 'Ana Sayfa' kelimesi geçmeli
        self.assertIn("Ana Sayfa", self.driver.title)

    def tearDown(self):
        # Test sonrası tarayıcıyı kapat
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
def run_tests():
    unittest.main()