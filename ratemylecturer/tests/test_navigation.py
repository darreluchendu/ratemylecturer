from django.urls import reverse
from ratemylecturer.tests.test_utils import BaseLiveServerTestCase
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class SiteNavigationTest(BaseLiveServerTestCase):


    def test_navigate_to_home(self):
        # open the lick we want to test.
        self.driver.get('http://127.0.0.1:8000/')
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.title_contains('Home'))
        self.assertTrue(element)

    def test_navigate_from_home_to_about(self):
        # open the lick we want to test.
        self.driver.get('http://127.0.0.1:8000/')
        wait = WebDriverWait(self.driver, 10)
        link = self.driver.find_element_by_link_text('About')
        link.click()
        element = wait.until(EC.title_contains('About'))
        self.assertTrue(element)

    def test_navigate_from_home_to_login(self):
        # open the lick we want to test.
        self.driver.get('http://127.0.0.1:8000/')
        wait = WebDriverWait(self.driver, 10)
        link = self.driver.find_element_by_link_text('Login')
        link.click()
        element = wait.until(EC.title_contains('Login'))
        self.assertTrue(element)

    def test_navigate_from_home_to_register(self):
        # open the lick we want to test.
        self.driver.get('http://127.0.0.1:8000/')
        wait = WebDriverWait(self.driver, 10)
        link = self.driver.find_element_by_link_text('Register')
        link.click()
        element = wait.until(EC.title_contains('Register'))
        self.assertTrue(element)
