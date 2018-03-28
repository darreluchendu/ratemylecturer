from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ratemylecturer.tests.test_utils import BaseLiveServerTestCase


class SiteNavigationTest(BaseLiveServerTestCase):

    def test_navigate_from_home_to_about(self):
        # open the lick we want to test.
        self.driver.get(self.live_server_url)
        wait = WebDriverWait(self.driver, 10)
        link = self.driver.find_element_by_link_text('About')
        link.click()
        element = wait.until(EC.title_contains('About'))
        self.assertTrue(element)

    def test_navigate_from_home_to_login(self):
        # open the lick we want to test.
        self.driver.get(self.live_server_url)
        wait = WebDriverWait(self.driver, 10)
        link = self.driver.find_element_by_link_text('Login')
        link.click()
        element = wait.until(EC.title_contains('Login'))
        self.assertTrue(element)

    def test_navigate_from_home_to_register(self):
        # open the lick we want to test.
        self.driver.get(self.live_server_url)
        wait = WebDriverWait(self.driver, 10)
        link = self.driver.find_element_by_link_text('Register')
        link.click()
        element = wait.until(EC.title_contains('Register'))
        self.assertTrue(element)
