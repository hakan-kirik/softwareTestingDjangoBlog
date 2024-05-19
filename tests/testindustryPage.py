import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import os

class IndustryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        cls.driver.set_window_size(1500, 1000) 
        cls.driver.get("http://127.0.0.1:8000/")

    def setUp(self):
        self.username = IndustryTest.username
        self.password = IndustryTest.password

    def login(self):
        print("Login işlemi başlatıldı.")
        open_modal_button = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(@class,'action__btn action__btn-login open-login-popup')]"))
        )
        open_modal_button.click()

        self.driver.implicitly_wait(5)
        username_input = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        password_input = self.driver.find_element(By.ID, "password")
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        login_button = self.driver.find_element(By.XPATH, "//button[@type='submit'][contains(., 'Giriş Yap')]")
        login_button.click()

        WebDriverWait(self.driver, 5).until(EC.url_contains("/admin"))
        self.assertIn("http://127.0.0.1:8000/admin", self.driver.current_url, "Giriş yapılamadı")
        print("Login işlemi başarıyla tamamlandı.")

    def add_industry(self, name, content, user_index, image_path=None, icon_class="fas fa-industry", subdescription=""):
        print("Endüstri ekleme işlemi başlatıldı.")
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Industries"))
        ).click()

        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.LINK_TEXT, "ADD INDUSTRY"))
        ).click()

        name_input = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, "id_name"))
        )
        content_input = self.driver.find_element(By.ID, "id_content")
        user_select = Select(self.driver.find_element(By.ID, "id_user"))
        icon_class_input = self.driver.find_element(By.ID, "id_icon_class")
        subdescription_input = self.driver.find_element(By.ID, "id_subdescription")

        name_input.send_keys(name)
        content_input.send_keys(content)
        user_select.select_by_index(user_index)
        icon_class_input.send_keys(icon_class)
        subdescription_input.send_keys(subdescription)
        if image_path:
            image_input = self.driver.find_element(By.ID, "id_image")
            image_input.send_keys(image_path)

        save_button = self.driver.find_element(By.NAME, "_save")
        save_button.click()
        print("Endüstri ekleme işlemi tamamlandı.")

    def delete_industry(self, name):
        print("Endüstri silme işlemi başlatıldı.")
        self.driver.get("http://127.0.0.1:8000/admin/blog/industry/")
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.LINK_TEXT, name))
        ).click()

        delete_button = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "deletelink"))
        )
        delete_button.click()

        confirm_button = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='submit']"))
        )
        confirm_button.click()
        print("Endüstri silme işlemi tamamlandı.")

    def find_industry_in_pages(self, industry_name):
        while True:
            industry_names = self.driver.find_elements(By.XPATH, f"//h4[contains(text(), '{industry_name}')]")
            if len(industry_names) > 0:
                return True

            # Sonraki sayfa kontrolü
            try:
                next_button = self.driver.find_element(By.LINK_TEXT, "»")
                next_button.click()
                WebDriverWait(self.driver, 5).until(EC.staleness_of(next_button))
            except:
                return False

    def delete_all_test_industries(self):
        try:
            self.logout()
        except:
            pass
        self.driver.get("http://127.0.0.1:8000/")
        WebDriverWait(self.driver, 5).until(
            EC.url_to_be("http://127.0.0.1:8000/")
        )
        print("Tüm 'Test Industry Name' endüstrilerini silme işlemi başlatıldı. Bu testte bir süre bekleyebilirsiniz.")
        self.login()
        while True:
            try:
                self.delete_industry("Test Industry Name")
                print("'Test Industry Name' endüstri silindi.")
            except:
                break
        while True:
            try:
                self.delete_industry("Updated Industry Name")
                print("'Updated Industry Name' endüstri silindi.")
            except:
                break  
        self.logout()

    def test_active_industry_link(self):
        # "Hizmetlerimiz" linkini bul ve 'active' sınıfına sahip olup olmadığını kontrol et
        self.driver.get("http://127.0.0.1:8000/industries/")
        industry_link = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//li[contains(@class, 'nav__item') and contains(@class, 'has-dropdown')]/a[contains(@class, 'nav__item-link') and contains(@class, 'dropdown-toggle') and contains(text(), 'Hizmetlerimiz')]"))
        )
        self.assertIn("active", industry_link.get_attribute("class"), "Hizmetlerimiz sekmesi 'active' sınıfına sahip değil")

    def test_add_and_web_view_verify_industry(self):
        self.delete_all_test_industries() # name unique olduğundan bir hata olmasın diye
        self.login()
        image_path = os.path.abspath("./tests/test_image.jpg")
        industry_name = "Test Industry Name"
        self.add_industry(industry_name, "This is a test industry content.", 1, image_path)

        success_message = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "success"))
        )
        self.assertIn("was added successfully", success_message.text)

        # Web görünümüne gidip endüstriyi kontrol et
        self.driver.get("http://127.0.0.1:8000/industries/")
        industry_found = self.find_industry_in_pages(industry_name)
        self.assertTrue(industry_found, "Endüstri web görünümünde bulunamadı")
        
        self.delete_industry(industry_name)  # Test sonunda eklenen endüstriyi sil
        self.logout()
        print("test_add_and_web_view_verify_industry testi başarıyla tamamlandı.")

    def test_update_and_web_view_verify_industry(self):
        self.delete_all_test_industries() # name unique olduğundan bir hata olmasın diye
        self.login()
        image_path = os.path.abspath("./tests/test_image.jpg")
        old_name = "Test Industry Name"
        new_name = "Updated Industry Name"
        self.add_industry(old_name, "This is a test industry content.", 1, image_path)

        # Endüstriyi güncelle
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.LINK_TEXT, old_name))
        ).click()

        name_input = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, "id_name"))
        )
        name_input.clear()
        name_input.send_keys(new_name)

        save_button = self.driver.find_element(By.NAME, "_save")
        save_button.click()

        success_message = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "success"))
        )
        self.assertIn("was changed successfully", success_message.text)

        # Güncellenmiş endüstriyi kontrol et
        self.driver.get("http://127.0.0.1:8000/industries/")
        industry_found = self.find_industry_in_pages(new_name)
        self.assertTrue(industry_found, "Güncellenmiş endüstri web görünümünde bulunamadı")

        self.delete_industry(new_name)  # Test sonunda güncellenen endüstriyi sil
        self.logout()
        print("test_update_and_web_view_verify_industry testi başarıyla tamamlandı.")

    def logout(self):
        print("Logout işlemi başlatıldı.")
        self.driver.get("http://127.0.0.1:8000/admin/")
        logout_button = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//button[@type='submit' and text()='Log out']"))
        )
        logout_button.click()
        WebDriverWait(self.driver, 5).until(
            EC.url_to_be("http://127.0.0.1:8000/")
        )
        self.assertEqual(self.driver.current_url, "http://127.0.0.1:8000/", "Çıkış yapılamadı")
        print("Logout işlemi başarıyla tamamlandı.")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

def run_industry_tests(username, password):
    IndustryTest.username = username
    IndustryTest.password = password

    suite = unittest.TestSuite()
    suite.addTest(IndustryTest('test_active_industry_link'))
    suite.addTest(IndustryTest('test_add_and_web_view_verify_industry'))
    suite.addTest(IndustryTest('test_update_and_web_view_verify_industry'))

    runner = unittest.TextTestRunner()
    runner.run(suite)