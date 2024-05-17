import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class IndustryPageActiveLinkTest(unittest.TestCase):
    def setUp(self):
        # Tarayıcı ayarları ve WebDriver başlatma
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Arayüz gösterilmeden çalıştır
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.driver.get("http://127.0.0.1:8000/industries/")  # Sayfa URL'si

    def test_active_industry_link(self):
        # XPath ile "Hizmetlerimiz" linkini bul ve 'active' sınıfına sahip olup olmadığını kontrol et
        industry_link = self.driver.find_element(By.XPATH, "//li[contains(@class, 'nav__item') and contains(@class, 'has-dropdown')]/a[contains(@class, 'nav__item-link') and contains(@class, 'dropdown-toggle') and contains(text(), 'Hizmetlerimiz')]")
        self.assertIn("active", industry_link.get_attribute("class"), "Hizmetlerimiz sekmesi 'active' sınıfına sahip değil")

    def tearDown(self):
        # Test sonrası tarayıcıyı kapat
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()


def run_tests():
    # Testleri yükleyip çalıştırma
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(IndustryPageActiveLinkTest)
    runner = unittest.TextTestRunner()
    runner.run(suite)
