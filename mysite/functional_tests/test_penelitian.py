from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class FunctionalTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def test_homepage(self):
        self.browser.get('http://localhost:8000/')
        self.assertIn('Penelitian', self.browser.title)

    def test_search_functionality(self):
        self.browser.get('http://localhost:8000/penelitian/')
        search_input = self.browser.find_element(By.NAME, 'search')
        search_input.send_keys('BPMN')
        search_input.send_keys(Keys.RETURN)
        time.sleep(2)
        results = self.browser.find_elements(By.CSS_SELECTOR, '.article-title')
        self.assertTrue(any('BPMN' in result.text for result in results), "Search results did not match.")
