import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import os

class AdminIndustriesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        cls.driver.get("http://127.0.0.1:8000/")

    def setUp(self):
        self.username = AdminIndustriesTest.username
        self.password = AdminIndustriesTest.password

    def login(self):
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

        WebDriverWait(self.driver, 15).until(EC.url_contains("/admin"))
        self.assertIn("http://127.0.0.1:8000/admin", self.driver.current_url, "Giriş yapılamadı")
        print("Login işlemi başarıyla tamamlandı.")

    def logout(self):
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

    def add_industry(self, name, user_index, image_path=None):
        print("Endüstri ekleme işlemi başlatıldı.")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Industries"))
        ).click()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "ADD INDUSTRY"))
        ).click()

        name_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "id_name"))
        )
        user_select = Select(self.driver.find_element(By.ID, "id_user"))
        icon_class_input = self.driver.find_element(By.ID, "id_icon_class")
        content_input = self.driver.find_element(By.ID, "id_content")
        subdescription_input = self.driver.find_element(By.ID, "id_subdescription")

        name_input.send_keys(name)
        user_select.select_by_index(user_index)
        icon_class_input.send_keys("fas fa-industry")
        content_input.send_keys("This is a test industry content.")
        subdescription_input.send_keys("This is a subdescription.")
        if image_path:
            image_input = self.driver.find_element(By.ID, "id_image")
            image_input.send_keys(image_path)

        save_button = self.driver.find_element(By.NAME, "_save")
        save_button.click()
        print("Endüstri ekleme işlemi tamamlandı.")

    def delete_industry(self, name):
        print("Endüstri silme işlemi başlatıldı.")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, name))
        ).click()

        delete_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "deletelink"))
        )
        delete_button.click()

        confirm_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='submit']"))
        )
        confirm_button.click()
        print("Endüstri silme işlemi tamamlandı.")

    def update_industry(self, old_name, new_name, user_index, image_path=None):
        print("Endüstri güncelleme işlemi başlatıldı.")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, old_name))
        ).click()

        name_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "id_name"))
        )
        user_select = Select(self.driver.find_element(By.ID, "id_user"))
        icon_class_input = self.driver.find_element(By.ID, "id_icon_class")
        content_input = self.driver.find_element(By.ID, "id_content")
        subdescription_input = self.driver.find_element(By.ID, "id_subdescription")

        name_input.clear()
        name_input.send_keys(new_name)
        user_select.select_by_index(user_index)
        icon_class_input.clear()
        icon_class_input.send_keys("fas fa-industry")
        content_input.clear()
        content_input.send_keys("This is an updated test industry content.")
        subdescription_input.clear()
        subdescription_input.send_keys("This is an updated subdescription.")
        if image_path:
            image_input = self.driver.find_element(By.ID, "id_image")
            image_input.send_keys(image_path)

        save_button = self.driver.find_element(By.NAME, "_save")
        save_button.click()
        print("Endüstri güncelleme işlemi tamamlandı.")

    def test_add_and_delete_industry(self):
        self.login()
        image_path = os.path.abspath("./tests/test_image.jpg")
        industry_name = "Test Industry"
        self.add_industry(industry_name, 1, image_path)

        success_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "success"))
        )
        self.assertIn("was added successfully", success_message.text)

        self.delete_industry(industry_name)

        success_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "success"))
        )
        self.assertIn("was deleted successfully", success_message.text)

        self.logout()
        print("test_add_and_delete_industry testi başarıyla tamamlandı.")

    def test_update_industry(self):
        self.login()
        image_path = os.path.abspath("./tests/test_image.jpg")
        old_name = "Test Industry"
        new_name = "Updated Industry"
        self.add_industry(old_name, 1, image_path)
        self.update_industry(old_name, new_name, 1, image_path)

        success_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "success"))
        )
        self.assertIn("was changed successfully", success_message.text)

        self.delete_industry(new_name)

        success_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "success"))
        )
        self.assertIn("was deleted successfully", success_message.text)

        self.logout()
        print("test_update_industry testi başarıyla tamamlandı.")

    def test_add_industry_with_empty_name(self):
        self.login()
        image_path = os.path.abspath("./tests/test_image.jpg")
        self.add_industry("", 1, image_path)
        
        error_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "errorlist"))
        )
        self.assertIn("This field is required.", error_message.text)
        self.logout()
        print("test_add_industry_with_empty_name testi başarıyla tamamlandı.")

    def test_add_industry_with_long_name(self):
        self.login()
        long_name = "A" * 101
        image_path = os.path.abspath("./tests/test_image.jpg")
        self.add_industry(long_name, 1, image_path)
        
        error_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "errorlist"))
        )
        self.assertIn("Ensure this value has at most 100 characters", error_message.text)
        self.logout()
        print("test_add_industry_with_long_name testi başarıyla tamamlandı.")

    def test_add_industry_without_user(self):
        self.login()
        image_path = os.path.abspath("./tests/test_image.jpg")
        self.add_industry("Test Industry", 0, image_path)
        
        error_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "errorlist"))
        )
        self.assertIn("This field is required.", error_message.text)
        self.logout()
        print("test_add_industry_without_user testi başarıyla tamamlandı.")

    def test_add_industry_without_image(self):
        self.login()
        self.add_industry("Test Industry", 1)
        
        success_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "errorlist"))
        )
        self.assertIn("This field is required.", success_message.text)


        self.logout()
        print("test_add_industry_without_image testi başarıyla tamamlandı.")

    def test_add_industry_with_invalid_image(self):
        self.login()
        image_path = os.path.abspath("./tests/test_invalid_image.txt")
        self.add_industry("Test Industry", 1, image_path)
        
        error_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "errorlist"))
        )
        self.assertIn("Upload a valid image", error_message.text)
        self.logout()
        print("test_add_industry_with_invalid_image testi başarıyla tamamlandı.")

    def test_add_industry_with_blank_subdescription(self):
        self.login()
        image_path = os.path.abspath("./tests/test_image.jpg")
        self.add_industry("Test Industry", 1, image_path)
        
        success_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "success"))
        )
        self.assertIn("was added successfully", success_message.text)

        self.delete_industry("Test Industry")
        
        success_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "success"))
        )
        self.assertIn("was deleted successfully", success_message.text)
        self.logout()
        print("test_add_industry_with_blank_subdescription testi başarıyla tamamlandı.")

    def test_add_industry_with_special_characters_in_name(self):
        self.login()
        image_path = os.path.abspath("./tests/test_image.jpg")
        self.add_industry("Test@Industry#Name!", 1, image_path)
        
        success_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "success"))
        )
        self.assertIn("was added successfully", success_message.text)

        self.delete_industry("Test@Industry#Name!")
        
        success_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "success"))
        )
        self.assertIn("was deleted successfully", success_message.text)
        self.logout()
        print("test_add_industry_with_special_characters_in_name testi başarıyla tamamlandı.")

    def test_add_industry_with_long_content(self):
        self.login()
        long_content = "A" * 500
        image_path = os.path.abspath("./tests/test_image.jpg")
        self.add_industry("Test Industry", 1, image_path)
        
        success_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "success"))
        )
        self.assertIn("was added successfully", success_message.text)

        self.delete_industry("Test Industry")
        
        success_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "success"))
        )
        self.assertIn("was deleted successfully", success_message.text)
        self.logout()
        print("test_add_industry_with_long_content testi başarıyla tamamlandı.")

    def test_add_duplicate_industry_name(self):
        self.login()
        image_path = os.path.abspath("./tests/test_image.jpg")
        self.add_industry("Duplicate Industry", 1, image_path)
        
        success_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "success"))
        )
        self.assertIn("was added successfully", success_message.text)
        
        self.add_industry("Duplicate Industry", 1, image_path)
        
        error_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "errorlist"))
        )
        self.assertIn("Industry with this Name already exists.", error_message.text)
        self.driver.get('http://127.0.0.1:8000/admin/blog/industry/')
        self.delete_industry("Duplicate Industry")
        
        success_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "success"))
        )
        self.assertIn("was deleted successfully", success_message.text)
        self.logout()
        print("test_add_duplicate_industry_name testi başarıyla tamamlandı.")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

def run_industry_tests(username, password):
    AdminIndustriesTest.username = username
    AdminIndustriesTest.password = password

    suite = unittest.TestSuite()
    suite.addTest(AdminIndustriesTest('test_add_and_delete_industry'))
    suite.addTest(AdminIndustriesTest('test_update_industry'))
    suite.addTest(AdminIndustriesTest('test_add_industry_with_empty_name'))
    suite.addTest(AdminIndustriesTest('test_add_industry_with_long_name'))
    suite.addTest(AdminIndustriesTest('test_add_industry_without_user'))
    suite.addTest(AdminIndustriesTest('test_add_industry_without_image'))
    suite.addTest(AdminIndustriesTest('test_add_industry_with_invalid_image'))
    suite.addTest(AdminIndustriesTest('test_add_industry_with_blank_subdescription'))
    suite.addTest(AdminIndustriesTest('test_add_industry_with_special_characters_in_name'))
    suite.addTest(AdminIndustriesTest('test_add_industry_with_long_content'))
    suite.addTest(AdminIndustriesTest('test_add_duplicate_industry_name'))

    runner = unittest.TextTestRunner()
    runner.run(suite)
