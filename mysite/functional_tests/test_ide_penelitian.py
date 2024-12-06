import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class IdePenelitianTest(unittest.TestCase):
    def setUp(self):
        # Setup WebDriver
        self.driver = webdriver.Chrome()
        self.base_url = "http://127.0.0.1:8000/ide-penelitian/"  # URL halaman pencarian

    def tearDown(self):
        # Tutup browser setelah pengujian selesai
        self.driver.quit()

    def test_cari_ide_penelitian_valid(self):
        driver = self.driver
        driver.get(self.base_url)

        input_box = driver.find_element(By.ID, "chat-input")
        input_box.send_keys("Dr. Rimuljo Hendradi, S.Si., M.Si.")  # Masukkan nama dosen valid
        send_button = driver.find_element(By.CLASS_NAME, "icon-button")
        send_button.click()

        driver.implicitly_wait(5)
        chat_box = driver.find_element(By.ID, "chat-box")
        
        # Debugging untuk melihat isi chat_box
        print(chat_box.text)
        
        # Pencocokan dengan case-insensitive
        self.assertIn("rimuljo hendradi", chat_box.text.lower())  # Menggunakan .lower() untuk pencocokan lebih fleksibel


    def test_cari_ide_penelitian_invalid(self):
        driver = self.driver
        driver.get(self.base_url)

        # GIVEN saya berada di halaman pencarian ide penelitian
        self.assertIn("Ide Penelitian", driver.title)

        # WHEN saya memasukkan nama dosen yang tidak valid
        input_box = driver.find_element(By.ID, "chat-input")
        input_box.send_keys("Nama Dosen Tidak Valid")
        send_button = driver.find_element(By.CLASS_NAME, "icon-button")
        send_button.click()

        # THEN saya akan melihat pesan error
        driver.implicitly_wait(5)  # Tunggu respons dari backend
        chat_box = driver.find_element(By.ID, "chat-box")
        self.assertIn("Tidak ditemukan dosen", chat_box.text)

if __name__ == "__main__":
    unittest.main()
