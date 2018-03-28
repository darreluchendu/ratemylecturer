from django.test import TestCase
from django.urls import reverse


# Create your tests here.

class IndexViewTests(TestCase):

    def test_index_uses_index_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'ratemylecturer/index.html')

    def test_links(self):
        response = self.client.get((reverse("index")))  # returns the home page
        self.assertContains(response, "about".lower())
        self.assertContains(response, "Login".lower())
        self.assertContains(response, "Register".lower())

    def test_recent_reviews_displayed(self):
        response = self.client.get((reverse("index")))  # returns the home page
