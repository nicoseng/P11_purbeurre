import time

from django.contrib.staticfiles.testing import LiveServerTestCase
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service


class TestAuthentication(LiveServerTestCase):
    def setUp(self):
        service = Service('/Users/nicolassengmany/Desktop/OCR/Python/Projets/P8_purbeurre/purbeurre/purbeurre_website'
                          '/tests/functional_tests/chromedriver')
        self.browser = webdriver.Chrome(service=service)
        self.browser.maximize_window()

    def test_authentication(self):

        self.browser.get('http://127.0.0.1:8000/create_account/')
        time.sleep(3)
        username = self.browser.find_element(By.NAME, "username")
        email = self.browser.find_element(By.NAME, "email")
        password1 = self.browser.find_element(By.NAME, "password1")
        password2 = self.browser.find_element(By.NAME, "password2")
        submit = self.browser.find_element(By.NAME, "submit")

        username.send_keys("jean")
        email.send_keys("abc@gmail.com")
        password1.send_keys("molaires")
        password2.send_keys("molaires")
        submit.send_keys(Keys.RETURN)
        time.sleep(3)

        self.browser.get('http://127.0.0.1:8000/login_user/')
        time.sleep(5)

        email = self.browser.find_element(By.NAME, "email")
        password = self.browser.find_element(By.NAME, "password")
        email.send_keys("abc@gmail.com")
        password.send_keys("molaires")
        submit = self.browser.find_element(By.NAME, "submit")
        submit.send_keys(Keys.RETURN)
        time.sleep(3)

    def tearDown(self):
        self.browser.close()
