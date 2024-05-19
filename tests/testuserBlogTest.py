import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import os

class BlogTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        cls.driver.set_window_size(1500, 1000) 
        cls.driver.get("http://127.0.0.1:8000/")

    def setUp(self):
        self.username = BlogTest.username
        self.password = BlogTest.password

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

    def add_blog(self, title, content, author_index, category_index, tag_index, image_path=None):
        print("Blog ekleme işlemi başlatıldı.")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Blog posts"))
        ).click()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "ADD BLOG POST"))
        ).click()

        title_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "id_title"))
        )
        content_input = self.driver.find_element(By.ID, "id_content")
        author_select = Select(self.driver.find_element(By.ID, "id_author"))
        category_select = Select(self.driver.find_element(By.ID, "id_category"))
        tags_select = Select(self.driver.find_element(By.ID, "id_tags"))

        title_input.send_keys(title)
        content_input.send_keys(content)
        author_select.select_by_index(author_index)
        category_select.select_by_index(category_index)
        tags_select.select_by_index(tag_index)
        if image_path:
            cover_image_input = self.driver.find_element(By.ID, "id_cover_image")
            cover_image_input.send_keys(image_path)

        save_button = self.driver.find_element(By.NAME, "_save")
        save_button.click()
        print("Blog ekleme işlemi tamamlandı.")

    def delete_blog(self, title):
        print("Blog silme işlemi başlatıldı.")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, title))
        ).click()

        delete_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "deletelink"))
        )
        delete_button.click()

        confirm_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='submit']"))
        )
        confirm_button.click()
        print("Blog silme işlemi tamamlandı.")

    def find_blog_in_pages(self, blog_title):
        while True:
            blog_titles = self.driver.find_elements(By.XPATH, f"//h4/a[contains(text(), '{blog_title}')]")
            if len(blog_titles) > 0:
                return True

            # Sonraki sayfa kontrolü
            try:
                next_button = self.driver.find_element(By.LINK_TEXT, "»")
                next_button.click()
                WebDriverWait(self.driver, 10).until(EC.staleness_of(next_button))
            except:
                return False

    def test_add_and_web_view_verify_blog(self):
        self.login()
        image_path = os.path.abspath("./tests/test_image.jpg")
        blog_title = "Test Blog Title"
        self.add_blog(blog_title, "This is a test blog content.", 1, 1, 1, image_path)

        success_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "success"))
        )
        self.assertIn("was added successfully", success_message.text)

        # Web görünümüne gidip blogu kontrol et
        self.driver.get("http://127.0.0.1:8000/blogs/")
        blog_found = self.find_blog_in_pages(blog_title)
        self.assertTrue(blog_found, "Blog web görünümünde bulunamadı")

        self.logout()
        print("test_add_and_web_view_verify_blog testi başarıyla tamamlandı.")

    def test_update_and_web_view_verify_blog(self):
        self.login()
        image_path = os.path.abspath("./tests/test_image.jpg")
        old_title = "Test Blog Title"
        new_title = "Updated Blog Title"
        self.add_blog(old_title, "This is a test blog content.", 1, 1, 1, image_path)

        # Blogu güncelle
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, old_title))
        ).click()

        title_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "id_title"))
        )
        title_input.clear()
        title_input.send_keys(new_title)
        
        save_button = self.driver.find_element(By.NAME, "_save")
        save_button.click()

        success_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "success"))
        )
        self.assertIn("was changed successfully", success_message.text)

        # Güncellenmiş blogu kontrol et
        self.driver.get("http://127.0.0.1:8000/blogs/")
        blog_found = self.find_blog_in_pages(new_title)
        self.assertTrue(blog_found, "Güncellenmiş blog web görünümünde bulunamadı")

        self.logout()
        print("test_update_and_web_view_verify_blog testi başarıyla tamamlandı.")

    def logout(self):
        print("Logout işlemi başlatıldı.")
        self.driver.get("http://127.0.0.1:8000/admin/")
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

def run_blog_tests(username, password):
    BlogTest.username = username
    BlogTest.password = password

    suite = unittest.TestSuite()
    suite.addTest(BlogTest('test_add_and_web_view_verify_blog'))
    suite.addTest(BlogTest('test_update_and_web_view_verify_blog'))

    runner = unittest.TextTestRunner()
    runner.run(suite)
