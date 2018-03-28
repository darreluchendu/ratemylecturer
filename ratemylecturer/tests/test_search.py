from django.contrib.auth.models import User
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ratemylecturer.tests.test_utils import BaseLiveServerTestCase


class SearchTest(BaseLiveServerTestCase):

    def test_search_a_given_lecturer(self):
        print(User.objects.filter(username='alice'))
        self.driver.get(self.live_server_url)
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.title_contains('Home'))
        search = self.driver.find_element_by_class_name('main-search')
        button = self.driver.find_element_by_class_name('search-button')
        search.send_keys('alice')
        button.click()
        element = wait.until(EC.title_contains('Profile'))
        self.assertIn('Alice', self.driver.find_element_by_tag_name('body').text)
