import time
import os
from django.contrib.staticfiles.testing import LiveServerTestCase
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class TestUpdateUser(LiveServerTestCase):
    def setUp(self):
        if os.environ.get("ENV") == 'production':
            pythonpath = '/home/travis/build/nicoseng/P10_purbeurre/purbeurre_website/tests/functional_tests/chromedriver'
        else:
            pythonpath = '/Users/nicolassengmany/Desktop/OCR/Python/Projets/P11_purbeurre/purbeurre/purbeurre_website/tests/functional_tests/chromedriver'
        service = Service(pythonpath)
        self.chromeoption = Options()
        self.chromeoption.add_argument('--headless')
        self.chromeoption.add_argument('--no-sandbox')
        self.chromeoption.add_argument('--disable-gpu')
        self.browser = webdriver.Chrome(service=service, options=self.chromeoption)
        self.browser.maximize_window()

    def test_update_user(self):
        self.browser.get(self.live_server_url + '/create_account/')
        if os.environ.get("ENV") == 'development':
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
        if os.environ.get("ENV") == 'development':
            time.sleep(3)

        self.browser.get(self.live_server_url + '/login_user/')
        if os.environ.get("ENV") == 'development':
            time.sleep(5)

        email = self.browser.find_element(By.NAME, "email")
        password = self.browser.find_element(By.NAME, "password")
        email.send_keys("abc@gmail.com")
        password.send_keys("molaires")
        submit = self.browser.find_element(By.NAME, "submit")
        submit.send_keys(Keys.RETURN)
        if os.environ.get("ENV") == 'development':
            time.sleep(3)

        self.browser.get(self.live_server_url + '/user_account/update_user')
        if os.environ.get("ENV") == 'development':
            time.sleep(3)
        new_username = self.browser.find_element(By.NAME, "new_username")
        new_email = self.browser.find_element(By.NAME, "new_email")
        submit = self.browser.find_element(By.NAME, "submit")

        new_username.send_keys("xyz")
        new_email.send_keys("xyz@gmail.com")
        submit.send_keys(Keys.RETURN)
        if os.environ.get("ENV") == 'development':
            time.sleep(3)

        self.browser.get(self.live_server_url + '/login_user/')
        if os.environ.get("ENV") == 'development':
            time.sleep(5)

        email = self.browser.find_element(By.NAME, "email")
        password = self.browser.find_element(By.NAME, "password")
        email.send_keys("xyz@gmail.com")
        password.send_keys("molaires")
        submit = self.browser.find_element(By.NAME, "submit")
        submit.send_keys(Keys.RETURN)
        if os.environ.get("ENV") == 'development':
            time.sleep(3)

    def tearDown(self):
        self.browser.close()
