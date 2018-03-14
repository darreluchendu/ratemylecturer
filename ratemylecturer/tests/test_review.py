from django.urls import reverse
from ratemylecturer.tests.test_utils import BaseLiveServerTestCase
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ReviewsTest(BaseLiveServerTestCase):

    def test_registered_user_can_add_review(self):
        self.driver.get('http://127.0.0.1:8000/')

    def test_unregistered_user_can_not_add_review(self):
        self.driver.get('http://127.0.0.1:8000/')

    def test_regisstered_user_can_view_review(self):
        self.driver.get('http://127.0.0.1:8000/')

    def test_unregistered_user_can_view_review(self):
        self.driver.get('http://127.0.0.1:8000/')