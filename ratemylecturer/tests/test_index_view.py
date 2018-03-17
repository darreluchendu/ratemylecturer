from django.test import TestCase
from django.urls import reverse, resolve
from ratemylecturer.tests.test_utils import BaseLiveServerTestCase
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ratemylecturer.views import index


# Create your tests here.

class IndexViewTests(TestCase):

    def test_index_uses_index_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response,'ratemylecturer/index.html')


    def test_links(self):
        response = self.client.get((reverse("index"))) # returns the home page
        self.assertContains(response,"about".lower())
        self.assertContains(response,"Login".lower())
        self.assertContains(response,"Register".lower())

    def test_recent_reviews_displayed(self):
        response = self.client.get((reverse("index"))) # returns the home page




    def test_display_lecturer_Of_the_week_image(self):
        """
        ensures that index page display image for lecturer of the
        week.
        """
        response = self.client.get((reverse("index")))
        self.assertContains(response, 'profile_image')







