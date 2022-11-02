import time

from django.contrib.staticfiles.testing import LiveServerTestCase
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class TestAuthentication(LiveServerTestCase):
    def setUp(self):
        pythonpath = '/home/travis/build/nicoseng/P10_purbeurre/purbeurre_website/tests/functional_tests/chromedriver'
        # pythonpath = '/Users/nicolassengmany/Desktop/OCR/Python/Projets/P10_purbeurre/purbeurre/purbeurre_website/tests/functional_tests/chromedriver'
        service = Service(pythonpath)
        self.chromeoption = Options()
        self.chromeoption.add_argument('--headless')
        # self.options.add_argument('--disable-gpu')
        self.browser = webdriver.Chrome(service=service, options=self.chromeoption)
        self.browser.maximize_window()
        # chromeoption = Options()
        # chromeoption.add_argument('--headless')
        # browser = webdriver.Chrome(options=chromeoption)

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
