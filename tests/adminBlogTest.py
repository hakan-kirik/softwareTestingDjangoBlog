import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import os

class AdminBlogTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        cls.driver.get("http://127.0.0.1:8000/")

    def setUp(self):
        self.username = AdminBlogTest.username
        self.password = AdminBlogTest.password

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

    def add_blog(self, title, content, author_index, category_index, tag_index, image_path=None):
        print("Blog ekleme işlemi başlatıldı.")
        # Blog ekleme sayfasına git
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Blog posts"))
        ).click()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "ADD BLOG POST"))
        ).click()

        # Blog yazısını ekle
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

        # Blog yazısını kaydet
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

    def update_blog(self, old_title, new_title, new_content, author_index, category_index, tag_index, image_path=None):
        print("Blog güncelleme işlemi başlatıldı.")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, old_title))
        ).click()

        title_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "id_title"))
        )
        content_input = self.driver.find_element(By.ID, "id_content")
        author_select = Select(self.driver.find_element(By.ID, "id_author"))
        category_select = Select(self.driver.find_element(By.ID, "id_category"))
        tags_select = Select(self.driver.find_element(By.ID, "id_tags"))

        title_input.clear()
        title_input.send_keys(new_title)
        content_input.clear()
        content_input.send_keys(new_content)
        author_select.select_by_index(author_index)
        category_select.select_by_index(category_index)
        tags_select.select_by_index(tag_index)
        if image_path:
            cover_image_input = self.driver.find_element(By.ID, "id_cover_image")
            cover_image_input.send_keys(image_path)

        save_button = self.driver.find_element(By.NAME, "_save")
        save_button.click()
        print("Blog güncelleme işlemi tamamlandı.")

    def test_add_and_delete_blog(self):
        print("test_add_and_delete_blog testi başlatıldı.")
        self.login()
        image_path = os.path.abspath("./tests/test_image.jpg")
        self.add_blog("Test Blog Title", "This is a test blog content.", 1, 1, 1, image_path)

        # Blog yazısının başarılı bir şekilde eklendiğini kontrol et
        success_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "success"))
        )
        self.assertIn("was added successfully", success_message.text)

        self.delete_blog("Test Blog Title")

        # Blog yazısının silindiğini kontrol et
        success_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "success"))
        )
        self.assertIn("was deleted successfully", success_message.text)

        self.logout()
        print("test_add_and_delete_blog testi başarıyla tamamlandı.")

    def test_empty_blog_title(self):
        print("test_empty_blog_title testi başlatıldı.")
        self.login()
        self.add_blog("", "This is a test blog content.", 1, 1, 1)
        error_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "errorlist"))
        )
        self.assertIn("This field is required.", error_message.text)
        self.logout()
        print("test_empty_blog_title testi başarıyla tamamlandı.")

    def test_empty_blog_content(self):
        print("test_empty_blog_content testi başlatıldı.")
        self.login()
        self.add_blog("Test Blog Title", "", 1, 1, 1)
        error_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "errorlist"))
        )
        self.assertIn("This field is required.", error_message.text)
        self.logout()
        print("test_empty_blog_content testi başarıyla tamamlandı.")

    def test_no_category_selected(self):
        print("test_no_category_selected testi başlatıldı.")
        self.login()
        self.add_blog("Test Blog Title", "This is a test blog content.", 1, 0, 1)
        error_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "errorlist"))
        )
        self.assertIn("This field is required.", error_message.text)
        self.logout()
        print("test_no_category_selected testi başarıyla tamamlandı.")

    def test_no_tag_selected(self):
        print("test_no_tag_selected testi başlatıldı.")
        self.login()
        self.add_blog("Test Blog Title", "This is a test blog content.", 1, 1, 0)
        error_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "errorlist"))
        )
        self.assertIn("This field is required.", error_message.text)
        self.logout()
        print("test_no_tag_selected testi başarıyla tamamlandı.")

    def test_valid_image_upload(self):
        print("test_valid_image_upload testi başlatıldı.")
        self.login()
        image_path = os.path.abspath("./tests/test_image.jpg")
        self.add_blog("Test Blog Title", "This is a test blog content.", 1, 1, 1, image_path)
        success_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "success"))
        )
        self.assertIn("was added successfully", success_message.text)
        self.logout()
        print("test_valid_image_upload testi başarıyla tamamlandı.")

    def test_invalid_image_upload(self):
        print("test_invalid_image_upload testi başlatıldı.")
        self.login()
        image_path = os.path.abspath("./tests/test_invalid_image.txt")
        self.add_blog("Test Blog Title", "This is a test blog content.", 1, 1, 1, image_path)
        error_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "errorlist"))
        )
        self.assertIn("Upload a valid image", error_message.text)
        self.logout()
        print("test_invalid_image_upload testi başarıyla tamamlandı.")

    def test_blog_update(self):
        print("test_blog_update testi başlatıldı.")
        self.login()
        image_path = os.path.abspath("./tests/test_image.jpg")
        self.add_blog("Test Blog Title", "This is a test blog content.", 1, 1, 1, image_path)
        self.update_blog("Test Blog Title", "Updated Blog Title", "Updated blog content", 1, 1, 1, image_path)
        success_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "success"))
        )
        self.assertIn("was changed successfully", success_message.text)
        self.logout()
        print("test_blog_update testi başarıyla tamamlandı.")

    def test_multiple_blog_add_and_delete(self):
        print("test_multiple_blog_add_and_delete testi başlatıldı.")
        self.login()
        image_path = os.path.abspath("./tests/test_image.jpg")
        self.add_blog("Test Blog Title 1", "This is a test blog content 1.", 1, 1, 1, image_path)
        self.add_blog("Test Blog Title 2", "This is a test blog content 2.", 1, 1, 1, image_path)
        self.delete_blog("Test Blog Title 1")
        self.delete_blog("Test Blog Title 2")
        self.logout()
        print("test_multiple_blog_add_and_delete testi başarıyla tamamlandı.")

    def test_add_blog_without_login(self):
        print("test_add_blog_without_login testi başlatıldı.")
        self.driver.get("http://127.0.0.1:8000/admin/blog/add/")
        login_page_title = WebDriverWait(self.driver, 10).until(
            EC.title_contains("Log in")
        )
        self.assertTrue(login_page_title)
        self.driver.get("http://127.0.0.1:8000/")
        print("test_add_blog_without_login testi başarıyla tamamlandı.")

    def delete_all_test_blogs(self):
        try:
            self.logout()
        except:
            pass
        
        print("Tüm 'Test Blog Title' bloglarını silme işlemi başlatıldı.Bu testte bir süre bekleyebilirsiniz.")
        self.login()
        while True:
            try:
                self.delete_blog("Test Blog Title")
                print("'Test Blog Title' blog silindi.")
            except:
                break
        while True:
            try:
                self.delete_blog("Updated Blog Title")
                print("'Updated Blog Title' blog silindi.")
            except:
                break  
        self.logout()
        print("Tüm Test bloglarını silme işlemi tamamlandı.")

    @classmethod
    def tearDownClass(cls):
        # Testlerden sonra tüm 'Test Blog Title' bloglarını sil
        AdminBlogTest().delete_all_test_blogs()
        cls.driver.quit()

def run_tests(username, password):
    AdminBlogTest.username = username
    AdminBlogTest.password = password

    suite = unittest.TestSuite()
    suite.addTest(AdminBlogTest('test_add_and_delete_blog'))
    suite.addTest(AdminBlogTest('test_empty_blog_title'))
    suite.addTest(AdminBlogTest('test_empty_blog_content'))
    suite.addTest(AdminBlogTest('test_no_category_selected'))
    suite.addTest(AdminBlogTest('test_no_tag_selected'))
    suite.addTest(AdminBlogTest('test_valid_image_upload'))
    suite.addTest(AdminBlogTest('test_invalid_image_upload'))
    suite.addTest(AdminBlogTest('test_blog_update'))
    suite.addTest(AdminBlogTest('test_multiple_blog_add_and_delete'))
    suite.addTest(AdminBlogTest('test_add_blog_without_login'))

    runner = unittest.TextTestRunner()
    runner.run(suite)


