import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HomePageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Tarayıcı ayarları ve WebDriver başlatma
        cls.base_url = "http://localhost:8000/"
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Arayüz gösterilmeden çalıştır
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        cls.driver.get(cls.base_url)
        print("Tarayıcı başlatıldı ve ana sayfaya gidildi.")

    def test_active_home_link(self):
        print("test_active_home_link başlatıldı.")
        self.driver.get(self.base_url)
        WebDriverWait(self.driver, 10).until(EC.url_to_be(self.base_url))
        # Ana sayfa linkini bul ve 'active' sınıfına sahip olup olmadığını kontrol et
        home_link = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "li.nav__item a.nav__item-link"))
        )
        cl = home_link.get_attribute("class")
        self.assertIn("active", cl, "Ana sayfa linki 'active' sınıfına sahip değil")
        print("test_active_home_link başarıyla tamamlandı.")

    def test_navigation_links(self):
        print("test_navigation_links başlatıldı.")
        self.driver.get(self.base_url)
        WebDriverWait(self.driver, 10).until(EC.url_to_be(self.base_url))
        # Navigasyon linklerinin doğru çalıştığını kontrol et
        links = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.navbar-nav > li.nav__item > a.nav__item-link"))
        )
        for i in range(len(links)):
            # Her iterasyonda linkleri tekrar bul
            links = self.driver.find_elements(By.CSS_SELECTOR, "ul.navbar-nav > li.nav__item > a.nav__item-link")
            url = links[i].get_attribute("href")
            if url:
                self.driver.get(url)
                WebDriverWait(self.driver, 10).until(EC.url_to_be(url))
                self.assertEqual(self.driver.current_url, url, f"{url} adresine gidilemedi")
                self.driver.get(self.base_url)
                WebDriverWait(self.driver, 10).until(EC.url_to_be(self.base_url))
        print("test_navigation_links başarıyla tamamlandı.")

    def test_logo_presence(self):
        print("test_logo_presence başlatıldı.")
        # Logo varlığını kontrol et
        self.driver.get(self.base_url)
        WebDriverWait(self.driver, 10).until(EC.url_to_be(self.base_url))
        logos = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.navbar-brand img"))
        )
        is_display = False
        for logo in logos:
            if logo.is_displayed():
                is_display = True

        self.assertTrue(is_display, "Logo görüntülenemiyor")
        print("test_logo_presence başarıyla tamamlandı.")

    @classmethod
    def tearDownClass(cls):
        # Testler sonrası tarayıcıyı kapat
        cls.driver.quit()
        print("Tarayıcı kapatıldı.")

def run_tests():
    # Testleri yükleyip çalıştırma
    suite = unittest.TestSuite()
    suite.addTest(HomePageTest('test_active_home_link'))
    suite.addTest(HomePageTest('test_navigation_links'))
    suite.addTest(HomePageTest('test_logo_presence'))
    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == "__main__":
    run_tests()