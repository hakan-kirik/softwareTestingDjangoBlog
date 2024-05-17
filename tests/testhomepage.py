import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def run_tests():
    # Test sınıfı
    class HomePageTest(unittest.TestCase):
        def setUp(self):
            # Tarayıcı ayarları ve WebDriver başlatma
            chrome_options = Options()
            # chrome_options.add_argument("--headless")  # Arayüz gösterilmeden çalıştır
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            self.driver.get("http://localhost:8000")  # Bu URL'yi kendi Django sunucunuzun URL'si ile değiştirin

        def test_active_home_link(self):
            # Ana sayfa linkini bul ve 'active' sınıfına sahip olup olmadığını kontrol et
            home_link = self.driver.find_element(By.CSS_SELECTOR, "li.nav__item a.nav__item-link")
            cl=home_link.get_attribute("class")
            self.assertIn("active",cl, "Ana sayfa linki 'active' sınıfına sahip değil")

        def tearDown(self):
            # Test sonrası tarayıcıyı kapat
            self.driver.quit()

    # Testleri yükleyip çalıştırma
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(HomePageTest)
    runner = unittest.TextTestRunner()
    runner.run(suite)
